"""Build the Misprint theme for T3 Code: misprint.json (+ the SVG plates under assets/svg).

Two inks (fluoro pink, teal) on cream stock. While a turn runs the plates slip out of
register; when it ends they snap back and overprint to a deep indigo.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
PINK = "#ff2e88"
TEAL = "#00a99d"
INK = "#141a45"       # close to the true pink x teal overprint (#001e53), lifted a touch for text
CREAM = "#f5eddb"
SIDE = "#efe4ca"
PAPER = "#fffaf0"
MONO = "ui-monospace,'SF Mono',Menlo,monospace"
HEAD = "Futura,'Avenir Next Condensed','Arial Narrow',system-ui,sans-serif"
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"


def f(x):
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


# ---------------------------------------------------------------- halftone
def halftone(shape, pitch, field, maxr=None):
    """Staggered 45-degree dot screen. shape(x,y)->bool, field(x,y)->0..1 (dot area)."""
    maxr = maxr or pitch * 0.36
    out = []
    ys = 0
    row = 0
    H = 700
    while ys < H:
        x = (pitch / 2) if row % 2 else 0
        while x < 320:
            if shape(x, ys):
                t = max(0.0, min(1.0, field(x, ys)))
                r = maxr * math.sqrt(t)
                if r > 0.7:
                    out.append(f"<circle cx='{round(x)}' cy='{round(ys)}' r='{round(r*2)/2:g}'/>")
            x += pitch
        ys += pitch / 2
        row += 1
    return "".join(out)


def target(cx, cy, r=18):
    return (f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='none' stroke-width='2'/>"
            f"<circle cx='{cx}' cy='{cy}' r='{r // 3}'/>"
            f"<path d='M{cx - r - 14} {cy}H{cx + r + 14}M{cx} {cy - r - 14}V{cy + r + 14}' stroke-width='2' fill='none'/>")


def svg(w, h, color, body, opacity=1):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'>"
            f"<g fill='{color}' stroke='{color}' stroke-width='0' opacity='{opacity}'>{body}</g></svg>")


def label(x, y, t, anchor="start"):
    return (f"<text x='{x}' y='{y}' text-anchor='{anchor}' stroke='none' style='font:700 10px ui-monospace,Menlo,monospace;letter-spacing:.16em'>{t}</text>")


def disc(cx, cy, R):
    return lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 <= R * R


def rect(x0, y0, x1, y1):
    return lambda x, y: x0 <= x <= x1 and y0 <= y <= y1


# gutter plates (300 x 620) ------------------------------------------------
def left_pink():
    sun = halftone(disc(150, 150, 132), 16, lambda x, y: max(.3, 1.05 - math.hypot(x - 105, y - 100) / 215))
    bars = "".join(f"<rect x='30' y='{338 + k * 19}' width='240' height='11' stroke='none'/>" for k in range(5))
    return svg(300, 620, PINK, sun + bars + target(150, 556) + label(30, 604, "PLATE 1 · PINK"))


def left_teal():
    ramp = halftone(rect(126, 170, 290, 372), 16, lambda x, y: (x - 126) / 164 * .55 + (y - 170) / 202 * .6 + .1)
    dot = "<circle cx='206' cy='408' r='50' stroke='none'/>"
    return svg(300, 620, TEAL, ramp + dot + target(150, 556) + label(270, 604, "PLATE 2 · TEAL", "end"))


def right_pink():
    stripes = "".join(f"<rect x='40' y='{136 + k * 26}' width='220' height='14' stroke='none'/>" for k in range(8))
    clip = "<clipPath id='c'><circle cx='150' cy='236' r='100'/></clipPath>"
    ramp = halftone(rect(30, 392, 270, 520), 16, lambda x, y: (x - 30) / 240 * 1.0 + .1)
    sq = "<rect x='206' y='566' width='40' height='40' stroke='none'/>"
    return svg(300, 620, PINK, clip + f"<g clip-path='url(%23c)'><g transform='rotate(-28 150 236)'>{stripes}</g></g>" + ramp + sq + target(150, 56))


def right_teal():
    ring = "<circle cx='150' cy='236' r='96' fill='none' stroke-width='16'/>"
    ramp = halftone(rect(30, 392, 270, 520), 16, lambda x, y: (270 - x) / 240 * 1.0 + .1)
    sq = "<rect x='226' y='584' width='40' height='40' stroke='none'/>"
    return svg(300, 620, TEAL, ring + ramp + sq + target(150, 56))


# sidebar-foot plates (200 x 150) -----------------------------------------------
def small_pink():
    sun = halftone(disc(78, 76, 60), 11, lambda x, y: max(.3, 1.05 - math.hypot(x - 58, y - 56) / 100))
    return svg(200, 150, PINK, sun + target(168, 36, 12))


def small_teal():
    ramp = halftone(rect(70, 40, 190, 140), 11, lambda x, y: (x - 70) / 120 * .6 + (y - 40) / 100 * .6 + .1)
    return svg(200, 150, TEAL, ramp + target(168, 36, 12))


# narrow-dock strips (240 x 112, shown at 120 x 56): a short halftone ramp and a registration target per ink
def strip_pink(op=1):
    ramp = halftone(rect(8, 8, 150, 104), 11, lambda x, y: (x - 8) / 142 * 1.0 + .1)
    return svg(240, 112, PINK, ramp + target(196, 56, 16), op)


def strip_teal(op=1):
    ramp = halftone(rect(70, 8, 212, 104), 11, lambda x, y: (212 - x) / 142 * .9 + .1)
    return svg(240, 112, TEAL, ramp + target(196, 56, 16), op)


def data_uri(s):
    out = s.replace("%23", "\0").replace("%", "%25").replace("#", "%23").replace('"', "'").replace("<", "%3C").replace("\0", "%23")
    return 'url("data:image/svg+xml,' + out + '")'


GRAIN_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n' x='0' y='0' width='100%' height='100%'>"
             "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
             "<feColorMatrix values='0 0 0 0 .15 0 0 0 0 .1 0 0 0 0 .25 0 0 0 1.5 -.62'/></filter>"
             "<rect width='240' height='240' filter='url(%23n)' opacity='.3'/></svg>")

# ---------------------------------------------------------------- colours
colors = {
    "canvas": CREAM, "chrome": SIDE, "toolbar": CREAM, "toolbarForeground": INK,
    "toolbarBorder": "#d5c8a5", "toolbarControl": "#ebe0c3", "toolbarControlForeground": INK,
    "toolbarControlHover": "#e2d5b0", "surface": PAPER, "surfaceRaised": "#fffcf4", "surfaceOverlay": "#fffcf4",
    "text": INK, "textMuted": "#5a4a72", "border": "#d5c8a5", "input": "#8f82a6", "focus": "#00877f",
    "accent": PINK, "accentForeground": INK, "secondary": "#e9dfc1", "secondaryForeground": INK,
    "muted": "#e9dfc1", "mutedForeground": "#5a4a72", "placeholder": "#6e6086", "secondaryLabel": "#5a4a72",
    "iconMuted": "#66577e", "error": "#b3261e", "errorForeground": "#8c1812", "errorSurface": "#fbd8cd",
    "warning": "#9a5b00", "warningForeground": "#6b3f00", "warningSurface": "#f9e3a8",
    "update": "#007a73", "updateForeground": "#00504c", "updateSurface": "#c9ece6",
    "accentSurface": "#ffd0e4", "accentSurfaceForeground": "#5e0a33",
    "messageSurface": "#ffd6e7", "messageForeground": INK, "messageAction": PINK,
    "messageActionForeground": INK, "messageActionHover": "#ff5aa3",
    "codeBackground": "#fbf7ea", "codeForeground": INK,
    "searchMatchBackground": "#ffd0e4", "searchMatchForeground": INK,
    "searchMatchActiveBackground": PINK, "searchMatchActiveForeground": INK,
    "sidebar": SIDE, "sidebarForeground": INK, "sidebarMutedForeground": "#5a4a72",
    "sidebarControlSurface": PAPER, "sidebarRowHover": "#e6d9b6", "sidebarRowActive": "#ffc7de",
    "sidebarRowSelected": "#ffc2dc", "sidebarBorder": "#cdbf9a",
    "terminalBackground": "#fbf7ea", "terminalForeground": INK, "terminalCursor": PINK,
    "terminalSelection": "#b9e8e1", "terminalScrollbar": "#cdbf9a", "terminalScrollbarHover": TEAL,
}

CW = "var(--chat-content-max-width,46rem)"
G = f"(100% - {CW})/2"          # one gutter beside the reading column


def gutter_size(threshold=200, maxw=300):
    """Plate width: full size when there is room, shrinks with the gutter, vanishes below `threshold`."""
    return f"min({maxw}px,clamp(0px,({G} - {threshold}px)*1000,{G} - 48px)) auto"


BUSY = ('body:has([data-timeline-row-kind="working"])',
        'body:has([data-thread-item] [aria-busy="true"][aria-current]:not([aria-current="false"]))')


def busy(sel):
    return ",".join(f"{b} {sel}" for b in BUSY)


PLATE_A = "[data-workspace-area=\"conversation\"]::before"
PLATE_B = "[data-workspace-area=\"conversation\"]::after"
SB_A = "[data-slot=\"sidebar-inner\"]::before"
SB_B = "[data-slot=\"sidebar-inner\"]::after"
GRAIN = "var(--ms-grain)"
DASH = lambda c: f"repeating-linear-gradient(90deg,{c} 0 8px,transparent 8px 16px)"

SB_BG = "radial-gradient(ellipse 100% 135% at 50% 0%,rgba(239,228,202,.95) 0,rgba(239,228,202,.9) 40%,rgba(239,228,202,0) 100%)"
INKA = lambda a: f"rgba(20,26,69,{a})"
BTN = ("[data-slot=\"button\"]:not(:where([data-chat-header] *,.composer-tiptap *))")
css = (
    "@property --jx{syntax:'<number>';inherits:false;initial-value:0}"
    "@property --jy{syntax:'<number>';inherits:false;initial-value:0}"
    "@property --set{syntax:'<number>';inherits:false;initial-value:1}"
    "@property --amt{syntax:'<length>';inherits:false;initial-value:0px}"
    "@property --hs{syntax:'<length>';inherits:false;initial-value:0px}"
    "@property --rh{syntax:'<length>';inherits:false;initial-value:3px}"
    ":root{--ms-grain:" + data_uri(GRAIN_SVG) + ";--ms-lp:" + data_uri(left_pink()) + ";--ms-lt:" + data_uri(left_teal())
    + ";--ms-rp:" + data_uri(right_pink()) + ";--ms-rt:" + data_uri(right_teal())
    + ";--ms-sp:" + data_uri(strip_pink()) + ";--ms-st:" + data_uri(strip_teal(.3)) + "}"
    # the press: a jitter clock. Holds are the ink sitting slipped; the 2% hops are the clack between them.
    "@keyframes ms-jit{0%,6%{--jx:0;--jy:0}8%,22%{--jx:1;--jy:-.55}24%,38%{--jx:-.6;--jy:.9}40%,52%{--jx:.35;--jy:.25}"
    "54%,70%{--jx:-1;--jy:-.7}72%,86%{--jx:.7;--jy:.6}88%,100%{--jx:0;--jy:0}}"
    # strong hit at turn start, then the slip settles to ~40% and holds there for as long as the turn runs
    "@keyframes ms-settle{0%,12%{--set:1}100%{--set:.4}}"
    # one-shot at turn end: the header rule thickens once, like a registration pin seating
    "@keyframes ms-done{0%{--rh:3px}25%{--rh:7px}100%{--rh:3px}}"
    "@keyframes ms-march{to{background-position:16px 100%,-16px 100%}}"
    # --- stock: cream paper with grain, and two ink plates in the gutters
    f"[data-workspace-area=\"conversation\"]{{position:relative;isolation:isolate;background:{GRAIN},{CREAM}!important}}"
    f"{PLATE_A},{PLATE_B}{{content:\"\";position:absolute;inset:0;z-index:-1;pointer-events:none;mix-blend-mode:multiply;"
    "background-repeat:no-repeat;--amt:0px;transition:--amt .6s cubic-bezier(.2,1.9,.35,1);"
    "animation:ms-jit 4.5s ease-out infinite paused;will-change:transform}"
    f"{PLATE_A}{{background-image:var(--ms-lp),var(--ms-rp);background-position:left 24px top 64px,right 24px top 64px;"
    f"background-size:{gutter_size()},{gutter_size()};"
    "transform:translate(calc(var(--jx)*var(--amt)*var(--set)),calc(var(--jy)*var(--amt)*var(--set)))}"
    f"{PLATE_B}{{background-image:var(--ms-lt),var(--ms-rt);background-position:left 24px top 64px,right 24px top 64px;"
    f"background-size:{gutter_size()},{gutter_size()};"
    "transform:translate(calc(var(--jx)*var(--amt)*var(--set)*-1),calc(var(--jy)*var(--amt)*var(--set)*-1))}"
    + busy(PLATE_A) + "," + busy(PLATE_B) + "{--amt:10px;animation:ms-jit 4.5s ease-out infinite running,ms-settle 7s ease-out forwards;transition:--amt .25s ease-out}"
    # --- header: a dashed rule printed in both inks; the inks drift apart while working
    f"[data-chat-header]{{--hs:0px;background-color:{CREAM}!important;background-image:{DASH(PINK)},{DASH(TEAL)}!important;"
    "background-repeat:repeat-x!important;background-size:16px var(--rh)!important;background-blend-mode:multiply;"
    "background-position:calc(var(--jx)*var(--hs)*var(--set)) 100%,calc(var(--jx)*var(--hs)*var(--set)*-1) 100%!important;"
    "transition:--hs .6s cubic-bezier(.2,1.9,.35,1);animation:ms-jit 4.5s ease-out infinite paused,ms-done 1s ease-out 1}"
    + busy("[data-chat-header]") + "{--hs:7px;animation:ms-jit 4.5s ease-out infinite running,ms-settle 7s ease-out forwards;transition:--hs .25s ease-out}"
    # --- sidebar: mono-feeling poster face, an overprinted open row, and a hover rule painted above the row fill
    f"[data-slot=\"sidebar-inner\"]{{position:relative;isolation:isolate;background:{GRAIN},{SIDE}!important;font-family:{HEAD};letter-spacing:.02em}}"
    f"{SB_A},{SB_B}{{display:none}}"
    f"[data-thread-item]{{position:relative}}"
    f"[data-thread-item]::after{{content:\"\";position:absolute;left:8px;right:8px;bottom:1px;height:2px;pointer-events:none;"
    f"background-image:linear-gradient({PINK},{PINK}),linear-gradient({TEAL},{TEAL});background-repeat:no-repeat;"
    "background-size:0 2px,0 2px;background-position:left bottom,right bottom;background-blend-mode:multiply;"
    "transition:background-size .4s cubic-bezier(.2,.7,.2,1)}"
    "[data-thread-item]:hover::after{background-size:60% 2px,60% 2px}"
    "[data-thread-item]:has([aria-busy=\"true\"])::after{background-size:0 2px,0 2px!important}"
    f"[data-thread-item] [aria-current]:not([aria-current=\"false\"]){{box-shadow:inset 3px 0 0 {PINK},inset 5px 0 0 {TEAL};"
    f"background-image:{DASH(PINK)},{DASH(TEAL)};background-size:16px 2px,16px 2px;background-repeat:repeat-x;"
    "background-position:0 100%,8px calc(100% - 1px);background-blend-mode:multiply}"
    "[data-thread-item] [role=\"button\"]{border-radius:3px!important}"
    f"[data-slot=\"project-monogram\"]{{background:{PINK}!important;color:{INK}!important;border:1.5px solid {INK}!important;border-radius:2px!important;box-shadow:2px 2px 0 {TEAL};font-family:{MONO};font-weight:700}}"
    # busy thread rows + the live Working row: two dashed rules marching in opposite directions
    "[data-timeline-row-kind=\"working\"],[data-thread-item] [aria-busy=\"true\"]{"
    f"background-image:{DASH(PINK)},{DASH(TEAL)}!important;background-size:16px 2px,16px 2px!important;background-repeat:repeat-x!important;"
    "background-position:0 100%,0 100%;background-blend-mode:multiply;animation:ms-march 1.5s steps(6) infinite}"
    # the live row's text is itself a bad print: ghosts of each ink slip around it (small, so the label stays legible)
    f"[data-timeline-row-kind=\"working\"]{{--amt:.7px;animation:ms-jit 4.5s ease-out infinite,ms-march 1.5s steps(6) infinite;"
    f"text-shadow:calc(var(--jx)*var(--amt)) calc(var(--jy)*var(--amt)) 0 {PINK},calc(var(--jx)*var(--amt)*-1) calc(var(--jy)*var(--amt)*-1) 0 {TEAL}}}"
    f"[data-timeline-row-kind=\"work\"]{{font-family:{MONO};font-size:.92em;box-shadow:inset 2px 0 0 {TEAL};padding-left:.6em}}"
    # --- conversation surfaces
    f"[data-user-message-bubble]{{background:#ffd6e7!important;border:1.5px solid {INK}!important;border-radius:3px!important;box-shadow:3px 3px 0 {TEAL}}}"
    f".chat-markdown{{font-family:{SERIF}}}"
    f".chat-markdown :is(h1,h2,h3,h4){{font-family:{HEAD};font-weight:800;text-transform:uppercase;letter-spacing:.04em;color:{INK}}}"
    f".chat-markdown :is(h1,h2){{text-shadow:1.5px 1.5px 0 {TEAL}}}"
    ".chat-markdown :is(h1,h2,h3,h4) code{text-transform:none}"
    f".chat-markdown :is(h1,h2){{border-bottom:3px double {INK};padding-bottom:.15em}}"
    f".chat-markdown a{{color:#00665f!important;text-decoration:underline {PINK} 2px;text-underline-offset:3px}}"
    f".chat-markdown :not(pre)>code{{font-family:{MONO};background:#ffe0ee;color:{INK};padding:.05em .3em;border-radius:2px;border:1px solid {INKA(.35)}}}"
    f".chat-markdown-codeblock,.chat-markdown-codeblock code{{font-family:{MONO}}}"
    f".chat-markdown-codeblock{{background:#fbf7ea!important;border:1.5px solid {INK}!important;border-radius:3px!important;box-shadow:4px 4px 0 {TEAL}}}"
    f".chat-markdown blockquote{{border-left:4px solid {PINK};box-shadow:-4px 0 0 {TEAL};padding-left:.9em}}"
    f".chat-markdown table{{border-collapse:collapse}}"
    f".chat-markdown th{{font-family:{MONO};font-size:.8em;text-transform:uppercase;letter-spacing:.1em;text-align:left;border-bottom:3px double {INK}}}"
    f".chat-markdown td{{border-bottom:1px dashed {INKA(.4)}}}"
    f".chat-markdown hr{{border:0;height:4px;background-image:{DASH(PINK)},{DASH(TEAL)};background-size:16px 2px,16px 2px;"
    "background-repeat:repeat-x;background-position:0 0,5px 2px;background-blend-mode:multiply}"
    f".chat-markdown ul>li::marker{{content:\"\\25A0  \";color:{PINK};font-size:.8em}}"
    f".chat-markdown ol>li::marker{{font-family:{MONO};font-weight:700;color:#00877f}}"
    # composer: one ink on the plate at rest, both inks once you're typing
    f"[data-slot=\"composer-host\"]{{background:{PAPER}!important;border:1.5px solid {INK}!important;border-radius:4px!important;"
    f"box-shadow:3px 3px 0 {PINK},0 0 0 0 {TEAL};transition:box-shadow .3s cubic-bezier(.2,.9,.3,1.4)}}"
    f"[data-slot=\"composer-host\"]:focus-within{{box-shadow:3px 3px 0 {PINK},-3px -3px 0 {TEAL}}}"
    f".composer-tiptap{{font-family:{SERIF};font-size:1.02em;caret-color:{PINK}}}"
    "[data-slot=\"composer-host\"] :focus-visible,.composer-tiptap:focus-visible{outline:none!important}"
    # --- controls: a printed label with a hard teal offset that collapses when pressed
    f"{BTN}{{border:1.5px solid {INK}!important;border-radius:3px!important;box-shadow:2px 2px 0 {TEAL};transition:transform .08s,box-shadow .08s}}"
    f"{BTN}:hover{{box-shadow:3px 3px 0 {TEAL}}}"
    f"{BTN}:active{{transform:translate(2px,2px);box-shadow:0 0 0 {TEAL}}}"
    f"[data-slot=\"button\"]:focus-visible{{outline:2px solid #00877f;outline-offset:2px}}"
    f"[data-slot=\"input\"],[data-slot=\"select-trigger\"]{{border:1.5px solid {INK}!important;border-radius:3px!important;box-shadow:2px 2px 0 {TEAL};background:{PAPER}!important}}"
    f"[data-slot=\"input\"]:focus-visible,[data-slot=\"select-trigger\"]:focus-visible{{outline:none;box-shadow:2px 2px 0 {PINK},-2px -2px 0 {TEAL}}}"
    f"[data-slot=\"switch\"]{{border:1.5px solid {INK}!important;border-radius:2px!important;background:#e9dfc1!important}}"
    f"[data-slot=\"switch\"][aria-checked=\"true\"]{{background:{PINK}!important}}"
    f"[data-slot=\"switch\"]>span{{background:{INK}!important;border-radius:1px!important}}"
    f"[data-slot=\"switch\"]:focus-visible{{outline:2px solid #00877f;outline-offset:2px}}"
    f"[data-slot=\"dialog-popup\"],[data-slot=\"popover-popup\"],[data-slot=\"menu-popup\"]{{border:1.5px solid {INK}!important;border-radius:4px!important;box-shadow:5px 5px 0 {TEAL}!important}}"
    f"[data-slot=\"tooltip-popup\"]{{background:{INK}!important;color:{PAPER}!important;border-radius:2px!important;box-shadow:2px 2px 0 {PINK}!important}}"
    f"[data-thread-details-card]{{border:1.5px solid {INK}!important;border-radius:4px!important;box-shadow:4px 4px 0 {PINK}}}"
    f"[data-thread-terminal-drawer]{{border-top:2px solid {INK}!important}}"
    f"[data-settings-page-scroll]{{background:{GRAIN},{CREAM}!important}}"
    f":focus-visible{{outline:2px solid #00877f;outline-offset:2px}}"
    f"::selection{{background:#ffa3c9;color:{INK}}}"
    f"::-webkit-scrollbar-track,[data-slot=\"scroll-area-scrollbar\"]{{background:{INKA(.05)}!important;border-left:1px dashed {INKA(.25)}}}"
    f"::-webkit-scrollbar-thumb,[data-slot=\"scroll-area-thumb\"]{{background:{INKA(.35)}!important;border-radius:0!important;border:1px solid {INK}}}"
    f"::-webkit-scrollbar-thumb:hover,[data-slot=\"scroll-area-thumb\"]:hover{{background:{PINK}!important}}"
    "svg.lucide{stroke-width:2.2;stroke-linecap:square;stroke-linejoin:miter}"
    # --- narrow windows: no gutters. A small two-ink strip docks at the sidebar foot, faint, under a sidebar-coloured scrim.
    # The teal plate is a static background layer; the pink plate slips above it; the scrim (::after) sits over both and under the rows' text.
    "@media (max-width:1459px){"
    f"{PLATE_A},{PLATE_B}{{display:none}}"
    f"[data-slot=\"sidebar-inner\"]{{background:var(--ms-st) center bottom 48px/120px 56px no-repeat,{GRAIN},{SIDE}!important}}"
    f"{SB_A},{SB_B}{{display:block;content:\"\";position:absolute;left:50%;bottom:48px;margin-left:-60px;z-index:-1;pointer-events:none}}"
    f"{SB_A}{{width:120px;height:56px;mix-blend-mode:multiply;background:var(--ms-sp) center/contain no-repeat;opacity:.3;"
    "--amt:0px;transition:--amt .6s cubic-bezier(.2,1.9,.35,1);animation:ms-jit 4.5s ease-out infinite paused;"
    "transform:translate(calc(var(--jx)*var(--amt)*var(--set)),calc(var(--jy)*var(--amt)*var(--set)))}"
    f"{SB_B}{{width:180px;margin-left:-90px;height:72px;background:{SB_BG}}}"
    + busy(SB_A) + "{--amt:5px;animation:ms-jit 4.5s ease-out infinite running,ms-settle 7s ease-out forwards;transition:--amt .25s ease-out}}"
    # --- reduced motion: frozen, registered, still good-looking
    "@media (prefers-reduced-motion:reduce){"
    f"{PLATE_A},{PLATE_B},{SB_A},{SB_B},[data-chat-header],[data-thread-item],[data-thread-item]::after,[data-thread-item] [aria-busy],[data-timeline-row-kind],[data-slot=\"composer-host\"],[data-slot=\"button\"]{{"
    "animation:none!important;transition:none!important;--amt:0px!important;--hs:0px!important}"
    "[data-timeline-row-kind=\"working\"]{text-shadow:1px 0 " + PINK + ",-1px 0 " + TEAL + "}}"
)

theme = {"version": 1, "id": "misprint", "name": "Misprint", "appearance": "light", "accent": PINK, "canvas": CREAM,
         "colors": colors, "css": css}

if __name__ == "__main__":
    with open(os.path.join(HERE, "..", "misprint.json"), "w") as fh:
        json.dump(theme, fh, ensure_ascii=False)
    print("css chars:", len(css))
    os.makedirs(os.path.join(HERE, "..", "assets", "svg"), exist_ok=True)
    for n, s in (("left-pink", left_pink()), ("left-teal", left_teal()), ("right-pink", right_pink()),
                 ("right-teal", right_teal()), ("strip-pink", strip_pink()), ("strip-teal", strip_teal())):
        with open(os.path.join(HERE, "..", "assets", "svg", f"{n}.svg"), "w") as fh:
            fh.write(s.replace("%23", "#"))
