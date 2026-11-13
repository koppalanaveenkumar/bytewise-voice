# ByteWise Voice — Development Plan

*v1 · 13 Nov 2026 · Companion to [ROADMAP.md](ROADMAP.md) (the roadmap says **what and why**, this plan says **how and in what order**).*

**Assumes:** one full-time developer, 2-week sprints. Each sprint ends with everything working on **both macOS and Windows**.

---

## 1. What we build vs. what we use

| We **use** (download, don't build) | We **build** (our code) |
|---|---|
| Pre-trained speech models: Kokoro, Chatterbox, Orpheus | The engine: text cleanup, chunking, pauses, streaming, joining |
| Ollama (runs Orpheus and Qwen) | The FastAPI server: jobs, projects, voices, exports |
| Open-source libraries (FastAPI, React, Tauri …) | The React studio app and design system |
| | The desktop packaging, installers, model download manager |

**No model training** until at least Stage 7 (and even then only fine-tuning, see the roadmap).

---

## 2. Development environment

Install these **when Sprint 1 starts**, not before. Same list on Mac and Windows.

| Tool | Version | Needed from |
|---|---|---|
| Git | latest | Sprint 0 |
| Python | 3.12 | Sprint 1 |
| Node.js | current LTS | Sprint 1 |
| pnpm | latest | Sprint 1 |
| VS Code + extensions: Python, Ruff, ESLint, Tailwind CSS IntelliSense | latest | Sprint 1 |
| Rust toolchain (for Tauri) | stable | Sprint 4 |
| Ollama | latest | Sprint 8 |

**Rules:**
- Each machine creates its own `venv`. Never copy a venv between Mac and Windows.
- Model weights are downloaded **once, on purpose**, into the Hugging Face cache, never committed to git.
- For UI work you don't need any model: run with `BYTEWISE_BACKEND=fake` (see 3.3).

---

## 3. Architecture decisions (the contracts)

These are the rules every sprint builds on. Change them only with a note in `docs/decisions/`.

### 3.1 Repository layout

```
bytewise-voice/
├── app/                        Python backend (FastAPI)
│   ├── main.py                 creates the app, registers routers
│   ├── config.py               settings (env vars + settings file)
│   ├── paths.py                where user data lives (see 3.6)
│   ├── db.py                   SQLite connection + tables
│   ├── api/                    one file per area
│   │   ├── health.py
│   │   ├── voices.py
│   │   ├── projects.py
│   │   ├── jobs.py
│   │   └── exports.py
│   ├── engine/
│   │   ├── pipeline.py         text → chunks → audio → files
│   │   ├── text.py             normalisation + sentence chunking
│   │   ├── audio.py            trim, pauses, loudness, resample, encode
│   │   ├── jobs.py             job queue + single worker thread
│   │   └── backends/
│   │       ├── base.py         the Backend interface (3.3)
│   │       ├── registry.py     picks backends per machine
│   │       ├── fake_backend.py tests + UI work without models
│   │       ├── mlx_backend.py  Apple Silicon
│   │       ├── torch_backend.py Windows / Linux / Intel Mac
│   │       └── ollama_backend.py Orpheus via Ollama (Sprint 8)
│   └── models.py               database tables (SQLModel)
├── tests/                      pytest
├── scripts/
│   ├── dev.py                  starts backend + frontend together
│   └── benchmark.py            speed test per model per machine
├── frontend/                   React app
│   ├── src/
│   │   ├── components/ui/      design system
│   │   ├── features/           studio, voices, projects, settings, onboarding
│   │   ├── lib/                api client, audio player, shortcuts
│   │   ├── styles/             design tokens
│   │   └── api-types.ts        generated from FastAPI (3.5)
│   └── e2e/                    Playwright tests
├── desktop/                    Tauri shell (Sprint 4)
├── docs/decisions/             architecture decision records
├── .github/workflows/          CI
├── pyproject.toml              dependencies + extras (dev, mlx, torch), ruff + pytest config
├── README.md · ROADMAP.md · DEVELOPMENT_PLAN.md
└── LICENSE · CONTRIBUTING.md · THIRD_PARTY_LICENSES
```

### 3.2 Request flow

```
React app ──HTTP──▶ FastAPI ──▶ Job queue ──▶ single worker thread
    ▲                                              │
    │                                     pipeline.py
    │                                     text.py → chunks
    │                                     backend.generate(chunk)
    │                                     audio.py → pauses, trim
    └──────── WebSocket: progress + audio chunks ◀─┘
```

- **One worker thread** runs all generation. Models are big and not thread-safe, so jobs wait in a queue instead of running in parallel.
- The API never blocks while audio is being generated. It returns a `job_id` straight away.

### 3.3 The Backend interface

Every engine implements the same small interface, so the rest of the app never knows which one is running:

```python
class Backend(Protocol):
    name: str  # "mlx" | "torch" | "ollama" | "fake"

    def is_available(self) -> bool: ...  # can it run on this machine?
    def models(self) -> list[ModelInfo]: ...  # e.g. kokoro, chatterbox
    def preset_voices(self, model: str) -> list[VoiceInfo]: ...
    def generate(self, req: SpeechRequest) -> Iterator[np.ndarray]:
        ...
        # yields float32 mono audio at 24 kHz, chunk by chunk


@dataclass
class SpeechRequest:
    model: str  # "kokoro" | "chatterbox" | "orpheus"
    text: str  # one chunk, already cleaned
    voice: str  # preset voice id, or path to a reference sample
    speed: float = 1.0
    energy: float = 0.5
    lang: str = "en"
```

**Backend selection** (`registry.py`):
1. `BYTEWISE_BACKEND` env var wins if set (`mlx`, `torch`, `fake`).
2. macOS + arm64 → `mlx`.
3. Everything else → `torch` (CUDA if available, else CPU).
4. `ollama` is added on top whenever `localhost:11434` responds.

**`fake` backend:** returns a short tone per chunk, with a small delay. Used in CI and for frontend work, so nobody needs gigabytes of models to work on the UI.

### 3.4 API (v1)

All routes are under `/api`. FastAPI's `/docs` page always shows the live version.

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Backend, device, loaded models, Ollama status, app version |
| GET | `/models` | Models: installed or not, size, which backend |
| GET | `/voices` | Preset + cloned voices |
| POST | `/voices` | Create a cloned voice (multipart: name, sample file, `consent=true`) |
| PATCH / DELETE | `/voices/{id}` | Rename / delete a voice |
| GET | `/voices/{id}/preview` | Short preview clip |
| GET / POST | `/projects` | List / create projects |
| GET / PATCH / DELETE | `/projects/{id}` | One project (title, default voice, settings) |
| PUT | `/projects/{id}/blocks` | Save all paragraph blocks of a project |
| POST | `/projects/{id}/generate` | Generate all blocks or a list of `block_ids`. Returns `job_id` |
| POST | `/tts` | Quick generate without a project. Returns `job_id` |
| GET | `/jobs/{id}` | Status, progress, error |
| POST | `/jobs/{id}/cancel` | Cancel a job |
| WS | `/jobs/{id}/stream` | Live progress + audio chunks (3.7) |
| POST | `/projects/{id}/export` | Export WAV or MP3. Returns `job_id` |
| GET | `/exports` · `/exports/{id}/file` | Export history / download |
| GET / PATCH | `/settings` | App settings |

### 3.5 Frontend ↔ backend types

- FastAPI generates an OpenAPI description automatically.
- `pnpm gen:api` runs **openapi-typescript** and writes `frontend/src/api-types.ts`.
- The frontend never hand-writes API types. If the backend changes, regenerate.

### 3.6 Data storage

User data is stored in the operating system's normal app-data folder (via the `platformdirs` package), **not** inside the project folder:

| OS | Location |
|---|---|
| macOS | `~/Library/Application Support/ByteWise/` |
| Windows | `%LOCALAPPDATA%\ByteWise\` (local, not roaming: audio files are large) |

Inside it: `bytewise.db` (SQLite), `voices/`, `audio/` (block audio), `exports/`, `logs/`.

**Database tables** (SQLModel on SQLite):

| Table | Main fields |
|---|---|
| `voice` | id, name, kind (`preset`/`cloned`/`expressive`), model, sample_path, language, consent_at, consent_by, created_at |
| `project` | id, title, default_voice_id, settings (JSON), created_at, updated_at |
| `block` | id, project_id, position, text, voice_id (empty = project default), settings (JSON), audio_path, **audio_hash**, status |
| `job` | id, type, status (`queued`/`running`/`done`/`failed`/`canceled`), progress, error, created_at |
| `export` | id, project_id, format, path, duration_s, created_at |

**`audio_hash` = hash of (text + voice + settings + model version).** When a project is generated again, only blocks whose hash changed are regenerated. This makes per-paragraph editing fast.

### 3.7 Streaming protocol (WebSocket)

Messages from server to browser:

```
{"type": "progress", "block_id": "...", "done": 3, "total": 12}
{"type": "chunk", "block_id": "...", "seq": 7, "sample_rate": 24000}   ← followed by one binary frame: float32 PCM
{"type": "block_done", "block_id": "...", "audio_url": "/api/..."}
{"type": "done"} | {"type": "error", "message": "..."}
```

The browser queues chunks in the Web Audio API and plays them back to back. wavesurfer.js redraws the waveform as chunks arrive.

### 3.8 Local security

A server on `localhost` can be reached by any website the user visits, so:
- Bind to **127.0.0.1 only**, never `0.0.0.0`.
- The desktop app starts the server with a **random port and a random token**. Every request must send the token in a header.
- Strict CORS: only the app's own origin.
- Reject requests whose `Host` header isn't `127.0.0.1` / `localhost` (protects against DNS rebinding).
- Uploaded files: check type and size, and store them under generated names, never the user's file name.

### 3.9 Audio standards

- Internal format: **float32, mono, 24 kHz** everywhere.
- Voice samples on upload: convert to mono 24 kHz WAV, trim silence, check length 10–30 s, normalise loudness.
- Exports: WAV (16-bit) and MP3. Prefer a pip package with a built-in MP3 encoder over bundling `ffmpeg` (check during Sprint 3).
- Final loudness target: about −16 LUFS (typical for spoken content), with no clipping.

---

## 4. Coding standards

| Area | Standard |
|---|---|
| Python style | **Ruff** for linting + formatting. Type hints on all public functions |
| Python tests | **pytest** + `httpx` test client. The `fake` backend in CI |
| TypeScript | `strict` mode, **ESLint** + **Prettier** |
| Frontend tests | **Vitest** (units), **Playwright** (main flows), **axe** (accessibility) |
| Commits | Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:` |
| Branches | `feat/short-name`, `fix/short-name`. `main` is always releasable |
| Pull requests | Small, one topic, CI green on Mac + Windows, screenshots for UI changes |
| Versions | Semantic versioning: `0.x` until public launch, `1.0.0` at launch |
| Decisions | Important choices go into `docs/decisions/NNNN-title.md` with the reason |

**Definition of Done (every task):**
1. Works on macOS **and** Windows
2. Tests added or updated, CI green
3. UI: checked in dark + light theme, keyboard usable, passes axe
4. Docs or README updated if behaviour changed
5. No secrets, personal audio or model files committed

---

## 5. Sprint plan

Task IDs: **B** = backend, **F** = frontend, **D** = desktop/devops, **S** = spike (a short experiment to remove a risk early).

### Sprint 0 — Foundations (Weeks 1–2) · Roadmap Stage 0

Runs alongside the validation work (interviews, landing page, mockups).

- [ ] **D0.1** `git init`, `.gitignore` (venv, `output/`, `node_modules/`, `__pycache__/`, `.env`, `*.wav` outside `tests/fixtures`)
- [ ] **D0.2** Delete the old Gradio `app.py`
- [ ] **D0.3** `README.md` (what it is, how to run on Mac/Windows), `LICENSE`, `CONTRIBUTING.md`, `THIRD_PARTY_LICENSES`
- [ ] **D0.4** Record `voices/myvoice.wav` (English, 10–20 s, quiet room)
- [ ] **D0.5** Generate 3 demo clips on the Mac with the existing MLX code (for the landing page)
- [ ] **D0.6** Create the GitHub repo (private until the licence is chosen and the clean-up is done)

**Done when:** clean repo on GitHub, demo clips ready, Figma mockups done (design track).

### Sprint 1 — Cross-platform engine + app shell (Weeks 3–4) · Roadmap Stage 1

Backend:
- [ ] **B1.1** New layout from 3.1. Move current code into `app/engine/`
- [ ] **B1.2** `backends/base.py`: `Backend`, `SpeechRequest`, `ModelInfo`, `VoiceInfo`
- [ ] **B1.3** `fake_backend.py`
- [ ] **B1.4** `mlx_backend.py`: port the current Kokoro + Chatterbox MLX code
- [ ] **B1.5** `torch_backend.py`: Kokoro (`kokoro` package) + Chatterbox (`chatterbox-tts`), device = CUDA or CPU
- [ ] **B1.6** `registry.py`: selection rules from 3.3
- [ ] **B1.7** `config.py` + `paths.py` (platformdirs)
- [ ] **B1.8** `GET /api/health`, `GET /api/models`, `GET /api/voices` (presets only)
- [ ] **B1.9** FastAPI becomes API-only: remove the `static/` folder and the static-file mounts
- [ ] **B1.10** `pyproject.toml` with extras: `dev`, `mlx` (Apple Silicon only), `torch`. Engines are installed separately, on purpose
- [ ] **B1.11** `scripts/benchmark.py`: fixed 3-paragraph English text, prints seconds of audio per second of compute, per model

Frontend:
- [ ] **F1.1** Set up `frontend/`: Vite + React + TypeScript + Tailwind + shadcn/ui + React Router
- [ ] **F1.2** Design tokens from Figma (colours, type, spacing, radius, shadows), dark + light
- [ ] **F1.3** Base components: Button, Input, Textarea, Slider, Select, Card, Dialog, Toast, Progress, Badge, Tooltip
- [ ] **F1.4** App shell: sidebar (Projects, Voices, History, Settings), top bar, theme switch, `Cmd/Ctrl+K` command menu
- [ ] **F1.5** API client + `pnpm gen:api` (3.5), TanStack Query set up
- [ ] **F1.6** Engine status badge from `/api/health`

DevOps:
- [ ] **D1.1** `scripts/dev.py`: one command starts FastAPI + Vite (Vite forwards `/api` to FastAPI)
- [ ] **D1.2** GitHub Actions matrix **macOS + Windows**: ruff, pytest (fake backend), ESLint, typecheck, Vitest, frontend build
- [ ] **D1.3** Pre-commit hooks (ruff, prettier)

Spikes (time-boxed, 1 day each):
- [ ] **S1.1** Chatterbox speed on the Windows laptop CPU. Record the benchmark in the roadmap
- [ ] **S1.2** Packaging test: bundle a tiny FastAPI + torch app with PyInstaller on Mac and Windows. Note the size and startup time. **This removes the biggest technical risk early.**

**Done when:** the same English script makes audio with both models on Mac (mlx) and Windows (torch). The app shell runs on both and shows the live engine status. CI is green on both.

### Sprint 2 — Text pipeline, jobs, projects, studio editor (Weeks 5–6) · Roadmap Stage 2

Backend:
- [ ] **B2.1** `text.py`: split paragraphs → sentences → chunks under ~250 characters. Normalise numbers, dates, currency, abbreviations, URLs. Pronunciation dictionary. `[pause 1s]` markup
- [ ] **B2.2** Unit tests for `text.py` (the easiest place to get lots of test coverage)
- [ ] **B2.3** `db.py` + `models.py`: tables from 3.6
- [ ] **B2.4** Projects + blocks API, with `audio_hash` caching
- [ ] **B2.5** `jobs.py`: queue, one worker thread, progress, cancel
- [ ] **B2.6** `/projects/{id}/generate`, `/tts`, `/jobs/{id}`, `/jobs/{id}/cancel`
- [ ] **B2.7** WebSocket streaming (3.7)
- [ ] **B2.8** `audio.py`: pauses between sentences/paragraphs, trim silence, loudness normalisation

Frontend:
- [ ] **F2.1** Projects screen: grid, create, rename, delete
- [ ] **F2.2** Studio editor with TipTap: paragraph blocks, `[pause]` chips, block status
- [ ] **F2.3** Voice + speed/energy side panel, per-block voice override
- [ ] **F2.4** Streaming player: Web Audio queue + wavesurfer.js waveform that grows live
- [ ] **F2.5** Generate / regenerate block / cancel, with progress
- [ ] **F2.6** Shortcuts: `Space`, `Cmd/Ctrl+Enter`, `Cmd/Ctrl+S`

Spike:
- [ ] **S2.1** Streaming latency: measure the time to first audio with Kokoro on both OSes. Target under 2 s

**Done when:** write a project with several paragraphs, generate it, hear audio start in about 2 s, edit one paragraph, and only that paragraph regenerates.

### Sprint 3 — Voice library, cloning, exports, polish (Weeks 7–8) · Roadmap Stage 2

Backend:
- [ ] **B3.1** Voice upload: check type/size, convert to mono 24 kHz, trim, check 10–30 s, normalise
- [ ] **B3.2** Consent stored with the voice (`consent_at`, `consent_by`). Upload is rejected without it
- [ ] **B3.3** Voice preview endpoint, rename, delete (also deletes the files)
- [ ] **B3.4** Export WAV + MP3 as a job. Export history
- [ ] **B3.5** Error handling: clear messages for "model not installed", "sample too short", "out of memory"

Frontend:
- [ ] **F3.1** Voice library: cards, preview, filters, rename, delete
- [ ] **F3.2** Clone wizard: record in the browser (MediaRecorder) or upload → level meter → consent → test sentence → save
- [ ] **F3.3** History & exports screen
- [ ] **F3.4** Loading, empty and error states for every screen
- [ ] **F3.5** Playwright tests: create project → generate → export; clone a voice
- [ ] **F3.6** Accessibility pass (axe in CI, keyboard-only walkthrough)

**Done when:** you can make a real 10-minute narration with your cloned voice and export an MP3, all inside the app. **Usability test:** 5 creators, rating 8/10 or higher.

🎯 **Milestone: MVP complete.** Tag `v0.1.0`.

### Sprint 4 — Desktop app, Mac first (Weeks 9–10) · Roadmap Stage 3

- [ ] **D4.1** `desktop/`: Tauri v2 shell loading the built React app
- [ ] **D4.2** Python server bundled with PyInstaller (using the findings from S1.2), started by Tauri as a sidecar with a random port + token (3.8)
- [ ] **D4.3** Clean shutdown: the server stops when the app closes
- [ ] **B4.1** Model manager API: list, download with progress, delete, disk usage, **model storage location** (user picks a drive. Warn when the drive has less than ~10 GB free)
- [ ] **F4.1** Welcome / first-run screens: hardware check → recommended engine → model download with progress → optional voice recording
- [ ] **F4.2** Settings screen: engines and models, theme, privacy, shortcuts, about
- [ ] **D4.4** Mac signing + notarisation, `.dmg` build in CI
- [ ] **F4.3** Native polish: app icon, menus, `Cmd` shortcuts

**Done when:** a fresh Mac with nothing installed can download the `.dmg`, install it, and generate audio within 10 minutes.

### Sprint 5 — Windows app + private beta (Weeks 11–12) · Roadmap Stage 3

- [ ] **D5.1** Windows build: installer, code signing, `Ctrl` shortcuts
- [ ] **D5.2** Auto-update (Tauri updater) on both OSes
- [ ] **D5.3** Opt-in crash reports + anonymous usage stats. **Never** script text or audio
- [ ] **D5.4** Release workflow: tag → CI builds Mac + Windows → draft GitHub release
- [ ] **D5.5** Beta feedback channel (form or Discord) linked from the app
- [ ] Bug-fix buffer: keep ~30% of this sprint free for beta issues

**Done when:** 20–50 beta users installed. 70%+ generate their first audio within 10 minutes. Crash-free sessions above 98%. Tag `v0.2.0-beta`.

### Later sprints (outline, detailed planning when we get there)

| Sprints | Roadmap stage | Main work |
|---|---|---|
| 6–7 | Stage 4: Launch | Licence keys + Pro feature flags (`/api/features`), merchant-of-record checkout + webhooks, Pro add-ons as a separate private package, website + docs, launch. Tag `v1.0.0` |
| 8–9 | Stage 5: Expressive | `ollama_backend.py` (Orpheus → SNAC decoder → audio chunks), emotion-tag chips in the editor, one-click "pull model", Qwen script helper. Phonon on Apple Silicon if the licence allows |
| 10–12 | Stage 6: Cloud + API | Docker image for GPU servers, accounts + API keys + rate limits, measured GPU cost → credit pricing, "generate in cloud" button |

---

## 6. Testing strategy

| Level | What | Where it runs |
|---|---|---|
| Unit (Python) | `text.py`, `audio.py`, hashing, job states | CI, every push |
| API (Python) | Every endpoint, with the `fake` backend | CI, every push |
| Unit (frontend) | Hooks, utilities, components | CI, every push |
| End-to-end | Main flows in a real browser against the `fake` backend | CI, every push |
| Accessibility | axe on every screen | CI, every push |
| **Real models** | One English sentence per model: not silent, correct sample rate, reasonable length | **Manually before every release**, on a Mac and a Windows machine (models are too big for every CI run) |
| Benchmarks | `scripts/benchmark.py` | Before every release. Results logged in the roadmap |

---

## 7. Release checklist

1. All sprint tasks meet the Definition of Done
2. Real-model tests pass on Mac + Windows
3. Benchmarks recorded, no big slowdown
4. `THIRD_PARTY_LICENSES` up to date, every model licence re-checked
5. Changelog written
6. Version bumped, git tag created, CI builds signed installers
7. Install the built app on a clean machine of each OS and generate audio

---

## 8. Biggest technical risks and when we tackle them

| Risk | Tackled in | How |
|---|---|---|
| PyTorch makes the desktop app huge or slow to start | **Sprint 1 (S1.2)** | Packaging test early. Download models on first run. Consider ONNX builds for Windows if needed |
| Chatterbox too slow on CPU-only Windows | **Sprint 1 (S1.1)** | Measure. Recommend Kokoro on slow machines, cloud tier later |
| Streaming playback stutters | **Sprint 2 (S2.1)** | Buffer 1–2 chunks before starting playback |
| MLX and PyTorch versions sound different | Sprint 1 | Compare the same sentences on both. Document the differences |
| Local server attacked by malicious websites | Sprint 1 onward | Security rules in 3.8 from day one |

---

## 9. How we'll work together

1. At the start of each sprint, you tell me which task IDs you're taking (e.g. "B1.1–B1.4").
2. I give you the code for those tasks, with the files, the code and how to test it.
3. You put it in, run it on Mac and Windows, and tell me the result or the error.
4. We tick the tasks off here and move on.

---

## 10. Benchmark log

Speed = seconds of audio produced per second of compute. **Above 1.0x** means faster than real time, so streaming never stalls.

| Date | Machine | Engine | Model | Load time | Speed | Notes |
|---|---|---|---|---|---|---|
| 2026-11-13 | Windows 11 laptop, Intel CPU, Iris Xe, 32 GB RAM, no NVIDIA GPU | torch (CPU) | Kokoro, `am_puck` | 22.1 s | **2.81x** | 12.6 s of audio in 4.5 s, measured with `scripts/say.py` |
