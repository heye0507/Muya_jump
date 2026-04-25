# Frame Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a usable Phase 1 frame extraction module that can extract reusable frames from a video with ffmpeg.

**Architecture:** `run_analysis.py` owns CLI parsing and delegates extraction to `FrameExtractor`. `FrameExtractor` builds an ffmpeg command, writes frames to `output_dir/frames`, and records run metadata in `metadata.json`. Later jump classification and rotation counting modules will consume the extracted frames instead of reprocessing videos.

**Tech Stack:** Python 3.8+, ffmpeg CLI, pytest.

---

### Task 1: Frame Extraction Tests

**Files:**
- Create: `tests/test_frame_extraction.py`
- Create: `tests/test_cli.py`

- [x] Write tests for ffmpeg command construction, optional fps filtering, missing video validation, metadata writing, and ffmpeg error wrapping.
- [x] Write a CLI parser test for `--video`, `--output`, and `--fps`.
- [x] Run `python -m pytest` and confirm tests fail because implementation files do not exist.

### Task 2: Frame Extraction Implementation

**Files:**
- Create: `src/frame_extraction/extractor.py`
- Create: `src/frame_extraction/__init__.py`
- Create: `run_analysis.py`

- [x] Implement `FrameExtractor.build_command`.
- [x] Implement `FrameExtractor.extract` to run ffmpeg, count frames, and write metadata.
- [x] Implement CLI entry points in `run_analysis.py`.

### Task 3: Project Scaffold

**Files:**
- Create: `README.md`
- Create: `docs/agents.md`
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `.github/workflows/python-ci.yml`
- Create: `src/jump_classification/classifier.py`
- Create: `src/rotation_counter/counter.py`

- [x] Document project purpose, usage, and phase status.
- [x] Add CI that installs dependencies and runs `python -m pytest`.
- [x] Add explicit Phase 2 placeholders for jump classification and rotation counting.

### Task 4: Verification

**Files:**
- Test: all project tests

- [x] Run `python -m pytest -p no:cacheprovider`.
- [x] Confirm all tests pass without relying on a real video or ffmpeg binary.
