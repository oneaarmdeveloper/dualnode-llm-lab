
```markdown
# DualNode LLM Lab 🤖

> A comparative performance study of self-hosted Large Language Models on consumer Windows hardware — with reproducible benchmarks, a custom dashboard, and honest results.

![Status](https://img.shields.io/badge/status-complete-success)
![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![Hardware](https://img.shields.io/badge/hardware-16GB%20RAM%20%7C%20Intel%20i7-orange)
![Level](https://img.shields.io/badge/level-beginner--friendly-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🎯 What This Project Is

Most "run AI locally" tutorials assume you own a gaming PC with 32+ GB RAM and a dedicated GPU. This project asks a more practical question:

> **"What can normal, everyday Windows PCs actually do with local AI?"**

**DualNode LLM Lab** answers with data. It benchmarks real performance on realistic hardware, provides reproducible tooling, and documents honest findings — including what *doesn't* work.

If you have never installed an AI model before, this guide takes you from zero to a working setup. If you have, it shows you how to structure the work like a real engineering project.

---

## 💻 Test System (PC-B)

| Component | Specification |
|-----------|--------------|
| **Model** | Acer Aspire A317-53 |
| **CPU** | Intel Core i7-1165G7 @ 2.80 GHz (11th Gen) |
| **RAM** | 16 GB DDR4 |
| **GPU** | Intel Iris Xe Graphics (integrated) |
| **Storage** | 512 GB NVMe SSD (301 GB free) |
| **OS** | Windows 11 Home, Build 26200 |
| **Network** | Mobile hotspot (personal) |

> ℹ️ This is a realistic consumer laptop — not a workstation. Results reflect what most users can expect.

---

## 📊 Benchmark Results

### Performance Summary

| Model | Size | Quantization | Avg Speed | Quality Rating | Notes |
|-------|------|--------------|-----------|----------------|-------|
| `llama3.2:3b` | 2.0 GB | Q4_K_M | **16.5 tok/s** | ⭐⭐⭐⭐ | Best speed/quality balance for 16 GB |
| `phi3:mini` | 2.3 GB | Q4_K_M | 14.4 tok/s | ⭐⭐⭐⭐ | Excellent reasoning, slightly slower |

*Metrics: 4 standardized prompts (reasoning, code, writing, knowledge), temperature=0.3, seed=42, num_predict=300. Full raw data in `benchmarks/`.*

### What "Tokens per Second" Means

- **>20 tok/s**: Feels instantaneous, like typing
- **10–20 tok/s**: Comfortable for interactive chat ✅ *Your results here*
- **5–10 tok/s**: Usable but noticeable delay
- **<5 tok/s**: Frustrating for conversation; better for background tasks

---

## 🚀 Quick Start

### Prerequisites
- Windows 10 or 11 (64-bit)
- 8+ GB RAM (16 GB recommended)
- 30+ GB free disk space
- Internet connection (for initial setup only)

### Step 1: Install Ollama
1. Download from [https://ollama.com](https://ollama.com)
2. Run `OllamaSetup.exe`
3. Verify: `ollama --version`

### Step 2: Pull a Model
```cmd
ollama pull llama3.2:3b
```

### Step 3: Run Locally
```cmd
ollama run llama3.2:3b
>>> Hello! Are you running on my PC?
```

### Step 4: Optional — Web Interface
```cmd
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```
Then visit: [http://localhost:3000](http://localhost:3000)

---

## 📁 Project Structure

```
dualnode/
├── README.md                    # You are here
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
│
├── scripts/
│   └── benchmark.py             # Python benchmark tool (stdlib only)
│
├── benchmarks/
│   ├── bench_PC-B_20260425_113650.json
│   └── bench_PC-B_20260425_*.json  # Raw performance data
│
├── dashboard/
│   └── index.html               # Interactive results dashboard (vanilla JS)
│
└── docs/
    ├── network-notes.md         # Real-world deployment constraints
    ├── results.md               # Detailed analysis (optional extension)
    └── hardware-specs.md        # Full system profiling data
```

---

## 🔍 Key Findings

### ✅ What Works Well
1. **16 GB RAM is sufficient** for 3B-parameter models at interactive speeds (>15 tok/s)
2. **Integrated graphics work** — no dedicated GPU required for basic inference
3. **Ollama + Open WebUI** provides a polished, ChatGPT-like experience locally
4. **Small models are surprisingly capable** — Phi-3 Mini and Llama 3.2 3B handle reasoning, code, and writing tasks well

### ⚠️ Real-World Constraints
1. **Network reliability matters** — Large model downloads (7B+) can fail on unstable/mobile connections due to DNS or CDN issues
2. **Model self-reports are unreliable** — Models may claim to be cloud-based even when running locally; empirical testing is essential
3. **RAM is the bottleneck** — Once a model loads, performance is CPU-bound; but loading requires contiguous free RAM

### 📉 Where 16 GB Hits Limits
- 7B+ models *can* run but may require careful memory management
- Context windows >4096 tokens increase RAM pressure significantly
- Running multiple models simultaneously is not feasible

---

## 🛠️ Tools & Technologies

| Tool | Purpose | Why Chosen |
|------|---------|------------|
| **Ollama** | Local inference runtime | Simple Windows install, clean API, active maintenance |
| **Open WebUI** | Chat interface | Polished UX, Docker-based, integrates seamlessly |
| **Python 3** | Benchmarking | Standard library only — no dependencies, maximum reproducibility |
| **Vanilla JS/HTML/CSS** | Dashboard | No build step, works forever, easy to audit |
| **Docker Desktop** | Containerization | Isolates Open WebUI, ensures consistent environment |

---

## 🔬 Methodology

### Benchmark Protocol
1. Close unnecessary applications to free RAM
2. Warm up each model with one trivial prompt
3. Run standardized prompt suite:
   - Reasoning: Widget production problem
   - Code: Prime number checker
   - Writing: Professional email
   - Knowledge: TCP vs UDP explanation
4. Capture Ollama's native timing metrics (`eval_duration`, `eval_count`)
5. Compute tokens per second: `eval_count / (eval_duration_ns / 1e9)`
6. Repeat for reproducibility

### Why This Matters
- Uses **model-reported timing** (more accurate than wall-clock)
- Fixed **temperature=0.3, seed=42** for reproducibility
- **Standard library only** — no pip dependencies to break
- Results saved as **structured JSON** for programmatic analysis

---

## 🌐 Network Notes

During development, large model downloads (7B+) occasionally failed on mobile hotspot connections with DNS resolution errors:

```
dial tcp: lookup ...cloudflarestorage.com: no such host
```

**Workarounds attempted:**
- DNS flush (`ipconfig /flushdns`)
- Alternative DNS servers (8.8.8.8, 1.1.1.1)
- Different model repositories

**Engineering takeaway:** Enterprise deployments should include:
- Local model caching/mirroring
- Robust retry logic with fallback CDNs
- Offline-first installation strategies

*See `docs/network-notes.md` for details.*

---

## 📈 Extending This Project

Ideas for further work:

- [ ] Add 7B model benchmarks when network conditions allow
- [ ] Implement quality scoring (LLM-as-judge) alongside speed metrics
- [ ] Add GPU acceleration measurements (if dedicated GPU available)
- [ ] Build a second node (8 GB PC) for distributed inference testing
- [ ] Add Prometheus/Grafana integration for production-style monitoring

---

## 🤝 Contributing

This project is designed to be forked and extended. If you run benchmarks on different hardware:

1. Fork the repo
2. Add your results to `benchmarks/` with a descriptive filename
3. Update `README.md` with your system specs
4. Submit a PR — community data makes this more valuable!

---

## 📄 License

MIT License — Use, extend, and learn freely.

> Copyright © 2026 Chukwuebuka Anselm Icheku  
>  
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  
>  
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  
>  
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

*Built for anyone who wants to understand what AI on their own hardware actually looks like — from the laptop under the desk to the home-lab box in the corner.*
``` 