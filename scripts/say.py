"""Turn text into a WAV file with the current engine.

Examples:
    python scripts/say.py "Hello from ByteWise Voice."
    python scripts/say.py "Good morning." --voice bf_emma
    python scripts/say.py "This is my voice." --model chatterbox --voice voices/myvoice.wav
"""

import argparse
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from app.engine.backends import SAMPLE_RATE, SpeechRequest, get_backend


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate speech to a WAV file.")
    parser.add_argument("text")
    parser.add_argument("--model", default="kokoro", choices=["kokoro", "chatterbox"])
    parser.add_argument("--voice", default="am_puck",
                        help="Kokoro voice id, or a sample file path for chatterbox")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--energy", type=float, default=0.5)
    parser.add_argument("--out", type=Path, default=Path("output/say.wav"))
    args = parser.parse_args()

    backend = get_backend()
    print(f"Engine: {backend.name} on {backend.device()}")

    # Load the model first, so the speed number measures generation only
    start = time.perf_counter()
    list(backend.generate(SpeechRequest(model=args.model, text="Ready.", voice=args.voice)))
    print(f"Model loaded in {time.perf_counter() - start:.1f} s")
    
    req = SpeechRequest(model=args.model, text=args.text, voice=args.voice,
                        speed=args.speed, energy=args.energy)
    start = time.perf_counter()
    chunks = list(backend.generate(req))
    elapsed = time.perf_counter() - start
    if not chunks:
        raise SystemExit("No audio was generated.")

    audio = np.concatenate(chunks)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(args.out, audio, SAMPLE_RATE)

    seconds = len(audio) / SAMPLE_RATE
    print(f"Saved {args.out}: {seconds:.1f} s of audio in {elapsed:.1f} s "
          f"({seconds / elapsed:.2f}x real time)")


if __name__ == "__main__":
    main()
