# Figure Skating Jump Analyzer

A Python project for extracting frames from figure skating videos, classifying jump types, counting rotations, and producing structured analysis reports.

## Project Status

Phase 1 is focused on frame extraction. Jump type classification, rotation counting, and final report generation are intentionally reserved for later phases.

## Requirements

- Python 3.8+
- ffmpeg installed and available on your shell path

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Extract every frame from a video:

```bash
python run_analysis.py --video path/to/video.mp4 --output output/sample_run
```

Extract frames at a fixed sampling rate:

```bash
python run_analysis.py --video path/to/video.mp4 --output output/sample_run --fps 10
```

The frame extraction step writes:

```text
output/sample_run/frames/frame_000001.jpg
output/sample_run/metadata.json
```

## Modules

- Frame Extraction: extracts video frames with ffmpeg and writes metadata.
- Jump Type Classification: planned for Phase 2.
- Rotation Counting: planned for Phase 2.
- Reporting: planned for Phase 3.

## Tests

```bash
python -m pytest
```
