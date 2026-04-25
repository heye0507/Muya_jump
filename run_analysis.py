"""Command line entry point for the jump analysis pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Optional, Sequence

from src.frame_extraction import FrameExtractionError, FrameExtractor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a figure skating jump video.")
    parser.add_argument("--video", required=True, type=Path, help="Path to the input video file.")
    parser.add_argument(
        "--output",
        default=Path("output/analysis"),
        type=Path,
        help="Directory where extracted frames and metadata will be written.",
    )
    parser.add_argument(
        "--fps",
        default=None,
        type=float,
        help="Optional extraction rate. Omit this to extract every frame.",
    )
    parser.add_argument(
        "--ffmpeg-path",
        default="ffmpeg",
        help="Path to the ffmpeg executable.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    extractor = FrameExtractor(ffmpeg_path=args.ffmpeg_path)
    result = extractor.extract(args.video, args.output, fps=args.fps)
    print(json.dumps(result.metadata, indent=2))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return run(args)
    except (FileNotFoundError, FrameExtractionError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
