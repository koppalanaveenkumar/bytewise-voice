# ByteWise Voice — notes for Claude

Open-source, private, unlimited AI voice studio for Mac and Windows, built on free pre-trained TTS models (Kokoro, Chatterbox; Ollama later). We build the product. We do not train models.

**Start here:** [docs/HANDOFF.md](docs/HANDOFF.md) (current status, decisions, problems solved, next steps), then [ROADMAP.md](ROADMAP.md) (product/startup plan) and [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) (architecture, API, sprint tasks with IDs like B1.4).

## How to work with this user

- **The user implements the code.** Give code in batches with exact file paths, then the commands to run and the expected output. Don't create or edit code files yourself unless asked. Updating the planning docs (ROADMAP.md, DEVELOPMENT_PLAN.md, docs/HANDOFF.md) directly is fine.
- **Never download or install anything** (packages, models) without the user deciding. State the download size first. Read-only checks are fine.
- Shell: **Git Bash on Windows**, **zsh on Mac**. Match the commands to the machine.
- Plain, simple language. Short steps and tables.
- After each result, update the Benchmark log (DEVELOPMENT_PLAN.md §10) and tick off tasks.
- **All Python code you hand over must already be ruff-formatted** (line length 100, see `pyproject.toml`). CI runs `ruff format --check` and fails otherwise.
- Keep [docs/HANDOFF.md](docs/HANDOFF.md) current at the end of each session (status, problems solved, next steps), so work can move between the Windows PC and the Mac.

## Key technical facts

- Engines: `mlx` (Apple Silicon, `mlx-audio`), `torch` (Windows/Linux/Intel Mac: `kokoro`, `chatterbox-tts`), `fake` (test tones for tests/CI/UI work). Selection is in `app/engine/backends/registry.py`. Override with `BYTEWISE_BACKEND`.
- All engines return float32 mono audio at 24 kHz through the `Backend` protocol in `app/engine/backends/base.py`.
- `chatterbox-tts` pins old versions (torch 2.6, numpy 1.26, starlette 0.52, gradio …), so don't install it into the main venv without a plan (see HANDOFF §6.3). Its watermarker needs `setuptools<81`.
- Voice samples in `voices/` are git-ignored and must never be committed.

## Commands

```bash
pip install -e ".[dev]"          # core + dev tools
pip install -e ".[torch]"        # PyTorch engine (Kokoro), ~1 GB incl. model on first use
pytest                           # tests use the fake engine
ruff check . --fix && ruff format .
uvicorn app.main:app --reload    # API at http://127.0.0.1:8000/docs
python scripts/say.py "Hello."   # text → output/say.wav with the current engine
```
