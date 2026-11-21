"""
Joyería Matallana VIP — Punto de entrada principal.
Enrutamiento via st.query_params["page"] para evitar Page not found.
"""
from pathlib import Path
import base64

import streamlit as st
from utils.session import init_session, esta_autenticado, contar_items_carrito

st.set_page_config(
    page_title="Joyería Matallana VIP — Esmeraldas de Colombia",
    page_icon=str(Path(__file__).parent / "assets" / "emblema-joyeria.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

from utils.analytics import registrar_evento

init_session()
if not st.session_state.get("preferencia_visual_v2"):
    st.session_state["modo_claro"] = True
    st.session_state["modo_oscuro"] = False
    st.session_state["preferencia_visual_v2"] = True

# ── Leer página actual desde query params ──────────────────────────
PAGINAS_VALIDAS = {"inicio", "catalogo", "a_medida", "carrito", "mi_cuenta", "admin", "diagnostico"}
page = st.query_params.get("page", "inicio")
if page not in PAGINAS_VALIDAS:
    page = "inicio"
if page in {"inicio", "catalogo", "a_medida", "carrito", "mi_cuenta"}:
    registrar_evento("visita", page)

user      = st.session_state.get("user") or {}
es_admin  = user.get("rol") == "admin"
carrito_n = contar_items_carrito()

# ── Helper de navegación ───────────────────────────────────────────
def ir_a(pagina):
    if pagina not in PAGINAS_VALIDAS:
        raise ValueError(f"Página desconocida: {pagina}")
    st.query_params["page"] = pagina
    st.rerun()

# ── CSS global ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');

[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[kind="header"],
[data-testid="stHeader"] { display:none !important; }

.stMainBlockContainer { padding:0 !important; max-width:100% !important; }
.stAppViewBlockContainer { padding:0 !important; max-width:100% !important; }
section.main > div { padding-top:0 !important; }

:root {
    --gold:#A77C28; --gold-light:#D8BD70; --gold-dark:#76561B;
    --emerald:#0B6B45; --bg:#FAF8F3; --bg-2:#FFFFFF; --bg-3:#F3EFE6;
    --text:#25231F; --muted:#6D6659; --border:#E8DFC9;
    --nav-text:#5F5A4E; --nav-icon:#0B6B45;
    --nav-icon-bg:rgba(255,255,255,.78); --nav-icon-border:rgba(11,107,69,.24);
}
*, *::before, *::after { box-sizing:border-box; margin:0; }
html, body, [data-testid="stApp"] {
    background:var(--bg) !important;
    color:var(--text) !important;
    font-family:'Montserrat',sans-serif !important;
}
a, a:visited, a:hover, a:active {
    color:var(--gold) !important;
    text-decoration:none !important;
}
[data-testid="stButton"] > button,
[data-testid="stLinkButton"] > a {
    position:relative !important;
    overflow:hidden !important;
    border:1px solid rgba(167,124,40,.5) !important;
    border-radius:0 !important;
    font-family:'Montserrat',sans-serif !important;
    letter-spacing:.14em !important;
    text-transform:uppercase !important;
    transition:background .3s ease, color .3s ease, border-color .3s ease, transform .3s ease !important;
    text-decoration:none !important;
}
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stLinkButton"] > a {
    color:#FFFFFF !important;
    background:linear-gradient(115deg,#79581C,#B58C3A 48%,#E3C878 52%,#B58C3A) !important;
    background-size:220% 100% !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover,
[data-testid="stLinkButton"] > a:hover {
    background-position:100% 0 !important;
    border-color:#F3E5AB !important;
    transform:translateY(-1px);
}
[data-testid="stButton"] > button[kind="primary"]::after,
[data-testid="stLinkButton"] > a::after {
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    transform:translateX(-130%);
    background:linear-gradient(110deg,transparent 35%,rgba(255,255,255,.55),transparent 65%);
}
[data-testid="stButton"] > button[kind="primary"]:hover::after,
[data-testid="stLinkButton"] > a:hover::after { transform:translateX(130%); transition:transform .75s ease; }
[data-testid="stButton"] > button[kind="secondary"] {
    color:var(--gold) !important;
    background:radial-gradient(circle at center,rgba(212,175,55,.2) 0%,transparent 0%) !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover {
    background:radial-gradient(circle at center,rgba(212,175,55,.2) 100%,transparent 100%) !important;
    border-color:var(--gold) !important;
    color:var(--text) !important;
}

/* ── NAVBAR ── */
.mvip-nav {
    position:fixed; top:0; left:0; right:0; z-index:9990;
    height:76px; display:flex; align-items:center;
    justify-content:space-between; padding:0 48px;
    background:rgba(250,248,243,.94);
    border-bottom:1px solid rgba(167,124,40,.22);
    backdrop-filter:blur(12px);
    -webkit-backdrop-filter:blur(12px);
}
.nav-logo-wrap {
    position:absolute; left:50%; transform:translateX(-50%);
    width:340px; height:76px; display:flex; align-items:center;
    justify-content:center; gap:5px; line-height:1;
}
.nav-emblem-wrap {
    position:relative; flex:0 0 62px; width:62px; height:62px;
    animation:logo-depth 4.2s ease-in-out infinite;
}
.nav-emblem {
    display:block; width:100%; height:100%; object-fit:contain;
    border-radius:50%;
}
.nav-emblem-wrap::before,.nav-emblem-wrap::after {
    position:absolute; z-index:2; color:#B58C3A;
    font-size:12px; line-height:1; pointer-events:none;
    content:"✦"; animation:logo-spark 2.8s ease-in-out infinite;
}
.nav-emblem-wrap::before { top:5px; right:1px; }
.nav-emblem-wrap::after { left:0; bottom:10px; font-size:9px; animation-delay:1.2s; }
.nav-wordmark { display:flex; flex-direction:column; gap:3px; white-space:nowrap; }
.nav-wordmark-kicker {
    color:#0B6B45; font-size:8px; font-weight:600; letter-spacing:.34em;
}
.nav-wordmark-name {
    color:transparent;
    background:linear-gradient(105deg,#84651F 0%,#B58C3A 38%,#F0DB9D 50%,#B58C3A 62%,#84651F 100%);
    background-size:220% 100%;
    background-position:100% 0;
    background-clip:text;
    -webkit-background-clip:text;
    font:400 18px 'Cormorant Garamond',serif;
    letter-spacing:.1em;
    animation:wordmark-shimmer 7s ease-in-out infinite;
}
.nav-wordmark-caption {
    color:#786A4A; font-size:5px; letter-spacing:.22em;
}
@keyframes logo-depth {
    0%,100% { transform:perspective(500px) translateY(0) scale(.96); }
    50% { transform:perspective(500px) translateY(-2px) scale(1.055); }
}
@keyframes logo-spark {
    0%,100% { opacity:.15; transform:scale(.7) rotate(0deg); }
    45% { opacity:.95; transform:scale(1.15) rotate(25deg); }
}
@keyframes wordmark-shimmer {
    0%,100% { background-position:100% 0; }
    50% { background-position:0 0; }
}
@media (prefers-reduced-motion: reduce) {
    .nav-emblem-wrap,.nav-emblem-wrap::before,.nav-emblem-wrap::after,.nav-wordmark-name { animation:none; }
}
@media (max-width:760px) {
    .nav-logo-wrap { width:220px; gap:2px; }
    .nav-emblem-wrap { flex-basis:50px; width:50px; height:50px; }
    .nav-wordmark-name { font-size:14px; }
    .nav-wordmark-kicker { font-size:6px; }
    .nav-wordmark-caption { font-size:4px; }
}
.nav-links { display:flex; gap:4px; align-items:center; }
.nav-actions { display:flex; gap:4px; align-items:center; }

/* Botones de navegación — aspecto de link */
.nav-btn {
    background:none !important; border:none !important;
    color:rgba(248,246,240,.65) !important;
    font-family:'Montserrat',sans-serif !important;
    font-size:.68rem !important; letter-spacing:.22em !important;
    text-transform:uppercase !important;
    padding:6px 14px !important; cursor:pointer !important;
    transition:color .2s !important;
    border-radius:0 !important;
    position:relative;
}
.nav-btn:hover { color:var(--gold-light) !important; }
.nav-btn::after {
    content:''; position:absolute; bottom:2px; left:14px; right:14px;
    height:1px; background:var(--gold);
    transform:scaleX(0); transform-origin:center;
    transition:transform .3s cubic-bezier(.22,1,.36,1);
}
.nav-btn:hover::after { transform:scaleX(1); }
.nav-btn-icon {
    background:none !important; border:none !important;
    color:rgba(248,246,240,.65) !important;
    padding:6px 10px !important; cursor:pointer !important;
    transition:color .2s !important;
    border-radius:0 !important;
    display:flex !important; align-items:center !important;
    position:relative;
}
.nav-btn-icon:hover { color:var(--gold) !important; }
.nav-btn-icon svg { width:18px; height:18px; stroke:currentColor; fill:none; stroke-width:1.25; stroke-linecap:round; stroke-linejoin:round; }
.nav-badge {
    position:absolute; top:-4px; right:4px;
    background:var(--gold); color:#080808;
    font-size:.52rem; font-weight:700;
    width:16px; height:16px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-family:'Montserrat',sans-serif;
}
.nav-user-label {
    font-family:'Montserrat',sans-serif; font-size:.62rem;
    letter-spacing:.14em; color:var(--gold);
    text-transform:uppercase; margin-left:4px;
}

/* Componentes globales */
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
.prod-card { background:rgba(17,17,17,.72); backdrop-filter:blur(12px); border:1px solid var(--border); overflow:hidden; transition:border-color .3s,transform .45s,box-shadow .3s; position:relative; animation:fade-up .65s cubic-bezier(.22,1,.36,1) both; }
.prod-card:hover { border-color:rgba(212,175,55,.8); transform:translateY(-4px); box-shadow:0 8px 32px rgba(212,175,55,.12); }
@keyframes fade-up { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
.prod-img { width:100%; height:240px; overflow:hidden; position:relative; background:#0d0d0d; cursor:zoom-in; }
.prod-img img { width:100%; height:100%; object-fit:cover; transition:transform .55s cubic-bezier(.25,.46,.45,.94),filter .4s; filter:brightness(.82); }
.prod-card:hover .prod-img img { transform:scale(1.08); filter:brightness(.68); }
.prod-img-overlay { position:absolute; inset:0; background:linear-gradient(0deg,rgba(8,8,8,.6) 0%,transparent 50%); }
.zoom-wrap { overflow:hidden; background:#000; position:relative; cursor:crosshair; }
.zoom-wrap img { width:100%; display:block; transition:transform .4s ease; transform-origin:center center; }
.zoom-wrap:hover img { transform:scale(2.6); }
.skeleton { background:linear-gradient(90deg,#111 25%,#1e1e1e 50%,#111 75%); background-size:400px 100%; animation:shimmer 1.4s ease infinite; border-radius:2px; }
@keyframes shimmer { 0%{background-position:-400px 0} 100%{background-position:400px 0} }
.skel-img { height:240px; width:100%; margin-bottom:8px; }
.skel-line { height:12px; margin-bottom:8px; }
.skel-line.w80 { width:80%; }
.skel-line.w50 { width:50%; }
.skel-line.w30 { width:30%; }
</style>
""", unsafe_allow_html=True)

if st.session_state.get("modo_claro", True):
    st.markdown("""
<style>
:root {
  --bg:#FAF8F5; --bg-2:#FFFFFF; --bg-3:#FFFDF9;
  --text:#181818; --muted:#675F55; --border:rgba(166,135,75,.28);
  --gold:#9A7416; --gold-light:#B28D2F; --gold-dark:#75550C; --emerald:#0B6B45;
}
html, body, [data-testid="stApp"] { background:var(--bg) !important; color:var(--text) !important; }
.mvip-nav { background:rgba(250,248,245,.94) !important; }
[data-testid="stMarkdownContainer"] [style*="color:#F5F0E8"],
[data-testid="stMarkdownContainer"] [style*="color:#F8F6F0"],
[data-testid="stMarkdownContainer"] [style*="color:#C8BFA8"],
[data-testid="stMarkdownContainer"] [style*="color:#9A9080"] { color:#3D382F !important; }
.fbar, .footer { background:#FFFFFF !important; }
.fbar-item { border-color:rgba(166,135,75,.2) !important; }
.fbar-title, .sec-title, .foot-brand { color:#70520C !important; }
.col-card, .prod-card { background:rgba(255,255,255,.82) !important; border-color:rgba(166,135,75,.28) !important; }
.col-name, .prod-card, .spec-val { color:#181818 !important; }
.cta-banner { background:linear-gradient(135deg,#fffdf9,#f4eedf,#fffdf9) !important; }
.nav-btn-icon, .nav-btn { color:#4B4337 !important; }
[data-testid="stToggle"] label { color:#3D382F !important; }
.st-key-nav_controls [data-testid="stButton"] > button { color:#423B30 !important; }
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
[data-baseweb="select"] > div, textarea { background:#FFFFFF !important; color:#181818 !important; }
</style>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<style>
:root {
  --bg:#11110F; --bg-2:#1A1916; --bg-3:#24221D;
  --text:#F7F2E6; --muted:#B7AD98; --border:rgba(216,189,112,.2);
  --gold:#D8BD70; --gold-light:#F3E5AB; --gold-dark:#9A7B1C; --emerald:#50C878;
  --nav-text:#E7DFCC; --nav-icon:#9CD6AE;
  --nav-icon-bg:rgba(36,34,29,.92); --nav-icon-border:rgba(216,189,112,.32);
}
html, body, [data-testid="stApp"] { background:var(--bg) !important; color:var(--text) !important; }
.mvip-nav { background:rgba(17,17,15,.94) !important; }
.nav-logo-wrap .brand-kicker { fill:#E8D492 !important; }
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
[data-baseweb="select"] > div, textarea { background:#24221D !important; color:#F7F2E6 !important; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR con botones Streamlit reales ────────────────────────────
logo_path = Path(__file__).parent / "assets" / "emblema-joyeria.png"
logo_data = base64.b64encode(logo_path.read_bytes()).decode("ascii")
logo_markup = (
    '<div class="nav-logo-wrap" aria-label="Joyería Matallana VIP">'
    '<div class="nav-emblem-wrap">'
    f'<img class="nav-emblem" src="data:image/png;base64,{logo_data}" alt="Emblema de esmeralda y árbol">'
    '</div>'
    '<div class="nav-wordmark">'
    '<span class="nav-wordmark-kicker">JOYERÍA</span>'
    '<span class="nav-wordmark-name">MATALLANA VIP</span>'
    '<span class="nav-wordmark-caption">ESMERALDAS COLOMBIANAS · ALTA JOYERÍA</span>'
    '</div></div>'
)

# Contenedor fijo del navbar via HTML puro (solo estructura visual)
st.markdown(
'<div class="mvip-nav" id="mvip-nav">'
'<div id="nav-links-slot" style="display:flex;gap:4px;align-items:center;min-width:260px;"></div>'
f'{logo_markup}'
'<div id="nav-actions-slot" style="display:flex;gap:4px;align-items:center;min-width:260px;justify-content:flex-end;"></div>'
'</div>'
'<div style="height:76px;"></div>',
unsafe_allow_html=True
)

# Botones reales de Streamlit en una fila horizontal (se renderizan debajo del nav visual,
# pero los movemos al nav via JS)
with st.container(key="nav_controls"):
    nav_columns = [1,1.2,1,5,1,1,1,1.5]
    nav_items = st.columns(nav_columns)
    n1, n2, n3, _sp, n4, n5, n6, n7 = nav_items[:8]
    with n1:
        if st.button("Inicio", key="nav_inicio"):
            ir_a("inicio")
    with n2:
        if st.button("Catálogo", key="nav_catalogo"):
            ir_a("catalogo")
    with n3:
        if st.button("A Medida", key="nav_amedida"):
            ir_a("a_medida")
    with n4:
        if st.button(" ", key="nav_buscar", icon=":material/search:", help="Buscar joyas"):
            ir_a("catalogo")
    with n5:
        if es_admin:
            if st.button(
                " ",
                key="nav_cuenta",
                icon=":material/admin_panel_settings:",
                help="Panel de administración",
            ):
                ir_a("admin")
        elif st.button(" ", key="nav_cuenta", icon=":material/person_outline:", help="Mi cuenta"):
            ir_a("mi_cuenta")
    with n6:
        lbl_carrito = str(carrito_n) if carrito_n > 0 else " "
        if st.button(lbl_carrito, key="nav_carrito", icon=":material/shopping_bag:", help=f"Bolsa de compras: {carrito_n} artículos"):
            ir_a("carrito")
    with n7:
        modo_claro = st.toggle("Tema claro", key="modo_claro")
        st.session_state["modo_oscuro"] = not modo_claro

# CSS para posicionar la fila de botones sobre el navbar
st.markdown("""
<style>
/* Tomar el primer stHorizontalBlock después del nav y superponerlo */
.st-key-nav_controls [data-testid="stHorizontalBlock"] {
    position:fixed !important;
    top:0 !important; left:0 !important; right:0 !important;
    height:76px !important; z-index:9995 !important;
    display:flex !important; align-items:center !important;
    padding:0 48px !important;
    pointer-events:auto !important;
    background:transparent !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div {
    display:flex !important; align-items:center !important;
    height:76px !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(1),
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(3) {
    flex:0 0 100px !important;
    width:100px !important;
    min-width:100px !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(2) {
    flex:0 0 120px !important;
    width:120px !important;
    min-width:120px !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(n+5):nth-child(-n+7) {
    flex:0 0 56px !important;
    width:56px !important;
    min-width:56px !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(8) {
    flex:0 0 140px !important;
    width:140px !important;
    min-width:140px !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(-n+3) [data-testid="stButton"] button {
    position:relative !important;
    background:transparent !important;
    border:0 !important;
    border-radius:0 !important;
    box-shadow:none !important;
    color:var(--nav-text) !important;
    font-family:'Montserrat',sans-serif !important;
    font-size:.69rem !important;
    font-weight:500 !important;
    letter-spacing:.12em !important;
    text-transform:uppercase !important;
    padding:10px 8px !important;
    white-space:nowrap !important;
    transition:color .22s ease !important;
    height:auto !important;
    min-height:unset !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(-n+3) [data-testid="stButton"] button::after {
    content:"";
    position:absolute;
    left:8px;
    right:8px;
    bottom:3px;
    height:1px;
    background:linear-gradient(90deg,transparent,#0B6B45,transparent);
    transform:scaleX(0);
    transition:transform .28s ease;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(-n+3) [data-testid="stButton"] button:hover {
    color:#0B6B45 !important;
    background:transparent !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(-n+3) [data-testid="stButton"] button:hover::after {
    transform:scaleX(1);
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(n+5):nth-child(-n+7) [data-testid="stButton"] button {
    width:42px !important;
    height:42px !important;
    min-height:42px !important;
    padding:0 !important;
    border:1px solid var(--nav-icon-border) !important;
    border-radius:50% !important;
    background:var(--nav-icon-bg) !important;
    box-shadow:0 2px 8px rgba(39,53,35,.05) !important;
    color:var(--nav-icon) !important;
    transition:background .22s ease,border-color .22s ease,color .22s ease,transform .22s ease,box-shadow .22s ease !important;
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(n+5):nth-child(-n+7) [data-testid="stButton"] button:hover {
    background:#0B6B45 !important;
    border-color:#0B6B45 !important;
    box-shadow:0 5px 14px rgba(11,107,69,.18) !important;
    color:#FFFFFF !important;
    transform:translateY(-1px);
}
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(n+5):nth-child(-n+7) [data-testid="stButton"] [data-testid="stIconMaterial"] {
    color:inherit !important;
    font-size:20px !important;
}
.st-key-nav_controls label[data-selected="true"] > div:first-of-type {
    background:#0B6B45 !important;
    border-color:#0B6B45 !important;
}
.st-key-nav_controls label[data-selected="false"] > div:first-of-type {
    background:#DDD6C5 !important;
    border-color:#C8BEA8 !important;
}
.st-key-nav_buscar [data-testid="stBaseButton-secondary"],
.st-key-nav_cuenta [data-testid="stBaseButton-secondary"],
.st-key-nav_carrito [data-testid="stBaseButton-secondary"] {
    width:42px !important;
    height:42px !important;
    min-height:42px !important;
    padding:0 !important;
    border:1px solid var(--nav-icon-border) !important;
    border-radius:50% !important;
    background:var(--nav-icon-bg) !important;
    color:var(--nav-icon) !important;
}
/* Spacer column invisible */
.st-key-nav_controls [data-testid="stHorizontalBlock"] > div:nth-child(4) {
    flex:1 1 auto !important;
    width:auto !important;
    min-width:120px !important;
    pointer-events:none !important;
}
</style>
""", unsafe_allow_html=True)

# ── Separador visual entre navbar y contenido ──────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Enrutamiento principal ─────────────────────────────────────────
if page == "inicio":
    from views.home import render
    render(ir_a)

elif page == "catalogo":
    import views.catalogo as _cat
    _cat.render()

elif page == "a_medida":
    import views.personalizador as _pm
    _pm.render()

elif page == "carrito":
    import views.carrito as _car
    _car.render()

elif page == "mi_cuenta":
    import views.auth as _auth
    _auth.render()

elif page == "admin":
    if not esta_autenticado():
        st.info("Inicia sesión con la cuenta administradora para abrir el panel.")
        import views.auth as _auth
        _auth.render()
    elif es_admin:
        import views.admin as _adm
        _adm.render()
    else:
        st.error("Esta cuenta no tiene permisos de administración.")

elif page == "diagnostico":
    if es_admin:
        import views.diagnostico as _diag
        _diag.render()
    else:
        st.error("Acceso restringido.")
