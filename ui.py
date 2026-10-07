"""Habillage visuel et composants HTML réutilisables."""
from __future__ import annotations

import html

import streamlit as st

CSS = """
<style>
:root{--yellow:#FFE600;--ink:#1A1A24;--ink2:#2E2E38;--muted:#6B6B76;--bg:#F4F4F0;--card:#FFFFFF;--line:#E3E3DC;--ok:#2E7D5B;--ko:#B3392F}
html, body, [data-testid="stAppViewContainer"], .stApp{background:var(--bg)!important;color:var(--ink)}
[data-testid="stHeader"]{background:transparent}
#MainMenu, footer{visibility:hidden}
.block-container{max-width:1180px;padding-top:1.4rem;padding-bottom:4rem}
[data-testid="stAppViewContainer"] .stMarkdown, [data-testid="stAppViewContainer"] .stMarkdown p,
[data-testid="stAppViewContainer"] .stMarkdown li, [data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] p, [data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2, [data-testid="stAppViewContainer"] h3, [data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] [data-testid="stMetricValue"], [data-testid="stAppViewContainer"] [data-testid="stMetricLabel"] p{color:var(--ink)!important}
[data-testid="stAppViewContainer"] .stMarkdown table{width:100%;border-collapse:collapse;font-size:.92rem;margin:.6rem 0}
[data-testid="stAppViewContainer"] .stMarkdown th{background:var(--ink);color:#fff!important;text-align:left;padding:8px 10px}
[data-testid="stAppViewContainer"] .stMarkdown td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink)!important}
[data-testid="stAppViewContainer"] .stMarkdown code{background:#EDEDE6;color:var(--ink)!important;padding:2px 5px;border-radius:4px}
[data-testid="stAppViewContainer"] .stMarkdown pre{background:var(--ink)!important;border-left:6px solid var(--yellow);border-radius:8px}
[data-testid="stAppViewContainer"] .stMarkdown pre code{background:transparent;color:#F5F5F0!important;font-size:.9rem}
[data-testid="stAppViewContainer"] blockquote{border-left:6px solid var(--yellow)!important;background:#fff;border-radius:6px;padding:10px 18px;margin:8px 0;opacity:1!important}
[data-testid="stAppViewContainer"] blockquote, [data-testid="stAppViewContainer"] blockquote *{color:var(--ink)!important}
[data-testid="stAppViewContainer"] blockquote p{font-size:1.15rem;font-weight:700;opacity:1!important}
[data-testid="stMain"] [data-baseweb="progress-bar"] > div > div{background-color:#E3E3DC!important;border-radius:6px}
[data-testid="stMain"] [data-baseweb="progress-bar"] > div > div > div{background-color:#F2C500!important;border-radius:6px}
[data-testid="stMain"] label[data-baseweb="radio"]:has(input:checked) > div:first-child{background-color:#1A1A24!important;border-color:#1A1A24!important}
[data-testid="stMain"] label[data-baseweb="checkbox"]:has(input:checked) > span:first-child{background-color:#1A1A24!important;border-color:#1A1A24!important}
[data-testid="stSidebar"]{background:var(--ink);border-right:6px solid var(--yellow)}
[data-testid="stSidebar"] *{color:#EDEDE8}
[data-testid="stSidebar"] .stMarkdown p{color:#BDBDB6}
[data-testid="stSidebar"] [role="radiogroup"]{gap:2px}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:9px 12px;border-radius:8px;border-left:4px solid transparent;width:100%;cursor:pointer}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:#ffffff14}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child{display:none}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:var(--yellow);border-left-color:#fff}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) *{color:var(--ink)!important;font-weight:700}
[data-testid="stSidebar"] .stButton button, [data-testid="stSidebar"] .stDownloadButton button{background:#2E2E38;border:1px solid #4a4a56;color:#fff}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section{background:#2E2E38;border:1px dashed #5a5a66}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button{background:#FFE600!important;color:#1A1A24!important;border:0;font-weight:800}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button *{color:#1A1A24!important}
[data-testid="stSidebar"] [data-testid="stFileUploader"] small{color:#A5A5AE!important}
.brand{display:flex;gap:12px;align-items:center;margin:2px 0 14px}
.brand .logo{width:42px;height:42px;background:var(--yellow);color:var(--ink);font-weight:900;font-size:22px;display:grid;place-items:center;clip-path:polygon(0 0,100% 0,100% 72%,72% 100%,0 100%)}
.brand b{display:block;color:#fff;font-size:1rem;line-height:1.1}.brand small{color:#A5A5AE}
.sb-progress{margin:6px 0 14px}.sb-progress .bar{height:6px;background:#3B3B46;border-radius:6px;overflow:hidden}
.sb-progress .bar i{display:block;height:100%;background:var(--yellow)}.sb-progress .lbl{display:flex;justify-content:space-between;font-size:.74rem;color:#A5A5AE;margin-top:5px}
.hero{display:grid;grid-template-columns:1fr auto;gap:24px;background:linear-gradient(120deg,#1A1A24 0%,#2E2E38 100%);color:#fff;border-radius:16px;padding:28px 32px;position:relative;overflow:hidden;margin-bottom:18px}
.hero:before{content:"";position:absolute;left:0;top:0;bottom:0;width:8px;background:var(--yellow)}
.hero > *{position:relative;z-index:2}
.hero .eyebrow{font-size:.7rem;letter-spacing:.2em;color:var(--yellow);font-weight:800;margin-bottom:8px}
.hero h1{color:#fff!important;font-size:2rem;line-height:1.15;margin:0 0 8px;padding:0}
[data-testid="stAppViewContainer"] .hero p{color:#D9D9D2!important;margin:0;max-width:680px;line-height:1.55}
[data-testid="stAppViewContainer"] .hero h1{color:#fff!important}
.hero .chips{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap}
.chip{background:#ffffff1c;border:1px solid #ffffff33;color:#fff;border-radius:999px;padding:4px 11px;font-size:.76rem;font-weight:600}
.chip.y{background:var(--yellow);color:var(--ink);border-color:var(--yellow)}
.hero-side{text-align:center;min-width:190px;align-self:center;background:var(--yellow);border-radius:12px;padding:16px 22px}
.hero-side .v{font-size:2.8rem;font-weight:900;color:var(--ink);line-height:1.05}
.hero-side .l{font-size:.68rem;letter-spacing:.14em;color:var(--ink);font-weight:800}
.hero-side .s{font-size:.78rem;color:var(--ink);font-weight:600;margin-top:2px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:6px 0 18px}
.stat{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--yellow);border-radius:10px;padding:14px 16px}
.stat .l{font-size:.68rem;letter-spacing:.12em;color:var(--muted);font-weight:800;text-transform:uppercase}
.stat .v{font-size:1.65rem;font-weight:800;color:var(--ink);margin-top:3px}
.stat .s{font-size:.78rem;color:var(--muted)}
.stepper{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:2px 0 14px}
.step{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;display:flex;gap:10px;align-items:center}
.step .dot{width:28px;height:28px;border-radius:50%;background:#E8E8E0;display:grid;place-items:center;font-weight:800;font-size:.8rem;color:var(--ink)}
.step.done{border-color:var(--ok)}.step.done .dot{background:var(--ok);color:#fff}
.step.active .dot{background:var(--yellow)}
.step b{display:block;font-size:.85rem;color:var(--ink)}.step small{color:var(--muted)}
.box{border-radius:10px;padding:14px 18px;margin:10px 0}
.box h4{margin:0 0 6px;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase}
.box ul{margin:0;padding-left:1.1rem}.box li{margin:3px 0;line-height:1.5}
.box.key{background:#FFF9C2;border-left:6px solid var(--yellow);color:var(--ink)}
.box.warn{background:#FBEAE8;border-left:6px solid var(--ko);color:var(--ink)}
.box.obj{background:#fff;border:1px solid var(--line);border-left:6px solid var(--ink);color:var(--ink)}
.box *{color:var(--ink)!important}
.sec-title{display:flex;align-items:center;gap:10px;margin:4px 0 6px}
.sec-title .n{background:var(--yellow);color:var(--ink);font-weight:900;border-radius:6px;padding:2px 9px}
.stTabs [data-baseweb="tab-list"]{gap:4px;border-bottom:2px solid var(--line)}
.stTabs [data-baseweb="tab"]{height:46px;padding:0 18px;font-weight:700;color:var(--muted)!important}
.stTabs [aria-selected="true"]{color:var(--ink)!important}
.stTabs [data-baseweb="tab-highlight"]{background-color:var(--yellow)!important;height:4px}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primaryFormSubmit"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"]{background:var(--yellow)!important;color:var(--ink)!important;border:1px solid var(--ink)!important;font-weight:800}
.stButton button, .stDownloadButton button{border-radius:8px;font-weight:700}
div[data-testid="stExpander"]{background:var(--card);border:1px solid var(--line);border-radius:10px}
div[data-testid="stExpander"] summary p{font-weight:700;color:var(--ink)!important}
div[data-testid="stMetric"]{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px}
@media(max-width:900px){.hero{grid-template-columns:1fr}.stats,.stepper{grid-template-columns:1fr 1fr}.hero-side{text-align:left}}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def esc(x) -> str:
    return html.escape(str(x))


def hero(eyebrow: str, title: str, subtitle: str, chips: list[str] | None = None,
         side_value: str | None = None, side_label: str = "", side_sub: str = "") -> None:
    chips_html = "".join(f'<span class="chip{" y" if i == 0 else ""}">{esc(c)}</span>' for i, c in enumerate(chips or []))
    side = (f'<div class="hero-side"><div class="l">{esc(side_label)}</div><div class="v">{esc(side_value)}</div>'
            f'<div class="s">{esc(side_sub)}</div></div>') if side_value is not None else "<div></div>"
    st.markdown(
        f'<div class="hero"><div><div class="eyebrow">{esc(eyebrow)}</div><h1>{esc(title)}</h1>'
        f'<p>{esc(subtitle)}</p><div class="chips">{chips_html}</div></div>{side}</div>',
        unsafe_allow_html=True)


def stats(items: list[tuple[str, str, str]]) -> None:
    cells = "".join(f'<div class="stat"><div class="l">{esc(l)}</div><div class="v">{esc(v)}</div><div class="s">{esc(s)}</div></div>'
                    for l, v, s in items)
    st.markdown(f'<div class="stats">{cells}</div>', unsafe_allow_html=True)


def stepper(steps: list[tuple[str, str, bool]]) -> None:
    out = ""
    first_todo = next((i for i, s in enumerate(steps) if not s[2]), -1)
    for i, (title, sub, done) in enumerate(steps):
        cls = "step done" if done else ("step active" if i == first_todo else "step")
        out += f'<div class="{cls}"><div class="dot">{"✓" if done else i + 1}</div><div><b>{esc(title)}</b><small>{esc(sub)}</small></div></div>'
    st.markdown(f'<div class="stepper">{out}</div>', unsafe_allow_html=True)


def box(kind: str, title: str, items: list[str]) -> None:
    lis = "".join(f"<li>{esc(i)}</li>" for i in items)
    st.markdown(f'<div class="box {kind}"><h4>{esc(title)}</h4><ul>{lis}</ul></div>', unsafe_allow_html=True)


def section_title(n: int, text: str) -> None:
    st.markdown(f'<div class="sec-title"><span class="n">{n}</span><h3 style="margin:0">{esc(text)}</h3></div>', unsafe_allow_html=True)


def sidebar_brand(pct: int, label: str) -> None:
    st.markdown(
        '<div class="brand"><div class="logo">A</div><div><b>Strategy &amp; M&amp;A Academy</b><small>Parcours Stratégie Groupe</small></div></div>'
        f'<div class="sb-progress"><div class="bar"><i style="width:{pct}%"></i></div>'
        f'<div class="lbl"><span>{esc(label)}</span><span>{pct}%</span></div></div>',
        unsafe_allow_html=True)


def md_table(rows: list[dict]) -> None:
    """Affiche une liste de dicts sous forme de tableau markdown stylé (sans colonne d'index)."""
    if not rows:
        return
    cols = list(rows[0].keys())
    head = "| " + " | ".join(cols) + " |\n|" + "|".join(["---"] * len(cols)) + "|\n"
    body = "".join("| " + " | ".join(str(r.get(c, "")).replace("|", "/").replace("\n", " ") for c in cols) + " |\n" for r in rows)
    st.markdown(head + body)
