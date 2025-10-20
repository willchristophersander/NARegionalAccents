#!/usr/bin/env python3
"""
Diagnostic plots for extracted IDEA accent features.

Generates waveform, log-mel spectrogram, MFCC heatmap, and pitch contour figures
for selected samples to visually verify feature quality.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


LOG = logging.getLogger("feature_visualizer")


@dataclass
class SampleMeta:
    state: str
    sample_id: str
    features_path: Path
    sample_rate: int
    hop_length: int
    duration_sec: float


def load_manifest(path: Path, hop_length: int) -> Dict[str, SampleMeta]:
    """
    Returns a mapping from feature file paths to SampleMeta.
    """
    lookup: Dict[str, SampleMeta] = {}
    if not path.exists():
        LOG.warning("Manifest %s not found; falling back to defaults", path)
        return lookup

    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            features_path = Path(data["features_path"]).resolve()
            sample_rate = int(data.get("sample_rate", 16_000))
            duration_sec = float(data.get("duration_sec", 0.0))
            hp = int(data.get("hop_length", hop_length))
            lookup[str(features_path)] = SampleMeta(
                state=data.get("state", "unknown"),
                sample_id=data.get("sample_id", features_path.stem),
                features_path=features_path,
                sample_rate=sample_rate,
                hop_length=hp,
                duration_sec=duration_sec,
            )
    return lookup


def build_state_index(manifest: Dict[str, SampleMeta]) -> Dict[str, List[SampleMeta]]:
    index: Dict[str, List[SampleMeta]] = {}
    for meta in manifest.values():
        key = meta.state.lower()
        index.setdefault(key, []).append(meta)
    # Sort samples per state for deterministic selection
    for metas in index.values():
        metas.sort(key=lambda m: m.sample_id)
    return index


def select_samples(
    manifest: Dict[str, SampleMeta],
    state_index: Dict[str, List[SampleMeta]],
    states: Sequence[str],
    per_state: int,
    extra_files: Sequence[Path],
    default_sample_rate: int,
    default_hop: int,
) -> List[SampleMeta]:
    selections: List[SampleMeta] = []

    for state in states:
        metas = state_index.get(state.lower())
        if not metas:
            LOG.warning("No samples found for state '%s'", state)
            continue
        selections.extend(metas[:per_state])

    for file_path in extra_files:
        resolved = file_path.resolve()
        key = str(resolved)
        if key in manifest:
            selections.append(manifest[key])
            continue

        # Fallback: infer minimal metadata from path
        state = resolved.parent.name
        selections.append(
            SampleMeta(
                state=state,
                sample_id=resolved.stem,
                features_path=resolved,
                sample_rate=default_sample_rate,
                hop_length=default_hop,
                duration_sec=0.0,
            )
        )

    # Deduplicate while preserving order
    seen = set()
    deduped: List[SampleMeta] = []
    for meta in selections:
        key = (meta.features_path, meta.sample_id)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(meta)

    return deduped


def plot_sample(
    meta: SampleMeta,
    features: Dict[str, np.ndarray],
    output_dir: Path,
    dpi: int,
) -> Path:
    sfreq = meta.sample_rate
    hop = meta.hop_length
    title = f"{meta.state} / {meta.sample_id}"
    waveform = features.get("waveform")

    if waveform is None:
        raise KeyError("waveform array missing in features archive")

    wave_time = np.arange(waveform.shape[0]) / sfreq
    frame_count = features.get("log_mel", np.empty((0, 0))).shape[1]
    frame_times = np.arange(frame_count) * hop / sfreq

    fig, axes = plt.subplots(4, 1, figsize=(12, 12), constrained_layout=True)
    fig.suptitle(title, fontsize=14)

    axes[0].plot(wave_time, waveform, linewidth=0.8)
    axes[0].set_title("Waveform")
    axes[0].set_ylabel("Amplitude")
    axes[0].set_xlabel("Time (s)")

    log_mel = features.get("log_mel")
    if log_mel is not None and log_mel.size:
        im = axes[1].imshow(
            log_mel,
            origin="lower",
            aspect="auto",
            extent=[frame_times[0] if frame_times.size else 0, frame_times[-1] if frame_times.size else 0, 0, log_mel.shape[0]],
            cmap="magma",
        )
        axes[1].set_title("Log-Mel Spectrogram")
        axes[1].set_ylabel("Mel bins")
        axes[1].set_xlabel("Time (s)")
        fig.colorbar(im, ax=axes[1], format="%.1f")
    else:
        axes[1].set_visible(False)

    mfcc = features.get("mfcc")
    if mfcc is not None and mfcc.size:
        im = axes[2].imshow(
            mfcc,
            origin="lower",
            aspect="auto",
            extent=[frame_times[0] if frame_times.size else 0, frame_times[-1] if frame_times.size else 0, 0, mfcc.shape[0]],
            cmap="viridis",
        )
        axes[2].set_title("MFCCs")
        axes[2].set_ylabel("Coefficient")
        axes[2].set_xlabel("Time (s)")
        fig.colorbar(im, ax=axes[2], format="%.1f")
    else:
        axes[2].set_visible(False)

    pitch = features.get("pitch")
    if pitch is not None and pitch.size:
        pitch_time = np.arange(pitch.shape[0]) * hop / sfreq
        axes[3].plot(pitch_time, pitch, linewidth=0.8)
        axes[3].set_title("Pitch Contour")
        axes[3].set_ylabel("Frequency (Hz)")
        axes[3].set_xlabel("Time (s)")
    else:
        axes[3].set_visible(False)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{meta.state}_{meta.sample_id}.png"
    fig.savefig(output_path, dpi=dpi)
    plt.close(fig)
    LOG.info("Saved %s", output_path)
    return output_path


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plot waveform, spectrogram, MFCC, and pitch for selected accent samples."
    )
    parser.add_argument("--manifest", type=Path, default=Path("features_manifest.jsonl"))
    parser.add_argument("--states", nargs="*", default=[], help="State names to visualise.")
    parser.add_argument("--per-state", type=int, default=1, help="Number of samples per state to plot.")
    parser.add_argument("--files", nargs="*", type=Path, default=[], help="Direct .npz paths to include.")
    parser.add_argument("--output-dir", type=Path, default=Path("feature_plots"))
    parser.add_argument("--sample-rate", type=int, default=16_000, help="Fallback sample rate if manifest metadata is missing.")
    parser.add_argument("--hop-length", type=int, default=512, help="Fallback hop length if manifest metadata is missing.")
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    args = parser.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(levelname)s %(message)s")

    manifest_lookup = load_manifest(args.manifest, args.hop_length)
    state_index = build_state_index(manifest_lookup)

    available_states = sorted(state_index.keys())
    if not args.states and available_states:
        # Default to first three states alphabetically
        default_states = available_states[: min(3, len(available_states))]
        LOG.info("No states provided; defaulting to %s", ", ".join(default_states))
        states = default_states
    else:
        states = args.states

    samples = select_samples(
        manifest=manifest_lookup,
        state_index=state_index,
        states=states,
        per_state=args.per_state,
        extra_files=args.files,
        default_sample_rate=args.sample_rate,
        default_hop=args.hop_length,
    )

    if not samples:
        LOG.error("No samples selected; check states/files arguments.")
        return 1

    for meta in samples:
        if not meta.features_path.exists():
            LOG.warning("Feature file missing: %s", meta.features_path)
            continue

        with np.load(meta.features_path) as bundle:
            features = {key: bundle[key] for key in bundle}
        plot_sample(meta, features, args.output_dir, args.dpi)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
