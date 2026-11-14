"""작성 예시 페이지(guide/showcase.qmd)에 쓰는 예시 그림을 만든다.

가상 자료다(실제 통계가 아님). 실행:
    .venv\\Scripts\\python.exe scripts\\make_showcase_chart.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "guide" / "figures" / "showcase-gap.svg"

rng = np.random.default_rng(7)
n = 80
t = np.arange(n)
trend = 100 * np.exp(0.006 * t)
cycle = 1.5 * np.sin(t / 6.0) + rng.normal(0, 0.4, n)
y = trend * (1 + cycle / 100)

# HP 필터(λ=1600) — 희소 행렬 없이 작은 표본용으로 직접 푼다
lam = 1600.0
D = np.diff(np.eye(n), n=2, axis=0)
tau = np.linalg.solve(np.eye(n) + lam * D.T @ D, np.log(y))
gap = 100 * (np.log(y) - tau)

plt.rcParams.update({
    "font.family": ["Malgun Gothic", "DejaVu Sans"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#9aa3ae",
    "axes.labelcolor": "#3d4553",
    "xtick.color": "#5b6472",
    "ytick.color": "#5b6472",
    "font.size": 10,
    "svg.fonttype": "path",
})
fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.axhline(0, color="#9aa3ae", lw=0.8)
ax.fill_between(t, gap, 0, where=gap >= 0, color="#1f3a5f", alpha=0.18, lw=0)
ax.fill_between(t, gap, 0, where=gap < 0, color="#b5543a", alpha=0.18, lw=0)
ax.plot(t, gap, color="#1f3a5f", lw=1.6)
ax.set_ylabel("GDP 갭(%)")
ax.set_xlabel("분기")
ax.set_xlim(0, n - 1)
ax.grid(axis="y", color="#e3e6ea", lw=0.7)
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT)
print(OUT)
