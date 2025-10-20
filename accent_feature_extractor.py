#!/usr/bin/env python3
"""
Batch audio feature extraction for IDEA U.S. accent samples.

Loads every audio file under --audio-root, resamples to mono 16 kHz (configurable),
removes leading/trailing silence, and writes compressed NumPy archives with rich
descriptors suitable for downstream ML experiments.

Outputs per clip:
  features/<state>/<sample>.npz   # waveform + feature matrices
  features_manifest.jsonl         # summary metadata for quick inspection
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np

try:
    import librosa
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "librosa is required. Install with: pip install librosa soundfile"
    ) from exc


LOG = logging.getLogger("accent_feature_extractor")


@dataclass
class FeatureSummary:
    audio_path: str
    state: str
    sample_id: str
    features_path: str
    sample_rate: int
    num_samples: int
    duration_sec: float
    original_sample_rate: int
    original_duration_sec: float
    trimmed: bool
    rms_db: float
    spectral_centroid_mean: float
    spectral_bandwidth_mean: float
    pitch_voiced_ratio: float
    tempo_bpm: Optional[float]
    feature_shapes: Dict[str, Tuple[int, ...]]


def _safe_float(value: float) -> float:
    if np.isnan(value) or np.isinf(value):
        return float("nan")
    return float(value)


def extract_features(
    audio_path: Path,
    sample_rate: int,
    trim_top_db: float,
    n_fft: int,
    hop_length: int,
    n_mels: int,
    n_mfcc: int,
) -> Tuple[Dict[str, np.ndarray], FeatureSummary]:
    start = time.perf_counter()
    y, orig_sr = librosa.load(audio_path, sr=None, mono=True)
    original_duration = len(y) / orig_sr if len(y) else 0.0

    if orig_sr != sample_rate:
        y = librosa.resample(y, orig_sr=orig_sr, target_sr=sample_rate)
    sr = sample_rate

    y = librosa.util.normalize(y)
    y_trimmed, idx = librosa.effects.trim(y, top_db=trim_top_db)
    trimmed = bool(idx[0] != 0 or idx[1] != len(y))
    if y_trimmed.size:
        y = y_trimmed

    if not y.size:
        raise ValueError("Empty audio after trimming")

    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    magnitude = np.abs(stft)

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0,
    )
    log_mel = librosa.power_to_db(mel, ref=np.max)
    mfcc = librosa.feature.mfcc(
        S=librosa.power_to_db(mel, ref=np.max), sr=sr, n_mfcc=n_mfcc
    )
    spectral_contrast = librosa.feature.spectral_contrast(
        S=magnitude, sr=sr, n_fft=n_fft, hop_length=hop_length
    )
    chroma = librosa.feature.chroma_stft(
        S=magnitude, sr=sr, n_fft=n_fft, hop_length=hop_length
    )
    spectral_centroid = librosa.feature.spectral_centroid(
        S=magnitude, sr=sr, n_fft=n_fft, hop_length=hop_length
    )
    spectral_bandwidth = librosa.feature.spectral_bandwidth(
        S=magnitude, sr=sr, n_fft=n_fft, hop_length=hop_length
    )
    rms = librosa.feature.rms(y=y, hop_length=hop_length)
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop_length)

    try:
        pitch = librosa.yin(
            y,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7"),
            sr=sr,
            hop_length=hop_length,
        )
        pitch[np.isnan(pitch)] = 0.0
        voiced_ratio = float(np.count_nonzero(pitch) / pitch.size)
    except Exception:
        pitch = np.zeros((1,), dtype=np.float32)
        voiced_ratio = 0.0

    try:
        tempo, _ = librosa.beat.beat_track(
            y=y, sr=sr, hop_length=hop_length, tightness=100
        )
        tempo_bpm = float(tempo)
    except Exception:
        tempo_bpm = None

    features = {
        "waveform": y.astype(np.float32),
        "mfcc": mfcc.astype(np.float32),
        "log_mel": log_mel.astype(np.float32),
        "spectral_contrast": spectral_contrast.astype(np.float32),
        "chroma": chroma.astype(np.float32),
        "spectral_centroid": spectral_centroid.astype(np.float32),
        "spectral_bandwidth": spectral_bandwidth.astype(np.float32),
        "rms": rms.astype(np.float32),
        "zcr": zcr.astype(np.float32),
        "pitch": pitch.astype(np.float32),
    }

    summary = FeatureSummary(
        audio_path=str(audio_path),
        state=audio_path.parent.name,
        sample_id=audio_path.stem,
        features_path="",
        sample_rate=sr,
        num_samples=int(y.size),
        duration_sec=float(y.size / sr),
        original_sample_rate=int(orig_sr),
        original_duration_sec=float(original_duration),
        trimmed=trimmed,
        rms_db=_safe_float(float(librosa.amplitude_to_db(rms).mean())),
        spectral_centroid_mean=_safe_float(float(spectral_centroid.mean())),
        spectral_bandwidth_mean=_safe_float(float(spectral_bandwidth.mean())),
        pitch_voiced_ratio=_safe_float(voiced_ratio),
        tempo_bpm=_safe_float(tempo_bpm) if tempo_bpm is not None else None,
        feature_shapes={k: tuple(v.shape) for k, v in features.items()},
    )

    elapsed = time.perf_counter() - start
    LOG.debug("Extracted %s in %.2fs", audio_path, elapsed)
    return features, summary


def iter_audio_files(root: Path, exts: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for ext in exts:
        files.extend(root.rglob(f"*{ext}"))
    return sorted(files)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert IDEA accent MP3s into ML-friendly feature archives."
    )
    parser.add_argument(
        "--audio-root",
        type=Path,
        default=Path("audio"),
        help="Directory containing per-state audio folders.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("features"),
        help="Directory to write feature archives.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("features_manifest.jsonl"),
        help="Path to write JSONL manifest of extracted clips.",
    )
    parser.add_argument("--sample-rate", type=int, default=16_000)
    parser.add_argument("--trim-top-db", type=float, default=25.0)
    parser.add_argument("--n-fft", type=int, default=2048)
    parser.add_argument("--hop-length", type=int, default=512)
    parser.add_argument("--n-mels", type=int, default=64)
    parser.add_argument("--n-mfcc", type=int, default=13)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Recompute features even if the output file already exists.",
    )
    parser.add_argument(
        "--exts",
        nargs="+",
        default=[".mp3", ".wav", ".m4a", ".aac", ".ogg"],
        help="Audio file extensions to include.",
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

    if not args.audio_root.exists():
        LOG.error("Audio root %s does not exist", args.audio_root)
        return 1

    audio_files = iter_audio_files(args.audio_root, args.exts)
    if not audio_files:
        LOG.warning("No audio files found under %s", args.audio_root)
        return 0

    LOG.info("Found %d audio files", len(audio_files))
    manifest: List[FeatureSummary] = []
    skipped = 0
    failures = 0

    for audio_path in audio_files:
        rel = audio_path.relative_to(args.audio_root)
        output_path = args.output_root / rel.parent / f"{audio_path.stem}.npz"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists() and not args.overwrite:
            skipped += 1
            LOG.debug("Skipping existing %s", output_path)
            continue

        try:
            features, summary = extract_features(
                audio_path=audio_path,
                sample_rate=args.sample_rate,
                trim_top_db=args.trim_top_db,
                n_fft=args.n_fft,
                hop_length=args.hop_length,
                n_mels=args.n_mels,
                n_mfcc=args.n_mfcc,
            )
            np.savez_compressed(output_path, **features)
            summary.features_path = str(output_path)
            manifest.append(summary)
            LOG.info(
                "Processed %s -> %s (%.1fs)",
                audio_path,
                output_path,
                summary.duration_sec,
            )
        except Exception as exc:  # pragma: no cover
            failures += 1
            LOG.error("Failed %s: %s", audio_path, exc)
            LOG.debug("Traceback:", exc_info=True)

    if manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        with args.manifest.open("w", encoding="utf-8") as fh:
            for item in manifest:
                fh.write(json.dumps(asdict(item)) + "\n")

    LOG.info(
        "Completed: %d extracted, %d skipped, %d failed",
        len(manifest),
        skipped,
        failures,
    )
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
