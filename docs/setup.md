# Setup

1. Install Python 3.10 or newer (64-bit). A GPU is not needed.
2. Clone and create a virtual environment:
   ```bash
   git clone https://github.com/brahmanandmathpati/Self-Learning-AI-Agent.git
   cd Self-Learning-AI-Agent
   python -m venv .venv
   source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```
3. Install PyTorch (CPU build) and the project:
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   pip install -e ".[dev]"
   ```
4. Create the database and check the install:
   ```bash
   sla init-db
   pytest -q
   ```
5. Optional: copy `.env.example` to `.env` to change the database path, run folder or Ollama settings. No API keys are used.
6. Optional explanations by a local LLM: install [Ollama](https://ollama.com), run `ollama pull qwen2.5:1.5b`. If Ollama is not running, the deterministic template is used automatically.
7. Optional: `pip install pygame` to show the CartPole picture on the Environments page.
