# ByteWise Voice — Startup Plan & Roadmap

*Draft v3 · 13 Nov 2026 · Living document: update it at the end of every stage.*

**Decided:** open source (open-core) · creators first · English first · beautiful custom-designed app (no plain static page) · pricing to be tested with users in Stage 0

---

## 1. One-line pitch

**ByteWise Voice is an open-source, private, unlimited AI voice studio that runs on your own Mac or PC.**
Studio-quality narration and voice cloning, with no per-character fees and no script ever leaving your computer. Because the code is open, anyone can check that promise.

## 2. The problem

People who make a lot of voice content with cloud tools like ElevenLabs hit three walls:

1. **Usage limits and rising bills.** Pricing is per character, so long-form work (courses, audiobooks, daily videos) gets expensive fast.
2. **Privacy.** Every script and every voice sample is uploaded to someone else's server. Companies with confidential training material, agencies under NDA, and people cloning their own voice often aren't comfortable with that.
3. **Lock-in.** Your voices and projects live inside someone else's platform.

## 3. Who we serve first (beachhead)

A startup wins by owning one small group first, then expanding.

**Primary: solo creators who produce long-form narration every week**
- YouTube narrators, "faceless" channels, course creators, audiobook and podcast makers
- They generate hours of audio per month, so per-character pricing hurts them most
- Many already own an Apple Silicon Mac, which runs our models fast

**Secondary (later): small companies with private content**
- Internal training videos, product demos, e-learning teams
- They pay more and care most about "nothing leaves our machines"

**Not our customer yet:** call centres, real-time voice agents, big enterprises. These need low-latency cloud infrastructure and sales teams we don't have.

## 4. Why we can win

| | Cloud voice platforms | **ByteWise Voice** |
|---|---|---|
| Where it runs | Their servers | **Your Mac / PC** (cloud optional, later) |
| Cost model | Pay per character | **Flat price, unlimited local generation** |
| Privacy | Scripts and voices uploaded | **Stays on device** |
| Source code | Closed | **Open source**, so the privacy claim can be verified |
| Our cost per extra hour of audio | — | **~Zero** (the user's hardware does the work) |
| Voice quality | Best in class | Good and improving fast (open models) |

**Our honest weakness:** top cloud platforms still sound better and support more languages. We don't win on raw quality. We win on **price, privacy, and unlimited use**, and we keep closing the quality gap as open models improve.

**Our unfair advantage over time:** a polished studio (editing, projects, long-form workflow) on top of open models. Most open-source TTS tools are developer demos, not products creators can use. Being open source ourselves brings trust, free distribution through GitHub, and community contributions (new voices, bug fixes, translations).

## 5. Product

### Product tiers (built in this order)

1. **ByteWise Studio (desktop app).** Mac first, then Windows. Runs fully offline after models are downloaded.
2. **ByteWise Cloud (later).** The same engine on rented GPUs, for users whose computers are too slow (e.g. Windows laptops without an NVIDIA GPU).
3. **ByteWise API (later).** For developers and businesses that want to build on our engine.

### Core features for v1

- Paste a long script and get clean narration, with streaming playback
- Preset voices (fast, any machine)
- Clone your own voice from a 10–20 s sample, with consent built in
- Edit and regenerate a single paragraph without redoing everything
- Projects, history, export WAV / MP3

### Signature feature for v1.5: Expressive voices

- Emotion tags in the script: `<laugh>`, `<sigh>`, `<gasp>`, …
- Powered by **Ollama**, running locally

### Experience & design

Design is a core feature, not decoration. Creators choose tools that feel good to use every day. Most open-source TTS tools look like developer demos, so **a beautiful app is one of our biggest differentiators.**

**Design principles**
1. **Calm, focused, pro-tool feel:** like a modern audio or video editor, never cluttered.
2. **Dark mode by default**, with a light mode of equal quality.
3. **Instant feedback:** every action shows progress. Audio streams in and the waveform grows live as it's generated.
4. **Keyboard-first:** `Space` play/pause, `Ctrl/Cmd + Enter` generate, `Ctrl/Cmd + K` command menu.
5. **Accessible:** WCAG AA contrast, full keyboard use, screen-reader labels.
6. **Feels native on Mac and Windows:** correct shortcuts (`Cmd` vs `Ctrl`) and window controls.
7. **Design system first:** colours, type, spacing and components are defined once. Screens only combine them.

**Key screens**

| Screen | What it does |
|---|---|
| **Welcome / first run** | Detects the computer's hardware, recommends the best engine, downloads models with a progress bar, offers to record your voice |
| **Projects** | Grid of recent projects with waveform thumbnails, search, new project |
| **Studio editor** (main screen) | Script as paragraph blocks. Each block has its own voice, status and a regenerate button. Waveform timeline + player at the bottom, voice settings panel on the side. Emotion tags and pauses appear as inline chips |
| **Voice library** | Voice cards with preview, filters (preset / cloned / expressive) |
| **Clone a voice** wizard | Record or upload → auto-clean → consent → test sentence → save |
| **History & exports** | Every generated file: play, download, delete |
| **Settings** | Engines and models (download, remove, disk usage), Ollama status, theme, shortcuts, privacy |

## 6. Business model: open-core

Open source and making money work together through **open-core**: the core is free and open, and people pay for convenience, extra features and cloud power.

### What is open vs paid

| Part | Open source (free forever) | Paid |
|---|---|---|
| Engine (backends, text cleanup, long-form, streaming) | ✅ | |
| Studio basics: preset voices, voice cloning with consent, projects, WAV/MP3 export | ✅ | |
| Run it from source (developers) | ✅ | |
| **Signed one-click installer + auto-update** for Mac & Windows | | ✅ Pro |
| **Pro add-ons:** expressive voices editor, AI script helper, per-paragraph timeline editor, batch export, premium voice packs | | ✅ Pro |
| **Cloud credits:** generate on our GPUs when your machine is slow | | ✅ Pay as you go |
| **Team / self-host:** shared voice library, admin, priority support | | ✅ Annual licence |

**Why this works for creators:** developers can build from source for free and spread the word. Creators don't want to install Python. They pay for an app that just works, plus the Pro features.

### Licence

**Recommended: AGPL-3.0 for the open-source core, plus a Contributor License Agreement (CLA).**
- AGPL lets anyone use and change the code, but a company that runs a modified version as an online service must publish its changes. This stops a big company from quietly turning our work into a closed cloud product.
- The CLA lets ByteWise keep shipping closed Pro add-ons and sell commercial licences (dual licensing), even after outside contributions.
- Alternative: **Apache-2.0** brings more adoption and contributors but no protection. Decide before the repo goes public (Stage 0).
- All bundled models must have a licence compatible with this. Kokoro (Apache 2.0) and Chatterbox (MIT) are fine.

### Pricing (to be tested)

*All prices are hypotheses. **You will test them in Stage 0** (see the pricing test there).*

| Plan | Who | Price hypothesis |
|---|---|---|
| **Open source** | Developers, tinkerers | $0, build it yourself |
| **Pro** | Creators | Flat monthly (e.g. $9–15) **or** one-time licence (e.g. $79–129) |
| **Cloud credits** | Users with slow machines | Per hour of audio, priced above our GPU cost |
| **Team / Self-host** | Small companies | Annual licence |

**Unit economics:**
- Local generation costs us almost nothing per user. Models download straight from Hugging Face, and the user's machine does the work. **This is the core of the business.**
- Cloud credits must be priced from measured GPU cost per hour of audio (measure in Stage 4). Never offer "unlimited" on cloud.
- Use a **merchant of record** (Paddle or Lemon Squeezy) for payments. They handle global sales tax and VAT, which is critical for a small team.

## 7. Technology

### Principles

1. **Free, open models only.** No paid AI APIs.
2. **Commercial-safe licences only.** Every model's licence is checked before it ships.
3. **Mac and Windows from day one**, with one codebase.
4. **Local-first.** The cloud tier runs the same engine, not a separate one.
5. **English first.** Launch with English only (American + British Kokoro voices, English cloning). Get one language excellent before adding more in Stage 7. Keep `lang` as a parameter everywhere so adding languages later needs no redesign.

### What we build vs. what we use

**We do not train AI models.** We use free, pre-trained models and build the product around them.

| We **use** (download, don't build) | We **build** (our code) |
|---|---|
| Speech models: Kokoro, Chatterbox, Orpheus | The engine: text cleanup, chunking, pauses, streaming |
| Ollama (runs Orpheus and the Qwen script helper) | The FastAPI server: jobs, projects, voices, exports |
| Open-source libraries | The React studio app, design system, desktop packaging |

| Level of AI work | Plan |
|---|---|
| Use pre-trained models | ✅ Now, through launch |
| Fine-tune an existing model on licensed recordings | ⏳ Maybe in Stage 7, for premium voices |
| Train our own model from scratch | ❌ Not planned. It needs huge licensed datasets, many GPUs and a research team |

Voice cloning needs no training either: Chatterbox copies a voice from a short sample instantly.

The step-by-step build plan is in [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md).

### Models

| Role | Model | Licence | Runs on |
|---|---|---|---|
| Fast preset voices | **Kokoro-82M** | Apache 2.0 | Every machine, fast even on CPU |
| Voice cloning | **Chatterbox** (Resemble AI) | MIT | Every machine. Fast on Apple Silicon / NVIDIA, slow on plain CPU |
| Expressive voices | **Orpheus 3B via Ollama** + SNAC decoder | Llama 3.2-based: **verify licence before launch** | Mac and Windows. Needs a decent GPU or Apple Silicon for real-time |
| Expressive (Mac) | **Ollama Phonon** (English model) | Some variants are **non-commercial**. Reports say the small English model is Apache 2.0: verify on the model card | Apple Silicon only today. Windows/Linux promised by Ollama |
| Script helper (optional) | **Qwen2.5 3B/7B via Ollama** | Apache 2.0 (check per size) | Mac and Windows |

**Rejected for commercial use:** XTTS-v2 (non-commercial licence) and F5-TTS weights (CC-BY-NC).

### One engine, several backends

The app picks the backend at startup (overridable with `BYTEWISE_BACKEND`):

| Machine | Kokoro + Chatterbox run on | Ollama engines |
|---|---|---|
| Apple Silicon Mac | `mlx-audio` (fastest) | Orpheus, Phonon |
| Windows / Linux / Intel Mac | PyTorch (`kokoro`, `chatterbox-tts`) | Orpheus |
| Any machine with NVIDIA GPU | PyTorch on CUDA | Orpheus (fast) |

Ollama runs as its own local server (`localhost:11434`). If it isn't running, the expressive features are hidden and everything else still works.

### Frontend stack

| Layer | Choice | Why |
|---|---|---|
| Framework | **React + TypeScript + Vite** | Largest ecosystem, easiest for open-source contributors, runs in the browser and inside Tauri |
| Styling | **Tailwind CSS** + design tokens (CSS variables) | Consistent design, easy dark/light themes |
| Components | **shadcn/ui** (built on Radix UI) | Beautiful and accessible. We own the component code, so it's easy to customise |
| Animation | **Motion** (formerly Framer Motion) | Smooth transitions and micro-interactions |
| Waveform & timeline | **wavesurfer.js** | Waveforms, regions per paragraph, live growth while streaming |
| Script editor | **TipTap** (open-source core) | Paragraph blocks, emotion tags and pauses as inline chips |
| Data from the API | **TanStack Query** | Job progress, caching, retries |
| UI state | **Zustand** | Simple global state |
| Routing | **React Router** | Screens and navigation |
| Icons | **Lucide** | Clean, consistent icon set |
| Tests | **Vitest** (unit) + **Playwright** (end-to-end) | Main flows tested on Mac and Windows in CI |

All of these are free, open-source libraries (MIT/BSD/ISC), compatible with our licence. Only use TipTap's free open-source extensions, not its paid ones.

**How the pieces connect:**
- **Development:** Vite dev server (hot reload) forwards `/api` calls to FastAPI. One command starts both.
- **Desktop app:** Tauri shows the built React app and talks to the local Python server.
- **Cloud tier (later):** the same React app runs in the browser against the cloud server.
- FastAPI serves **only the API**. It no longer serves any HTML pages.

### Architecture

```
┌──────────── Desktop app (Tauri shell) ────────────┐
│  React + Tailwind UI (frontend/)                  │
│        │ HTTP on localhost                        │
│  FastAPI server (app/main.py)   jobs, API, auth   │
│        │                                          │
│  Engine (app/engine.py)  split → generate → join  │
│        │                                          │
│  Backends (app/backends/)                         │
│   ├── mlx_backend.py     Apple Silicon            │
│   ├── torch_backend.py   Windows / Linux / Intel  │
│   └── ollama_backend.py  Orpheus / Phonon via HTTP│
└───────────────────────────────────────────────────┘
          Same FastAPI + engine runs in the cloud tier on GPU servers
```

Every backend has the same interface, so the engine and UI never change when we add a model:

```
list_voices()                                       -> list of voices
generate(model, text, voice, speed, energy)         -> audio chunks (numpy, 24 kHz)
```

### Folder layout

```
bytewise-voice/
├── app/
│   ├── main.py               API routes
│   ├── engine.py             text splitting, pauses, joining, saving
│   ├── text.py               text cleanup (numbers, dates, pronunciations)
│   ├── voices.py             voice library
│   ├── jobs.py               background jobs + progress
│   └── backends/
│       ├── __init__.py       pick_backend()
│       ├── base.py           shared interface
│       ├── mlx_backend.py
│       ├── torch_backend.py
│       └── ollama_backend.py
├── frontend/                 React app (the studio UI)
│   ├── src/
│   │   ├── components/ui/    design system (buttons, inputs, cards …)
│   │   ├── features/         studio, voices, projects, settings, onboarding
│   │   ├── lib/              API client, audio player, shortcuts
│   │   └── styles/           design tokens (colours, type, spacing)
│   └── package.json
├── desktop/                  Tauri shell (Stage 3)
├── voices/                   voice samples + voices.json
├── tests/                    smoke tests
├── output/                   generated audio (git-ignored)
├── requirements.txt          per-platform markers
├── README.md
└── ROADMAP.md
```

---

## 8. Roadmap by stage

*Timelines assume one full-time developer. Double them if part-time.*
**Rule:** a stage ends only when its exit criteria pass on **both Mac and Windows**.

### Stage 0 — Validate (Weeks 1–2)

**Goal:** prove people want this before building much.

Build:
- [ ] Clean up the repo: delete the old Gradio `app.py`, `git init`, `.gitignore`, `README.md`
- [ ] Record a real voice sample (`voices/myvoice.wav` is currently empty)
- [ ] Make 3 demo audio clips on the Mac (preset voice, cloned voice, long-form)

Design:
- [ ] Mood board: collect 10–15 apps whose look and feel you love (audio editors, writing apps, creator tools)
- [ ] Brand basics: logo, colour palette, fonts (free-licence fonts only), tone of voice
- [ ] **Figma mockups (free plan)** in dark and light: Welcome, Studio editor, Voice library, Clone wizard
- [ ] Turn the mockups into a clickable prototype and **show it in the creator interviews**. Their reaction to the design is validation too
- [ ] Landing page uses the same brand and screenshots of the mockups

Open source setup:
- [ ] Choose the licence (AGPL-3.0 recommended, see section 6) and add `LICENSE`
- [ ] Add `CONTRIBUTING.md`, a CLA (e.g. via a CLA bot on GitHub), `CODE_OF_CONDUCT.md`, issue templates
- [ ] `THIRD_PARTY_LICENSES` listing every model and library
- [ ] Make the GitHub repo public **only after** the clean-up. Check that no secrets or private audio are in git history

Business:
- [ ] Landing page: pitch, demo clips, waitlist email form, link to GitHub
- [ ] Talk to **15–20 English-speaking creators**. Ask what they use now, what they pay, what annoys them, and whether they'd pay for a private, unlimited local tool
- [ ] **Pricing test:**
  - In interviews, show monthly vs one-time and ask which they'd pick and at what price ("too cheap / fair / too expensive")
  - On the landing page, split visitors between two price options and count waitlist signups for each
  - Record results in this file under "Pricing results"
- [ ] Post demos in 3–5 English creator communities and measure the reaction

**Exit criteria:** 100+ waitlist signups **or** 10+ people who say "I'd pay for this now", **and** a clear winner between monthly and one-time pricing. If not, revisit the beachhead in section 3.

**Pricing results:** *(fill in after the test)*

### Stage 1 — Cross-platform engine (Weeks 3–4)

**Goal:** the core engine runs the same on Mac and Windows.

- [ ] Split `requirements.txt` by platform (`mlx-audio` on Apple Silicon, PyTorch packages elsewhere)
- [ ] `app/backends/` with `base.py`, `mlx_backend.py`, `torch_backend.py`, `pick_backend()`
- [ ] `engine.py` calls only the backend interface
- [ ] `GET /api/health` reports backend, device, and loaded models
- [ ] Benchmark script: time a fixed 3-paragraph script per model per machine, results logged in this file
- [ ] GitHub Actions CI on **macOS and Windows** runners (lint + import + short smoke test)

Frontend foundation:
- [ ] Delete the old `static/` page and the static-file mounts in `main.py`. FastAPI becomes API-only. Until the new UI can generate audio, test the API with FastAPI's built-in `/docs` page
- [ ] Set up `frontend/` with Vite + React + TypeScript + Tailwind + shadcn/ui
- [ ] Design tokens from the Figma mockups (colours, type scale, spacing, radius) for dark and light themes
- [ ] Base components: button, input, slider, select, card, dialog, toast, progress
- [ ] App shell: sidebar navigation, top bar, theme switch, `Cmd/Ctrl + K` command menu, empty screens
- [ ] Engine status badge in the app, from `GET /api/health`
- [ ] One command starts FastAPI + Vite together

**Exit criteria:** same script → audio with both voices on both OSes, no code changes. Benchmarks recorded. The new app shell runs on both OSes and shows the live engine status.

### Stage 2 — MVP studio (Weeks 5–8)

**Goal:** something a creator can actually use for real work, built as the designed screens from Stage 0.

Screens:
- [ ] **Studio editor:** paragraph blocks (TipTap), voice per block, regenerate button, status per block, waveform timeline + player (wavesurfer.js), settings side panel
- [ ] **Voice library** and **Clone a voice** wizard (record in the browser, auto-clean, consent, test sentence)
- [ ] **Projects** home and **History & exports**
- [ ] Loading, empty and error states designed for every screen, not just the "happy path"
- [ ] Keyboard shortcuts and a shortcuts help sheet

Engine features behind the screens:
- [ ] Long-form: paragraph → sentence chunks (under ~250 characters), different pause lengths
- [ ] Text cleanup (`text.py`): numbers, dates, currency, abbreviations, URLs, pronunciation dictionary, `[pause 1s]` markup
- [ ] Background jobs with progress and cancel (`jobs.py`)
- [ ] **Streaming playback:** first audio in under 2 s with Kokoro
- [ ] Voice library: upload or record in the browser, auto-clean the sample, **mandatory consent checkbox**, preview, rename, delete
- [ ] Per-paragraph regenerate
- [ ] Projects + history (SQLite)
- [ ] Export WAV + MP3, loudness normalisation, silence trimming

**Exit criteria:** you produce a real 10-minute narration with your cloned voice, with no manual fixes outside the app. **Usability test:** 5 creators complete "clone your voice and narrate a script" without help, and rate the design 8/10 or higher.

### Stage 3 — Private beta (Weeks 9–12)

**Goal:** real users on their own machines.

- [ ] Package the React app as a desktop app with **Tauri**, with the Python server bundled alongside it. **Mac first**
- [ ] **Welcome / first-run screens:** detect hardware, download models with a progress bar, recommend the best engine for the machine
- [ ] **Settings screen:** engines and models, disk usage, privacy, theme
- [ ] Native polish: app icon, menus, window controls, `Cmd` vs `Ctrl` shortcuts
- [ ] Mac code signing + notarisation (Apple Developer account)
- [ ] Windows installer + code signing certificate
- [ ] Auto-update
- [ ] Opt-in crash reports and anonymous usage stats (respect the privacy promise: no script text ever)
- [ ] Invite 20–50 waitlist users. Weekly feedback calls with 5 of them

**Exit criteria:** 70%+ of beta users generate their first audio within 10 minutes of installing. Crash-free sessions above 98%.

### Stage 4 — Public launch v1.0 (Months 4–5)

**Goal:** first paying customers.

- [ ] Payments + licence keys through a merchant of record
- [ ] Free vs Pro feature gating
- [ ] Website: pricing, docs, FAQ, comparison page, privacy policy, terms, acceptable-use policy
- [ ] Launch: Product Hunt, "Show HN" on Hacker News, GitHub release, creator communities, YouTube demo, "build in public" posts
- [ ] Community: Discord or GitHub Discussions, "good first issue" labels for contributors
- [ ] Support inbox + public changelog

**Exit criteria:** first 50 paying customers. Free → Pro conversion measured.

### Stage 5 — Expressive voices with Ollama (Months 5–7)

**Goal:** our signature feature, and closer to the expressive style of the top cloud tools.

- [ ] `ollama_backend.py`: send text to Orpheus in Ollama, decode the audio tokens with SNAC, stream the chunks
- [ ] On Apple Silicon: add Ollama Phonon models whose licence allows commercial use
- [ ] Emotion tags in the editor (`<laugh>`, `<sigh>`, `<gasp>` …) with autocomplete and a preview
- [ ] Auto-detect Ollama, with one-click "pull model" from inside the app
- [ ] Script helper (Qwen2.5 via Ollama): "clean up for speech", "suggest pronunciations", "suggest emotion tags"
- [ ] **Legal check:** confirm the Orpheus and Phonon licences allow commercial distribution

**Exit criteria:** expressive mode runs at real-time speed or better on an M-series Mac, and is usable (if slower) on Windows with an NVIDIA GPU.

### Stage 6 — Cloud tier + API (Months 7–10)

**Goal:** serve users with weak hardware, and developers.

- [ ] Docker image of the same server for Linux GPU machines
- [ ] Measure GPU cost per hour of generated audio, then set cloud credit prices
- [ ] Accounts, API keys, rate limits, job queue
- [ ] "Generate in cloud" button in the desktop app for slow machines
- [ ] Public API docs (FastAPI `/docs`)

**Exit criteria:** cloud credits have a positive margin, and at least one external app uses the API.

### Stage 7 — Grow (Months 10+)

Pick based on data from earlier stages:
- More languages (Chatterbox Multilingual, Kokoro languages)
- Multi-voice dialogue and podcast mode
- Team plan and self-hosted licence
- Fine-tune our own premium voices on licensed voice-actor recordings (pay actors, written contracts)
- Speech-to-speech (change the voice of a recording)
- Audio watermark detection tool

---

## 9. Metrics we track

| Stage | North-star metric | Supporting metrics |
|---|---|---|
| 0 Validate | Waitlist signups | Interview "would pay" count, demo engagement, pricing test result |
| 1–2 Build | Time to first audio | Generation speed per machine, failed jobs |
| 3 Beta | Activation (first audio < 10 min) | Crash-free %, weekly active users |
| 4 Launch | Paying customers | Free → Pro conversion, refunds, churn |
| 5–6 Grow | **Hours of audio generated per week** | Retention at 30 days, cloud margin |
| All stages | — | GitHub stars, outside contributors, merged community pull requests |

## 10. Trust, safety & legal

This is a voice-cloning product. Trust is a feature, and a legal requirement.

- **Consent:** cloning needs a consent checkbox plus a stored consent record (who, when, which sample). Later, require the speaker to read a short consent sentence in the sample.
- **Watermarking:** keep the inaudible watermark Chatterbox adds. Add our own to all engines later. This also helps meet rules that require AI-generated audio to be identifiable, such as the EU AI Act's transparency rules.
- **Acceptable-use policy:** no impersonation without permission, no fraud, no harassment, no political deception. Licence can be revoked.
- **Model licences:** keep a `THIRD_PARTY_LICENSES` file. Re-check every model before each release.
- **Privacy promise:** local mode never sends script text or audio anywhere. Telemetry is opt-in and contains no content.
- **Company basics:** register the company, get a lawyer to review terms and privacy policy before Stage 4, and check trademark availability for the name "ByteWise".

## 11. Risks & mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Open-model quality not good enough for paying creators | High | Validate with demos in Stage 0. Keep the backend layer pluggable so better models drop in |
| Slow on Windows laptops without an NVIDIA GPU | High | Kokoro works everywhere. Recommend the engine per machine. Cloud tier in Stage 6 |
| Desktop packaging is hard (PyTorch is huge) | Medium | Mac first. Download models on first run, not inside the installer. Consider ONNX builds for Windows |
| Model licence changes or turns out non-commercial | High | Licence checklist per release. At least two engines for every feature |
| Misuse of voice cloning | High | Consent, watermark, acceptable-use policy, ability to revoke licences |
| Big competitors drop prices | Medium | Our cost per user is near zero locally, and privacy is a lasting difference |
| Ollama speech support changes | Low | Ollama is optional. Core product doesn't depend on it |
| Someone forks the open code and competes | Medium | AGPL means they must share their changes. Our edge is the polished app, Pro features, brand and community, not secret code |
| Open source means few people pay | Medium | Keep the free version great for developers. Make the paid app clearly easier for creators. Measure conversion in Stage 4 |

## 12. Lean budget (first 6 months)

| Item | Notes |
|---|---|
| Apple Developer Program | $99 / year, needed for Mac signing |
| Windows code signing certificate | Yearly cost, varies by provider |
| Domain + landing page hosting | Low |
| Payments (merchant of record) | Percentage per sale, no fixed fee |
| Test machine: Windows PC with an NVIDIA GPU | Optional but very useful |
| Cloud GPUs | Only from Stage 6, pay per hour |
| Lawyer review of terms / privacy | One-time, before launch |

## 13. How we work (engineering practices)

- **Git from day one.** `main` is always releasable. One branch per feature.
- **CI on macOS + Windows** for every push.
- **Smoke tests:** generate one short sentence per engine and check the audio isn't silent and has the right sample rate.
- **Decision log:** record important choices (model, licence, architecture) with the reason, in `docs/decisions/`.
- **Release cadence:** one release every 2 weeks from beta onward, with a public changelog.
- **Downloads are deliberate:** packages and model weights are installed only when we choose to, never automatically by scripts.
- **Public repo hygiene:** no secrets, API keys or personal voice samples in git. Use `.env` files that are git-ignored. Pro add-ons live in a separate private repo.
- **Review all outside pull requests** before merging, and sign the CLA first.
- **Frontend rules:**
  - New UI pieces go into the design system (`components/ui/`) first. Screens only combine existing components.
  - No hard-coded colours or sizes. Always use the design tokens, so dark/light and future rebrands stay easy.
  - Playwright tests for the main flows (generate, clone a voice, export) run in CI on Mac and Windows.
  - Automatic accessibility check (axe) in CI. Every screen must pass before merging.
  - Check every screen in dark and light, and at small and large window sizes.

## 14. Decisions

| # | Decision | Status |
|---|---|---|
| 1 | Pricing: monthly vs one-time vs both | **Testing** in Stage 0 (pricing test) |
| 2 | Open source? | **Decided: yes, open-core** (section 6) |
| 3 | Beachhead | **Decided: creators first** |
| 4 | Launch language | **Decided: English first** |
| 5 | Licence: AGPL-3.0 + CLA (recommended) vs Apache-2.0 | **Open:** decide before the repo goes public |
| 6 | UI | **Decided: custom-designed React app** (no plain static page). Stack in section 7 |
| 7 | Name: keep "ByteWise Voice"? | **Open:** after a trademark check |

## 15. Next 2 weeks (concrete)

1. Repo clean-up: `git init`, `.gitignore`, delete the old `app.py`, write the `README.md`
2. Pick the licence (decision 5), add `LICENSE`, `CONTRIBUTING.md`, `THIRD_PARTY_LICENSES`
3. Record a clean `voices/myvoice.wav` (English, 10–20 s)
4. Generate 3 English demo clips on the Mac with the existing MLX code
5. Mood board + brand basics, then Figma mockups of the Studio editor and Voice library
6. Put up the landing page + waitlist with the two-price test, using the new brand
7. Book 15 English-speaking creator interviews. Show the clickable prototype and ask the pricing questions
8. Then start Stage 1 code: I'll give you the backend and frontend-foundation code to add yourself
