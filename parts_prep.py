# Builds index.html. Add new sections to SECTIONS (and TOC) — each is one annotated diagram.
import base64, pathlib
D = pathlib.Path(__file__).parent
def img(name): return "data:image/jpeg;base64," + base64.b64encode((D/"images"/name).read_bytes()).decode()

CSS = """
:root{--bg:#f6f5f1;--card:#fff;--ink:#1f2328;--muted:#656d76;--line:#d9d5cb;--accent:#d2491f;--accent2:#1d5fa8;--ok:#1f7a4d;--bad:#c62828;--soft:#fbece5;--okbg:#e4f3ea;--badbg:#fdeaea;--blue:#e3eefa;--grey:#ecebe6}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#17181a;--card:#202225;--ink:#ececec;--muted:#9aa0a6;--line:#44474c;--accent:#ff8a5c;--accent2:#7db4ec;--ok:#6cc59a;--bad:#ff8080;--soft:#3a2a23;--okbg:#1f3329;--badbg:#3a2222;--blue:#1f2d3d;--grey:#2a2c2f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",Pretendard,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:28px 16px 96px}h1{font-size:30px;margin:0 0 4px}.sub{color:var(--muted);margin:0 0 18px}
nav.toc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 18px;margin-bottom:22px}nav.toc ol{margin:6px 0 0;padding-left:22px}nav.toc a{color:var(--ink)}
.legend{font-size:13px;color:var(--muted);margin:0 0 18px}.tag{display:inline-block;border-radius:999px;padding:1px 10px;font-size:13px;font-weight:700;margin-right:4px}
.t-code{background:var(--okbg);color:var(--ok)}.t-run{background:var(--blue);color:var(--accent2)}.t-guess{background:#fbf0d4;color:#8a6100}
section.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 18px 14px;margin-bottom:22px}
section.card h2{font-size:23px;margin:0 0 4px}.q{color:var(--muted);font-size:15px;margin:0 0 12px}
.fig{width:100%;height:auto;display:block}.fig text{font-family:inherit;fill:var(--ink)}
.fig .t{font-size:17px}.fig .tb{font-size:18px;font-weight:700}.fig .ts{font-size:14px;fill:var(--muted)}
.fig .box{fill:var(--card);stroke:var(--ink);stroke-width:1.5}.fig .soft{fill:var(--grey);stroke:var(--line)}
.fig .ln{stroke:var(--accent);stroke-width:2.5;fill:none}.fig .arr{stroke:var(--ink);stroke-width:2.5;fill:none}
.fig .hl{fill:none;stroke:var(--accent);stroke-width:3}.fig .lab{fill:var(--card);stroke:var(--accent);stroke-width:2}
.fig .n{fill:var(--accent)}.fig .nt{fill:#fff;font-size:16px;font-weight:700;text-anchor:middle}
.fig .okf{fill:var(--okbg);stroke:var(--ok);stroke-width:1.5}.fig .badf{fill:var(--badbg);stroke:var(--bad);stroke-width:1.5}
.fig .okt{fill:var(--ok);font-weight:700}.fig .badt{fill:var(--bad);font-weight:700}
.fig .photo{stroke:var(--line)}
.take{background:var(--soft);border-left:4px solid var(--accent);border-radius:6px;padding:10px 14px;margin:14px 0 2px;font-weight:700;font-size:18px}
details{margin-top:8px;font-size:14px;color:var(--muted)}pre{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px;overflow-x:auto;font-size:12px;color:var(--ink)}
"""

def marker(n,x,y): return f'<circle class="n" cx="{x}" cy="{y}" r="14"/><text class="nt" x="{x}" y="{y+5}">{n}</text>'
def arrowdef(): return '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="24" markerHeight="24" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>'

# ---- annotated screenshot helper: photo on left (W x H frame), labels on right ----
def shot(imgname, W, H, items, alt, right=980, f=1.0):
    # items: (n, rect(x,y,w,h), label_lines, label_y)
    total = W + right + 60
    out = [f'<svg class="fig" viewBox="0 0 {total} {H}" role="img" aria-label="{alt}">{arrowdef()}',
           f'<image class="photo" href="{img(imgname)}" x="0" y="0" width="{W}" height="{H}"/>']
    for n,(x,y,w,h),lines,ly in items:
        out.append(f'<rect class="hl" x="{x}" y="{y}" width="{w}" height="{h}" rx="8" vector-effect="non-scaling-stroke"/>')
        out.append(f'<line class="ln" x1="{x+w}" y1="{y+h/2}" x2="{W+40}" y2="{ly+34}" vector-effect="non-scaling-stroke"/>')
        bh = int((62*len(lines)+30)*f)
        out.append(f'<rect class="lab" x="{W+40}" y="{ly}" width="{right}" height="{bh}" rx="12" vector-effect="non-scaling-stroke"/>')
        out.append(f'<circle class="n" cx="{W+84}" cy="{ly+bh/2}" r="{30*f}"/><text class="nt" style="font-size:{36*f}px" x="{W+84}" y="{ly+bh/2+13*f}">{n}</text>')
        for i,l in enumerate(lines):
            wt = 'tb' if i==0 else 't'
            out.append(f'<text style="font-size:{(52 if i==0 else 44)*f}px;{"font-weight:700" if i==0 else ""}" x="{W+135*f+20}" y="{ly+52*f+i*62*f}">{l}</text>')
    out.append('</svg>'); return "\n".join(out)

S1 = shot("panel_before_init.jpg", 600, 877, [
  (1,(34,208,523,50),["Initialize (Remote)","여기를 눌러야 시작"],100),
  (2,(60,262,470,26),["Status: not initialized","아직 서버와 연결 안 됨"],250),
  (3,(31,406,531,44),["Positive / Negative","회색 = 지금은 잠김"],410),
  (4,(31,498,531,176),["점·박스·낙서·올가미","전부 회색 = 못 누름"],560),
], "Initialize 전 화면 주석", right=640, f=0.6)


def pill(x,y,w,h,cls="lab"): return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
# ---- Section 2: initialize flow ----
S2 = f"""<svg class="fig" viewBox="0 0 760 570" role="img" aria-label="Initialize 흐름">{arrowdef()}
<rect class="box" x="10" y="20" width="210" height="500" rx="14"/><text class="tb" x="115" y="52" text-anchor="middle">Slicer</text>
<rect class="soft" x="30" y="80" width="170" height="74" rx="8"/><text class="tb" x="115" y="112" text-anchor="middle">간 CT</text><text class="ts" x="115" y="136" text-anchor="middle">512×512×172</text>
<rect class="badf" x="30" y="380" width="170" height="110" rx="8"/><text class="tb" x="115" y="412" text-anchor="middle">도구 버튼</text><text class="badt" x="115" y="446" text-anchor="middle" style="font-size:17px">🔒 잠김</text><text class="ts" x="115" y="472" text-anchor="middle">③ 이후 🔓 켜짐</text>
<rect class="box" x="540" y="20" width="210" height="500" rx="14"/><text class="tb" x="645" y="52" text-anchor="middle">서버</text>
<rect class="soft" x="560" y="80" width="170" height="74" rx="8"/><text class="tb" x="645" y="112" text-anchor="middle">모델</text><text class="ts" x="645" y="136" text-anchor="middle">이미 로드됨</text>
<rect class="okf" x="560" y="190" width="170" height="130" rx="8"/><text class="tb" x="645" y="222" text-anchor="middle">세션</text><text class="t" x="645" y="248" text-anchor="middle">(이 CT 전용)</text><text class="ts" x="645" y="278" text-anchor="middle">CT 사본 +</text><text class="ts" x="645" y="298" text-anchor="middle">클릭 기록 보관</text>
<line class="arr" x1="222" y1="116" x2="538" y2="116" marker-end="url(#ah)"/>
{pill(238,84,284,64)}{marker(1,262,116)}<text class="tb" x="396" y="110" text-anchor="middle">세션 만들어 줘</text><text class="ts" x="396" y="132" text-anchor="middle">127.0.0.1:1527 접속</text>
<line class="arr" x1="538" y1="176" x2="222" y2="176" marker-end="url(#ah)" stroke-dasharray="7 6"/>
<text class="ts" x="380" y="168" text-anchor="middle">사용 가능한 도구 · 라이선스 응답</text>
<line class="arr" x1="222" y1="262" x2="538" y2="262" marker-end="url(#ah2)" style="stroke-width:6"/>
{pill(238,226,284,72)}{marker(2,262,262)}<text class="tb" x="396" y="256" text-anchor="middle">CT 한 번 전송</text><text class="ts" x="396" y="280" text-anchor="middle">가장 오래 걸리는 단계</text>
<line class="arr" x1="538" y1="430" x2="222" y2="430" marker-end="url(#ah)"/>
{pill(238,396,284,68)}{marker(3,262,430)}<text class="tb" x="396" y="424" text-anchor="middle">준비 끝</text><text class="ts" x="396" y="448" text-anchor="middle">initialized (remote)</text>
<text class="ts" x="380" y="552" text-anchor="middle">걸린 시간: 6.7초 (서버를 막 켠 직후 첫 호출은 34.8초)</text>
</svg>"""

# ---- Section 3: why initialize ----
def block(x,y,w=70,h=36): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="var(--accent2)" opacity=".9"/><text x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle" style="fill:#fff;font-size:16px;font-weight:700">CT</text>'
def dot(x,y): return f'<circle cx="{x}" cy="{y}" r="8" fill="var(--accent)"/>'
S3 = f"""<svg class="fig" viewBox="0 0 760 610" role="img" aria-label="Initialize가 필요한 이유">{arrowdef()}
<text class="tb" x="10" y="26">A. Initialize 없이 매번 보낸다면 (비교용 가정)</text>
<rect class="soft" x="10" y="40" width="740" height="190" rx="10"/>
<text class="t" x="24" y="96">클릭 1</text>{block(100,76)}<line class="arr" x1="178" y1="94" x2="735" y2="94" marker-end="url(#ah)"/>
<text class="t" x="24" y="152">클릭 2</text>{block(100,132)}<line class="arr" x1="178" y1="150" x2="735" y2="150" marker-end="url(#ah)"/>
<text class="t" x="24" y="208">클릭 3</text>{block(100,188)}<line class="arr" x1="178" y1="206" x2="735" y2="206" marker-end="url(#ah)"/>
{pill(10,242,740,48,"badf")}<text class="badt" x="380" y="273" text-anchor="middle" style="font-size:17px">클릭할 때마다 큰 CT를 또 보냄 → 느림</text>
<text class="tb" x="10" y="338">B. 실제 방식: Initialize에서 CT를 한 번만 올림</text>
<rect class="soft" x="10" y="352" width="740" height="190" rx="10"/>
<text class="t" x="24" y="414">Initialize</text>{block(128,394)}<line class="arr" x1="206" y1="412" x2="735" y2="412" marker-end="url(#ah2)" style="stroke-width:6"/>
<text class="t" x="24" y="470">클릭 1</text>{dot(150,466)}<line class="arr" x1="162" y1="466" x2="735" y2="466" marker-end="url(#ah)"/>
<text class="t" x="24" y="522">클릭 2</text>{dot(150,518)}<line class="arr" x1="162" y1="518" x2="735" y2="518" marker-end="url(#ah)"/>
{pill(10,554,740,48,"okf")}<text class="okt" x="380" y="585" text-anchor="middle" style="font-size:17px">이후엔 클릭 좌표만 보냄 (서버가 CT를 이미 가짐)</text>
</svg>"""

# ---- Section 4: remote vs local ----
S4 = f"""<svg class="fig" viewBox="0 0 760 570" role="img" aria-label="Local과 Remote 비교">{arrowdef()}
<text class="tb" x="10" y="26">Local: Slicer 안에서 직접 계산</text>
<rect class="box" x="10" y="40" width="740" height="210" rx="12"/><text class="tb" x="30" y="72">Slicer 프로그램</text>
<rect class="badf" x="30" y="90" width="700" height="140" rx="8"/>{marker(1,52,112)}
<text class="t" x="80" y="118">Slicer 안의 PyTorch 2.2.2</text><text class="ts" x="80" y="140">Intel Mac용 마지막 버전 (Slicer가 Rosetta로 실행 중)</text>
<text class="badt" x="80" y="182" style="font-size:17px">✗ 필요한 연산이 없어 실패</text><text class="ts" x="80" y="206">upsample_nearest3d (Half 정밀도)</text>
<text class="tb" x="10" y="296">Remote: 따로 띄운 서버가 계산 (현재 사용)</text>
<rect class="box" x="10" y="310" width="200" height="200" rx="12"/><text class="tb" x="110" y="342" text-anchor="middle">Slicer</text><text class="t" x="110" y="410" text-anchor="middle">CT 보여주기</text><text class="t" x="110" y="438" text-anchor="middle">클릭 받기</text>
<line class="arr" x1="212" y1="394" x2="338" y2="394" marker-end="url(#ah)"/><text class="ts" x="275" y="384" text-anchor="middle">CT·클릭</text>
<line class="arr" x1="338" y1="450" x2="212" y2="450" marker-end="url(#ah)"/><text class="ts" x="275" y="440" text-anchor="middle">마스크</text>
<rect class="box" x="340" y="310" width="410" height="200" rx="12"/><text class="tb" x="360" y="342">서버</text>
<rect class="okf" x="360" y="358" width="370" height="132" rx="8"/>{marker(2,382,380)}
<text class="t" x="410" y="386">Apple 칩용 PyTorch 2.14</text><text class="ts" x="410" y="408">.venv-nni · Apple GPU(MPS) 사용</text><text class="okt" x="410" y="452" style="font-size:17px">✓ 계산 성공</text>
<text class="ts" x="10" y="548">※ 서버를 먼저 켜 둬야 Initialize가 성공합니다</text>
</svg>"""

# ---- Section 5: server setting ----
def col(x,hdr,c3cls,c3a,c3b,c4cls,c4t):
    return f"""<text class="tb" x="{x+160}" y="28" text-anchor="middle">{hdr}</text>
<rect class="box" x="{x}" y="50" width="320" height="56" rx="8"/><text class="t" x="{x+160}" y="85" text-anchor="middle">첫 클릭 도착</text>
<line class="arr" x1="{x+160}" y1="108" x2="{x+160}" y2="130" marker-end="url(#ah)"/>
<rect class="box" x="{x}" y="132" width="320" height="56" rx="8"/><text class="t" x="{x+160}" y="167" text-anchor="middle">Apple GPU(MPS)로 계산</text>
<line class="arr" x1="{x+160}" y1="190" x2="{x+160}" y2="212" marker-end="url(#ah)"/>
<rect class="{c3cls}" x="{x}" y="214" width="320" height="76" rx="8"/><text class="{'badt' if c3cls=='badf' else 't'}" x="{x+160}" y="246" text-anchor="middle" style="font-size:17px">{c3a}</text><text class="ts" x="{x+160}" y="270" text-anchor="middle">{c3b}</text>
<line class="arr" x1="{x+160}" y1="292" x2="{x+160}" y2="314" marker-end="url(#ah)"/>
<rect class="{c4cls}" x="{x}" y="316" width="320" height="56" rx="8"/><text class="{'badt' if c4cls=='badf' else 'okt'}" x="{x+160}" y="351" text-anchor="middle" style="font-size:17px">{c4t}</text>"""
S5 = f"""<svg class="fig" viewBox="0 0 760 500" role="img" aria-label="MPS 폴백 설정">{arrowdef()}
{col(30,"설정 없이 켠 서버","badf","✗ 연산 미지원","_adaptive_avg_pool3d (GPU에 없음)","badf","500 오류")}
{col(410,"FALLBACK=1 로 켠 서버","soft","그 연산만 CPU로 넘김","(폴백)","okf","✓ 분할 성공")}
{pill(10,404,740,84)}<text class="tb" x="30" y="436">대가: 속도 (클릭 약 46초 · 박스 약 26초)</text><text class="ts" x="30" y="462">서버는 이 Mac(127.0.0.1)에서만 접속되고 인증은 없음 · 모델 가중치는 비상업 라이선스</text>
</svg>"""

