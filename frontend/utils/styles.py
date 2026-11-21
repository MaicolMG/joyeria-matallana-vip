"""
Sistema de temas global — Oscuro (por defecto) y Claro elegante.
Cada vista llama tema() que detecta la preferencia de session_state.
"""
import streamlit as st

# ────────────────────────────────────────────────────────────────────
# PALETA OSCURA — Fondo casi negro, dorado D4AF37
# ────────────────────────────────────────────────────────────────────
_CSS_DARK = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');

/* ── Transición suave entre temas ─── */
*, html, body { transition: background-color .35s ease, color .25s ease, border-color .25s ease !important; }

:root {
  --gold:       #D4AF37;
  --gold-light: #F0D060;
  --gold-dark:  #9A7B1C;
  --bg:         #080808;
  --bg-2:       #111111;
  --bg-3:       #1a1a1a;
  --text:       #F5F0E8;
  --muted:      #9A9080;
  --border:     #252525;
}

html, body, [data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Montserrat', sans-serif !important;
}
*, *::before, *::after { box-sizing: border-box; }

.stMainBlockContainer { padding-top:28px !important; max-width:1280px !important; }
[data-testid="stHeader"] { background: rgba(8,8,8,.96) !important; border-bottom: 1px solid var(--border) !important; }
[data-testid="stHeader"] * { color: var(--text) !important; }

[data-testid="stSidebar"] { background: #060606 !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebarNav"] a { border-radius:3px !important; padding:8px 14px !important; font-size:.78rem !important; letter-spacing:.08em !important; transition: background .2s !important; }
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] a[aria-current="page"] { background: rgba(212,175,55,.12) !important; color: var(--gold) !important; }
[data-testid="stSidebarNavItems"] > div > span { font-size:.6rem !important; letter-spacing:.3em !important; color: #383828 !important; text-transform:uppercase !important; padding: 14px 14px 4px !important; }

h1 { font-family:'Cormorant Garamond',serif !important; color:var(--gold) !important; font-size:2.4rem !important; font-weight:400 !important; letter-spacing:.06em !important; }
h2 { font-family:'Cormorant Garamond',serif !important; color:var(--gold-light) !important; font-weight:300 !important; }
h3, h4 { color:var(--text) !important; }
p, li { color:var(--muted) !important; }

[data-testid="stButton"] > button { border-radius:0 !important; font-family:'Montserrat',sans-serif !important; letter-spacing:.12em !important; font-size:.72rem !important; text-transform:uppercase !important; transition: all .2s !important; }
[data-testid="stButton"] > button[kind="primary"] { background:linear-gradient(135deg,var(--gold-dark),var(--gold)) !important; color:#080808 !important; border:none !important; font-weight:600 !important; box-shadow:0 2px 16px rgba(212,175,55,.2) !important; }
[data-testid="stButton"] > button[kind="primary"]:hover { opacity:.88 !important; transform:translateY(-1px) !important; }
[data-testid="stButton"] > button[kind="secondary"] { background:transparent !important; border:1px solid rgba(212,175,55,.35) !important; color:var(--muted) !important; }
[data-testid="stButton"] > button[kind="secondary"]:hover { border-color:var(--gold) !important; color:var(--gold) !important; }

input, textarea, [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-baseweb="select"] > div { background:var(--bg-3) !important; color:var(--text) !important; border:1px solid var(--border) !important; border-radius:0 !important; font-family:'Montserrat',sans-serif !important; font-size:.82rem !important; }
input:focus { border-color:var(--gold) !important; box-shadow:0 0 0 2px rgba(212,175,55,.1) !important; }
[data-baseweb="select"] * { color:var(--text) !important; background:var(--bg-3) !important; }
[data-baseweb="menu"] { background:#1a1a1a !important; border:1px solid var(--border) !important; }

[data-testid="stWidgetLabel"] p { color:var(--muted) !important; font-size:.72rem !important; letter-spacing:.1em !important; text-transform:uppercase !important; }
[data-testid="stVerticalBlockBorderWrapper"] { background:var(--bg-2) !important; border:1px solid var(--border) !important; border-radius:0 !important; }

[data-testid="stMetric"] { background:var(--bg-2) !important; border:1px solid var(--border) !important; padding:16px !important; border-radius:0 !important; }
[data-testid="stMetricLabel"] p { font-size:.65rem !important; letter-spacing:.15em !important; text-transform:uppercase !important; color:var(--muted) !important; }
[data-testid="stMetricValue"] { font-family:'Cormorant Garamond',serif !important; font-size:1.6rem !important; color:var(--gold) !important; }

hr { border:none !important; border-top:1px solid var(--border) !important; }
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--gold-dark); border-radius:2px; }

[data-testid="stTabs"] [role="tablist"] { border-bottom:1px solid var(--border) !important; gap:0 !important; }
[data-testid="stTabs"] button[role="tab"] { font-size:.72rem !important; letter-spacing:.14em !important; text-transform:uppercase !important; color:var(--muted) !important; padding:10px 20px !important; border-radius:0 !important; border-bottom:2px solid transparent !important; transition:color .2s, border-color .2s !important; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color:var(--gold) !important; border-bottom-color:var(--gold) !important; }

[data-testid="stSuccess"] { background:rgba(212,175,55,.08) !important; border-left:3px solid var(--gold) !important; border-radius:0 !important; }
[data-testid="stWarning"] { background:rgba(180,120,0,.1) !important; border-left:3px solid #b87800 !important; border-radius:0 !important; }
[data-testid="stError"]   { background:rgba(160,30,30,.12) !important; border-left:3px solid #a01e1e !important; border-radius:0 !important; }
[data-testid="stInfo"]    { background:rgba(212,175,55,.05) !important; border-left:3px solid var(--gold-dark) !important; border-radius:0 !important; }
[data-testid="stToast"]   { background:#1a1508 !important; border:1px solid rgba(212,175,55,.3) !important; color:var(--text) !important; border-radius:0 !important; }

[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,var(--gold-dark),var(--gold)) !important; }
[data-testid="stCheckbox"] label { color:var(--text) !important; font-size:.82rem !important; }
[data-testid="stSegmentedControl"] button { border-radius:0 !important; font-size:.72rem !important; letter-spacing:.12em !important; }
[data-testid="stSegmentedControl"] button[aria-pressed="true"] { background:rgba(212,175,55,.15) !important; color:var(--gold) !important; }
[data-testid="stNumberInput"] button { background:var(--bg-3) !important; border:1px solid var(--border) !important; color:var(--gold) !important; border-radius:0 !important; }

/* ── Skeleton loader ── */
.skeleton { background: linear-gradient(90deg, #111 25%, #1e1e1e 50%, #111 75%); background-size:400px 100%; animation: shimmer 1.4s ease infinite; border-radius:2px; }
@keyframes shimmer { 0%{background-position:-400px 0} 100%{background-position:400px 0} }
.skel-img  { height:240px; width:100%; margin-bottom:8px; }
.skel-line { height:12px; margin-bottom:8px; }
.skel-line.w80 { width:80%; }
.skel-line.w50 { width:50%; }
.skel-line.w30 { width:30%; }

/* ── Componentes custom ── */
.badge { display:inline-block; padding:2px 10px; margin:2px; font-size:.62rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase; background:rgba(212,175,55,.08); border:1px solid rgba(212,175,55,.22); color:var(--gold); }
.price-tag { font-family:'Cormorant Garamond',serif; font-size:1.4rem; color:var(--gold); font-weight:600; }
.price-tag-small { font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:var(--gold-light); }
.sec-eye { font-size:.62rem; letter-spacing:.45em; color:var(--muted); text-transform:uppercase; margin-bottom:6px; }
.sec-title { font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--text); font-weight:300; margin-bottom:0; }
.sec-line { width:48px; height:1px; margin:12px 0 0; background:linear-gradient(90deg,var(--gold),transparent); }
.spec-row { display:flex; justify-content:space-between; padding:9px 0; border-bottom:1px solid var(--border); font-size:.8rem; }
.spec-row:last-child { border-bottom:none; }
.spec-lbl { color:var(--muted); }
.spec-val { color:var(--text); font-weight:500; }
.prod-card { background:var(--bg-2); border:1px solid var(--border); overflow:hidden; transition:border-color .3s,transform .3s,box-shadow .3s; position:relative; }
.prod-card:hover { border-color:rgba(212,175,55,.5); transform:translateY(-3px); box-shadow:0 8px 32px rgba(0,0,0,.5); }
.prod-img { width:100%; height:240px; overflow:hidden; position:relative; background:#0d0d0d; cursor:zoom-in; }
.prod-img img { width:100%; height:100%; object-fit:cover; transition:transform .55s cubic-bezier(.25,.46,.45,.94),filter .4s; filter:brightness(.82); }
.prod-card:hover .prod-img img { transform:scale(1.08); filter:brightness(.68); }
.prod-img-overlay { position:absolute; inset:0; background:linear-gradient(0deg,rgba(8,8,8,.6) 0%,transparent 50%); }
.zoom-wrap { overflow:hidden; background:#000; position:relative; cursor:crosshair; }
.zoom-wrap img { width:100%; display:block; transition:transform .4s ease; transform-origin:center center; }
.zoom-wrap:hover img { transform:scale(2.6); }
</style>
"""

# ────────────────────────────────────────────────────────────────────
# PALETA CLARA — Marfil/perla, dorado sobrio, texto oscuro #2C2C2C
# ────────────────────────────────────────────────────────────────────
_CSS_LIGHT = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');

*, html, body { transition: background-color .35s ease, color .25s ease, border-color .25s ease !important; }

:root {
  --gold:       #9A7B1C;
  --gold-light: #B89420;
  --gold-dark:  #6B5510;
  --bg:         #F9F8F6;
  --bg-2:       #F1EDE4;
  --bg-3:       #E8E2D6;
  --text:       #2C2C2C;
  --muted:      #7A7060;
  --border:     #DDD5C0;
}

html, body, [data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Montserrat', sans-serif !important;
}
*, *::before, *::after { box-sizing: border-box; }

.stMainBlockContainer { padding-top:28px !important; max-width:1280px !important; }
[data-testid="stHeader"] { background: rgba(249,248,246,.97) !important; border-bottom:1px solid var(--border) !important; }
[data-testid="stHeader"] * { color: var(--text) !important; }

[data-testid="stSidebar"] { background: #EDE8DE !important; border-right:1px solid var(--border) !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebarNav"] a { border-radius:3px !important; padding:8px 14px !important; font-size:.78rem !important; letter-spacing:.08em !important; transition:background .2s !important; }
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] a[aria-current="page"] { background:rgba(154,123,28,.14) !important; color:var(--gold) !important; }
[data-testid="stSidebarNavItems"] > div > span { font-size:.6rem !important; letter-spacing:.3em !important; color:#B0A080 !important; text-transform:uppercase !important; padding:14px 14px 4px !important; }

h1 { font-family:'Cormorant Garamond',serif !important; color:var(--gold) !important; font-size:2.4rem !important; font-weight:400 !important; letter-spacing:.06em !important; }
h2 { font-family:'Cormorant Garamond',serif !important; color:var(--gold-dark) !important; font-weight:300 !important; }
h3, h4 { color:var(--text) !important; }
p, li { color:var(--muted) !important; }

[data-testid="stButton"] > button { border-radius:0 !important; font-family:'Montserrat',sans-serif !important; letter-spacing:.12em !important; font-size:.72rem !important; text-transform:uppercase !important; transition:all .2s !important; }
[data-testid="stButton"] > button[kind="primary"] { background:linear-gradient(135deg,var(--gold-dark),var(--gold)) !important; color:#fff !important; border:none !important; font-weight:600 !important; box-shadow:0 2px 14px rgba(154,123,28,.25) !important; }
[data-testid="stButton"] > button[kind="primary"]:hover { opacity:.88 !important; transform:translateY(-1px) !important; }
[data-testid="stButton"] > button[kind="secondary"] { background:transparent !important; border:1px solid rgba(154,123,28,.35) !important; color:var(--gold) !important; }
[data-testid="stButton"] > button[kind="secondary"]:hover { border-color:var(--gold) !important; color:var(--gold-dark) !important; }

input, textarea, [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-baseweb="select"] > div { background:#fff !important; color:var(--text) !important; border:1px solid var(--border) !important; border-radius:0 !important; font-size:.82rem !important; }
input:focus { border-color:var(--gold) !important; box-shadow:0 0 0 2px rgba(154,123,28,.12) !important; }
[data-baseweb="select"] * { color:var(--text) !important; background:#fff !important; }
[data-baseweb="menu"] { background:#F9F8F6 !important; border:1px solid var(--border) !important; }

[data-testid="stWidgetLabel"] p { color:var(--muted) !important; font-size:.72rem !important; letter-spacing:.1em !important; text-transform:uppercase !important; }
[data-testid="stVerticalBlockBorderWrapper"] { background:var(--bg-2) !important; border:1px solid var(--border) !important; border-radius:0 !important; box-shadow:0 2px 12px rgba(0,0,0,.06) !important; }

[data-testid="stMetric"] { background:var(--bg-2) !important; border:1px solid var(--border) !important; padding:16px !important; border-radius:0 !important; box-shadow:0 2px 8px rgba(0,0,0,.05) !important; }
[data-testid="stMetricLabel"] p { font-size:.65rem !important; letter-spacing:.15em !important; text-transform:uppercase !important; color:var(--muted) !important; }
[data-testid="stMetricValue"] { font-family:'Cormorant Garamond',serif !important; font-size:1.6rem !important; color:var(--gold) !important; }

hr { border:none !important; border-top:1px solid var(--border) !important; }
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--gold); border-radius:2px; }

[data-testid="stTabs"] [role="tablist"] { border-bottom:1px solid var(--border) !important; }
[data-testid="stTabs"] button[role="tab"] { font-size:.72rem !important; letter-spacing:.14em !important; text-transform:uppercase !important; color:var(--muted) !important; padding:10px 20px !important; border-radius:0 !important; border-bottom:2px solid transparent !important; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color:var(--gold) !important; border-bottom-color:var(--gold) !important; }

[data-testid="stSuccess"] { background:rgba(154,123,28,.08) !important; border-left:3px solid var(--gold) !important; border-radius:0 !important; }
[data-testid="stWarning"] { background:rgba(180,120,0,.08) !important; border-left:3px solid #b87800 !important; border-radius:0 !important; }
[data-testid="stError"]   { background:rgba(160,30,30,.07) !important; border-left:3px solid #a01e1e !important; border-radius:0 !important; }
[data-testid="stInfo"]    { background:rgba(154,123,28,.06) !important; border-left:3px solid var(--gold-dark) !important; border-radius:0 !important; }
[data-testid="stToast"]   { background:#F9F4E8 !important; border:1px solid rgba(154,123,28,.3) !important; color:var(--text) !important; border-radius:0 !important; }

[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,var(--gold-dark),var(--gold)) !important; }
[data-testid="stCheckbox"] label { color:var(--text) !important; font-size:.82rem !important; }
[data-testid="stSegmentedControl"] button { border-radius:0 !important; font-size:.72rem !important; }
[data-testid="stSegmentedControl"] button[aria-pressed="true"] { background:rgba(154,123,28,.15) !important; color:var(--gold) !important; }
[data-testid="stNumberInput"] button { background:var(--bg-3) !important; border:1px solid var(--border) !important; color:var(--gold) !important; border-radius:0 !important; }

/* ── Skeleton loader modo claro ── */
.skeleton { background:linear-gradient(90deg,#E8E2D6 25%,#F1EDE4 50%,#E8E2D6 75%); background-size:400px 100%; animation:shimmer 1.4s ease infinite; border-radius:2px; }
@keyframes shimmer { 0%{background-position:-400px 0} 100%{background-position:400px 0} }
.skel-img  { height:240px; width:100%; margin-bottom:8px; }
.skel-line { height:12px; margin-bottom:8px; }
.skel-line.w80 { width:80%; }
.skel-line.w50 { width:50%; }
.skel-line.w30 { width:30%; }

/* ── Componentes custom modo claro ── */
.badge { display:inline-block; padding:2px 10px; margin:2px; font-size:.62rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase; background:rgba(154,123,28,.1); border:1px solid rgba(154,123,28,.25); color:var(--gold); }
.price-tag { font-family:'Cormorant Garamond',serif; font-size:1.4rem; color:var(--gold); font-weight:600; }
.price-tag-small { font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:var(--gold-dark); }
.sec-eye { font-size:.62rem; letter-spacing:.45em; color:var(--muted); text-transform:uppercase; margin-bottom:6px; }
.sec-title { font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--text); font-weight:300; margin-bottom:0; }
.sec-line { width:48px; height:1px; margin:12px 0 0; background:linear-gradient(90deg,var(--gold),transparent); }
.spec-row { display:flex; justify-content:space-between; padding:9px 0; border-bottom:1px solid var(--border); font-size:.8rem; }
.spec-row:last-child { border-bottom:none; }
.spec-lbl { color:var(--muted); }
.spec-val { color:var(--text); font-weight:500; }
.prod-card { background:#fff; border:1px solid var(--border); overflow:hidden; transition:border-color .3s,transform .3s,box-shadow .3s; position:relative; }
.prod-card:hover { border-color:rgba(154,123,28,.5); transform:translateY(-3px); box-shadow:0 8px 28px rgba(0,0,0,.12); }
.prod-img { width:100%; height:240px; overflow:hidden; position:relative; background:var(--bg-3); cursor:zoom-in; }
.prod-img img { width:100%; height:100%; object-fit:cover; transition:transform .55s cubic-bezier(.25,.46,.45,.94),filter .4s; filter:brightness(.92); }
.prod-card:hover .prod-img img { transform:scale(1.08); filter:brightness(.78); }
.prod-img-overlay { position:absolute; inset:0; background:linear-gradient(0deg,rgba(0,0,0,.25) 0%,transparent 50%); }
.zoom-wrap { overflow:hidden; background:var(--bg-2); position:relative; cursor:crosshair; }
.zoom-wrap img { width:100%; display:block; transition:transform .4s ease; transform-origin:center center; }
.zoom-wrap:hover img { transform:scale(2.6); }
</style>
"""


def aplicar_estilos():
    """Aplica el CSS oscuro (legado — mantiene compatibilidad)."""
    st.markdown(_CSS_DARK, unsafe_allow_html=True)


def aplicar_modo_claro():
    """Aplica el CSS claro elegante marfil/dorado."""
    st.markdown(_CSS_LIGHT, unsafe_allow_html=True)


def tema():
    """
    Función central: detecta la preferencia de session_state y aplica
    el CSS correcto. TODAS las vistas deben llamar tema() en lugar de
    aplicar_estilos() para que el toggle funcione globalmente.
    """
    if st.session_state.get("modo_oscuro", True):
        st.markdown(_CSS_DARK, unsafe_allow_html=True)
    else:
        st.markdown(_CSS_LIGHT, unsafe_allow_html=True)


def skeleton_catalogo():
    """Muestra 6 tarjetas skeleton mientras el catálogo carga."""
    for _ in range(2):
        cols = st.columns(3)
        for col in cols:
            with col:
                st.markdown(
                    '<div style="margin-bottom:24px">'
                    '<div class="skeleton skel-img"></div>'
                    '<div class="skeleton skel-line w80"></div>'
                    '<div class="skeleton skel-line w50"></div>'
                    '<div class="skeleton skel-line w30"></div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
