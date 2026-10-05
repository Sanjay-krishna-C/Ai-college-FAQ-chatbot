import os
import re
import time
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.core.logging import logger
from app.schemas.chat import ChatRequest, ChatResponse, ChatSourceItem
from app.rag.embeddings import GeminiEmbeddingService, GeminiEmbeddingError
from app.rag.vector_store import ChromaVectorStore


class ChatService:
    """
    CampusAI RAG Chat Service.
    Orchestrates:
    1. Query validation and sanitization.
    2. Gemini query embedding generation (gemini-embedding-2, 768 dimensions).
    3. ChromaDB vector search against campusai_institutional_knowledge_gemini.
    4. Context assembly preserving document, page, and regulation metadata.
    5. Grounded LLM response synthesis using Gemini generative model.
    6. Structured citations and confidence scoring.
    """

    FALLBACK_NO_INFO = (
        "I couldn't find enough information in the official college documents to answer this question. "
        "Please check the relevant college office or official notice."
    )

    SYSTEM_INSTRUCTION = (
        "You are CampusAI, an official college information assistant for students.\n"
        "Your mission is to provide direct, clean, student-friendly answers based strictly on the retrieved college documents.\n\n"
        "DIRECT ANSWER PRINCIPLES:\n"
        "1. START WITH THE EXACT ANSWER: The very first sentence must give the direct, concrete answer immediately.\n"
        "   - Never start with meta-phrases like 'Based on the official college documents...', 'According to the retrieved context...', or 'The documents state...'.\n"
        "   - Example: For 'What is the attendance requirement?', start directly: 'Students must maintain at least 80% attendance in the courses registered during the semester to be eligible for the Semester End Examination.'\n"
        "2. ACCURACY & NUMBERS: Never omit numerical values, percentages, or conditions found in the text (e.g. 80% attendance, 70-79% condonation).\n"
        "3. SECONDARY DETAILS: If additional regulations or programmes apply (e.g. M.E./M.Tech or MBA), add a brief second paragraph or clean bullet points below the primary answer.\n"
        "4. NO UNRENDERED JARGON OR DANGLING HEADINGS: Do not produce unclosed headings or raw Markdown syntax. Write clean, complete sentences.\n"
        "5. NO HALLUCINATIONS: If the context does not contain enough information, state: 'I couldn't find enough information in the official college documents to answer this question. Please check the relevant college office or official notice.'\n"
        "6. NO INTERNAL TERMS: Never mention RAG, chunks, vector database, embeddings, or retrieval."
    )

    def __init__(
        self,
        embedding_service: Optional[GeminiEmbeddingService] = None,
        vector_store: Optional[ChromaVectorStore] = None,
    ):
        self.api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.generation_model = settings.GEMINI_GENERATION_MODEL or "gemini-3.5-flash"
        self.embedding_service = embedding_service or GeminiEmbeddingService()
        self.vector_store = vector_store or ChromaVectorStore(
            collection_name=settings.CHROMA_COLLECTION_NAME
        )
        self.top_k = settings.RAG_TOP_K or 5
        self.similarity_threshold = getattr(settings, "RAG_SIMILARITY_THRESHOLD", 0.72)
        self._genai_client = None
        self._init_genai_client()

    def _init_genai_client(self):
        """Initialize Google GenAI client for answer generation."""
        if not self.api_key or len(self.api_key.strip()) < 10:
            logger.warning("GEMINI_API_KEY is not set. Gemini generation will not be available.")
            return

        try:
            from google import genai
            self._genai_client = genai.Client(api_key=self.api_key)
            logger.info(f"Initialized Gemini Generation client with model '{self.generation_model}'")
        except Exception as e:
            logger.warning(f"Could not initialize google.genai for generation: {e}")
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self._genai_client = legacy_genai
                logger.info(f"Initialized legacy google.generativeai for generation model '{self.generation_model}'")
            except Exception as leg_e:
                logger.error(f"Failed to initialize any Gemini client: {leg_e}")

    def build_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Assemble retrieved chunks into structured, formatted context for Gemini.
        Preserves document name, page, regulation, and chunk content.
        """
        context_blocks = []
        for idx, chunk in enumerate(retrieved_chunks, 1):
            meta = chunk.get("metadata", {})
            doc_name = meta.get("document_name") or meta.get("source_file", "Official Document")
            source_file = meta.get("source_file", "")
            page = meta.get("page_number", "N/A")
            regulation = meta.get("regulation", "General")
            text = chunk.get("text", "").strip()

            block = (
                f"SOURCE {idx}\n"
                f"Document: {doc_name} ({source_file})\n"
                f"Page: {page}\n"
                f"Regulation: {regulation}\n"
                f"Content:\n{text}\n"
            )
            context_blocks.append(block)

        return "\n---\n".join(context_blocks)

    def extract_sources(self, retrieved_chunks: List[Dict[str, Any]]) -> List[ChatSourceItem]:
        """
        Extract clean, deduplicated structured sources from retrieved chunks.
        """
        seen_keys = set()
        sources: List[ChatSourceItem] = []

        for chunk in retrieved_chunks:
            meta = chunk.get("metadata", {})
            doc_name = meta.get("document_name") or meta.get("source_file", "Official College Document")
            source_file = meta.get("source_file") or doc_name
            page_num = meta.get("page_number")
            regulation = meta.get("regulation")
            distance = chunk.get("distance")

            # Calculate relevance score if distance is available (cosine distance -> similarity)
            relevance = None
            if distance is not None:
                relevance = max(0.0, min(1.0, round(1.0 - float(distance), 4)))

            dedup_key = (doc_name, page_num)
            if dedup_key not in seen_keys:
                seen_keys.add(dedup_key)
                snippet = chunk.get("text", "")[:280].strip()
                if len(chunk.get("text", "")) > 280:
                    snippet += "..."

                sources.append(
                    ChatSourceItem(
                        document_name=doc_name,
                        source_file=source_file,
                        title=doc_name,
                        page_number=page_num if isinstance(page_num, int) else None,
                        regulation=str(regulation) if regulation else None,
                        snippet=snippet,
                        relevance_score=relevance,
                    )
                )

        return sources

    def generate_llm_answer(self, query: str, context: str) -> str:
        """
        Call Gemini generative model to synthesize a grounded answer from context.
        Implements automatic backoff on rate limits.
        """
        if not self._genai_client:
            raise RuntimeError("Gemini client is not initialized. Please verify GEMINI_API_KEY.")

        prompt = (
            f"Official College Information:\n"
            f"-----------------------------------------\n"
            f"{context}\n"
            f"-----------------------------------------\n\n"
            f"Student Question: {query}\n\n"
            f"Instructions:\n"
            f"1. State the exact, direct answer immediately in the very first sentence.\n"
            f"2. Do NOT use filler intros like 'Based on the official college documents...'.\n"
            f"3. Make sure to include exact percentages, rules, or numbers from the documents.\n"
            f"4. If additional programme rules exist, explain them clearly and concisely below the main answer."
        )

        candidate_models = [self.generation_model]
        if "flash-lite" not in self.generation_model:
            candidate_models.append("gemini-3.5-flash-lite")

        for model_to_use in candidate_models:
            model_id = model_to_use.replace("models/", "")
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    # Modern google.genai SDK
                    if hasattr(self._genai_client, "models") and hasattr(self._genai_client.models, "generate_content"):
                        from google.genai import types
                        config = types.GenerateContentConfig(
                            system_instruction=self.SYSTEM_INSTRUCTION,
                            temperature=0.2,
                            max_output_tokens=1024,
                        )

                        response = self._genai_client.models.generate_content(
                            model=model_id,
                            contents=prompt,
                            config=config,
                        )
                        return response.text.strip() if response.text else self.FALLBACK_NO_INFO

                    # Legacy google.generativeai SDK
                    else:
                        leg_id = model_to_use if model_to_use.startswith("models/") else f"models/{model_to_use}"
                        model = self._genai_client.GenerativeModel(
                            model_name=leg_id,
                            system_instruction=self.SYSTEM_INSTRUCTION
                        )
                        response = model.generate_content(prompt)
                        return response.text.strip() if response.text else self.FALLBACK_NO_INFO

                except Exception as exc:
                    err_str = str(exc)
                    is_rate_limit = "RESOURCE_EXHAUSTED" in err_str or "429" in err_str
                    is_503 = "503" in err_str or "UNAVAILABLE" in err_str
                    if is_rate_limit:
                        delay = 15
                        m = re.search(r"retry in (\d+(?:\.\d+)?)s", err_str)
                        if m:
                            delay = int(float(m.group(1))) + 2
                        logger.warning(f"Gemini LLM Rate limit reached on {model_id}. Pausing {delay}s...")
                        time.sleep(delay)
                    elif is_503 and model_to_use != candidate_models[-1]:
                        logger.warning(f"Model {model_id} busy (503). Failing over to {candidate_models[-1]}...")
                        break
                    elif attempt < max_retries - 1:
                        logger.warning(f"Gemini LLM retry {attempt+1}/{max_retries} on {model_id}: {exc}")
                        time.sleep(2 * (attempt + 1))
                    else:
                        logger.error(f"Gemini LLM generation failed on {model_id}: {exc}")
                        if model_to_use == candidate_models[-1]:
                            raise

        return self.FALLBACK_NO_INFO

    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        """
        Process incoming chat message through the RAG pipeline.
        """
        user_message = request.message.strip()
        logger.info(f"[CHAT] Query received: '{user_message[:80]}'")

        # 1. Validation
        if not user_message:
            return ChatResponse(
                answer="Please enter a question about college academics, regulations, examinations, or services.",
                sources=[],
                mode="rag_gemini",
                session_id=request.conversation_id
            )

        # 2. Query Embedding
        try:
            query_embedding = self.embedding_service.embed_query(user_message)
            logger.info("[RAG] Query embedded")
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            return ChatResponse(
                answer="CampusAI is temporarily unable to reach the AI embedding service. Please try again.",
                sources=[],
                mode="error",
                session_id=request.conversation_id
            )

        # 3. ChromaDB Retrieval
        try:
            retrieved_chunks = self.vector_store.search_similar(
                query_embedding=query_embedding,
                top_k=self.top_k
            )
            logger.info(f"[RAG] Retrieved {len(retrieved_chunks)} chunks")
        except Exception as e:
            logger.error(f"Error querying ChromaDB vector store: {e}")
            return ChatResponse(
                answer="CampusAI is temporarily unable to retrieve college documents. Please try again.",
                sources=[],
                mode="error",
                session_id=request.conversation_id
            )

        # 4. Check Relevance / Empty Chunks
        if not retrieved_chunks:
            logger.info("[RAG] No chunks retrieved for query")
            return ChatResponse(
                answer=self.FALLBACK_NO_INFO,
                sources=[],
                mode="rag_gemini",
                confidence=0.0,
                session_id=request.conversation_id
            )

        # Filter out chunks exceeding distance threshold
        best_distance = retrieved_chunks[0].get("distance")
        if best_distance is not None and best_distance >= self.similarity_threshold:
            logger.info(f"[RAG] Best distance {best_distance:.4f} exceeds threshold {self.similarity_threshold}. Returning fallback without LLM call.")
            return ChatResponse(
                answer=self.FALLBACK_NO_INFO,
                sources=[],
                mode="rag_gemini",
                confidence=0.0,
                session_id=request.conversation_id
            )

        # Retain chunks within acceptable threshold
        valid_chunks = [
            c for c in retrieved_chunks
            if c.get("distance") is None or c.get("distance") < self.similarity_threshold
        ]

        if not valid_chunks:
            valid_chunks = retrieved_chunks[:2]

        # 5. Build Context & Extract Sources
        context = self.build_context(valid_chunks)
        sources = self.extract_sources(valid_chunks)

        # 6. Generate Grounded LLM Answer
        logger.info("[LLM] Generating grounded answer")
        try:
            answer = self.generate_llm_answer(user_message, context)
            logger.info("[CHAT] Response generated successfully")
        except Exception as e:
            logger.error(f"Error during Gemini LLM answer generation: {e}")
            return ChatResponse(
                answer="CampusAI is temporarily unable to reach the AI generation service. Please try again.",
                sources=sources,
                mode="error",
                session_id=request.conversation_id
            )

        # Compute average confidence from relevance
        confidence = None
        if sources and sources[0].relevance_score is not None:
            confidence = round(sum(s.relevance_score for s in sources if s.relevance_score is not None) / len(sources), 3)

        return ChatResponse(
            answer=answer,
            sources=sources,
            mode="rag_gemini",
            confidence=confidence,
            session_id=request.conversation_id
        )


chat_service = ChatService()

