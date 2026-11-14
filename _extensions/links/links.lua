-- {{< links 키 >}} : _links.yml 의 links.<키> 에서 app·repo·doc 주소를 읽어
-- 버튼 줄을 만든다. 빈 주소는 건너뛰고, 모두 비면 '준비 중' 안내를 낸다.
-- 버튼 문구는 문서의 lang(ko/en)에 따라 바뀐다.

-- {{< app 키 >}} : links.<키>.app 주소를 본문에 끼워 넣는다(iframe, Streamlit embed 모드).
-- 주소가 비어 있으면 아무것도 그리지 않는다.

local LABELS = {
  ko = { app = "새 창에서 열기", repo = "GitHub 저장소", doc = "설명서",
         pending = "외부 연결(앱·저장소)은 준비 중입니다.",
         frame = "분석 앱",
         wake = "화면이 비어 있거나 'Zzzz' 안내가 나오면 앱이 잠들어 있는 것입니다. 깨우는 버튼을 누르고 1분쯤 기다리거나 새 창에서 여세요." },
  en = { app = "Open in new tab", repo = "GitHub repository", doc = "Documentation",
         pending = "Links to the app and repository are coming soon.",
         frame = "Analysis app",
         wake = "If the frame is blank or says 'Zzzz', the app is asleep: press the wake button and wait about a minute, or open it in a new tab." },
}
local ORDER = { "app", "repo", "doc" }

local function str(x)
  if x == nil then return "" end
  return pandoc.utils.stringify(x)
end

local function esc(s)
  s = s:gsub("&", "&amp;")
  s = s:gsub('"', "&quot;")
  s = s:gsub("<", "&lt;")
  return s
end

return {
  ["links"] = function(args, kwargs, meta)
    local key = str(args[1])
    local lang = str(meta.lang):sub(1, 2)
    local L = LABELS[lang] or LABELS.ko

    local entry = meta.links and meta.links[key] or nil
    if entry == nil then
      quarto.log.warning("links: _links.yml 에 '" .. key .. "' 항목이 없습니다.")
    end

    local items = {}
    for _, k in ipairs(ORDER) do
      local url = entry and str(entry[k]) or ""
      if url ~= "" then
        local cls = (#items == 0) and "mml-btn mml-btn-primary" or "mml-btn"
        local ext = url:match("^https?://") and ' target="_blank" rel="noopener"' or ""
        table.insert(items, string.format('<a class="%s" href="%s"%s>%s</a>',
          cls, esc(url), ext, L[k]))
      end
    end

    if not quarto.doc.is_format("html") then
      return pandoc.Null()
    end
    if #items == 0 then
      return pandoc.RawBlock("html",
        '<p class="mml-links mml-links-pending">' .. L.pending .. "</p>")
    end
    return pandoc.RawBlock("html",
      '<div class="mml-links">' .. table.concat(items) .. "</div>")
  end,

  -- {{< status 키 >}} : 앱 주소가 있으면 '실행 가능', 없으면 '준비 중' 표지(첫 화면 카드용)
  ["status"] = function(args, kwargs, meta)
    if not quarto.doc.is_format("html") then
      return pandoc.Null()
    end
    local key = str(args[1])
    local lang = str(meta.lang):sub(1, 2)
    local entry = meta.links and meta.links[key] or nil
    local url = entry and str(entry.app) or ""
    local live = url ~= ""
    local isapp = url:match("%.streamlit%.app") ~= nil   -- 계산 앱이면 '실행', 그 밖(교재 등)은 '열람'
    local text
    if lang == "en" then
      text = (not live) and "Coming soon" or (isapp and "Live" or "Read online")
    else
      text = (not live) and "준비 중" or (isapp and "실행 가능" or "열람 가능")
    end
    return pandoc.RawInline("html", string.format('<span class="mml-chip %s">%s</span>',
      live and "is-live" or "is-soon", text))
  end,

  ["app"] = function(args, kwargs, meta)
    if not quarto.doc.is_format("html") then
      return pandoc.Null()
    end
    local key = str(args[1])
    local lang = str(meta.lang):sub(1, 2)
    local L = LABELS[lang] or LABELS.ko
    local entry = meta.links and meta.links[key] or nil
    local url = entry and str(entry.app) or ""
    if url == "" then
      return pandoc.Null()
    end
    -- Streamlit Cloud 의 기본 주소는 앱을 한 겹 더 싼 틀을 주는데, 다른 사이트 안에
    -- 넣으면 그 틀이 앱 높이를 150px 로 묶는다. 앱 본체(/~/+/)를 직접 연다.
    -- Streamlit 이 아닌 주소(예: 교재 사이트)는 그대로 넣는다.
    local src = url
    if src:match("%.streamlit%.app") then
      if not src:find("/~/+/", 1, true) then
        local base, query = src:match("^([^?]*)%??(.*)$")
        base = base:gsub("/+$", "")
        src = base .. "/~/+/" .. (query ~= "" and ("?" .. query) or "")
      end
      local sep = src:find("?", 1, true) and "&" or "?"
      src = src .. sep .. "embed=true&embed_options=light_theme"
    end
    -- body 에 mml-fullapp 를 달면 CSS 가 제목·소개·바닥글을 숨기고 앱이 본문 영역 전체를 채운다.
    return pandoc.RawBlock("html", string.format(
      '<script>document.body.classList.add("mml-fullapp")</script>' ..
      '<div class="mml-app"><iframe src="%s" title="%s" ' ..
      'allow="clipboard-write; fullscreen"></iframe>' ..
      '<a class="mml-app-open" href="%s" target="_blank" rel="noopener" title="%s">%s ↗</a></div>',
      esc(src), L.frame, esc(url), L.wake, L.app))
  end
}
