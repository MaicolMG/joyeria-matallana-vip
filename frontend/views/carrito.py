"""
Carrito, datos de entrega y creación de órdenes pendientes.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from api.client import api
from utils.analytics import sesion_anonima
from utils.format import formatear_precio, formatear_peso
from utils.session import (
    actualizar_cantidad,
    contar_items_carrito,
    eliminar_del_carrito,
    esta_autenticado,
    vaciar_carrito,
)


_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_TELEFONO = re.compile(r"^\+?[\d\s()-]{7,24}$")
_METODOS_PAGO = {
    "Transferencia bancaria": "transferencia",
    "PSE": "pse",
    "Tarjeta": "tarjeta",
    "Contraentrega asegurada": "contraentrega",
    "Reserva en sala VIP": "reserva_vip",
}


def _resumen_orden(orden):
    lineas = [
        "MATALLANA VIP — COMPROBANTE DE PEDIDO",
        f"Orden: {orden['numero']}",
        f"Estado: {orden['estado'].upper()} (sin cobro en línea)",
        f"Fecha: {orden['fecha']}",
        "",
        "PIEZAS",
    ]
    lineas.extend(orden["items"])
    lineas.extend([
        "",
        f"Envío asegurado: {orden['envio']}",
        f"Descuento: {orden['descuento']}",
        f"Total pendiente de confirmación: {orden['total']}",
        f"Método solicitado: {orden['metodo']}",
        "",
        "El pago no fue procesado. Un asesor confirmará disponibilidad, envío y pago.",
    ])
    return "\n".join(lineas)


def render():
    st.markdown(
        '<div class="sec-head"><div class="sec-eye">Selección privada</div>'
        '<div class="sec-title">Tu carrito</div><div class="sec-line"></div></div>',
        unsafe_allow_html=True,
    )
    carrito = st.session_state.get("carrito", [])
    if not carrito:
        st.info("Tu carrito está vacío. Explora el catálogo para elegir una pieza.")
        orden_guardada = st.session_state.get("comprobante_orden")
        if orden_guardada:
            st.success(f"Pedido registrado: {orden_guardada['numero']}")
            st.download_button(
                "Descargar comprobante",
                data=_resumen_orden(orden_guardada),
                file_name=f"{orden_guardada['numero']}.txt",
                mime="text/plain",
                width="content",
            )
        return

    subtotal = 0
    for item in carrito:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.markdown(f"**{item.get('nombre', 'Pieza')}**")
                st.caption(
                    f"{item.get('material', '')} · {item.get('tipo', '').capitalize()} · "
                    f"{formatear_peso(item.get('oro_18k_g', item.get('peso', 0)))} de oro 18K · "
                    f"{float(item.get('esmeralda_ct', 0) or 0):.2f} ct"
                )
                st.caption(f"Precio unitario: {formatear_precio(item.get('precio', 0))}")
            with c2:
                quantity = st.number_input(
                    "Cantidad",
                    min_value=1,
                    max_value=99,
                    value=int(item.get("cantidad", 1)),
                    key=f"cantidad_{item['producto_id']}",
                )
                if quantity != item.get("cantidad"):
                    actualizar_cantidad(item["producto_id"], quantity)
                    st.rerun()
            with c3:
                total_linea = float(item.get("precio", 0)) * int(item.get("cantidad", 1))
                subtotal += total_linea
                st.markdown("**Subtotal**")
                st.write(formatear_precio(total_linea))
                if st.button("Retirar", key=f"retirar_{item['producto_id']}"):
                    eliminar_del_carrito(item["producto_id"])
                    st.rerun()

    gramos = sum(
        float(item.get("oro_18k_g", item.get("peso", 0)) or 0) * int(item["cantidad"])
        for item in carrito
    )
    quilates = sum(
        float(item.get("esmeralda_ct", 0) or 0) * int(item["cantidad"])
        for item in carrito
    )
    st.markdown("#### Resumen")
    total_col, detalle_col = st.columns([1, 2])
    total_col.metric("Subtotal piezas", formatear_precio(subtotal))
    with detalle_col:
        st.write(f"Peso total de oro 18K: **{formatear_peso(gramos)}**")
        st.write(f"Esmeraldas: **{quilates:.2f} ct**")
        st.caption("El costo del envío asegurado se confirma según destino antes de cobrar.")
    if st.button("Vaciar carrito", type="secondary"):
        vaciar_carrito()
        st.rerun()

    if not esta_autenticado():
        st.info("Inicia sesión para continuar con los datos de entrega.")
        return

    with st.expander("Datos de entrega y confirmación", expanded=True):
        user = st.session_state.get("user") or {}
        with st.form("checkout_pendiente"):
            nombre = st.text_input("Nombre completo", value=user.get("nombre", ""), max_chars=120)
            email = st.text_input("Correo electrónico", value=user.get("email", ""), max_chars=254)
            telefono = st.text_input("Teléfono de contacto", max_chars=24)
            direccion = st.text_input("Dirección de entrega", max_chars=180)
            ciudad = st.text_input("Ciudad", max_chars=80)
            departamento = st.text_input("Departamento", max_chars=80)
            notas = st.text_area("Indicaciones de entrega (opcional)", max_chars=500)
            metodo_label = st.selectbox("Método de pago solicitado", list(_METODOS_PAGO))
            codigo = st.text_input("Código promocional (opcional)", max_chars=40)
            st.caption(
                "La orden queda pendiente. Esta app no captura pagos ni confirma "
                "transacciones PSE o de tarjeta."
            )
            enviar = st.form_submit_button(
                "Crear pedido pendiente",
                type="primary",
                width="stretch",
            )

    if enviar:
        email_limpio = email.strip().lower()
        if (
            not nombre.strip()
            or not _EMAIL.fullmatch(email_limpio)
            or not _TELEFONO.fullmatch(telefono.strip())
            or not direccion.strip()
            or not ciudad.strip()
            or not departamento.strip()
        ):
            st.error("Completa los datos de contacto y entrega con un correo y teléfono válidos.")
            return

        payload = {
            "items": [
                {"producto_id": item["producto_id"], "cantidad": int(item["cantidad"])}
                for item in carrito
            ],
            "metodoPago": _METODOS_PAGO[metodo_label],
            "codigoPromocional": codigo.strip(),
            "sesionAnonima": sesion_anonima(),
            "datosEnvio": {
                "nombre": nombre.strip(),
                "email": email_limpio,
                "telefono": telefono.strip(),
                "direccion": direccion.strip(),
                "ciudad": ciudad.strip(),
                "departamento": departamento.strip(),
                "notas": notas.strip(),
            },
        }
        with st.spinner("Verificando existencias y creando tu pedido..."):
            response = api.crear_orden(payload)
        if isinstance(response, dict) and response.get("error"):
            st.error(f"No se pudo crear el pedido: {response['error']}")
            return
        if not isinstance(response, dict) or not response.get("numero"):
            st.error("La API no devolvió un número de pedido válido.")
            return

        receipt = {
            "numero": response["numero"],
            "estado": response.get("estado", "pendiente"),
            "fecha": response.get("fecha", ""),
            "items": [
                f"{item['cantidad']} × {item['nombre']} — "
                f"{formatear_precio(float(item['precio']) * int(item['cantidad']))}"
                for item in carrito
            ],
            "envio": formatear_precio(response.get("envioAsegurado", 0)),
            "descuento": formatear_precio(response.get("descuento", 0)),
            "total": formatear_precio(response.get("total", subtotal)),
            "metodo": metodo_label,
        }
        st.session_state["comprobante_orden"] = receipt
        vaciar_carrito()
        st.success(f"Pedido {receipt['numero']} registrado como pendiente.")
        st.info("No se realizó ningún cobro. El equipo confirmará envío, disponibilidad y pago.")
        st.download_button(
            "Descargar comprobante",
            data=_resumen_orden(receipt),
            file_name=f"{receipt['numero']}.txt",
            mime="text/plain",
            width="content",
        )
