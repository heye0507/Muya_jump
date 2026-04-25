from pathlib import Path

from run_analysis import build_parser


def test_cli_accepts_video_output_and_fps_options():
    parser = build_parser()

    args = parser.parse_args(
        [
            "--video",
            "input/jump.mp4",
            "--output",
            "output/sample_run",
            "--fps",
            "10",
        ]
    )

    assert args.video == Path("input/jump.mp4")
    assert args.output == Path("output/sample_run")
    assert args.fps == 10
