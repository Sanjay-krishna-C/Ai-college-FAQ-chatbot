import urllib.request
import json
import time

questions = [
    "What is the attendance requirement?",
    "What are the examination regulations?",
    "What are the hostel rules?",
    "What is relative grading?"
]

for q in questions:
    print(f"\n{'='*50}\nQUESTION: {q}")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/chat",
        data=json.dumps({"message": q}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            dt = time.time() - t0
            print(f"Status: {resp.status} ({dt:.1f}s)")
            print("DIRECT ANSWER:")
            print(data.get("answer", ""))
            print(f"\nSOURCES ({len(data.get('sources', []))}):")
            for s in data.get("sources", [])[:3]:
                print(f"  - {s.get('document_name')} (Page {s.get('page_number')})")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(2)
