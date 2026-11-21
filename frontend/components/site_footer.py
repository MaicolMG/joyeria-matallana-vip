"""Shared footer for the public storefront pages."""
from datetime import datetime

import streamlit as st


def render_footer():
    light = st.session_state.get("modo_claro", True)
    if light:
        palette = """
            --footer-bg:#F4F1E8; --footer-border:#E4DDCA;
            --footer-title:#0B6B45; --footer-text:#5F5B50;
            --footer-muted:#796329; --footer-rule:#DED6C3;
            --footer-bottom:#777064; --footer-link:#94701F;
        """
        social_border = "#D5CCB7"
    else:
        palette = """
            --footer-bg:#080808; --footer-border:#24221D;
            --footer-title:#D4AF37; --footer-text:#A79F91;
            --footer-muted:#B7AD98; --footer-rule:#24221D;
            --footer-bottom:#8B8375; --footer-link:#D8BD70;
        """
        social_border = "#38352D"

    st.markdown(
        f"""
<style>
.site-footer {{
    {palette}
    background:var(--footer-bg);
    border-top:1px solid var(--footer-border);
    padding:56px 48px 26px;
    color:var(--footer-text);
}}
.site-footer-grid {{
    display:grid;
    grid-template-columns:2fr 1fr 1fr 1.5fr;
    gap:48px;
    margin-bottom:44px;
}}
.site-footer-brand {{
    color:var(--footer-title);
    font:400 1.5rem 'Cormorant Garamond',serif;
    letter-spacing:.12em;
    margin-bottom:12px;
}}
.site-footer-desc,.site-footer-contact,.site-footer-link {{
    color:var(--footer-text);
    font-size:.77rem;
    line-height:1.9;
}}
.site-footer-title {{
    color:var(--footer-muted);
    font-size:.65rem;
    font-weight:600;
    letter-spacing:.28em;
    margin-bottom:16px;
    text-transform:uppercase;
}}
.site-footer-link {{
    display:block;
    margin-bottom:8px;
}}
.site-footer a {{
    color:var(--footer-link) !important;
    text-decoration:none !important;
}}
.site-footer a:hover {{ color:var(--footer-title) !important; }}
.site-footer-social {{ display:flex; gap:10px; margin-top:16px; }}
.site-footer-social a {{
    align-items:center;
    border:1px solid {social_border};
    border-radius:50%;
    display:flex;
    height:36px;
    justify-content:center;
    width:36px;
}}
.site-footer-social svg {{
    fill:none;
    height:15px;
    stroke:var(--footer-title);
    stroke-linecap:round;
    stroke-linejoin:round;
    stroke-width:1.5;
    width:15px;
}}
.site-footer-rule {{ background:var(--footer-rule); height:1px; margin-bottom:20px; }}
.site-footer-bottom {{
    color:var(--footer-bottom);
    display:flex;
    font-size:.68rem;
    justify-content:space-between;
    gap:12px;
}}
.site-wa-fab {{
    align-items:center;
    background:#080808;
    border:1px solid rgba(37,211,102,.4);
    border-radius:50%;
    bottom:28px;
    box-shadow:0 4px 20px rgba(0,0,0,.2);
    display:flex;
    height:54px;
    justify-content:center;
    position:fixed;
    right:28px;
    transition:transform .35s ease, box-shadow .35s ease;
    width:54px;
    z-index:9999;
}}
.site-wa-fab:hover {{ box-shadow:0 6px 24px rgba(37,211,102,.22); transform:translateY(-3px); }}
.site-wa-fab svg {{ fill:#25D366; height:22px; width:22px; }}
@media (max-width:760px) {{
    .site-footer {{ padding:36px 22px 24px; }}
    .site-footer-grid {{ grid-template-columns:1fr 1fr; gap:28px 20px; }}
    .site-footer-bottom {{ flex-direction:column; }}
}}
@media (max-width:420px) {{
    .site-footer-grid {{ grid-template-columns:1fr; }}
}}
</style>
<footer class="site-footer">
  <div class="site-footer-grid">
    <div>
      <div class="site-footer-brand">MATALLANA VIP</div>
      <p class="site-footer-desc">Joyería de alta gama en Colombia.<br>
      Esmeraldas, diamantes y metales preciosos certificados.<br>
      Más de 25 años creando piezas únicas con alma.</p>
      <div class="site-footer-social">
        <a href="https://wa.me/573014397403" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
          <svg viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
        </a>
        <a href="mailto:admin@matallanavip.com" aria-label="Correo electrónico">
          <svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 7 9 6 9-6"/></svg>
        </a>
      </div>
    </div>
    <div>
      <div class="site-footer-title">Horarios</div>
      <div class="site-footer-contact"><strong>Sede principal</strong><br>
      Lun–Vie: 9:00 am–6:00 pm<br>Sábado: 10:00 am–5:00 pm<br>
      Domingo: cerrado<br><br><strong>Tienda online</strong><br>24 horas · 7 días</div>
    </div>
    <div>
      <div class="site-footer-title">Explorar</div>
      <a class="site-footer-link" href="?page=catalogo">Catálogo</a>
      <a class="site-footer-link" href="?page=a_medida">Joyería a Medida</a>
      <a class="site-footer-link" href="https://wa.me/573014397403" target="_blank" rel="noopener noreferrer">Contacto</a>
    </div>
    <div>
      <div class="site-footer-title">Contacto</div>
      <div class="site-footer-contact">Bogotá D.C., Colombia<br><br>
      WhatsApp<br><a href="https://wa.me/573014397403" target="_blank" rel="noopener noreferrer">+57 301 439 7403</a><br><br>
      Correo<br><a href="mailto:admin@matallanavip.com">admin@matallanavip.com</a></div>
    </div>
  </div>
  <div class="site-footer-rule"></div>
  <div class="site-footer-bottom">
    <span>© {datetime.now().year} Joyería Matallana VIP · Bogotá, Colombia</span>
    <span>Esmeraldas colombianas · Alta joyería</span>
  </div>
</footer>
<a class="site-wa-fab" href="https://wa.me/573014397403" target="_blank" rel="noopener noreferrer" aria-label="Asesoría privada por WhatsApp">
  <svg viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
</a>
""",
        unsafe_allow_html=True,
    )
