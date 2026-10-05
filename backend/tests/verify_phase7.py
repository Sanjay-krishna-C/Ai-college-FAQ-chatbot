import sys
import json
import urllib.request
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

def run_post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return {
            "status": resp.status,
            "body": json.loads(resp.read().decode("utf-8"))
        }

def run_get(url: str) -> dict:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return {
            "status": resp.status,
            "body": json.loads(resp.read().decode("utf-8"))
        }

def main():
    base_url = "http://localhost:8000"
    print("=================================================================")
    print("      CAMPUSAI PHASE 7 — LIVE PIPELINE VERIFICATION")
    print("=================================================================")

    # 1. Health Check
    print("\n1. Testing GET /api/health ...")
    health = run_get(f"{base_url}/api/health")
    print(f"   * Status: {health['status']}")
    print(f"   * Body:   {health['body']}")
    assert health["status"] == 200, "Health endpoint failed!"

    # 2. RAG Stats Check
    print("\n2. Testing GET /api/rag/stats ...")
    stats = run_get(f"{base_url}/api/rag/stats")
    print(f"   * Status:               {stats['status']}")
    stats_data = stats["body"].get("stats", {})
    print(f"   * Collection Name:      {stats_data.get('collection_name')}")
    print(f"   * Total Indexed Chunks: {stats_data.get('total_chunks')}")
    print(f"   * Embedding Dimension:  {stats_data.get('embedding_dimension')}")
    print(f"   * Embedding Provider:   {stats_data.get('embedding_provider')}")
    print(f"   * Embedding Model:      {stats_data.get('embedding_model')}")

    # 3. Test Queries
    test_queries = [
        ("What is the attendance requirement?", "Attendance"),
        ("What are the examination regulations?", "Examination"),
        ("What is the academic calendar?", "Academic Calendar"),
        ("What are the hostel rules?", "Hostel Rules"),
        ("What is relative grading?", "Relative Grading"),
    ]

    print("\n3. Testing Mandatory RAG Test Queries against POST /api/chat ...")
    for idx, (query, label) in enumerate(test_queries, 1):
        print(f"\n   --- Query {idx}: '{query}' ({label}) ---")
        res = run_post(f"{base_url}/api/chat", {"message": query})
        status_code = res["status"]
        body = res["body"]
        answer = body.get("answer", "")
        sources = body.get("sources", [])
        mode = body.get("mode", "")

        print(f"   * HTTP Status:   {status_code}")
        print(f"   * Mode:          {mode}")
        print(f"   * Answer:        {answer[:160]}...")
        print(f"   * Sources Count: {len(sources)}")
        for s in sources[:2]:
            print(f"     - Doc: {s.get('document_name')} | Page: {s.get('page_number')} | Reg: {s.get('regulation')}")

        assert status_code == 200, f"Query '{query}' failed!"
        assert len(answer) > 20, "Answer is empty or too short!"
        assert len(sources) > 0, "No sources cited for institutional query!"

    # 4. Unsupported Query Check
    print("\n4. Testing Unsupported Query (Hallucination Prevention) ...")
    unsupported_query = "What is the formula for rocket fuel?"
    unsupported_res = run_post(f"{base_url}/api/chat", {"message": unsupported_query})
    u_body = unsupported_res["body"]
    u_answer = u_body.get("answer", "")
    u_sources = u_body.get("sources", [])

    print(f"   * Query:         '{unsupported_query}'")
    print(f"   * HTTP Status:   {unsupported_res['status']}")
    print(f"   * Answer:        '{u_answer}'")
    print(f"   * Sources Count: {len(u_sources)}")

    assert unsupported_res["status"] == 200
    assert "couldn't find enough information" in u_answer.lower() or "not enough information" in u_answer.lower(), (
        f"Model hallucinated an answer for unsupported query: {u_answer}"
    )
    assert len(u_sources) == 0, "Unsupported query returned citations!"

    print("\n=================================================================")
    print("  >>> ALL PHASE 7 VERIFICATION CHECKS PASSED SUCCESSFULLY! <<<")
    print("=================================================================")

if __name__ == "__main__":
    main()
