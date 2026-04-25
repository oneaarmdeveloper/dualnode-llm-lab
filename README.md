# DualNode LLM Lab

> A comparative performance study of self-hosted Large Language Models on consumer Windows hardware — with reproducible benchmarks, a custom dashboard, and honest results.

![Status](https://img.shields.io/badge/status-phase1_complete-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![Hardware](https://img.shields.io/badge/hardware-16GB%20RAM%20%7C%20Intel%20i7-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Project Status

| Node | RAM | Status | Models Tested |
|------|-----|--------|---------------|
| **PC-B** | 16 GB | Phase 1 Complete | llama3.2:3b, phi3:mini |
| **PC-A** | 8 GB | Phase 2 Pending | (awaiting hardware access) |

---

## Test System (PC-B)

| Component | Specification |
|-----------|---------------|
| **Model** | Acer Aspire A317-53 |
| **CPU** | Intel Core i7-1165G7 @ 2.80 GHz |
| **RAM** | 16 GB DDR4 |
| **GPU** | Intel Iris Xe Graphics (integrated) |
| **Storage** | 512 GB NVMe SSD (301 GB free) |
| **OS** | Windows 11 Home, Build 26200 |

---

## Benchmark Results (PC-B)

| Model | Size | Avg Speed | Notes |
|-------|------|-----------|-------|
| `llama3.2:3b` | 2.0 GB | **16.5 tok/s** | Best speed/quality balance |
| `phi3:mini` | 2.3 GB | 14.4 tok/s | Excellent reasoning for size |

*Full data: `benchmarks/bench_PC-B_*.json`*

---

## Quick Start

```cmd
ollama pull llama3.2:3b
ollama run llama3.2:3b
```

Web UI (optional):

```cmd
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

Then visit: [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
dualnode/
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   └── benchmark.py
├── benchmarks/
│   └── bench_PC-B_*.json
├── dashboard/
│   └── index.html
└── docs/
```

---

## Phase 2: PC-A (8 GB) Plan

When 8 GB hardware is available:

1. Install Ollama (same steps as PC-B)
2. Pull small models: `llama3.2:3b`, `phi3:mini`, `gemma2:2b`
3. Run `python scripts/benchmark.py --node PC-A`
4. Copy results to `benchmarks/`
5. Update dashboard to load both JSON files
6. Commit and push comparative results

---

## License

MIT License. See `LICENSE`.   