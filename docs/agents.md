# Codex Agents for Jump Analysis Project

## Overview

This repository implements a figure skating jump analysis tool. Codex agents should:

1. Extract frames from an input video.
2. Classify jump types from frames.
3. Count jump rotation.
4. Produce a structured JSON report.

## Environment Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest
```

## Coding Conventions

- Use Python 3.8+.
- Follow PEP8 style for Python code.
- Use type annotations when feasible.
- Keep project files, documentation, comments, and test names in English.

## Module Responsibilities

### FrameExtractor

Input: video file.

Output: extracted frames directory and metadata JSON.

### JumpTypeClassifier

Input: frame set or key frames.

Output: jump type string and confidence score.

### RotationCounter

Input: key frames with pose or rotation evidence.

Output: estimated rotations and missing rotation degrees.

### Reporter

Input: frame extraction metadata, jump type result, and rotation result.

Output: JSON report for the analyzed video.

## Acceptance Criteria

1. Must pass all tests under `/tests`.
2. All new code should include tests.
3. CLI should accept a video and produce a JSON-compatible report.
4. Phase 1 should allow later modules to reuse extracted frames without re-extracting the source video.
