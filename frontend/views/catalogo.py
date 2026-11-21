"""
Catálogo de Joyería.
"""
import sys
from pathlib import Path
from html import escape
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from api.client import api
from components.jewelry_360 import jewelry_360
from components.site_footer import render_footer
from utils.analytics import registrar_evento
from utils.session import agregar_al_carrito, esta_autenticado, contar_items_carrito
from utils.format import obtener_imagen_producto, formatear_precio, formatear_precio_corto, formatear_peso
from utils.styles import skeleton_catalogo


LEGACY_CATALOG_FIXES = {
    "Anillo Media Alianza Oro 14K": {
        "nombre": "Anillo sello de oro con escarabajo",
        "material": "Oro",
        "certificado_gemologico": "Por confirmar",
    },
    "Anillo Plata 925 con Cornalina": {
        "nombre": "Anillo de oro con cornalina",
        "material": "Oro",
        "gema": "Cornalina",
        "certificado_gemologico": "Por confirmar",
    },
    "Anillo Caballero Oro 18K": {
        "nombre": "Anillo de caballero con diamante negro",
        "gema": "Diamante negro",
    },
    "Anillo Platino 950 Hombre": {
        "nombre": "Anillo sello de oro con escarabajo de cornalina",
        "material": "Oro",
        "gema": "Cornalina",
        "certificado_gemologico": "Por confirmar",
    },
    "Anillo Plata 925 Hombre": {
        "nombre": "Anillo de oro con escarabajo",
        "material": "Oro",
        "certificado_gemologico": "Por confirmar",
    },
}


def _corregir_producto_legacy(prod):
    correccion = LEGACY_CATALOG_FIXES.get(prod.get("nombre"))
    return {**prod, **correccion} if correccion else prod


def _peso_y_etiqueta(prod):
    material = str(prod.get("material", "")).strip().lower()
    try:
        oro_18k = float(prod.get("oro_18k_g") or 0)
    except (TypeError, ValueError):
        oro_18k = 0
    if "oro 18k" in material:
        peso = oro_18k or prod.get("peso", 0)
        etiqueta = "Oro 18K"
    else:
        peso = prod.get("peso", 0)
        etiqueta = "Peso de la pieza"
    try:
        if float(peso or 0) <= 0:
            return "Por confirmar", etiqueta
    except (TypeError, ValueError):
        return "Por confirmar", etiqueta
    return formatear_peso(peso), etiqueta


def _gema_producto(prod):
    gema = str(prod.get("gema") or "").strip()
    if gema:
        return gema
    nombre = str(prod.get("nombre", "")).lower()
    for termino, etiqueta in (
        ("diamante negro", "Diamante negro"),
        ("diamante", "Diamante"),
        ("cornalina", "Cornalina"),
        ("esmeralda", "Esmeralda"),
        ("rubí", "Rubí"),
        ("rubi", "Rubí"),
        ("zafiro", "Zafiro"),
        ("topacio", "Topacio"),
        ("cuarzo", "Cuarzo"),
    ):
        if termino in nombre:
            return etiqueta
    return ""


def _producto_tiene_esmeralda(prod):
    try:
        quilates = float(prod.get("esmeralda_ct") or 0)
    except (TypeError, ValueError):
        quilates = 0
    return quilates > 0 or "esmeralda" in _gema_producto(prod).lower()


def _coincide_categoria(prod, categoria):
    tipos_por_categoria = {
        "Anillos": {"anillo", "anillos"},
        "Collares": {"cadena", "collar", "collares", "colgante"},
        "Aretes": {"aro", "aros", "arete", "aretes"},
        "Dijes": {"dije", "dijes"},
        "Manillas": {"manilla", "manillas"},
        "Pulseras": {"pulsera", "pulseras"},
    }
    if categoria == "Esmeraldas":
        return _producto_tiene_esmeralda(prod)
    tipo = str(prod.get("tipo", "")).strip().lower()
    return tipo in tipos_por_categoria.get(categoria, set())


def _solicitar_inicio_de_sesion(prod):
    st.session_state["compra_pendiente"] = prod
    st.session_state["auth_view"] = "registro"
    st.query_params["page"] = "mi_cuenta"
    st.rerun()


@st.dialog("Alta Resolución", width="large")
def modal_zoom():
    prod = st.session_state.get("producto_zoom")
    if not prod:
        st.stop()
    claro = st.session_state.get("modo_claro", True)
    titulo_color = "#25231F" if claro else "#F5F0E8"
    detalle_color = "#625D52" if claro else "#9A9080"
    c_img, c_info = st.columns([3, 2])
    with c_img:
        jewelry_360(prod, key=f"viewer_{prod.get('_id', 'joya')}")
        st.caption("Arrastra la pieza para inspeccionarla. Usa varias imágenes para una rotación 360° real.")
        if prod.get("video_url"):
            st.video(
                prod["video_url"],
                alt=f"Video de {prod.get('nombre', 'la pieza')}",
            )
        if prod.get("imagen_referencial"):
            st.caption("Fotografía referencial; no representa necesariamente la pieza exacta del inventario.")
    with c_info:
        nombre = escape(str(prod.get("nombre", "Joya")))
        st.markdown(
f'<div style="padding-bottom:16px;border-bottom:1px solid #222">'
f'<div style="font-size:.62rem;letter-spacing:.4em;color:{detalle_color};text-transform:uppercase;margin-bottom:8px">{escape(str(prod.get("tipo","")).capitalize())} · {escape(str(prod.get("genero","")).capitalize())}</div>'
f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.9rem;color:{titulo_color};font-weight:300;line-height:1.2">{nombre}</div>'
f'</div>'
f'<div style="padding:16px 0 12px;border-bottom:1px solid #222">'
f'<div style="font-size:.62rem;letter-spacing:.3em;color:#9A9080;text-transform:uppercase;margin-bottom:4px">Precio</div>'
f'<div class="price-tag">{formatear_precio(prod.get("precio",0))}</div>'
f'</div>',
            unsafe_allow_html=True
        )
        peso, etiqueta_peso = _peso_y_etiqueta(prod)
        specs = [
            ("Metal", str(prod.get("material") or "Por confirmar")),
            (etiqueta_peso, peso),
        ]
        esmeralda_ct = float(prod.get("esmeralda_ct", 0) or 0)
        gema = _gema_producto(prod)
        if esmeralda_ct > 0:
            specs.append(("Esmeralda", f"{esmeralda_ct:.2f} ct"))
            if prod.get("origen"):
                specs.append(("Origen", str(prod["origen"])))
        elif gema:
            specs.append(("Gema", gema))
        certificado = prod.get("certificado_gemologico") or (prod.get("certificado") or {}).get("calidad")
        if certificado:
            specs.append(("Certificado", str(certificado)))
        specs.append(("Disponibilidad", f"{prod.get('stock', 0)} unidades"))
        for lbl, val in specs:
            st.markdown(
f'<div class="spec-row"><span class="spec-lbl">{escape(lbl)}</span><span class="spec-val">{escape(val)}</span></div>',
                unsafe_allow_html=True
            )
        st.markdown(
f'<div style="margin:12px 0 20px"><span class="badge">{escape(str(prod.get("material","")))}</span><span class="badge">{escape(str(prod.get("tipo","")).capitalize())}</span></div>',
            unsafe_allow_html=True
        )
        if st.button("Agregar al carrito", type="primary", width="stretch"):
            if not esta_autenticado():
                _solicitar_inicio_de_sesion(prod)
            else:
                agregar_al_carrito(prod)
                st.toast("Agregado al carrito.", icon="✅")


def render():
    st.markdown(
'<div class="sec-head"><div class="sec-eye">Colección completa</div><div class="sec-title">Catálogo de Joyería</div><div class="sec-line"></div></div>',
        unsafe_allow_html=True
    )

    n = contar_items_carrito()
    if n > 0:
        st.markdown(f'<div style="margin-bottom:8px"><span class="badge">{n} artículo(s) en el carrito</span></div>', unsafe_allow_html=True)

    skel = st.empty()
    with skel.container():
        skeleton_catalogo()
    resultado = api.obtener_productos()
    skel.empty()

    if isinstance(resultado, dict) and "error" in resultado:
        st.error(f"No se pudo conectar: {resultado['error']}")
        st.info("Verifica que el backend esté corriendo: `cd backend && npm run dev`")
        render_footer()
        st.stop()

    productos = [
        _corregir_producto_legacy(p)
        for p in (resultado if isinstance(resultado, list) else [])
        if p.get("activo", True)
    ]
    if not productos:
        st.info("El catálogo está vacío.")
        render_footer()
        st.stop()

    cf1, cf2, cf3, cf4 = st.columns([1, 1, 1, 1])
    with cf1:
        categoria = st.selectbox(
            "Categoría",
            ["Todas", "Anillos", "Collares", "Dijes", "Manillas", "Pulseras", "Aretes", "Esmeraldas"],
            key="catalogo_categoria",
        )
    with cf2:
        metales = sorted({str(p.get("material", "")).strip() for p in productos if p.get("material")})
        metal_sel = st.selectbox("Metal", ["Todos"] + metales, key="catalogo_metal")
    with cf3:
        origenes = sorted({str(p.get("origen", "")).strip() for p in productos if p.get("origen")})
        origen_sel = st.selectbox("Origen", ["Todos"] + origenes, key="catalogo_origen")
    with cf4:
        busqueda = st.text_input(
            "Buscar",
            placeholder="Nombre o material",
            label_visibility="collapsed",
            key="catalogo_busqueda",
        )

    precios = [max(0, int(p.get("precio", 0) or 0)) for p in productos]
    precio_min, precio_max = min(precios, default=0), max(precios, default=0)
    if precio_min < precio_max:
        rango_precio = st.slider(
            "Rango de precio (COP)",
            min_value=precio_min,
            max_value=precio_max,
            value=(precio_min, precio_max),
            step=100_000,
            format="$%d",
            key="catalogo_precio",
        )
    else:
        rango_precio = (precio_min, precio_max)

    filtrados = productos
    if categoria != "Todas":
        filtrados = [p for p in filtrados if _coincide_categoria(p, categoria)]
    if metal_sel != "Todos":
        filtrados = [p for p in filtrados if str(p.get("material", "")).strip() == metal_sel]
    if origen_sel != "Todos":
        filtrados = [p for p in filtrados if str(p.get("origen", "")).strip() == origen_sel]
    filtrados = [
        p for p in filtrados
        if rango_precio[0] <= int(p.get("precio", 0) or 0) <= rango_precio[1]
    ]
    if busqueda.strip():
        q = busqueda.lower()
        filtrados = [
            p for p in filtrados
            if q in str(p.get("nombre", "")).lower()
            or q in str(p.get("material", "")).lower()
        ]

    st.markdown(
        f'<div style="color:#444;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;margin:8px 0 20px">{len(filtrados)} pieza(s)</div>',
        unsafe_allow_html=True,
    )

    for i in range(0, len(filtrados), 3):
        batch = filtrados[i:i+3]
        cols = st.columns(3, gap="small")
        claro = st.session_state.get("modo_claro", True)
        titulo_color = "#25231F" if claro else "#F5F0E8"
        detalle_color = "#625D52" if claro else "#9A9080"
        emphasis_color = "#333027" if claro else "#C8BFA8"
        for j, prod in enumerate(batch):
            pid    = prod.get("_id", str(i+j))
            img_url = obtener_imagen_producto(prod, size=600)
            nombre = str(prod.get("nombre", "Producto"))
            precio = prod.get("precio", 0)
            peso, etiqueta_peso = _peso_y_etiqueta(prod)
            mat    = str(prod.get("material", ""))
            tipo   = str(prod.get("tipo", ""))
            genero = str(prod.get("genero", ""))
            origen = str(prod.get("origen", ""))
            quilates = float(prod.get("esmeralda_ct", 0) or 0)
            gema = _gema_producto(prod)
            certificado = str(prod.get("certificado_gemologico") or
                              (prod.get("certificado") or {}).get("calidad") or "Por confirmar")
            stock  = prod.get("stock", 0)
            sin_stock = '<div style="position:absolute;top:12px;left:12px"><span class="badge" style="background:rgba(8,8,8,.8);color:#ef4444;border-color:rgba(239,68,68,.3)">Sin stock</span></div>' if stock == 0 else ""
            with cols[j]:
                st.markdown(
f'<div class="prod-card" style="animation-delay:{((i+j) % 3) * .08:.2f}s"><div class="prod-img"><img src="{escape(img_url, quote=True)}" alt="{escape(nombre, quote=True)}"><div class="prod-img-overlay"></div><div style="position:absolute;top:12px;right:12px"><span class="badge" style="background:rgba(8,8,8,.8)">{escape(tipo.capitalize())}</span></div>{sin_stock}</div></div>',
                    unsafe_allow_html=True
                )
                if prod.get("imagen_referencial"):
                    st.caption("Fotografía referencial")
                detalle_gema = (
                    f'<br>Esmeralda: <strong style="color:{emphasis_color}">{quilates:.2f} ct</strong>'
                    + (f' · {escape(origen)}' if origen else "")
                    if quilates > 0
                    else (f'<br>Gema: <strong style="color:{emphasis_color}">{escape(gema)}</strong>' if gema else "")
                )
                st.markdown(
f'<div style="padding:14px 2px 10px"><div style="font-family:\'Cormorant Garamond\',serif;font-size:1.15rem;color:{titulo_color};font-weight:400;margin-bottom:6px;line-height:1.2">{escape(nombre)}</div><div style="margin-bottom:8px"><span class="badge">{escape(mat)}</span><span class="badge">{escape(genero.capitalize())}</span></div><div style="color:{detalle_color};font-size:.75rem;line-height:1.8;margin-bottom:8px">{escape(etiqueta_peso)}: <strong style="color:{emphasis_color}">{peso}</strong>{detalle_gema}<br>Certificado: <strong style="color:{emphasis_color}">{escape(certificado)}</strong></div><div class="price-tag" style="font-size:1.25rem;margin-bottom:12px">{formatear_precio_corto(precio)} <span style="font-size:.7rem;color:#555">COP</span></div></div>',
                    unsafe_allow_html=True
                )
                b1, b2 = st.columns(2, gap="small")
                with b1:
                    if st.button("Detalle", key=f"z_{pid}", width="stretch"):
                        registrar_evento("producto", "catalogo", prod)
                        st.session_state["producto_zoom"] = prod
                        modal_zoom()
                with b2:
                    if st.button("Comprar", key=f"a_{pid}", type="primary", width="stretch", disabled=(stock == 0)):
                        if not esta_autenticado():
                            _solicitar_inicio_de_sesion(prod)
                        else:
                            agregar_al_carrito(prod)
                            st.toast(f"«{nombre}» agregado.", icon="✅")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    render_footer()
