"""
Joyería a Medida — configurador paso a paso.
"""
import sys
from pathlib import Path
from urllib.parse import urlencode
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from components.site_footer import render_footer
from utils.analytics import registrar_evento
from utils.format import (
    PRECIOS_METAL, PRECIOS_GEMA, PESO_BASE, TALLAS_ANILLO, TALLAS_CADENA,
    COSTO_GRABADO, MARGEN_MANO_OBRA,
    formatear_precio, formatear_peso, calcular_presupuesto,
)


def render():
    for k, v in {
        "custom_tipo": "anillo", "custom_metal": "oro_18k",
        "custom_gema": "esmeralda_colombiana", "custom_quilates": 0.25,
        "custom_grabado": False, "custom_texto_grabado": "",
        "custom_talla": "14", "custom_genero": "unisex",
        "custom_oro_color": "Amarillo", "custom_origen": "Muzo",
        "custom_calidad": "Por certificar", "custom_talla_gema": "Esmeralda",
        "paso_personalizador": 1,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

    c_tipo  = st.session_state["custom_tipo"]
    c_metal = st.session_state["custom_metal"]
    c_gema  = st.session_state["custom_gema"]
    c_quilat = st.session_state["custom_quilates"]
    c_grab  = st.session_state["custom_grabado"]
    paso    = st.session_state["paso_personalizador"]
    oro_color = st.session_state["custom_oro_color"]
    origen = st.session_state["custom_origen"]
    calidad = st.session_state["custom_calidad"]
    talla_gema = st.session_state["custom_talla_gema"]

    st.markdown(
'<div style="padding:20px 0 8px">'
'<div style="font-family:\'Cormorant Garamond\',serif;font-size:2.2rem;color:#D4AF37;letter-spacing:.06em">Joyer\u00eda a Medida</div>'
'<div style="color:#9A9080;font-size:.85rem;margin-top:4px">Dise\u00f1a tu pieza \u00fanica paso a paso \u00b7 Presupuesto en tiempo real</div>'
'</div><hr style="border-color:#2E2E2E;margin:12px 0 20px">',
        unsafe_allow_html=True
    )

    pasos_nombres = ["Tipo de Joya", "Material", "Gema", "Acabados y Talla"]
    st.progress(paso / 4, text=f"Paso {paso} de 4 — {pasos_nombres[paso-1]}")
    st.markdown("<br>", unsafe_allow_html=True)

    # PASO 1
    if paso == 1:
        st.markdown("### 1. Tipo de joya")
        iconos = {"anillo": "Anillo", "cadena": "Cadena", "manilla": "Manilla",
                  "pulsera": "Pulsera", "aro": "Aro", "colgante": "Colgante", "dije": "Dije"}
        cols = st.columns(len(PESO_BASE))
        for col, tipo in zip(cols, PESO_BASE.keys()):
            with col:
                if st.button(iconos.get(tipo, tipo).capitalize(),
                             width="stretch",
                             type="primary" if c_tipo == tipo else "secondary",
                             key=f"tipo_{tipo}"):
                    st.session_state["custom_tipo"] = tipo
                    st.rerun()
        st.markdown(
f'<div style="background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.2);border-radius:8px;padding:14px;margin-top:16px;font-size:.85rem;color:#C8BFA8">Peso base estimado: <strong style="color:#F5F0E8">{formatear_peso(PESO_BASE[c_tipo])}</strong></div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>**Para quien es?**")
        genero = st.radio("Seccion", ["hombre", "mujer", "unisex"],
                          format_func=lambda g: {"hombre": "Hombre", "mujer": "Mujer", "unisex": "Unisex"}[g],
                          horizontal=True, label_visibility="collapsed",
                          index=["hombre", "mujer", "unisex"].index(st.session_state.get("custom_genero", "unisex")))
        st.session_state["custom_genero"] = genero

    # PASO 2
    elif paso == 2:
        st.markdown("### 2. Material")
        for mk, mv in PRECIOS_METAL.items():
            sel = (c_metal == mk)
            with st.container(border=sel):
                c1, c2 = st.columns([3, 2])
                with c1:
                    lbl = ("[SEL] " if sel else "") + mv["nombre"]
                    if st.button(lbl, type="primary" if sel else "secondary",
                                 width="stretch", key=f"metal_{mk}"):
                        st.session_state["custom_metal"] = mk
                        st.rerun()
                with c2:
                    st.markdown(f'<div style="color:#D4AF37;font-size:.9rem;padding:8px 0">{formatear_precio(mv["precio_gramo"])} / gramo</div>', unsafe_allow_html=True)
        costo_m = PESO_BASE[c_tipo] * PRECIOS_METAL[c_metal]["precio_gramo"]
        st.markdown(f'<div style="background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.2);border-radius:8px;padding:14px;margin-top:16px;font-size:.85rem;color:#C8BFA8">Costo estimado del metal: <strong style="color:#D4AF37">{formatear_precio(costo_m)}</strong></div>', unsafe_allow_html=True)
        if c_metal == "oro_18k":
            oro_color_sel = st.segmented_control(
                "Color del oro 18K",
                ["Amarillo", "Blanco", "Rosa"],
                key="custom_oro_color",
            )
            oro_color = oro_color_sel or oro_color

    # PASO 3
    elif paso == 3:
        st.markdown("### 3. Gema")
        st.markdown('<div style="background:rgba(0,150,80,.08);border:1px solid rgba(0,180,100,.2);border-radius:6px;padding:10px 14px;margin-bottom:14px;font-size:.82rem;color:#88C899">Colombia es el mayor productor mundial de esmeraldas. Las de Muzo y Chivor (Boyaca) son las mas cotizadas del planeta.</div>', unsafe_allow_html=True)
        gemas = list(PRECIOS_GEMA.keys())
        gema_sel = st.selectbox("Tipo de gema", gemas, index=gemas.index(c_gema),
                                format_func=lambda k: PRECIOS_GEMA[k]["nombre"])
        if gema_sel != c_gema:
            st.session_state["custom_gema"] = gema_sel
            st.rerun()
        if gema_sel != "ninguna":
            quilates = st.number_input("Tamano en quilates (1 ct = 0.20 g)",
                                       min_value=0.10, max_value=5.0,
                                       value=float(c_quilat), step=0.05, format="%.2f")
            st.session_state["custom_quilates"] = quilates
            origen_sel = st.selectbox(
                "Origen de la esmeralda",
                ["Muzo", "Chivor", "Coscuez"],
                index=["Muzo", "Chivor", "Coscuez"].index(origen),
                key="custom_origen",
            )
            calidad_sel = st.selectbox(
                "Calidad solicitada",
                ["Por certificar", "Comercial", "Fina", "Alta"],
                index=["Por certificar", "Comercial", "Fina", "Alta"].index(calidad),
                key="custom_calidad",
            )
            talla_sel = st.selectbox(
                "Talla de la gema",
                ["Esmeralda", "Oval", "Redonda", "Pera"],
                index=["Esmeralda", "Oval", "Redonda", "Pera"].index(talla_gema),
                key="custom_talla_gema",
            )
            pq = PRECIOS_GEMA[gema_sel]["precio_quilate"]
            st.markdown(f'<div style="background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.2);border-radius:8px;padding:14px;font-size:.85rem;color:#C8BFA8">{quilates:.2f} ct x {formatear_precio(pq)}/ct = <strong style="color:#D4AF37">{formatear_precio(quilates * pq)}</strong></div>', unsafe_allow_html=True)
            st.caption("Origen y calidad se validan con el certificado gemológico de la piedra.")
        else:
            st.session_state["custom_quilates"] = 0.0
            origen_sel, calidad_sel, talla_sel = "No aplica", "No aplica", "No aplica"

    # PASO 4
    elif paso == 4:
        st.markdown("### 4. Acabados y Talla")
        grabar = st.checkbox(f"Agregar grabado (+{formatear_precio(COSTO_GRABADO)})", value=c_grab)
        st.session_state["custom_grabado"] = grabar
        if grabar:
            texto = st.text_input("Texto a grabar (max. 30 caracteres)",
                                  value=st.session_state.get("custom_texto_grabado", ""),
                                  max_chars=30, placeholder="Ej. Para siempre · 14.02.2025")
            st.session_state["custom_texto_grabado"] = texto
        st.markdown("<br>**Talla / Medida:**")
        if c_tipo == "anillo":
            talla = st.selectbox("Talla del anillo", TALLAS_ANILLO,
                                 index=TALLAS_ANILLO.index(st.session_state["custom_talla"])
                                 if st.session_state["custom_talla"] in TALLAS_ANILLO else 6)
        elif c_tipo in ("cadena", "pulsera"):
            talla = st.selectbox("Longitud", TALLAS_CADENA,
                                 index=TALLAS_CADENA.index(st.session_state["custom_talla"])
                                 if st.session_state["custom_talla"] in TALLAS_CADENA else 1)
        else:
            talla = st.text_input("Medida personalizada", value=st.session_state["custom_talla"],
                                  placeholder="Ej. 70 mm diametro")
        st.session_state["custom_talla"] = talla

    # PRESUPUESTO
    presupuesto = calcular_presupuesto(c_tipo, c_metal, c_gema, c_quilat, c_grab)
    if st.session_state.get("modo_claro", True):
        resumen_label = "#5F5B50"
        resumen_valor = "#25231F"
        resumen_borde = "#DED6C3"
        total_color = "#8B681F"
    else:
        resumen_label = "#B7AD98"
        resumen_valor = "#F5F0E8"
        resumen_borde = "#38352D"
        total_color = "#D8BD70"
    st.markdown("<hr style='border-color:#2E2E2E;margin:24px 0 16px'>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;color:#D4AF37;margin-bottom:12px">Presupuesto Estimado en Tiempo Real</div>', unsafe_allow_html=True)

    with st.container(border=True):
        cc1, cc2 = st.columns(2)
        with cc1:
            for lbl, val in [
                (f"Metal — {PRECIOS_METAL[c_metal]['nombre']} ({formatear_peso(presupuesto['peso_estimado'])})", presupuesto["costo_metal"]),
                (f"Gema — {PRECIOS_GEMA[c_gema]['nombre']}", presupuesto["costo_gema"]),
                ("Grabado personalizado", presupuesto["costo_grabado"]),
            ]:
                st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid {resumen_borde};font-size:.88rem"><span style="color:{resumen_label}">{lbl}</span><span style="color:{resumen_valor};font-weight:700;white-space:nowrap">{formatear_precio(val)}</span></div>', unsafe_allow_html=True)
        with cc2:
            for lbl, val in [
                ("Subtotal materiales", presupuesto["costo_materiales"]),
                (f"Mano de obra ({int(MARGEN_MANO_OBRA*100)}%)", presupuesto["mano_obra"]),
            ]:
                st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid {resumen_borde};font-size:.88rem"><span style="color:{resumen_label}">{lbl}</span><span style="color:{resumen_valor};font-weight:700;white-space:nowrap">{formatear_precio(val)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex;justify-content:space-between;gap:12px;padding:14px 0 4px"><span style="color:{resumen_label};font-weight:600;font-size:.95rem">TOTAL ESTIMADO</span><span style="color:{total_color};font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;font-weight:600;white-space:nowrap">{formatear_precio(presupuesto["total"])}</span></div>', unsafe_allow_html=True)
        st.caption("Estimacion referencial. El precio final se confirma tras cotizacion oficial.")

    # NAVEGACION
    st.markdown("<br>", unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns([1, 1, 2])
    with nav1:
        if paso > 1:
            if st.button("Anterior", width="stretch"):
                st.session_state["paso_personalizador"] = paso - 1
                st.rerun()
    with nav2:
        if paso < 4:
            if st.button("Siguiente", type="primary", width="stretch"):
                st.session_state["paso_personalizador"] = paso + 1
                st.rerun()
    with nav3:
        if paso == 4:
            oro_seleccionado = PRECIOS_METAL[c_metal]["nombre"]
            if c_metal == "oro_18k":
                oro_seleccionado = f"Oro 18K {oro_color}"
            texto = "\n".join([
                "Hola, quiero cotizar una joya a medida:",
                f"Tipo: {c_tipo.capitalize()}",
                f"Metal: {oro_seleccionado}",
                f"Gema: {PRECIOS_GEMA[c_gema]['nombre']}",
                f"Quilates: {c_quilat:.2f} ct",
                f"Origen: {origen}",
                f"Calidad solicitada: {calidad}",
                f"Talla de la gema: {talla_gema}",
                f"Grabado: {st.session_state['custom_texto_grabado'] if c_grab else 'No'}",
                f"Talla de la pieza: {st.session_state['custom_talla']}",
                f"Sección: {st.session_state['custom_genero']}",
                f"Presupuesto referencial: {formatear_precio(presupuesto['total'])}",
            ])
            wa_url = "https://wa.me/573014397403?" + urlencode({"text": texto})
            if st.button(
                "Cotizar pieza por WhatsApp",
                type="primary",
                width="stretch",
                key="registrar_cotizacion",
            ):
                registrar_evento("cotizacion", "a_medida")
                st.session_state["cotizacion_lista"] = True
            if st.session_state.get("cotizacion_lista"):
                st.link_button(
                    "Abrir WhatsApp con la cotización",
                    wa_url,
                    width="stretch",
                )
    render_footer()
