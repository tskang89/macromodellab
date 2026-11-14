"""인트로 애니메이션을 렌더해 assets/intro/ 에 놓는다.

    .venv\\Scripts\\python.exe scripts\\build_intro.py          # 1920x1080 30fps
    .venv\\Scripts\\python.exe scripts\\build_intro.py --draft  # 빠른 확인용 저해상도
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "scripts" / "intro_scene.py"
MEDIA = ROOT / "_manim"
OUT = ROOT / "assets" / "intro"


def manim(*args: str) -> None:
    cmd = [sys.executable, "-m", "manim", "render", str(SCENE), "Intro", "--media_dir", str(MEDIA),
           "--disable_caching", "-v", "WARNING", *args]
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    draft = "--draft" in sys.argv
    res = ["-r", "960,540", "--fps", "15"] if draft else ["-r", "1920,1080", "--fps", "30"]
    manim(*res)
    manim(*res, "-s")  # 마지막 장면(포스터)
    mp4 = next(MEDIA.rglob("Intro.mp4"))
    png = max(MEDIA.rglob("Intro*.png"), key=lambda p: p.stat().st_mtime)
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(mp4, OUT / "intro.mp4")
    shutil.copyfile(png, OUT / "intro-poster.png")
    for f in ("intro.mp4", "intro-poster.png"):
        print(OUT / f, (OUT / f).stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
