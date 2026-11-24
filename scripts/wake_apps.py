"""잠든 Streamlit 앱 깨우기 (GitHub Actions 예약 실행: .github/workflows/wake-apps.yml).

무료 Streamlit Community Cloud 앱은 한동안 방문이 없으면 잠든다. 사이트는 앱 본체(/~/+/)를
페이지 안에 끼워 넣으므로, 잠든 앱은 깨우기 버튼 없이 빈 화면으로 보인다.
이 스크립트는 _links.yml 에 적힌 *.streamlit.app 주소를 모두 실제 브라우저로 열어
잠들어 있으면 깨우기 버튼을 누르고, 앱 화면이 뜰 때까지 기다린다.

    python scripts/wake_apps.py            # 실패한 앱이 있으면 종료 코드 1 (Actions 가 실패 메일을 보냄)
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WAKE = re.compile(r"get this app back up", re.I)


def app_urls() -> list[str]:
    text = (ROOT / "_links.yml").read_text(encoding="utf-8")
    return sorted(set(re.findall(r"https://[\w.-]+\.streamlit\.app", text)))


def wake(pg, base: str) -> str:
    pg.goto(base + "/", wait_until="domcontentloaded", timeout=120_000)
    clicked = False
    t0 = time.time()
    while time.time() - t0 < 25:                       # 잠든 화면이면 깨우기 버튼이 나온다
        btn = pg.get_by_role("button", name=WAKE)
        if btn.count() and btn.first.is_visible():
            btn.first.click()
            clicked = True
            break
        pg.wait_for_timeout(1000)
    # 앱 본체가 실제로 그려지는지 확인(깨우는 데 1~3분)
    t0 = time.time()
    while time.time() - t0 < 360:
        pg.goto(base + "/~/+/", wait_until="domcontentloaded", timeout=120_000)
        try:
            pg.wait_for_selector("h1", timeout=60_000)
            return ("깨움" if clicked else "깨어 있음") + f" ({time.time() - t0:.0f}초)"
        except Exception:  # noqa: BLE001
            pg.wait_for_timeout(15_000)
    raise RuntimeError("앱 화면이 6분 안에 뜨지 않음")


def main() -> int:
    urls = app_urls()
    failed = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel=os.environ.get("PW_CHANNEL") or None)   # 로컬 시험: PW_CHANNEL=msedge
        for u in urls:
            pg = b.new_page(viewport={"width": 1280, "height": 900})
            try:
                print(f"{u}: {wake(pg, u)}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"{u}: 실패 — {e}", flush=True)
                failed.append(u)
            finally:
                pg.close()
        b.close()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
