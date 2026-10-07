# Builds index.html (self-contained). To add content: append a section to GROUPS and run `python3 build.py`.
import json, math, pathlib, sys
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D))
import parts_prep as P            # earlier cards (S1..S5) are reused as the "준비" group
from parts_prep import arrowdef, marker, pill

POINT = json.load(open(D / "point_grid.json"))   # 9x9 centre slice of the real point stamp (EDT ball, r=4)

CSS = """
:root{--bg:#f4f2ec;--card:#fff;--ink:#1d2127;--muted:#5d646c;--line:#d8d3c7;--accent:#d2491f;--accent2:#1d5fa8;
 --pos:#1f9d63;--neg:#d64545;--prev:#2f6fd6;--gest:#ffcf33;--soft:#fbece5;--grey:#ecebe6;--okbg:#e4f3ea;--badbg:#fdeaea;--blue:#e3eefa;--ok:#1f7a4d;--bad:#c62828}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15171a;--card:#1f2226;--ink:#eceef0;--muted:#a0a6ad;--line:#3e4348;--accent:#ff8a5c;--accent2:#7db4ec;
 --pos:#47c58a;--neg:#ff7b7b;--prev:#6fa3ff;--soft:#3a2a23;--grey:#2a2d31;--okbg:#1f3329;--badbg:#3a2222;--blue:#1f2d3d;--ok:#6cc59a;--bad:#ff8080}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.75 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",Pretendard,sans-serif}
.wrap{max-width:1060px;margin:0 auto;padding:28px 18px 120px}
h1{font-size:34px;line-height:1.25;margin:6px 0 6px}.sub{color:var(--muted);margin:0 0 20px;font-size:17px}
.nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);margin:0 -18px 26px;padding:10px 18px;display:flex;gap:8px;flex-wrap:wrap;font-size:15px}
.nav a{color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--card);border-radius:999px;padding:3px 13px;white-space:nowrap}
.nav a:hover{border-color:var(--accent);color:var(--accent)}
.group{font-size:15px;font-weight:700;letter-spacing:.04em;color:var(--accent);margin:46px 0 12px;text-transform:none}
.legend{display:flex;flex-wrap:wrap;gap:14px 22px;font-size:15px;color:var(--muted);margin:0 0 6px}
.dot{display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:-2px;margin-right:6px}
section.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px 26px 22px;margin:0 0 26px}
section.card h2{font-size:26px;line-height:1.3;margin:0 0 6px}
.q{color:var(--muted);font-size:16px;margin:0 0 16px}
.tag{display:inline-block;border-radius:999px;padding:1px 11px;font-size:14px;font-weight:700;margin-right:6px}
.t-code{background:var(--okbg);color:var(--ok)}.t-run{background:var(--blue);color:var(--accent2)}.t-paper{background:#efe6fa;color:#6b3fa0}.t-guess{background:#fbf0d4;color:#8a6100}
.fig{width:100%;height:auto;display:block;margin:6px 0}.fig text{font-family:inherit;fill:var(--ink)}
.fig .t{font-size:19px}.fig .tb{font-size:20px;font-weight:700}.fig .ts{font-size:16px;fill:var(--muted)}.fig .h{font-size:21px;font-weight:800}
.fig .box{fill:var(--card);stroke:var(--ink);stroke-width:1.6}.fig .soft{fill:var(--grey);stroke:var(--line)}
.fig .ln{stroke:var(--accent);stroke-width:2.5;fill:none}.fig .arr{stroke:var(--ink);stroke-width:2.6;fill:none}
.fig .hl{fill:none;stroke:var(--accent);stroke-width:3}.fig .lab{fill:var(--card);stroke:var(--accent);stroke-width:2}
.fig .n{fill:var(--accent)}.fig .nt{fill:#fff;font-size:17px;font-weight:700;text-anchor:middle}
.fig .okf{fill:var(--okbg);stroke:var(--ok);stroke-width:1.6}.fig .badf{fill:var(--badbg);stroke:var(--bad);stroke-width:1.6}
.fig .okt{fill:var(--ok);font-weight:700}.fig .badt{fill:var(--bad);font-weight:700}.fig .photo{stroke:var(--line)}
.fig .cell{fill:var(--card);stroke:var(--line);stroke-width:1}
.steps{counter-reset:s;list-style:none;padding:0;margin:14px 0 4px;display:grid;gap:10px}
.steps li{counter-increment:s;display:grid;grid-template-columns:38px 1fr;gap:12px;align-items:start}
.steps li:before{content:counter(s);width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;font-weight:800;display:grid;place-items:center;font-size:17px}
.steps b{font-weight:800}
table.sum{width:100%;border-collapse:collapse;margin:14px 0 4px;font-size:16.5px}
table.sum th{width:150px;text-align:left;color:var(--muted);font-weight:700;padding:8px 10px;border-top:1px solid var(--line);vertical-align:top}
table.sum td{padding:8px 10px;border-top:1px solid var(--line)}
.take{background:var(--soft);border-left:5px solid var(--accent);border-radius:8px;padding:12px 16px;margin:16px 0 4px;font-weight:700;font-size:19px}
.foot{color:var(--muted);font-size:14.5px;margin-top:14px}.foot a{color:var(--accent2)}
details{margin-top:10px;font-size:15px;color:var(--muted)}pre{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:12px;overflow-x:auto;font-size:13px;color:var(--ink)}
.refs{font-size:15px;color:var(--muted);border-top:1px solid var(--line);margin-top:40px;padding-top:14px}.refs li{margin:4px 0}.refs a{color:var(--accent2)}
@media (max-width:640px){body{font-size:17px}section.card{padding:18px 14px}.nav{font-size:14px}}
"""

# ------------------------------------------------------------------ shared drawing helpers
def mock_slice(x, y, w, h, gesture="", uid="a"):
    """Dark CT-like slice with a liver-shaped blob; gesture = svg drawn on top in --gest colour."""
    cx, cy = w * 0.5, h * 0.52
    return (f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="12" fill="#161616"/>'
            f'<path d="M{w*.12},{h*.5} C{w*.15},{h*.18} {w*.55},{h*.1} {w*.82},{h*.3} C{w*.95},{h*.45} {w*.8},{h*.78} {w*.5},{h*.84} C{w*.25},{h*.88} {w*.1},{h*.72} {w*.12},{h*.5}Z" fill="#8f8f8f"/>'
            f'<path d="M{w*.2},{h*.5} C{w*.25},{h*.3} {w*.5},{h*.22} {w*.72},{h*.34}" fill="none" stroke="#a9a9a9" stroke-width="5" opacity=".6"/>'
            f'{gesture}</g>')

def grid(x, y, cells, cell=36, rows=9, cols=9, cls="pos", labels=None, outline=None):
    """cells: {(r,c): value 0..1}. Draws a rows x cols grid; filled cells use var(--pos/neg/prev) with opacity=value."""
    o = []
    for r in range(rows):
        for c in range(cols):
            v = cells.get((r, c), 0)
            o.append(f'<rect class="cell" x="{x+c*cell}" y="{y+r*cell}" width="{cell}" height="{cell}"/>')
            if v > 0:
                o.append(f'<rect x="{x+c*cell}" y="{y+r*cell}" width="{cell}" height="{cell}" fill="var(--{cls})" fill-opacity="{max(v,.18):.2f}"/>')
                if labels:
                    txt = labels(v)
                    if txt:
                        o.append(f'<text x="{x+c*cell+cell/2}" y="{y+r*cell+cell/2+5}" text-anchor="middle" style="font-size:14px;font-weight:700;fill:{"#fff" if v>.55 else "var(--ink)"}">{txt}</text>')
    o.append(f'<rect x="{x}" y="{y}" width="{cols*cell}" height="{rows*cell}" fill="none" stroke="var(--ink)" stroke-width="1.8"/>')
    if outline: o.append(outline)
    return "\n".join(o)

CH = [("0", "직전 결과", "prev"), ("1", "상자·올가미 +", "pos"), ("2", "상자·올가미 −", "neg"),
      ("3", "점 +", "pos"), ("4", "점 −", "neg"), ("5", "붓 +", "pos"), ("6", "붓 −", "neg")]

def channel_col(x, y, active_pos, active_neg=None, w=236):
    """Vertical list of the 7 prompt channels, highlighting where this tool writes."""
    o = []
    for i, (n, name, kind) in enumerate(CH):
        yy = y + i * 40
        act = i in (active_pos, active_neg)
        col = f"var(--{kind})"
        o.append(f'<rect x="{x}" y="{yy}" width="{w}" height="34" rx="8" fill="{col}" fill-opacity="{.9 if act else .12}" stroke="{col}" stroke-width="{2.5 if act else 1}"/>')
        o.append(f'<text x="{x+14}" y="{yy+24}" style="font-size:17px;font-weight:{800 if act else 500};fill:{"#fff" if act else "var(--ink)"}">{n}  {name}</text>')
    return "\n".join(o)

def three_col(gesture, gridsvg, chan, cap1, cap2, cap3):
    return f"""<svg class="fig" viewBox="0 0 1000 440" role="img">{arrowdef()}
<text class="h" x="0" y="26">① 내가 하는 것</text>
{mock_slice(0,44,300,250,gesture)}
<text class="ts" x="0" y="326">{cap1[0]}</text><text class="ts" x="0" y="348">{cap1[1]}</text>
<path d="M312 170 H352" class="arr" marker-end="url(#ah2)"/>
<text class="h" x="366" y="26">② 만들어지는 숫자</text>
{gridsvg}
<text class="ts" x="366" y="396">{cap2[0]}</text><text class="ts" x="366" y="418">{cap2[1]}</text>
<path d="M702 170 H742" class="arr" marker-end="url(#ah2)"/>
<text class="h" x="756" y="26">③ 기록되는 채널</text>
{chan}
<text class="ts" x="756" y="346">{cap3[0]}</text><text class="ts" x="756" y="368">{cap3[1]}</text>
</svg>"""

def steps(items):
    return '<ol class="steps">' + "".join(f"<li><div>{t}</div></li>" for t in items) + "</ol>"

def table(rows):
    return '<table class="sum">' + "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows) + "</table>"

TAG = {"code": ("t-code", "코드로 확인"), "run": ("t-run", "실행으로 확인"), "paper": ("t-paper", "논문으로 확인"), "guess": ("t-guess", "추정")}

# ------------------------------------------------------------------ OVERVIEW POSTER
def icon(kind, x, y):
    g = {"point": '<circle cx="32" cy="32" r="9" fill="none" stroke="#ffcf33" stroke-width="5"/><circle cx="32" cy="32" r="3" fill="#ffcf33"/>',
         "box": '<rect x="12" y="16" width="40" height="32" fill="none" stroke="#ffcf33" stroke-width="5"/>',
         "scribble": '<path d="M10 40 C20 14 30 52 40 28 S50 20 56 24" fill="none" stroke="#ffcf33" stroke-width="6" stroke-linecap="round"/>',
         "lasso": '<path d="M14 36 C10 18 34 10 48 20 C58 30 46 50 30 50 C20 50 16 44 14 36Z" fill="none" stroke="#ffcf33" stroke-width="5" stroke-dasharray="2 8" stroke-linecap="round"/>'}[kind]
    return f'<g transform="translate({x},{y})"><rect width="64" height="64" rx="12" fill="#161616"/>{g}</g>'

def poster():
    o = [f'<svg class="fig" viewBox="-44 0 1088 900" role="img" aria-label="nnInteractive 한 판 정리">{arrowdef()}']
    # step 0
    o.append(f'{pill(0,0,1000,52,"soft")}<text class="tb" x="500" y="33" text-anchor="middle">⓪ 준비 — Initialize: CT를 서버에 한 번 올려 두고 세션을 만든다</text>')
    # step 1 tools
    o.append(f'{marker(1,14,92)}<text class="h" x="38" y="99">내가 하는 것 (2D 슬라이스 위에서)</text>')
    tools = [("point", "점 (Point)", "클릭한 한 곳"), ("box", "상자 (Box)", "상자 안쪽 전부"),
             ("scribble", "붓 (Scribble)", "붓이 지난 곳"), ("lasso", "올가미 (Lasso)", "닫은 선 안쪽")]
    for i, (k, nm, sub) in enumerate(tools):
        x = i * 255
        o.append(f'<rect class="box" x="{x}" y="118" width="235" height="168" rx="14"/>{icon(k, x+85, 132)}'
                 f'<text class="tb" x="{x+117}" y="236" text-anchor="middle">{nm}</text><text class="t" x="{x+117}" y="266" text-anchor="middle">{sub}</text>')
    o.append(f'<text class="t" x="0" y="318"><tspan style="fill:var(--pos);font-weight:800">Positive</tspan> = 여기를 포함해   ·   <tspan style="fill:var(--neg);font-weight:800">Negative</tspan> = 여기는 빼 줘   (모든 도구에 공통)</text>')
    o.append('<path d="M500 332 V366" class="arr" marker-end="url(#ah2)"/>')
    # step 2 channels
    o.append(f'{marker(2,14,398)}<text class="h" x="38" y="405">숫자 지도로 바꿔서 7개 채널에 기록</text>')
    for i, (n, name, kind) in enumerate(CH):
        x = i * 144
        sub = {"prev": "이전 예측", "pos": "+ 포함", "neg": "− 제외"}[kind]
        nm = name.replace(" +", "").replace(" −", "")
        o.append(f'<rect x="{x}" y="424" width="128" height="104" rx="12" fill="var(--{kind})" fill-opacity=".14" stroke="var(--{kind})" stroke-width="2.2"/>'
                 f'<circle cx="{x+22}" cy="448" r="14" fill="var(--{kind})"/><text class="nt" x="{x+22}" y="454">{n}</text>'
                 f'<text class="tb" x="{x+64}" y="494" text-anchor="middle" style="font-size:18px">{nm}</text><text class="ts" x="{x+64}" y="518" text-anchor="middle">{sub}</text>')
    o.append(f'<rect class="soft" x="0" y="542" width="1000" height="46" rx="10"/><text class="t" x="500" y="572" text-anchor="middle">+ CT 영상 (평균·표준편차로 정규화)  =  입력 <tspan style="font-weight:800">8채널</tspan></text>')
    o.append('<path d="M500 598 V632" class="arr" marker-end="url(#ah2)"/>')
    # step 3 model
    o.append(f'{marker(3,14,664)}<rect class="box" x="38" y="644" width="962" height="78" rx="14"/>'
             f'<text class="tb" x="60" y="676" style="font-size:22px">신경망 (ResEnc U-Net)</text><text class="t" x="60" y="706">마지막 입력 위치를 중심으로 192×192×192 복셀 조각을 잘라 한 번에 계산</text>')
    o.append('<path d="M500 730 V764" class="arr" marker-end="url(#ah2)"/>')
    # step 4 output + loop
    o.append(f'{marker(4,14,800)}<rect class="okf" x="38" y="778" width="470" height="78" rx="14"/>'
             f'<text class="tb" x="60" y="810" style="font-size:22px">간 마스크 (0 / 1)</text><text class="t" x="60" y="840">Slicer의 Liver 세그먼트에 칠해진다</text>')
    o.append(f'<rect class="lab" x="532" y="778" width="468" height="78" rx="14"/><text class="tb" x="552" y="808">⑤ 되먹임</text><text class="t" x="552" y="838">이 마스크가 다음 계산의 채널 0이 된다</text>')
    o.append('<path d="M532 817 H512" class="arr"/>')
    o.append('<path d="M-22 817 V476 H-4" class="arr" stroke="var(--prev)" marker-end="url(#ah)" style="stroke-dasharray:8 6"/><path d="M38 817 H-22" class="arr" stroke="var(--prev)" style="stroke-dasharray:8 6"/>')
    o.append(f'<text class="ts" x="0" y="886">+ 결과가 조각 테두리에 닿으면 자동으로 ×1.5씩 넓게 다시 본다 (최대 ×4) — 아래 \'AutoZoom\' 참고</text>')
    o.append('</svg>')
    return "\n".join(o)

# ------------------------------------------------------------------ TOOL PANELS
def liver_gesture_point():
    return '<circle cx="150" cy="120" r="14" fill="none" stroke="#ffcf33" stroke-width="5"/><circle cx="150" cy="120" r="3.5" fill="#ffcf33"/>'

def panel_point():
    cells = {(r, c): v for r, row in enumerate(POINT) for c, v in enumerate(row) if v > 0}
    g = grid(366, 44, cells, 36, labels=lambda v: f"{v:.1f}")
    return three_col(liver_gesture_point(), g, channel_col(756, 44, 3, 4),
                     ("클릭 한 번. 3D 위치라서", "앞뒤 슬라이스에도 값이 생김"),
                     ("한 슬라이스 단면 (실제 값). 가운데 1.0,", "가장자리로 갈수록 약해지는 공 모양"),
                     ("Positive → 채널 3", "Negative → 채널 4"))

def panel_box():
    cells = {(r, c): 1.0 for r in range(2, 7) for c in range(1, 8)}
    g = grid(366, 44, cells, 36, labels=lambda v: "1")
    ges = '<rect x="64" y="64" width="176" height="130" fill="none" stroke="#ffcf33" stroke-width="5"/>'
    return three_col(ges, g, channel_col(756, 44, 1, 2),
                     ("슬라이스 하나 위에 상자를 그림", "(그린 방향 두께 = 1칸)"),
                     ("상자 안쪽 전부 1, 바깥은 0", "(테두리만이 아니라 안쪽을 다 채움)"),
                     ("Positive → 채널 1", "Negative → 채널 2"))

def panel_scribble():
    path = [(6, 1), (5, 2), (5, 3), (4, 4), (4, 5), (3, 6), (3, 7)]
    cells = {}
    for r, c in path:
        cells[(r, c)] = 1.0; cells[(r + 1, c)] = 1.0
    g = grid(366, 44, cells, 36, labels=lambda v: "1")
    ges = '<path d="M60 170 C90 90 130 190 170 110 S220 80 244 96" fill="none" stroke="#ffcf33" stroke-width="9" stroke-linecap="round"/>'
    return three_col(ges, g, channel_col(756, 44, 5, 6),
                     ("붓으로 칠함. 모델이 선호하는", "붓 굵기는 2칸 (모델 설정값)"),
                     ("붓이 새로 지나간 칸만 1", "(이전에 칠한 칸은 다시 보내지 않음)"),
                     ("Positive → 채널 5", "Negative → 채널 6"))

def poly_cells(poly, rows=9, cols=9):
    def inside(px, py):
        n = len(poly); ins = False; j = n - 1
        for i in range(n):
            xi, yi = poly[i]; xj, yj = poly[j]
            if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi: ins = not ins
            j = i
        return ins
    return {(r, c): 1.0 for r in range(rows) for c in range(cols) if inside(c + .5, r + .5)}

def panel_lasso():
    poly = [(1.2, 3.2), (2.6, 1.2), (5.8, 1.6), (7.6, 3.6), (7.0, 6.6), (4.2, 7.6), (1.8, 6.2)]
    cells = poly_cells(poly)
    pts = " ".join(f"{366+x*36},{44+y*36}" for x, y in poly)
    g = grid(366, 44, cells, 36, labels=lambda v: "1", outline=f'<polygon points="{pts}" fill="none" stroke="var(--accent)" stroke-width="3" stroke-dasharray="6 5"/>')
    ges = '<path d="M62 120 C60 60 140 40 210 70 C264 100 240 176 160 190 C100 198 66 170 62 120Z" fill="none" stroke="#ffcf33" stroke-width="5" stroke-dasharray="3 9" stroke-linecap="round"/>'
    return three_col(ges, g, channel_col(756, 44, 1, 2),
                     ("마우스를 누른 채 한 바퀴 돌려", "닫힌 선을 그림 (축·관상·시상면만)"),
                     ("닫힌 선 안쪽을 다각형으로 채워 1", "(skimage의 polygon 채우기)"),
                     ("Positive → 채널 1", "Negative → 채널 2"))

def panel_prev():
    liver = poly_cells([(1.0, 3.0), (3.0, 1.0), (6.5, 1.5), (8.0, 4.0), (6.5, 7.5), (3.0, 7.5), (1.5, 5.5)])
    g = grid(366, 44, liver, 36, cls="prev", labels=lambda v: "1")
    ges = ('<path d="M40 150 C50 70 150 40 230 80 C270 120 230 190 150 200 C80 205 44 190 40 150Z" fill="#2f6fd6" fill-opacity=".55" stroke="#2f6fd6" stroke-width="4"/>')
    return three_col(ges, g, channel_col(756, 44, 0, None),
                     ("앞 단계의 예측 마스크, 또는", "내가 직접 칠해 둔 세그먼트"),
                     ("마스크 안쪽 = 1", "(약해지지 않는 0/1 값)"),
                     ("항상 채널 0", "새 예측마다 덮어씀"))

# ------------------------------------------------------------------ ENGINE FIGURES
def fig_input():
    o = [f'<svg class="fig" viewBox="0 0 1000 470" role="img">{arrowdef()}']
    o.append('<text class="h" x="0" y="26">① 전체 CT에서 한 조각을 잘라낸다</text>')
    o.append('<rect x="0" y="48" width="340" height="250" rx="10" fill="#161616"/><path d="M40 170 C50 90 150 70 230 100 C300 130 280 220 190 250 C110 275 40 240 40 170Z" fill="#8f8f8f"/>')
    o.append('<rect x="120" y="96" width="150" height="150" fill="none" stroke="#ffcf33" stroke-width="4" stroke-dasharray="8 6"/><circle cx="195" cy="171" r="6" fill="#ffcf33"/>')
    o.append('<text class="ts" x="0" y="326">전체 CT (예: 512×512×172)</text>')
    o.append('<text class="t" x="0" y="352" style="font-weight:700">노란 점선 = 192×192×192 복셀 조각</text>')
    o.append('<text class="ts" x="0" y="376">중심 = 마지막으로 넣은 입력의 위치</text>')
    o.append('<path d="M350 170 H398" class="arr" marker-end="url(#ah2)"/>')
    o.append('<text class="h" x="410" y="26">② 8장을 겹쳐 입력</text>')
    labels = [("CT 영상", "var(--ct,#888)", None), ("0 직전 결과", "var(--prev)", None), ("1·2 상자·올가미 ±", "var(--pos)", None), ("3·4 점 ±", "var(--pos)", None), ("5·6 붓 ±", "var(--pos)", None)]
    ys = 52
    sl = [("CT 영상 (1장)", "#8a8f96"), ("0  직전 결과", "var(--prev)"), ("1  상자·올가미 +", "var(--pos)"), ("2  상자·올가미 −", "var(--neg)"),
          ("3  점 +", "var(--pos)"), ("4  점 −", "var(--neg)"), ("5  붓 +", "var(--pos)"), ("6  붓 −", "var(--neg)")]
    for i, (t, col) in enumerate(sl):
        y = ys + i * 34
        o.append(f'<rect x="{410+i*6}" y="{y}" width="150" height="26" rx="5" fill="{col}" fill-opacity=".85"/>')
        o.append(f'<text x="{580+i*6}" y="{y+20}" style="font-size:17px">{t}</text>')
    o.append('<text class="ts" x="410" y="352">각 장 = 192×192×192 숫자 지도</text>')
    o.append('<path d="M410 372 H410" class="arr"/>')
    o.append('<path d="M770 170 H808" class="arr" marker-end="url(#ah2)"/>')
    o.append('<rect class="box" x="814" y="96" width="186" height="150" rx="12"/><text class="tb" x="907" y="140" text-anchor="middle">ResEnc</text><text class="tb" x="907" y="166" text-anchor="middle">U-Net</text><text class="ts" x="907" y="196" text-anchor="middle">nnU-Net 계열</text><text class="ts" x="907" y="220" text-anchor="middle">8채널 입력</text>')
    o.append('<path d="M907 252 V300" class="arr" marker-end="url(#ah2)"/>')
    o.append('<rect class="okf" x="814" y="306" width="186" height="64" rx="12"/><text class="tb okt" x="907" y="336" text-anchor="middle">마스크 조각</text><text class="ts" x="907" y="358" text-anchor="middle">배경 0 / 간 1</text>')
    o.append('<rect class="soft" x="0" y="404" width="1000" height="56" rx="10"/><text class="t" x="16" y="438">③ 마스크 조각을 전체 CT 자리에 붙이고, 같은 값을 채널 0에도 저장 → 다음 계산의 \'직전 결과\'</text>')
    o.append('</svg>')
    return "\n".join(o)

def fig_autozoom():
    o = [f'<svg class="fig" viewBox="0 0 1000 470" role="img">{arrowdef()}']
    o.append('<rect x="0" y="0" width="470" height="440" rx="12" fill="#161616"/>')
    o.append('<path d="M70 230 C60 120 200 40 330 80 C430 120 420 280 320 350 C220 410 80 360 70 230Z" fill="#8f8f8f"/>')
    sizes = [(1, 150, "var(--gest)", "6 5"), (1.5, 225, "#ff9f43", None), (2.25, 330, "#ff6b6b", None), (3.4, 440, "#c77dff", None)]
    for k, s, col, dash in sizes:
        x = 235 - s / 2; y = 220 - s / 2
        o.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="3.5"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
        o.append(f'<text x="{x+6}" y="{y+22}" style="font-size:17px;font-weight:800;fill:{col}">×{k}</text>')
    o.append('<circle cx="235" cy="220" r="6" fill="#fff"/>')
    o.append('<text class="ts" x="0" y="462">흰 점 = 클릭 위치,  사각형 = 모델이 한 번에 보는 범위</text>')
    steps_txt = [("1", "처음엔 ×1 (192³ 복셀)로 계산"), ("2", "결과 마스크가 조각 테두리에"), ("", "닿았나? 닿았으면 간이 더 크다는 뜻"),
                 ("3", "범위를 ×1.5 넓혀 다시 계산"), ("4", "테두리에 안 닿으면 멈춤 (최대 ×4)"),
                 ("5", "넓게 본 거친 결과 중 바뀐 부분만"), ("", "192³ 조각으로 나눠 다시 다듬음")]
    y = 36
    for n, t in steps_txt:
        if n: o.append(marker(n, 506, y - 5))
        o.append(f'<text class="t" x="534" y="{y}">{t}</text>')
        y += 38
    o.append('<rect class="soft" x="494" y="312" width="506" height="128" rx="12"/><text class="tb" x="512" y="344">왜 필요한가</text><text class="t" x="512" y="374">간처럼 큰 장기는 192 복셀 한 조각에 다 안 들어간다.</text><text class="t" x="512" y="404">그래서 넓게 한 번 훑고, 필요한 곳만 정밀하게 다시 본다.</text>')
    o.append('</svg>')
    return "\n".join(o)

def fig_decay():
    o = [f'<svg class="fig" viewBox="0 0 1000 330" role="img">{arrowdef()}']
    o.append('<text class="h" x="0" y="26">입력을 여러 번 넣을 때 — 오래된 입력일수록 조금씩 약해진다</text>')
    vals = [("가장 오래된", 0.98 ** 4), ("", 0.98 ** 3), ("", 0.98 ** 2), ("", 0.98), ("가장 최근", 1.0)]
    for i, (lab, v) in enumerate(vals):
        x = 60 + i * 100; h = 200 * v
        o.append(f'<rect x="{x}" y="{270-h}" width="64" height="{h}" rx="6" fill="var(--accent)" fill-opacity="{.35+.65*v:.2f}"/>')
        o.append(f'<text x="{x+32}" y="{262-h}" text-anchor="middle" style="font-size:17px;font-weight:700">{v:.2f}</text>')
        if lab: o.append(f'<text class="ts" x="{x+32}" y="298" text-anchor="middle">{lab}</text>')
    o.append('<text class="t" x="590" y="86">매번 새 입력은 이전 것의 <tspan style="font-weight:800">1/0.98배</tspan>로 크게</text><text class="t" x="590" y="116">써 넣는다 → 상대적으로 옛 입력이</text><text class="t" x="590" y="146">0.98배씩 약해지는 효과.</text>')
    o.append('<rect class="soft" x="590" y="176" width="410" height="102" rx="10"/><text class="ts" x="606" y="204">이 모델 파일의 설정(코드 기본값): 0.98</text><text class="ts" x="606" y="228">논문에는 0.9로 적혀 있음 → 값이 다름</text><text class="ts" x="606" y="252">(어느 쪽이 실제 학습값인지는 확인 못 함)</text>')
    o.append('</svg>')
    return "\n".join(o)

# ------------------------------------------------------------------ SECTIONS
def card(id, title, q, tags, body, take=None, foot=None):
    tg = "".join(f'<span class="tag {TAG[t][0]}">{TAG[t][1]}</span>' for t in tags)
    return (f'<section class="card" id="{id}"><h2>{title}</h2><div class="q">{tg}{q}</div>{body}'
            + (f'<div class="take">{take}</div>' if take else "") + (f'<div class="foot">{foot}</div>' if foot else "") + '</section>')

SRC_CODE = "근거: nnInteractive/inference/inference_session.py · interaction/point.py, SlicerNNInteractive.py"
GROUPS = [
 ("A  한 판 정리", [
  ("overview", "nnInteractive는 어떻게 계산하나 — 한 장 요약", "클릭 → 숫자 지도 → 신경망 → 마스크 → 되먹임", ["code", "paper"],
   poster(), "내가 한 입력은 '숫자 지도'로 바뀌어 CT와 함께 신경망에 들어가고, 결과는 다시 다음 계산의 입력이 된다",
   "근거: 코드(위 파일들) + 논문 <a href=\"https://arxiv.org/abs/2503.08373\">arXiv 2503.08373</a>"),
 ]),
 ("B  도구별 계산 방법", [
  ("point", "점 (Point)", "클릭한 곳 둘레에 '공 모양' 숫자 덩어리를 만든다", ["code", "paper"],
   panel_point() + steps(["클릭한 위치를 3D 복셀 좌표로 바꾼다.", "반지름 <b>4칸</b>의 공(9×9×9)을 만들고, 가운데 1.0에서 가장자리로 갈수록 작아지게 한다 (거리 변환 후 최대값 1로 정규화).",
                          "그 공을 채널 3(Positive) 또는 4(Negative)에 <b>더 큰 값만 남기며</b> 덮어쓴다.", "클릭 위치를 중심으로 192³ 조각을 잘라 ×1 확대로 신경망에 넣는다."])
   + table([("만드는 값", "공 257칸, 가운데 1.0 → 가장자리 약 0.2~0.3"), ("쓰는 채널", "3 (Positive) / 4 (Negative)"), ("예측 중심 · 확대", "클릭 위치 · ×1 (결과가 테두리에 닿으면 자동 확대)")]),
   "한 번의 클릭은 '작은 공'일 뿐이고, 간 전체로 퍼지는 건 신경망이 한다", SRC_CODE),
  ("box", "상자 (Bounding Box)", "상자 안쪽을 통째로 1로 채운다", ["code"],
   panel_box() + steps(["슬라이스 위에서 두 모서리를 찍는다. 그린 방향의 두께는 1칸이라 '2D 상자'가 된다 (모델이 2D 상자를 더 잘한다고 코드에 적혀 있음).",
                        "상자 안쪽 모든 복셀을 채널 1(Positive) 또는 2(Negative)에 현재 세기로 채운다.",
                        "상자 중심을 예측 중심으로 삼고, 상자 크기 + 64칸 여유가 192보다 크면 그만큼 <b>넓게</b> 본다 (확대 = max(1, (상자+64)/192))."])
   + table([("만드는 값", "상자 안쪽 전부 1 (두께 1칸)"), ("쓰는 채널", "1 (Positive) / 2 (Negative) — 올가미와 공유"), ("예측 중심 · 확대", "상자 중심 · 상자가 크면 ×1보다 크게")]),
   "상자는 '이 안에 대상이 있다'는 강한 힌트다", SRC_CODE),
  ("scribble", "붓 (Scribble)", "붓이 새로 지나간 칸만 1로 기록한다", ["code"],
   panel_scribble() + steps(["Slicer의 임시 세그먼트에 붓으로 칠한다.", "칠하기 전·후 마스크를 비교해 <b>새로 칠해진 칸</b>만 잘라낸다 (작은 조각 + 위치만 서버로 전송).",
                              "그 조각을 채널 5(Positive) 또는 6(Negative)에 더 큰 값만 남기며 쓴다.", "넓게 볼 때(확대 &gt;1) 점·붓 채널은 먼저 <b>굵게</b> 만든 뒤 줄여서, 얇은 선이 평균에 묻혀 사라지지 않게 한다."])
   + table([("만드는 값", "붓이 지난 칸 = 1"), ("쓰는 채널", "5 (Positive) / 6 (Negative)"), ("예측 중심 · 확대", "칠한 영역의 중심 · 칠한 영역이 크면 확대")]),
   "붓은 '여기가 대상이야 / 아니야'를 여러 칸에 걸쳐 알려 준다", SRC_CODE),
  ("lasso", "올가미 (Lasso)", "그린 닫힌 선 안쪽을 다각형으로 채운다", ["code", "paper"],
   panel_lasso() + steps(["한 슬라이스 위에서 마우스를 누른 채 한 바퀴 돈다 (축·관상·시상면만 가능, 비스듬한 단면은 불가).", "선의 점들을 화면 좌표 → 환자 좌표 → 복셀 좌표로 바꾼다.",
                           "닫힌 다각형 안쪽을 채워 1로 만든다 (두께 1칸).", "채널 1(Positive) 또는 2(Negative)에 쓰고, 상자와 같은 규칙으로 예측 중심·확대를 정한다."])
   + table([("만드는 값", "선 안쪽 전부 1 (두께 1칸)"), ("쓰는 채널", "1 (Positive) / 2 (Negative) — 상자와 공유"), ("예측 중심 · 확대", "채운 영역의 중심 · 영역이 크면 확대")]),
   "올가미는 상자보다 대상 모양에 가깝게 알려 줄 수 있다", SRC_CODE + " · 논문: 올가미는 이 모델이 새로 도입한 입력"),
  ("prev", "기존 마스크 (직전 결과 · 초기 세그먼트)", "채널 0 — 계산 결과가 다음 계산으로 돌아가는 통로", ["code"],
   panel_prev() + steps(["새 예측이 끝나면 그 마스크가 채널 0에 저장된다.", "Slicer에서 이미 그려 둔 세그먼트가 있으면, Initialize 때 그 마스크를 채널 0에 넣고 시작한다 (이때는 예측을 돌리지 않고 채널 0에만 기록하며, <b>이전 입력은 모두 지워진다</b>).",
                          "다음 입력을 더할 때 신경망은 '직전 결과'를 함께 보고 틀린 부분만 고친다."])
   + table([("값", "0 / 1 (다른 입력과 달리 시간이 지나도 약해지지 않음)"), ("채널", "0")]),
   "클릭을 더할수록 결과가 조금씩 다듬어지는 이유가 이 채널이다", SRC_CODE),
 ]),
 ("C  모든 도구가 공유하는 계산", [
  ("engine", "신경망 입력 만들기", "CT 조각 + 숫자 지도 7장 = 8채널", ["code", "paper"],
   fig_input() + table([("모델", "ResEnc U-Net (nnU-Net 계열), 이 체크포인트 설정 3d_fullres_ps192 — 조각 크기 192×192×192"), ("CT 정규화", "0이 아닌 영역의 평균·표준편차로 z-점수 (간격은 그대로 두고 복셀 단위로만 계산)"), ("출력", "배경/대상 2종류 → 큰 쪽을 골라 0/1 마스크")]),
   "신경망은 '지금 CT 조각'과 '내가 넣은 입력'을 8장 겹쳐 한 번에 읽는다", SRC_CODE),
  ("autozoom", "AutoZoom — 큰 장기를 놓치지 않게 넓게 보기", "결과가 조각 테두리에 닿으면 범위를 넓혀 다시 계산", ["code", "paper"],
   fig_autozoom(), "간은 한 조각보다 커서, 넓게 훑은 뒤 필요한 곳만 정밀하게 다시 본다", SRC_CODE + " (MAX_AUTOZOOM_FACTOR = 4, 확대 비율 1.5) · 논문과 일치"),
  ("decay", "입력이 쌓일 때의 가중치 (decay)", "최근 입력이 더 세게 반영된다", ["code", "paper"],
   fig_decay(), "오래된 입력일수록 조금씩 영향이 줄어든다", SRC_CODE),
 ]),
 ("D  사용 준비 · 서버 (앞서 설명한 내용)", [
  ("s1", "도구 버튼이 회색인 이유", "Initialize 전에는 잠겨 있다", ["code"], P.S1, "Initialize를 아직 안 눌러서 잠겨 있는 것입니다 (고장 아님)"),
  ("s2", "Initialize를 누르면 일어나는 일", "Remote 모드 기준", ["code", "run"], P.S2, "서버에 세션을 만들고, CT를 한 번 올려 두는 단계입니다"),
  ("s3", "왜 Initialize를 먼저 해야 하나", "CT를 매번 보내지 않으려는 구조", ["code", "guess"], P.S3, "모델이 \"어느 CT인지\" 기억한 채 클릭을 쌓아 가기 때문입니다"),
  ("s4", "Remote와 Local", "왜 서버를 따로 쓰나", ["code", "run"], P.S4, "이 Mac에서는 Slicer 안 계산이 실패해서 서버(Remote)를 씁니다"),
  ("s5", "서버를 켤 때 꼭 필요한 설정", "MPS 폴백", ["run"], P.S5, "PYTORCH_ENABLE_MPS_FALLBACK=1 이 없으면 첫 클릭에서 500 오류가 납니다"),
 ]),
]

REFS = [("nnInteractive 논문 (arXiv 2503.08373)", "https://arxiv.org/abs/2503.08373"),
        ("nnInteractive 공식 코드 (MIC-DKFZ)", "https://github.com/MIC-DKFZ/nnInteractive"),
        ("SlicerNNInteractive 확장", "https://github.com/coendevente/SlicerNNInteractive"),
        ("디자인 참고: The Illustrated Transformer — 큰 그림 먼저, 단계 번호, 색 일관성, 구체 예시 먼저", "https://jalammar.github.io/illustrated-transformer/"),
        ("디자인 참고: 주석 달린 스크린샷 가이드 (Nielsen Norman Group 인용 정리)", "https://www.docsie.io/blog/glossary/annotated-screenshots/")]

nav = "".join(f'<a href="#{items[0][0]}">{g}</a>' for g, items in GROUPS)
body = []
for g, items in GROUPS:
    body.append(f'<div class="group">{g}</div>')
    for it in items:
        body.append(card(*it))
refs = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in REFS)
html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>nnInteractive 이해하기</title><style>{CSS}</style></head><body><div class="wrap">
<h1>nnInteractive 이해하기</h1><p class="sub">클릭이 어떻게 3D 간 마스크가 되는지, 도구별 계산 방법을 그림으로 정리합니다. 새 설명이 나올 때마다 카드가 추가됩니다.</p>
<div class="legend"><span><span class="dot" style="background:var(--pos)"></span>Positive (포함)</span><span><span class="dot" style="background:var(--neg)"></span>Negative (제외)</span><span><span class="dot" style="background:var(--prev)"></span>직전 결과</span><span><span class="dot" style="background:var(--gest)"></span>내가 한 동작</span></div>
<div class="legend" style="margin-top:6px"><span><span class="tag t-code">코드로 확인</span></span><span><span class="tag t-paper">논문으로 확인</span></span><span><span class="tag t-run">실행으로 확인</span></span><span><span class="tag t-guess">추정</span></span></div>
<nav class="nav">{nav}</nav>
<!-- SECTIONS:START -->
{"".join(body)}
<!-- SECTIONS:END -->
<div class="refs"><b>참고한 자료</b><ul>{refs}</ul></div>
</div></body></html>'''
(D / "index.html").write_text(html, encoding="utf-8")
print("ok", len(html))
