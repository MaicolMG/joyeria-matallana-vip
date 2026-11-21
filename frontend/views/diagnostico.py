"""
Panel de Diagnostico del sistema.
"""
import sys
from pathlib import Path
from html import escape
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import requests
from datetime import datetime
from api.client import api
from utils.session import esta_autenticado


def render():
    st.markdown(
'<div style="padding:20px 0 8px">'
'<div style="font-family:\'Cormorant Garamond\',serif;font-size:2.2rem;color:#D4AF37;letter-spacing:.06em">Diagnostico del Sistema</div>'
'<div style="color:#9A9080;font-size:.82rem;margin-top:4px">Auto-analisis en tiempo real</div>'
'</div><hr style="border-color:#222;margin-bottom:20px">',
        unsafe_allow_html=True
    )

    if not st.button("Ejecutar diagnostico completo", type="primary"):
        st.markdown('<div style="text-align:center;padding:60px 20px;color:#9A9080">Presiona el boton para verificar que todo el sistema este funcionando.</div>', unsafe_allow_html=True)
        return

    resultados = []

    def check(nombre, ok, detalle=""):
        resultados.append(("OK" if ok else "ERROR", nombre, detalle, ok))

    # 1. Backend
    try:
        r = requests.get(f"{api.base_url}/productos", timeout=5)
        check("Backend Node.js/Express", r.status_code == 200, f"HTTP {r.status_code}")
    except requests.exceptions.RequestException:
        check("Backend Node.js/Express", False, "No se pudo conectar con la API")

    # 2. Productos en BD
    prods = api.obtener_productos()
    if isinstance(prods, list):
        check("Productos en base de datos", len(prods) > 0, f"{len(prods)} productos")
        check("Productos con stock", any(p.get("stock", 0) > 0 for p in prods),
              f"{sum(1 for p in prods if p.get('stock',0)>0)} con stock")
    else:
        check("Productos en base de datos", False, str(prods))

    # 3. Acceso de administrador con la sesión actual, sin credenciales de prueba
    if esta_autenticado() and (st.session_state.get("user") or {}).get("rol") == "admin":
        admin_productos = api.admin_productos()
        check(
            "Acceso de administrador",
            isinstance(admin_productos, list),
            "Sesión administrativa verificada" if isinstance(admin_productos, list)
            else "La API rechazó la sesión administrativa",
        )
    else:
        check("Acceso de administrador", False, "No hay una sesión admin verificada")

    # 4. Ruta admin protegida
    try:
        r2 = requests.get(f"{api.base_url}/admin/productos", timeout=5)
        check("Ruta /api/admin protegida", r2.status_code in (401, 403),
              f"Sin token -> HTTP {r2.status_code}")
    except requests.exceptions.RequestException:
        check("Ruta /api/admin protegida", False, "No se pudo conectar con la API")

    # 5. Archivos clave
    base = Path(__file__).resolve().parent.parent
    for archivo in ["app.py", "views/home.py", "views/catalogo.py", "views/carrito.py",
                    "views/auth.py", "views/personalizador.py", "views/admin.py",
                    "utils/session.py", "utils/format.py", "api/client.py"]:
        check(f"Archivo {archivo}", (base / archivo).exists())

    # Resultados
    total = len(resultados)
    exitosos = sum(1 for _, _, _, ok in resultados if ok)
    pct = int(exitosos / total * 100)
    color = "#22c55e" if pct == 100 else "#f59e0b" if pct >= 80 else "#ef4444"

    st.markdown(
f'<div style="background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.25);padding:24px;margin:16px 0;text-align:center">'
f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:3rem;color:{color};font-weight:700">{pct}%</div>'
f'<div style="color:#9A9080;font-size:.8rem;letter-spacing:.15em;text-transform:uppercase;margin-top:4px">{exitosos} de {total} verificaciones pasadas</div>'
f'</div>',
        unsafe_allow_html=True
    )

    for icono, nombre, detalle, ok in resultados:
        bg  = "rgba(34,197,94,.06)"  if ok else "rgba(239,68,68,.06)"
        brd = "rgba(34,197,94,.2)"   if ok else "rgba(239,68,68,.2)"
        sym = "✓" if ok else "✗"
        st.markdown(
f'<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 16px;margin:3px 0;background:{bg};border-left:3px solid {brd}">'
f'<span style="font-size:.85rem;color:#F8F6F0">{escape(str(sym + " " + nombre))}</span>'
f'<span style="font-size:.72rem;color:#9A9080">{escape(str(detalle))}</span>'
f'</div>',
            unsafe_allow_html=True
        )

    if pct == 100:
        st.success("Sistema al 100% — listo para produccion.")
        st.balloons()
    elif pct >= 80:
        st.warning(f"Sistema al {pct}% — revisa los puntos marcados.")
    else:
        st.error(f"Sistema al {pct}% — hay problemas criticos.")

    st.caption(f"Diagnostico: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
