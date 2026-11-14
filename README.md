# Macro Model Lab

<https://macromodellab.com> 의 원본. [Quarto](https://quarto.org) 정적 사이트이며,
`main` 에 푸시하면 GitHub Actions(`.github/workflows/publish.yml`)가 렌더해
GitHub Pages 로 배포한다.

## 구조

| 경로 | 내용 |
|:--|:--|
| `_quarto.yml` | 사이트 설정: 사이드바 메뉴(순서·이름), 테마, 수식(KaTeX), 렌더 대상 |
| `_links.yml` | **메뉴별 외부 연결 주소(앱·저장소·설명서) — 링크는 여기서만 고친다** |
| `index.qmd` | 한국어 첫 화면(사이트 루트) |
| `ko/*.qmd` | 한국어 주제 페이지 5개 |
| `en/*.qmd` | 영어판 초안(아직 렌더하지 않음) |
| `guide/showcase.qmd` | 수식·코드·그림·표 서식 견본(메뉴에 없음, 검색 제외) |
| `_extensions/links/` | `{{< links 키 >}}` 단축코드: `_links.yml` 값을 버튼으로 그린다 |
| `assets/` | 스타일(`styles.scss`), 글꼴 로딩(`head.html`), 파비콘 |
| `CNAME` | 사용자 도메인 `macromodellab.com` |

## 링크 바꾸기

`_links.yml` 에서 해당 항목의 `app`·`repo`·`doc` 에 주소를 넣고 푸시한다.
빈 칸은 버튼이 나오지 않고, 셋 다 비면 '준비 중' 안내가 나온다.
한국어판과 영어판이 같은 값을 쓴다.

## 영어판 열기

1. `en/*.qmd` 의 본문을 채운다(폴더의 `_metadata.yml` 이 `lang: en-US` 를 준다).
2. `_quarto.yml` 에서 `project.render` 의 `# - en/*.qmd` 주석을 푼다.
3. 같은 파일의 `website.sidebar` 에서 `en` 블록과, `ko` 블록의 `tools`(언어 전환) 주석을 푼다.

주소 체계: 한국어는 루트(`/`)와 `/ko/…`, 영어는 `/en/…`.
`lang` 값은 반드시 `ko-KR`·`en-US` 꼴로 쓴다 — `ko`·`en` 이라고만 쓰면 같은 이름의
폴더 경로로 해석된다.

## 로컬 빌드

```
quarto render          # _site/ 에 결과
quarto preview         # 미리보기 서버
```

이 PC에는 Quarto 1.11.9 가 `D:\Claude\Tools\quarto\bin\quarto.exe` 에 있다(Actions 도 같은 판).
견본 그림을 다시 만들 때만 파이썬이 필요하다: `python scripts/make_showcase_chart.py`.

## DNS(Cloudflare)

| 유형 | 이름 | 값 |
|:--|:--|:--|
| A | `@` | 185.199.108.153 |
| A | `@` | 185.199.109.153 |
| A | `@` | 185.199.110.153 |
| A | `@` | 185.199.111.153 |
| AAAA | `@` | 2606:50c0:8000::153 · 8001::153 · 8002::153 · 8003::153 |
| CNAME | `www` | tskang89.github.io |

프록시는 **DNS only(회색 구름)** 로 둔다. GitHub 가 인증서를 발급한 뒤
저장소 Settings → Pages 에서 Enforce HTTPS 를 켠다.
