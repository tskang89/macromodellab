"""첫 화면 인트로 애니메이션(Manim Community 0.22).

만들기(프로젝트 폴더에서):
    .venv\\Scripts\\python.exe scripts\\build_intro.py
결과: assets/intro/intro.mp4, assets/intro/intro-poster.png

흐름: GDP·잠재 GDP 곡선과 갭 → 핵심 식(LW형 IS곡선·필립스곡선·테일러 준칙)
      → 산업연관 네트워크의 파급 흐름 → 제목.
곡선은 설명용으로 만든 모양이며 실제 통계가 아니다.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Axes, Circle, Create, DashedLine, Dot, FadeIn, FadeOut, GrowFromCenter, LaggedStart, Line,
    MathTex, ReplacementTransform, Scene, ShowPassingFlash, TexTemplate, Text, VGroup, Write,
    DOWN, LEFT, RIGHT, UP, ORIGIN, TAU, config, linear, rate_functions, smooth,
)

BG = "#0b1626"
INK = "#e9eef6"
MUTED = "#8fa0b8"
AXIS = "#3c4a60"
GOLD = "#d4a95a"
BLUE = "#4f86c6"
CORAL = "#d9785f"
FONT = "Noto Sans KR"

config.background_color = BG

# 이 PC의 MiKTeX 에는 preview.sty 가 없고 자동 설치가 실패한다(Manim 기본 틀은 standalone[preview]).
# article 로 조판해도 dvisvgm 이 내용 크기로 잘라 주므로 결과는 같다.
TEX = TexTemplate(documentclass=r"\documentclass[12pt]{article}",
                  preamble=r"\usepackage{amsmath}\usepackage{amssymb}\pagestyle{empty}")


def gdp(x: float) -> float:
    return 0.36 * x + 0.75 * np.sin(1.25 * x) + 0.28 * np.sin(2.9 * x + 1.1) + 0.6


def trend(x: float) -> float:
    return 0.36 * x + 0.05 * np.sin(0.5 * x) + 0.6


class Intro(Scene):
    def construct(self):
        # 0. 옅은 가로줄 바탕
        rules = VGroup(*[Line(LEFT * 7.2 + UP * y, RIGHT * 7.2 + UP * y, stroke_width=1,
                              stroke_color=INK, stroke_opacity=0.045) for y in np.arange(-3.5, 3.6, 0.7)])
        self.add(rules)

        # 1. 축과 곡선
        ax = Axes(x_range=[0, 10, 1], y_range=[-0.5, 5.2, 1], x_length=5.6, y_length=4.0,
                  tips=False, axis_config={"stroke_color": AXIS, "stroke_width": 1.6,
                                           "include_ticks": False})
        ax.move_to(LEFT * 3.75 + DOWN * 0.1)
        g_line = ax.plot(gdp, x_range=[0, 10], color=INK, stroke_width=3.2)
        t_line = ax.plot(trend, x_range=[0, 10], color=GOLD, stroke_width=3.2)
        area_pos = ax.get_area(g_line, x_range=[0, 10], bounded_graph=t_line, color=BLUE, opacity=0.28)
        l_gdp = Text("GDP", font=FONT, color=INK, weight="MEDIUM").scale(0.36)
        l_pot = Text("잠재 GDP", font=FONT, color=GOLD, weight="MEDIUM").scale(0.36)
        # 끝점에서 두 선이 가까우므로 이름표를 위(잠재)·아래(GDP)로 벌린다
        hi, lo = (l_pot, l_gdp) if trend(10) >= gdp(10) else (l_gdp, l_pot)
        mid = ax.c2p(10, (gdp(10) + trend(10)) / 2)
        hi.next_to(mid, RIGHT, buff=0.18).shift(UP * 0.24)
        lo.next_to(mid, RIGHT, buff=0.18).shift(DOWN * 0.24)
        cap = Text("GDP 갭 = 실제 GDP − 잠재 GDP", font=FONT, color=MUTED).scale(0.32)
        cap.next_to(ax, DOWN, buff=0.3).align_to(ax, LEFT)

        self.play(Create(ax), run_time=0.8, rate_func=smooth)
        self.play(Create(g_line), run_time=1.6, rate_func=linear)
        self.play(FadeIn(l_gdp, shift=LEFT * 0.1), Create(t_line), run_time=1.1, rate_func=smooth)
        self.play(FadeIn(area_pos), FadeIn(l_pot, shift=LEFT * 0.1), FadeIn(cap, shift=UP * 0.1),
                  run_time=0.8)

        # 2. 핵심 식
        eq_kw = {"color": INK, "tex_template": TEX}
        e1 = MathTex(r"\tilde y_t = a_1 \tilde y_{t-1} + a_2 \tilde y_{t-2}"
                     r" + \tfrac{a_r}{2}\sum_{j=1}^{2}\left(r_{t-j}-r^*_{t-j}\right) + \varepsilon_t", **eq_kw)
        e2 = MathTex(r"\pi_t = b_\pi \pi_{t-1} + (1-b_\pi)\,\pi^e_t + b_y \tilde y_{t-1} + \varepsilon^{\pi}_t", **eq_kw)
        e3 = MathTex(r"i_t = r^*_t + \pi_t + 0.5\,(\pi_t-\pi^*) + 0.5\,\tilde y_t", **eq_kw)
        tags = [Text(s, font=FONT, color=MUTED).scale(0.34) for s in ("IS 곡선", "필립스 곡선", "테일러 준칙")]
        rows = VGroup()
        for tag, e in zip(tags, (e1, e2, e3)):
            e.scale(0.78)
            rows.add(VGroup(tag, e).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        if rows.width > 5.9:
            rows.scale_to_fit_width(5.9)
        rows.move_to(RIGHT * 3.45 + DOWN * 0.1)
        divider = Line(UP * 2.2, DOWN * 2.2, stroke_color=AXIS, stroke_width=1).move_to(RIGHT * 0.25 + DOWN * 0.1)
        self.play(Create(divider), run_time=0.4)
        for r in rows:
            self.play(FadeIn(r[0], shift=RIGHT * 0.08), Write(r[1]), run_time=0.85)
        self.wait(0.5)

        # 3. 산업연관 네트워크: 그림과 식을 걷어 내고 노드로
        chart = VGroup(ax, g_line, t_line, area_pos, l_gdp, l_pot, cap)
        self.play(FadeOut(chart, shift=LEFT * 0.3), FadeOut(rows, shift=RIGHT * 0.3), FadeOut(divider),
                  run_time=0.7)

        n = 12
        rng = np.random.default_rng(3)
        pts = [np.array([2.55 * np.cos(TAU * k / n + 0.2), 2.55 * np.sin(TAU * k / n + 0.2), 0]) for k in range(n)]
        sizes = rng.uniform(0.06, 0.13, n)
        nodes = VGroup(*[Dot(p, radius=s, color=INK) for p, s in zip(pts, sizes)])
        hub = Dot(ORIGIN, radius=0.16, color=GOLD)
        pairs = sorted({tuple(sorted(rng.choice(n, 2, replace=False))) for _ in range(26)})
        edges = VGroup(*[Line(pts[a], pts[b], stroke_width=1.3, stroke_color=INK, stroke_opacity=0.18)
                         for a, b in pairs])
        spokes = VGroup(*[Line(ORIGIN, p, stroke_width=1.3, stroke_color=GOLD, stroke_opacity=0.35) for p in pts])
        ring = Circle(radius=2.55, stroke_color=AXIS, stroke_width=1)
        net_cap = Text("산업 간 파급효과", font=FONT, color=MUTED).scale(0.32).next_to(ring, DOWN, buff=0.35)

        self.play(Create(ring), LaggedStart(*[GrowFromCenter(d) for d in nodes], lag_ratio=0.06),
                  run_time=1.0)
        self.play(Create(edges, lag_ratio=0.03), GrowFromCenter(hub), FadeIn(spokes), FadeIn(net_cap),
                  run_time=0.9)
        flashes = [ShowPassingFlash(Line(ORIGIN, p, stroke_width=4, color=GOLD), time_width=0.6) for p in pts]
        flashes += [ShowPassingFlash(e.copy().set_stroke(color=BLUE, width=3, opacity=1), time_width=0.5)
                    for e in edges]
        self.play(LaggedStart(*flashes, lag_ratio=0.025), run_time=1.6)

        # 4. 제목
        net = VGroup(ring, nodes, edges, spokes, net_cap, hub)
        title = Text("Macro Model Lab", font=FONT, color=INK, weight="MEDIUM").scale(1.05)
        rule = Line(LEFT * 2.6, RIGHT * 2.6, stroke_color=GOLD, stroke_width=2.2)
        sub = Text("거시경제 모형 · 추정 · 시뮬레이션", font=FONT, color=MUTED).scale(0.42)
        VGroup(title, rule, sub).arrange(DOWN, buff=0.32)
        self.play(FadeOut(net, scale=0.55), run_time=0.7, rate_func=rate_functions.ease_in_cubic)
        self.play(GrowFromCenter(rule), run_time=0.5, rate_func=rate_functions.ease_out_cubic)
        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        self.wait(1.3)
