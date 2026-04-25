from pathlib import Path
import subprocess

import pytest

from src.frame_extraction.extractor import FrameExtractionError, FrameExtractor


def test_build_command_extracts_all_frames_when_fps_is_none(tmp_path):
    extractor = FrameExtractor(ffmpeg_path="ffmpeg")
    video_path = tmp_path / "jump.mp4"
    frames_dir = tmp_path / "frames"

    command = extractor.build_command(video_path, frames_dir, fps=None)

    assert command == [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(video_path),
        str(frames_dir / "frame_%06d.jpg"),
    ]


def test_build_command_adds_fps_filter_when_requested(tmp_path):
    extractor = FrameExtractor(ffmpeg_path="ffmpeg")
    video_path = tmp_path / "jump.mp4"
    frames_dir = tmp_path / "frames"

    command = extractor.build_command(video_path, frames_dir, fps=12.5)

    assert "-vf" in command
    assert "fps=12.5" in command
    assert command[-1] == str(frames_dir / "frame_%06d.jpg")


def test_extract_rejects_missing_video(tmp_path):
    extractor = FrameExtractor()

    with pytest.raises(FileNotFoundError, match="Video file does not exist"):
        extractor.extract(tmp_path / "missing.mp4", tmp_path / "analysis")


def test_extract_writes_metadata_after_ffmpeg_run(tmp_path):
    video_path = tmp_path / "jump.mp4"
    video_path.write_bytes(b"fake video")
    output_dir = tmp_path / "analysis"
    calls = []

    def fake_runner(command, check, capture_output, text):
        calls.append(
            {
                "command": command,
                "check": check,
                "capture_output": capture_output,
                "text": text,
            }
        )
        frames_dir = output_dir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        (frames_dir / "frame_000001.jpg").write_bytes(b"frame 1")
        (frames_dir / "frame_000002.jpg").write_bytes(b"frame 2")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    extractor = FrameExtractor(ffmpeg_path="ffmpeg", runner=fake_runner)

    result = extractor.extract(video_path, output_dir, fps=10)

    assert result.frame_count == 2
    assert result.frames_dir == output_dir / "frames"
    assert result.metadata_path == output_dir / "metadata.json"
    assert result.metadata_path.exists()
    assert calls[0]["command"] == extractor.build_command(video_path, output_dir / "frames", fps=10)

    metadata = result.metadata
    assert metadata["video_path"] == str(video_path)
    assert metadata["frames_dir"] == str(output_dir / "frames")
    assert metadata["frame_count"] == 2
    assert metadata["fps"] == 10
    assert metadata["image_format"] == "jpg"


def test_extract_wraps_ffmpeg_failure(tmp_path):
    video_path = tmp_path / "jump.mp4"
    video_path.write_bytes(b"fake video")

    def failing_runner(command, check, capture_output, text):
        raise subprocess.CalledProcessError(1, command, stderr="bad video")

    extractor = FrameExtractor(runner=failing_runner)

    with pytest.raises(FrameExtractionError, match="ffmpeg failed"):
        extractor.extract(video_path, tmp_path / "analysis")
