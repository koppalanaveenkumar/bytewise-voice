# ByteWise Voice

**An open-source, private, unlimited AI voice studio that runs on your own Mac or PC.**

Turn scripts into natural narration and clone your own voice. No per-character fees, and your scripts never leave your computer.

> ⚠️ **Early development.** Not ready for everyday use yet. See the [roadmap](ROADMAP.md).

## Planned features

- Long-form narration with streaming playback
- Fast preset voices (Kokoro)
- Voice cloning from a 10–20 second sample, with consent built in (Chatterbox)
- Paragraph-by-paragraph editing, projects, WAV/MP3 export
- Expressive voices with emotion tags via Ollama (later)
- Runs on macOS (Apple Silicon and Intel) and Windows

## Current status

| Platform | Status |
|---|---|
| macOS (Apple Silicon) | Works (MLX engine) |
| Windows / Intel Mac | Coming in Sprint 1 |

## Run it (macOS, Apple Silicon)

Requires Python 3.12.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. The first generation downloads the models (this takes a while).

## Documentation

- [ROADMAP.md](ROADMAP.md): product and startup plan
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md): architecture and sprint plan
- [CONTRIBUTING.md](CONTRIBUTING.md): how to contribute

## Responsible use

Only clone a voice if you have that person's permission. Don't use ByteWise Voice to impersonate, deceive or harass anyone.

## License

ByteWise Voice is licensed under the [GNU Affero General Public License v3.0](LICENSE).
The AI models it uses have their own licenses: see [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES).
