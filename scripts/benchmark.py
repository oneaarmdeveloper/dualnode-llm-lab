import json
import time
import urllib.request
import sys
import socket
import platform
from datetime import datetime, timezone
from pathlib import Path

PROMPTS = [
    {"id": "reasoning", "prompt": "If it takes 5 machines 5 minutes to make 5 widgets, how long does it take 100 machines to make 100 widgets?"},
    {"id": "code", "prompt": "Write a Python function that checks if a number is prime."},
    {"id": "writing", "prompt": "Write a professional email declining a meeting due to a conflict. Under 80 words."},
    {"id": "knowledge", "prompt": "Explain the difference between TCP and UDP in one sentence."},
]

def fetch(url, data=None):
    req = urllib.request.Request(url, data=data.encode() if data else None, headers={"Content-Type": "application/json"} if data else {})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read().decode()

def main():
    print("="*60)
    print("DualNode LLM Benchmark - PC-B")
    print("="*60)
    
    host = "http://localhost:11434"
    response = fetch(f"{host}/api/tags")
    models = json.loads(response).get("models", [])
    
    if not models:
        print("No models found. Pull one with: ollama pull llama3.2:3b")
        return
    
    results = {
        "node": "PC-B",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": {"hostname": socket.gethostname(), "platform": platform.platform()},
        "models": {}
    }
    
    for model in models:
        name = model["name"]
        print(f"\n--- Benchmarking {name} ---")
        model_data = {"prompts": []}
        total_tokens, total_time = 0, 0.0
        
        for p in PROMPTS:
            print(f"  [{p['id']}]... ", end="", flush=True)
            payload = json.dumps({"model": name, "prompt": p["prompt"], "stream": False, "options": {"temperature": 0.3, "num_predict": 300, "seed": 42}})
            start = time.perf_counter()
            try:
                resp = fetch(f"{host}/api/generate", data=payload)
                data = json.loads(resp)
                wall = time.perf_counter() - start
                tokens = data.get("eval_count", 0)
                duration = data.get("eval_duration", 0)
                tps = tokens / (duration / 1e9) if duration > 0 else 0
                print(f"{tps:.1f} tok/s ({wall:.1f}s)")
                
                model_data["prompts"].append({"category": p["id"], "success": True, "tok_per_sec": round(tps, 2)})
                total_tokens += tokens
                total_time += tokens / max(tps, 0.1)
            except Exception as e:
                print(f"ERROR: {e}")
                model_data["prompts"].append({"category": p["id"], "success": False})
        
        avg_tps = total_tokens / total_time if total_time > 0 else 0
        model_data["summary"] = {"avg_tok_per_sec": round(avg_tps, 2), "prompts_run": len(PROMPTS)}
        results["models"][name] = model_data
        print(f"  Average: {avg_tps:.2f} tok/s")
    
    out_file = Path("benchmarks") / f"bench_PC-B_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_file.parent.mkdir(exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Results saved to: {out_file}")

if __name__ == "__main__":
    main()