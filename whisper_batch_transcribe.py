#!/usr/bin/env python3
"""
Batch Whisper transcription helper.

Walks the IDEA audio tree (audio/<state>/*.mp3), feeds each file through an
OpenAI Whisper model, and stores transcripts under:

    transcriptions/WhisperTranscription/<state>/<clip>.txt

Optionally writes the rich JSON output that Whisper returns for downstream
analysis.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional

LOG = logging.getLogger("whisper_batch")


def discover_audio_files(root: Path, exts: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for ext in exts:
        files.extend(root.rglob(f"*{ext}"))
    files.sort()
    return files


def ensure_package() -> None:
    try:
        import whisper  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Missing dependency 'whisper'. Install via 'pip install openai-whisper'."
        ) from exc


def load_model(name: str, device: Optional[str]) -> "whisper.Whisper":
    import torch
    import whisper

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    LOG.info("Loading Whisper model '%s' on %s", name, device)
    return whisper.load_model(name, device=device)


def transcribe_file(
    model: "whisper.Whisper",
    audio_path: Path,
    options: Dict[str, object],
) -> Dict[str, object]:
    LOG.info("Transcribing %s", audio_path)
    import whisper

    # Whisper expects native str paths, not Path objects
    result = model.transcribe(str(audio_path), **options)

    # Attach the computed prompt for downstream debugging
    if "segments" in result:
        for seg in result["segments"]:
            seg.pop("temperature", None)
    return result


def write_outputs(
    transcription: Dict[str, object],
    text_path: Path,
    json_path: Optional[Path],
) -> None:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text = transcription.get("text", "").strip()
    text_path.write_text(text + "\n", encoding="utf-8")
    LOG.debug("Wrote %s", text_path)

    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open("w", encoding="utf-8") as fh:
            json.dump(transcription, fh, ensure_ascii=False, indent=2)
        LOG.debug("Wrote %s", json_path)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Batch transcribe IDEA audio clips with Whisper."
    )
    parser.add_argument(
        "--audio-root",
        type=Path,
        default=Path("audio"),
        help="Root containing per-state audio folders.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("transcriptions/WhisperTranscription"),
        help="Directory to store per-state transcript folders.",
    )
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model size (tiny, base, small, medium, large, etc.).",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Torch device override (default auto-detect).",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Language hint (pass 'auto' to let Whisper detect).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature.",
    )
    parser.add_argument(
        "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Whisper task.",
    )
    parser.add_argument(
        "--exts",
        nargs="+",
        default=[".mp3", ".wav", ".m4a", ".aac", ".ogg"],
        help="Audio extensions to include.",
    )
    parser.add_argument(
        "--write-json",
        action="store_true",
        help="Also persist Whisper's JSON output alongside the text.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-run transcription even if text file already exists.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity.",
    )

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(levelname)s %(message)s",
    )

    ensure_package()

    if not args.audio_root.exists():
        LOG.error("Audio root %s does not exist", args.audio_root)
        return 1

    audio_files = discover_audio_files(args.audio_root, args.exts)
    if not audio_files:
        LOG.warning("No audio files found under %s", args.audio_root)
        return 0

    model = load_model(args.model, args.device)

    options: Dict[str, object] = {
        "language": None if args.language == "auto" else args.language,
        "temperature": args.temperature,
        "task": args.task,
    }

    processed = 0
    skipped = 0
    failed = 0

    for audio_path in audio_files:
        try:
            rel = audio_path.relative_to(args.audio_root)
        except ValueError:
            LOG.warning("Skipping %s (outside audio root?)", audio_path)
            continue

        state = rel.parent.name
        if not state:
            LOG.warning("Unable to infer state for %s", audio_path)
            continue

        output_dir = args.output_root / state
        text_path = output_dir / f"{audio_path.stem}.txt"
        json_path = output_dir / f"{audio_path.stem}.json" if args.write_json else None

        if text_path.exists() and not args.overwrite:
            skipped += 1
            LOG.debug("Skipping existing transcript %s", text_path)
            continue

        try:
            result = transcribe_file(model, audio_path, options)
        except Exception as exc:  # pragma: no cover
            failed += 1
            LOG.error("Failed to transcribe %s: %s", audio_path, exc)
            continue

        write_outputs(result, text_path, json_path)
        processed += 1

    LOG.info(
        "Transcription complete: %d processed, %d skipped, %d failed",
        processed,
        skipped,
        failed,
    )
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
