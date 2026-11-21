"""
Página de inicio — Matallana VIP Ultra Luxury.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import streamlit as st
from components.home_hero import home_hero
from components.site_footer import render_footer

W = "https://upload.wikimedia.org/wikipedia/commons/thumb"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');
@keyframes floatY{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.stMainBlockContainer{padding-top:0!important;padding-bottom:0!important;max-width:100%!important}
[data-testid="stHeader"]{display:none!important}
.fbar{display:grid;grid-template-columns:repeat(5,1fr);background:#0b0b0b;border-top:1px solid #1a1a1a;border-bottom:1px solid #1a1a1a}
.fbar-item{padding:30px 20px;text-align:center;border-right:1px solid #1a1a1a;transition:background .3s}
.fbar-item:last-child{border-right:none}
.fbar-item:hover{background:rgba(212,175,55,.04)}
.fbar-icon{width:28px;height:28px;margin:0 auto 12px;stroke:#D4AF37;fill:none;stroke-width:1.25;stroke-linecap:round;stroke-linejoin:round}
.fbar-title{font-family:'Cormorant Garamond',serif;font-size:1rem;color:#D4AF37;margin-bottom:5px;font-weight:400}
.fbar-desc{font-size:.72rem;color:#7A7060;line-height:1.6}
.sec-head{padding:72px 48px 0;text-align:center}
.sec-eye{font-family:'Montserrat',sans-serif;font-size:.65rem;letter-spacing:.5em;color:#7A7060;text-transform:uppercase;margin-bottom:10px}
.sec-title{font-family:'Cormorant Garamond',serif;font-size:clamp(1.9rem,3.5vw,2.9rem);color:#F8F6F0;font-weight:300;margin-bottom:0}
.sec-line{width:56px;height:1px;margin:18px auto 52px;background:linear-gradient(90deg,transparent,#D4AF37,transparent)}
.col-card{position:relative;overflow:hidden;cursor:pointer;height:240px;background:#0d0d0d;border:1px solid #1a1a1a;transition:border-color .3s}
.col-card:hover{border-color:rgba(212,175,55,.3)}
.col-card img{width:100%;height:100%;object-fit:cover;filter:brightness(.6);transition:transform .7s cubic-bezier(.22,1,.36,1),filter .5s;display:block}
.col-card:hover img{transform:scale(1.07);filter:brightness(.42)}
.col-overlay{position:absolute;bottom:0;left:0;right:0;padding:20px 18px;background:linear-gradient(0deg,rgba(0,0,0,.88),transparent)}
.col-cat{font-size:.6rem;letter-spacing:.32em;color:#D4AF37;text-transform:uppercase;margin-bottom:5px}
.col-name{font-family:'Cormorant Garamond',serif;font-size:1.35rem;color:#F8F6F0;font-weight:300}
.col-desc{font-size:.7rem;color:#7A7060;margin-top:4px}
.stat-n{font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:#D4AF37;font-weight:600}
.stat-l{font-size:.68rem;color:#7A7060;margin-top:3px}
.cta-banner{background:linear-gradient(135deg,#0d0b04,#1a1508,#0d0b04);border:1px solid rgba(212,175,55,.22);padding:56px 40px;text-align:center;margin:48px 0}
.cta-tag{display:inline-block;padding:4px 18px;margin:3px;background:rgba(212,175,55,.1);border:1px solid rgba(212,175,55,.28);border-radius:20px;font-size:.72rem;color:#D4AF37;letter-spacing:.08em}
.footer{background:#060606;border-top:1px solid #161616;padding:60px 48px 28px}
.foot-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1.5fr;gap:48px;margin-bottom:48px}
.foot-brand{font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:#D4AF37;letter-spacing:.12em;margin-bottom:12px}
.foot-desc{font-size:.77rem;color:#555;line-height:1.9}
.foot-ttl{font-size:.65rem;letter-spacing:.28em;color:#7A7060;text-transform:uppercase;margin-bottom:18px;font-weight:600}
.foot-link{display:block;font-size:.77rem;color:#555;text-decoration:none;margin-bottom:10px;transition:color .2s}
.foot-link:hover{color:#D4AF37}
.foot-contact{font-size:.77rem;color:#555;line-height:2.2}
.soc-row{display:flex;gap:10px;margin-top:18px}
.soc-btn{width:36px;height:36px;border-radius:50%;border:1px solid #222;display:flex;align-items:center;justify-content:center;text-decoration:none;transition:border-color .2s,background .2s}
.soc-btn svg{width:15px;height:15px;stroke:#555;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;transition:stroke .2s}
.soc-btn:hover{border-color:#D4AF37;background:rgba(212,175,55,.08)}
.soc-btn:hover svg{stroke:#D4AF37}
.foot-div{height:1px;background:#161616;margin-bottom:24px}
.foot-bot{display:flex;justify-content:space-between;font-size:.68rem;color:#333}
.foot-bot a{color:#444;text-decoration:none;transition:color .2s}
.foot-bot a:hover{color:#D4AF37}
.wa-fab{position:fixed;bottom:28px;right:28px;z-index:9999;width:54px;height:54px;border-radius:50%;background:#080808;border:1px solid rgba(37,211,102,.4);display:flex;align-items:center;justify-content:center;text-decoration:none;box-shadow:0 4px 20px rgba(0,0,0,.5);transition:border-color .2s,box-shadow .2s;animation:floatY 3.5s ease-in-out infinite}
.wa-fab:hover{border-color:#25D366;box-shadow:0 6px 28px rgba(37,211,102,.25)}
.wa-fab svg{width:22px;height:22px;fill:#25D366}
.wa-tooltip{position:absolute;right:62px;top:50%;background:#111;border:1px solid rgba(212,175,55,.2);color:#D4AF37;font-size:.65rem;letter-spacing:.1em;white-space:nowrap;padding:6px 12px;opacity:0;pointer-events:none;transition:opacity .25s;transform:translateY(-50%)}
.wa-fab:hover .wa-tooltip{opacity:1}
</style>
"""

def render(ir_a=None):
    if ir_a is None:
        def ir_a(p):
            st.query_params["page"] = p
            st.rerun()

    st.markdown(_CSS, unsafe_allow_html=True)
    if st.session_state.get("modo_claro", True):
        st.markdown("""
<style>
.fbar { background:#FFFFFF !important; border-color:#E7DFC9 !important; }
.fbar-item { border-color:#E7DFC9 !important; }
.fbar-icon { stroke:#0B6B45 !important; }
.fbar-title,.stat-n { color:#94701F !important; }
.fbar-desc,.stat-l,.sec-eye { color:#696456 !important; }
.sec-title { color:#25251F !important; }
.col-card { background:#F3EFE6 !important; border-color:#E1D7BD !important; }
.col-card img { filter:brightness(.82) saturate(.9) !important; }
.col-card:hover img { filter:brightness(.68) saturate(1) !important; }
.cta-banner { background:linear-gradient(135deg,#F5F0E2,#E9F0E7,#F8F4E9) !important; border-color:rgba(11,107,69,.24) !important; }
.cta-banner>div:first-child { color:#0B6B45 !important; }
.footer { background:#F4F1E8 !important; border-color:#E4DDCA !important; }
.foot-brand { color:#0B6B45 !important; }
.foot-desc,.foot-link,.foot-contact { color:#5F5B50 !important; }
.foot-ttl { color:#796329 !important; }
.foot-div { background:#DED6C3 !important; }
.foot-bot,.foot-bot a { color:#777064 !important; }
.soc-btn { border-color:#D5CCB7 !important; }
.soc-btn svg { stroke:#0B6B45 !important; }
[data-testid="stMarkdownContainer"] [style*="color:#F8F6F0"],
[data-testid="stMarkdownContainer"] [style*="color:#C8BFA8"],
[data-testid="stMarkdownContainer"] [style*="color:#7A7060"],
[data-testid="stMarkdownContainer"] [style*="color:#555"],
[data-testid="stMarkdownContainer"] [style*="color:#9A9080"] {
  color:#5F5B50 !important;
}
</style>
""", unsafe_allow_html=True)

    home_hero(ir_a)

    # FEATURES BAR
    st.markdown(
'<div class="fbar">'
'<div class="fbar-item"><svg class="fbar-icon" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><div class="fbar-title">Materiales Certificados</div><div class="fbar-desc">Oro 18K, Plata 925 y Platino<br>con certificado de autenticidad</div></div>'
'<div class="fbar-item"><svg class="fbar-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg><div class="fbar-title">Esmeraldas Colombianas</div><div class="fbar-desc">Muzo y Chivor, Boyac\u00e1<br>Las m\u00e1s finas del mundo</div></div>'
'<div class="fbar-item"><svg class="fbar-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg><div class="fbar-title">Dise\u00f1o a Medida</div><div class="fbar-desc">Tu pieza, tu historia<br>Configurada desde cero</div></div>'
'<div class="fbar-item"><svg class="fbar-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg><div class="fbar-title">Garant\u00eda Total</div><div class="fbar-desc">+25 a\u00f1os de tradici\u00f3n<br>Garant\u00eda en cada pieza</div></div>'
'<div class="fbar-item"><svg class="fbar-icon" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><div class="fbar-title">Env\u00edo Seguro</div><div class="fbar-desc">Env\u00edo asegurado<br>a toda Colombia</div></div>'
'</div>',
        unsafe_allow_html=True
    )

    # COLECCIONES
    st.markdown(
'<div class="sec-head"><div class="sec-eye">Descubre</div><div class="sec-title">Nuestras Colecciones</div><div class="sec-line"></div></div>',
        unsafe_allow_html=True
    )

    colecciones = [
        (W+"/b/bb/Starlight_-_white_gold_ring_with_diamonds.jpg/960px-Starlight_-_white_gold_ring_with_diamonds.jpg", "Anillos", "Solitarios, medias alianzas y dise\u00f1os exclusivos"),
        (W+"/c/ce/Gold_chain_in_three_strands_MET_DP257487.jpg/960px-Gold_chain_in_three_strands_MET_DP257487.jpg", "Cadenas", "Cadenas en oro y plata desde 40 hasta 70 cm"),
        (W+"/6/64/Gold_bracelet_MET_DT333008.jpg/960px-Gold_bracelet_MET_DT333008.jpg", "Manillas", "Manillas de lujo en oro 18K, 14K y plata 925"),
        (W+"/d/dc/Gold_earrings_with_carnelian_on_oranges_by_ASQ.jpg/960px-Gold_earrings_with_carnelian_on_oranges_by_ASQ.jpg", "Aros", "Aros y aretes en oro y plata para toda ocasi\u00f3n"),
        (W+"/2/2f/Gold_necklace_with_crescent-shaped_pendant_MET_DP160653.jpg/960px-Gold_necklace_with_crescent-shaped_pendant_MET_DP160653.jpg", "Colgantes", "Dijes y colgantes \u00fanicos con gemas colombianas"),
        (W+"/d/df/Silver_bracelet_and_cherries_by_ASQ.jpg/960px-Silver_bracelet_and_cherries_by_ASQ.jpg", "Pulseras", "Pulseras delicadas en plata 925 y oro 14K"),
    ]
    cols = st.columns(3, gap="small")
    for i, (img, nombre, desc) in enumerate(colecciones):
        with cols[i % 3]:
            st.markdown(
f'<div class="col-card" style="margin-bottom:6px"><img src="{img}" alt="{nombre}"><div class="col-overlay"><div class="col-cat">Colecci\u00f3n</div><div class="col-name">{nombre}</div><div class="col-desc">{desc}</div></div></div>',
                unsafe_allow_html=True
            )

    # QUIÉNES SOMOS
    st.markdown("<div style='height:64px'></div>", unsafe_allow_html=True)
    qi1, qi2 = st.columns([1, 1], gap="small")
    with qi1:
        st.image(W+"/b/ba/Gold_and_diamond_rings_with_passion_fruit_by_ASQ.jpg/960px-Gold_and_diamond_rings_with_passion_fruit_by_ASQ.jpg", width="stretch")
    with qi2:
        st.markdown(
'<div style="padding:48px 28px 20px">'
'<div class="sec-eye" style="text-align:left">Nuestra Historia</div>'
'<div style="font-family:\'Cormorant Garamond\',serif;font-size:2.5rem;color:#F8F6F0;font-weight:300;line-height:1.15;margin-bottom:18px">Arte &amp; Tradici\u00f3n<br><em style="color:#D4AF37">desde 1998</em></div>'
'<div style="width:48px;height:1px;background:#D4AF37;margin-bottom:24px"></div>'
'<p style="color:#7A7060;font-size:.87rem;line-height:1.95;margin-bottom:14px">Joyer\u00eda Matallana VIP naci\u00f3 en Bogot\u00e1 como un taller artesanal familiar con una convicci\u00f3n: <strong style="color:#C8BFA8">cada joya debe contar una historia.</strong></p>'
'<p style="color:#7A7060;font-size:.84rem;line-height:1.95">Somos referentes en joyer\u00eda de alta gama en Colombia, especializados en piezas con esmeraldas de Boyac\u00e1, diamantes y metales certificados.</p>'
'<div style="display:flex;gap:32px;margin-top:40px">'
'<div style="text-align:center"><div class="stat-n">+25</div><div class="stat-l">A\u00f1os</div></div>'
'<div style="text-align:center"><div class="stat-n">+8K</div><div class="stat-l">Piezas creadas</div></div>'
'<div style="text-align:center"><div class="stat-n">100%</div><div class="stat-l">Certificado</div></div>'
'</div></div>',
            unsafe_allow_html=True
        )

    # CTA BANNER
    st.markdown(
'<div class="cta-banner">'
'<div style="font-family:\'Cormorant Garamond\',serif;font-size:2.3rem;color:#D4AF37;margin-bottom:12px;font-weight:300">\u00bfLista tu joya a medida?</div>'
'<div style="color:#7A7060;font-size:.86rem;margin-bottom:28px;line-height:1.9">Usa nuestro configurador y recibe tu presupuesto en tiempo real.<br>Esmeraldas desde <strong style="color:#C8BFA8">$ 420.000 COP/ct</strong> \u00b7 Oro 18K desde <strong style="color:#C8BFA8">$ 189.000 COP/g</strong></div>'
'<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">'
'<span class="cta-tag">Esmeraldas Colombianas</span>'
'<span class="cta-tag">Grabado Personalizado</span>'
'<span class="cta-tag">Env\u00edo a toda Colombia</span>'
'</div></div>',
        unsafe_allow_html=True
    )

    render_footer()
