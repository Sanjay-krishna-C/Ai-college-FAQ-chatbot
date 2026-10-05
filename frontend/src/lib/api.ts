/**
 * CampusAI Frontend API Client
 * Connects Next.js UI to the FastAPI backend.
 */

export interface ChatSource {
  document_name: string;
  source_file?: string;
  title?: string;
  page_number?: number | null;
  regulation?: string | null;
  clause_reference?: string | null;
  snippet?: string | null;
  relevance_score?: number | null;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
  mode: string;
  confidence?: number | null;
  session_id?: string | null;
}

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${apiUrl}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    throw new Error(`CampusAI backend returned status ${response.status}`);
  }

  return response.json();
}
