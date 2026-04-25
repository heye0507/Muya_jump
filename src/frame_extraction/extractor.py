"""ffmpeg-backed frame extraction for figure skating videos."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

PathLike = Union[str, Path]
Runner = Callable[..., subprocess.CompletedProcess]


class FrameExtractionError(RuntimeError):
    """Raised when ffmpeg cannot extract frames from the input video."""


@dataclass(frozen=True)
class FrameExtractionResult:
    """Result returned after a frame extraction run."""

    video_path: Path
    output_dir: Path
    frames_dir: Path
    metadata_path: Path
    frame_pattern: str
    fps: Optional[float]
    image_format: str
    frame_count: int
    metadata: Dict[str, Any]


class FrameExtractor:
    """Extract frames from a video file using ffmpeg."""

    def __init__(self, ffmpeg_path: str = "ffmpeg", runner: Runner = subprocess.run) -> None:
        self.ffmpeg_path = ffmpeg_path
        self._runner = runner

    def build_command(
        self,
        video_path: PathLike,
        frames_dir: PathLike,
        fps: Optional[float] = None,
        image_format: str = "jpg",
    ) -> List[str]:
        """Build the ffmpeg command used for extraction."""
        self._validate_image_format(image_format)
        fps_filter = self._format_fps_filter(fps)
        frame_pattern = Path(frames_dir) / f"frame_%06d.{image_format}"

        command = [
            self.ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video_path),
        ]

        if fps_filter is not None:
            command.extend(["-vf", fps_filter])

        command.append(str(frame_pattern))
        return command

    def extract(
        self,
        video_path: PathLike,
        output_dir: PathLike,
        fps: Optional[float] = None,
        image_format: str = "jpg",
    ) -> FrameExtractionResult:
        """Extract frames into output_dir/frames and write metadata.json."""
        video = Path(video_path)
        if not video.exists():
            raise FileNotFoundError(f"Video file does not exist: {video}")

        output = Path(output_dir)
        frames_dir = output / "frames"
        metadata_path = output / "metadata.json"
        frame_pattern = frames_dir / f"frame_%06d.{image_format}"
        command = self.build_command(video, frames_dir, fps=fps, image_format=image_format)

        frames_dir.mkdir(parents=True, exist_ok=True)

        try:
            self._runner(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            detail = f": {stderr}" if stderr else ""
            raise FrameExtractionError(f"ffmpeg failed{detail}") from exc
        except OSError as exc:
            raise FrameExtractionError(f"Could not run ffmpeg: {exc}") from exc

        frame_count = self._count_frames(frames_dir, image_format)
        metadata = {
            "video_path": str(video),
            "output_dir": str(output),
            "frames_dir": str(frames_dir),
            "metadata_path": str(metadata_path),
            "frame_pattern": str(frame_pattern),
            "fps": fps,
            "image_format": image_format,
            "frame_count": frame_count,
            "ffmpeg_command": command,
        }
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        return FrameExtractionResult(
            video_path=video,
            output_dir=output,
            frames_dir=frames_dir,
            metadata_path=metadata_path,
            frame_pattern=str(frame_pattern),
            fps=fps,
            image_format=image_format,
            frame_count=frame_count,
            metadata=metadata,
        )

    @staticmethod
    def _count_frames(frames_dir: Path, image_format: str) -> int:
        return len(list(frames_dir.glob(f"frame_*.{image_format}")))

    @staticmethod
    def _format_fps_filter(fps: Optional[float]) -> Optional[str]:
        if fps is None:
            return None

        fps_value = float(fps)
        if fps_value <= 0:
            raise ValueError("fps must be greater than 0")

        if fps_value.is_integer():
            fps_text = str(int(fps_value))
        else:
            fps_text = str(fps_value)
        return f"fps={fps_text}"

    @staticmethod
    def _validate_image_format(image_format: str) -> None:
        allowed_formats = {"jpg", "jpeg", "png"}
        if image_format not in allowed_formats:
            allowed = ", ".join(sorted(allowed_formats))
            raise ValueError(f"image_format must be one of: {allowed}")
