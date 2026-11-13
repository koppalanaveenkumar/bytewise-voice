# Handoff — continuing on another machine

*Written 2026-11-13 at the end of the first working session (on Windows). It summarizes everything decided and done so far, so work can continue on the Mac, or with a new Claude Code session that has no chat history.*

Read in this order: **this file → [ROADMAP.md](../ROADMAP.md) → [DEVELOPMENT_PLAN.md](../DEVELOPMENT_PLAN.md)**.

---

## 1. The project in one paragraph

ByteWise Voice is an **open-source, private, unlimited AI voice studio** (similar in spirit to ElevenLabs) that runs on the user's own Mac or PC. It uses **free, pre-trained open models** (Kokoro for fast preset voices, Chatterbox for voice cloning, optionally Orpheus/Phonon via Ollama later). **We do not train models.** We build the product around them: engine, API, a beautifully designed studio app and desktop packaging. Business model: **open-core** (free open-source core, paid Pro app/add-ons, cloud credits later).

## 2. Decisions made

| Topic | Decision |
|---|---|
| Platforms | Must run on **macOS and Windows** (one codebase) |
| Models | Free, open, commercial-safe licenses only. Kokoro (Apache-2.0), Chatterbox (MIT). Rejected: XTTS-v2, F5-TTS (non-commercial) |
| Training | **No training.** Use pre-trained models. Fine-tuning maybe in Stage 7 |
| Ollama | Optional "expressive voices" engine (Orpheus with emotion tags; Phonon on Apple Silicon) + Qwen script helper. Planned for Stage 5 / Sprint 8 |
| Open source | **Yes, open-core** |
| License | **AGPL-3.0 + CLA.** CLA (via CLA Assistant + standard template) only needed before the first outside contributor / before the repo goes public. A lawyer is optional, recommended before charging money |
| First customers | **Creators first** (YouTube narrators, course creators, audiobooks) |
| Language | **English first** |
| Pricing | Not decided: **to be tested** with users in Stage 0 (monthly vs one-time) |
| UI | **Custom-designed React app** (no plain static HTML). React + TypeScript + Vite + Tailwind + shadcn/ui |
| Name | "ByteWise Voice": trademark check still open |

## 3. How we work (important for Claude)

- **The user implements the code.** Claude gives code in batches, with exact file paths, commands to run and the expected output. The user creates the files and runs them, then reports results or errors.
- **No downloads or installs without the user's decision.** Always say how big a download is before it happens.
- Claude may update the planning docs (ROADMAP.md, DEVELOPMENT_PLAN.md, this file) directly.
- Shell: **Git Bash on Windows**, **zsh (Terminal) on Mac**. Give commands for the shell in use.
- Keep explanations simple and plain. Use tables and step-by-step lists.

## 4. Status

### Sprint 0 (setup)
- [x] Old prototype (Gradio `app.py`, `static/`, old `app/`) deleted. Starting fresh
- [x] Docs: README, CONTRIBUTING, THIRD_PARTY_LICENSES, LICENSE (AGPL-3.0)
- [x] `git init` (branch `main`)
- [x] First commit + private GitHub repo: https://github.com/koppalanaveenkumar/bytewise-voice (branch `main`)
- [x] New README with badges, feature status, quick start, Mermaid diagram, and an **animated SVG banner** (`docs/assets/banner.svg`, respects reduced motion)
- [ ] Own voice recording (currently using a test clip, see 6.7)
- [ ] Demo clips, landing page, mockups, creator interviews (business/design track, not started)

### Sprint 1 (engine + app shell)
**Batch 1: backend skeleton.** ✅ Done on Windows: **11 tests pass**.
- `pyproject.toml` (extras: `dev`, `torch`), settings, data folders, security (localhost only, optional token), engine interface, fake engine, engine selection, `/api/health`, `/api/models`, `/api/voices`, tests, CI workflow (Mac + Windows)

**Batch 2: real voices.** In progress.
- ✅ `torch_backend.py` (Kokoro + Chatterbox via PyTorch) and `scripts/say.py` (text → WAV from the terminal)
- ✅ Kokoro works on Windows CPU at **2.81x real time**
- ⏳ Chatterbox cloning on Windows: model downloaded, watermarker fix found (6.4), **result not yet tested**
- ⬜ `mlx_backend.py` for Apple Silicon (**next task on the Mac**, see section 7)
- ⬜ `scripts/benchmark.py` (B1.11)

**D1.3 (pre-commit with ruff):** ✅ done and committed (`.pre-commit-config.yaml`, ruff-pre-commit `v0.17.5`, hooks `ruff-check --fix` + `ruff-format`). On each new machine, run `pre-commit install` once.

**Batch 3: React app.** Not started: F1.1–F1.6, D1.1 (`scripts/dev.py`).
**Spike S1.2** (PyInstaller packaging test): not started.

## 5. Code that exists now

```
app/
  __init__.py              version
  config.py                settings from BYTEWISE_* env vars / .env
  paths.py                 user data folder (platformdirs)
  security.py              optional X-ByteWise-Token check, allowed hosts
  main.py                  FastAPI app: TrustedHost + CORS, /api router
  api/deps.py              BackendDep
  api/health.py            GET /api/health, GET /api/models
  api/voices.py            GET /api/voices (preset voices)
  engine/backends/
    base.py                Backend protocol, SpeechRequest, ModelInfo, VoiceInfo, SAMPLE_RATE=24000
    fake_backend.py        test tones. Used by tests/CI and for UI work
    registry.py            picks engine: BYTEWISE_BACKEND, else mlx on Apple Silicon, else torch.
                           Falls back to fake (with a warning) if the engine isn't installed
    torch_backend.py       Kokoro (KPipeline) + Chatterbox (ChatterboxTTS), lazy-loaded
scripts/say.py             python scripts/say.py "text" [--model chatterbox --voice voices/myvoice.wav]
tests/                     conftest (fake engine + temp data dir), test_api, test_fake_backend
.github/workflows/ci.yml   ruff + pytest on macos-latest and windows-latest
```

## 6. Problems we hit and how we solved them

1. **MLX doesn't run on Windows.** `mlx` fails with `DLL load failed`. That's why there are two engines: `mlx` (Apple Silicon) and `torch` (everything else).
2. **`ImportError: cannot import name 'Backend' from 'app.engine.backends' (unknown location)`.** The `__init__.py` files were missing. Every package folder needs one (`app/api`, `app/engine`, `app/engine/backends`, `tests`).
3. **`chatterbox-tts` pins exact old versions.** A dry run showed it would downgrade torch 2.15→2.6, numpy 2.5→1.26, starlette 1.10→0.52 (our web server!), huggingface_hub 2.4→1.33, transformers/tokenizers/safetensors, and add gradio, pandas, onnx etc. **Solution for now:** a separate experiment venv `venv-clone` (`pip install -e ".[torch]" chatterbox-tts`). The main `venv` stays clean. Kokoro also works in `venv-clone` (2.30x). **Open decision for Sprint 2:** how to ship Chatterbox in the main app (e.g. `--no-deps` + only the packages it really needs, or accept its pins).
4. **Chatterbox: `TypeError: 'NoneType' object is not callable` at `perth.PerthImplicitWatermarker()`.** The real error was `No module named 'pkg_resources'`: the `resemble-perth` watermarker needs `pkg_resources`, which setuptools ≥ 81 no longer ships. **Fix:** `pip install "setuptools<81"` in that venv. Keep the watermark: the safety plan relies on it.
5. **Drive C: on the Windows PC filled up.** The Hugging Face model cache was moved to `E:\hf-cache` (`setx HF_HOME 'E:\hf-cache'` + `export HF_HOME="E:/hf-cache"` in `~/.bashrc`). VS Code terminals only see new env vars after VS Code is fully restarted. This led to a planned feature: **model storage location** in Settings (task B4.1).
6. **Git Bash path gotcha.** `pip freeze > output\file.txt` created a file named `outputfile.txt`. In Git Bash, always use forward slashes.
7. **Test voice.** For local testing only, the voice sample is an ElevenLabs clip ("Marcus", a Professional Voice Clone of a real person) converted to `voices/myvoice.wav` (32.8 s; Chatterbox uses about the first 10 s). **Never commit it, never use it in demos or on the landing page, and replace it with the founder's own recording before beta.** Files in `voices/` are git-ignored.
8. **CI failed on `ruff format --check`.** Code handed over in Batch 2 wasn't in ruff's formatting (lint itself passed). Fixed with `ruff format .`. **Rule from now on:** all code Claude gives must already be ruff-formatted (line length 100), and pre-commit catches anything missed.

## 7. Next steps on the Mac

1. Set up the project (section 9).
2. Run `pytest`: it should show 11 passed (fake engine).
3. **B1.4: write `app/engine/backends/mlx_backend.py`** (ask Claude for the code). Notes from the old prototype, which worked on the Mac with `mlx-audio`:
   - Kokoro: `load_model("mlx-community/Kokoro-82M-bf16")`, then `model.generate(text=..., voice="am_puck", speed=..., lang_code="a")`
   - Chatterbox: `load_model("mlx-community/chatterbox-multilingual-v3")`, then `model.generate(text=..., ref_audio=path, exaggeration=..., lang_code="en")`
   - Each result has `.audio`: `np.array(r.audio).flatten()`, at 24 kHz
   - `from mlx_audio.tts.utils import load_model`. The old requirements had `mlx-audio` and `misaki`
   - Add an `mlx` extra to `pyproject.toml` (Apple Silicon only, via environment markers)
4. Benchmark Kokoro + Chatterbox on the Mac with `scripts/say.py` and add the results to the Benchmark log (DEVELOPMENT_PLAN.md §10).
5. Until `mlx_backend.py` exists, the Mac can also use the PyTorch engine: `pip install -e ".[torch]"` and run with `BYTEWISE_BACKEND=torch`.
6. Then Batch 3 (React app shell), D1.3, B1.11, spike S1.2.

**Still open on Windows:** finish the Chatterbox test in `venv-clone` (6.4 fix, then `say.py --model chatterbox`) and record the speed.

## 8. Before leaving the Windows PC: commit and push

See the step-by-step list in the chat message that came with this file (fix `.gitignore`, add `.gitattributes`, delete the stray file, commit, create a private GitHub repo, push).

**Doesn't travel through git** (copy by hand or recreate):
| Item | On the Mac |
|---|---|
| `venv/`, `venv-clone/` | Create a new venv (venvs can't be copied between OSes) |
| AI models | Downloaded again on first use (the Mac uses MLX versions anyway) |
| `voices/test-voice.mp3`, `voices/myvoice.wav` | Copy via AirDrop / USB / cloud drive if you want the same test voice |
| `output/` | Not needed |
| Claude's memory notes on Windows | Replaced by `CLAUDE.md` + this file |

## 9. Mac setup (zsh)

```bash
# Python 3.12 (if missing): brew install python@3.12
git clone https://github.com/<your-username>/bytewise-voice.git
cd bytewise-voice
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest                      # expect 11 passed
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

Then open the folder in VS Code, start Claude Code, and say: **"Read docs/HANDOFF.md and let's continue with B1.4 (mlx_backend)."**

## 10. Benchmarks so far

| Machine | Engine | Model | Load | Speed |
|---|---|---|---|---|
| Windows laptop (Intel CPU, no NVIDIA GPU, 32 GB) | torch CPU, main venv | Kokoro | 22.1 s | **2.81x** |
| same | torch CPU, `venv-clone` (torch 2.6) | Kokoro | 29.6 s | 2.30x |
| same | torch CPU | Chatterbox | — | not measured yet |
