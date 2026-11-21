"""
Panel de administración de inventario, caja y actividad.
"""
import sys
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from api.client import api
from utils.format import formatear_precio, formatear_precio_corto, formatear_peso
from utils.session import esta_autenticado


def _imagen_urls(texto):
    urls = []
    for linea in texto.splitlines():
        url = linea.strip()
        if not url:
            continue
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Cada imagen debe tener una URL http(s) válida.")
        urls.append(url)
    if len(urls) > 36:
        raise ValueError("Puedes registrar hasta 36 imágenes por pieza.")
    return urls


def _validar_video_url(url):
    url = url.strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("El video debe usar una URL https válida.")
    return url


def _subir_archivos(producto_id, archivos):
    if not archivos:
        return True
    if len(archivos) > 8:
        st.error("Puedes subir hasta 8 imágenes por operación.")
        return False
    for archivo in archivos:
        if archivo.size > 1_000_000:
            st.error(f"{archivo.name}: el tamaño máximo por imagen es 1 MB.")
            return False

    correcto = True
    for archivo in archivos:
        response = api.admin_subir_imagen(
            producto_id,
            archivo.getvalue(),
            archivo.type,
        )
        if isinstance(response, dict) and response.get("error"):
            st.error(f"{archivo.name}: {response['error']}")
            correcto = False
    return correcto


@st.dialog("Editar pieza", width="large")
def _editar_pieza_dialog(producto):
    with st.form(f"editar_producto_{producto['_id']}"):
        nombre = st.text_input("Nombre", value=producto.get("nombre", ""), max_chars=120)
        tipo = st.selectbox(
            "Categoría",
            ["anillo", "cadena", "colgante", "dije", "aro", "arete", "pulsera", "manilla", "esmeralda"],
            index=(
                ["anillo", "cadena", "colgante", "dije", "aro", "arete", "pulsera", "manilla", "esmeralda"]
                .index(producto.get("tipo", "anillo"))
                if producto.get("tipo", "anillo") in
                ["anillo", "cadena", "colgante", "dije", "aro", "arete", "pulsera", "manilla", "esmeralda"]
                else 0
            ),
        )
        material = st.text_input("Metal", value=producto.get("material", ""), max_chars=80)
        c1, c2, c3 = st.columns(3)
        with c1:
            precio = st.number_input("Precio COP", min_value=0, value=int(producto.get("precio", 0)), step=50_000)
            costo_unitario = st.number_input(
                "Costo de compra o fabricación por unidad (COP)",
                min_value=0,
                value=int(producto.get("costo_unitario") or 0),
                step=50_000,
                help="Regístralo para calcular la utilidad; déjalo en 0 si no lo conoces.",
            )
            peso = st.number_input(
                "Peso total (g)",
                min_value=0.0,
                value=float(producto.get("peso", 0)),
                step=0.1,
            )
        with c2:
            oro_18k_g = st.number_input("Oro 18K (g)", min_value=0.0, value=float(producto.get("oro_18k_g", producto.get("peso", 0))), step=0.1)
            esmeralda_ct = st.number_input("Esmeralda (ct)", min_value=0.0, value=float(producto.get("esmeralda_ct", 0)), step=0.05)
        with c3:
            origen = st.selectbox(
                "Origen",
                ["Por confirmar", "Muzo", "Chivor", "Coscuez"],
                index=["Por confirmar", "Muzo", "Chivor", "Coscuez"].index(
                    producto.get("origen") if producto.get("origen") in
                    {"Muzo", "Chivor", "Coscuez"} else "Por confirmar"
                ),
            )
            stock = st.number_input("Stock", min_value=0, value=int(producto.get("stock", 0)))
        imagen = st.text_input("Imagen principal (URL)", value=producto.get("imagen", ""), max_chars=2048)
        video_url = st.text_input(
            "Video de la pieza (URL https opcional)",
            value=producto.get("video_url", ""),
            max_chars=2048,
            help="Pega un enlace https de un video MP4 o YouTube.",
        )
        imagenes = st.text_area(
            "Imágenes para rotación 360° (una URL http(s) por línea)",
            value="\n".join(producto.get("imagenes_360") or []),
            height=120,
        )
        certificado = st.text_input(
            "Certificado gemológico",
            value=producto.get("certificado_gemologico", ""),
            max_chars=160,
        )
        guardar = st.form_submit_button("Guardar cambios", type="primary", width="stretch")
    archivos = st.file_uploader(
        "Añadir imágenes al visor 360°",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        key=f"imagenes_edit_{producto['_id']}",
    )

    if guardar:
        try:
            imagenes_360 = _imagen_urls(imagenes)
            video_url = _validar_video_url(video_url)
        except ValueError as error:
            st.error(str(error))
            return
        if not nombre.strip() or precio <= 0:
            st.error("El nombre y un precio mayor que cero son obligatorios.")
            return
        response = api.admin_editar_producto(producto["_id"], {
            "nombre": nombre.strip(),
            "tipo": tipo,
            "material": material.strip(),
            "precio": precio,
            "costo_unitario": costo_unitario or None,
            "peso": peso,
            "oro_18k_g": oro_18k_g,
            "esmeralda_ct": esmeralda_ct,
            "origen": origen if origen != "Por confirmar" else "",
            "certificado_gemologico": certificado.strip(),
            "stock": stock,
            "imagen": imagen.strip(),
            "video_url": video_url,
            "imagenes_360": imagenes_360,
        })
        if isinstance(response, dict) and response.get("error"):
            st.error(response["error"])
        else:
            imagenes_correctas = _subir_archivos(producto["_id"], archivos)
            if imagenes_correctas:
                st.success("Pieza actualizada.")
            st.rerun()


@st.fragment(run_every="15s")
def _pedidos():
    respuesta = api.admin_ordenes()
    if isinstance(respuesta, dict) and respuesta.get("error"):
        st.error(f"No se pudieron cargar los pedidos: {respuesta['error']}")
        return
    if not isinstance(respuesta, list):
        st.error("La API devolvió una respuesta de pedidos no válida.")
        return

    pedidos = respuesta
    pendientes = [pedido for pedido in pedidos if pedido.get("estado") == "pendiente"]
    st.info(
        "Los pedidos del sitio quedan pendientes porque no se cobra en línea. "
        "Confirma el pago manualmente antes de marcar una venta como procesada."
    )
    metricas = st.columns(3)
    metricas[0].metric("Pedidos pendientes", len(pendientes))
    metricas[1].metric(
        "Valor pendiente",
        formatear_precio(sum(float(p.get("total", 0) or 0) for p in pendientes)),
    )
    metricas[2].metric(
        "Pedidos confirmados",
        sum(p.get("estado") in {"procesado", "enviado"} for p in pedidos),
    )

    if not pedidos:
        st.caption("Aún no hay pedidos registrados.")
        return

    st.subheader("Pedidos recibidos")
    for pedido in pedidos:
        numero = escape(str(pedido.get("numero", "Pedido")))
        estado = str(pedido.get("estado", "pendiente"))
        envio = pedido.get("datosEnvio") or {}
        with st.container(border=True):
            titulo, total = st.columns([3, 1])
            titulo.markdown(f"**{numero} · {escape(estado.capitalize())}**")
            titulo.caption(
                f"{escape(str(pedido.get('fecha', ''))[:19].replace('T', ' '))} · "
                f"Pago solicitado: {escape(str(pedido.get('metodoPago', '')))}"
            )
            total.metric("Total", formatear_precio(pedido.get("total", 0)))

            st.write(
                f"**Cliente:** {escape(str(envio.get('nombre', '')))} · "
                f"{escape(str(envio.get('email', '')))} · "
                f"{escape(str(envio.get('telefono', '')))}"
            )
            st.caption(
                f"Entrega: {escape(str(envio.get('direccion', '')))}, "
                f"{escape(str(envio.get('ciudad', '')))}, "
                f"{escape(str(envio.get('departamento', '')))}"
            )
            for item in pedido.get("items", []):
                st.write(
                    f"{int(item.get('cantidad', 0) or 0)} × "
                    f"{escape(str(item.get('nombre', 'Pieza')))} · "
                    f"{formatear_precio(item.get('precio', 0))}"
                )

            siguiente_estado = {
                "pendiente": ("procesado", "Confirmar pago recibido"),
                "procesado": ("enviado", "Marcar pedido enviado"),
            }.get(estado)
            if siguiente_estado:
                estado_destino, etiqueta = siguiente_estado
                if st.button(
                    etiqueta,
                    key=f"avanzar_pedido_{pedido.get('_id')}",
                    type="primary" if estado == "pendiente" else "secondary",
                ):
                    resultado = api.admin_actualizar_estado_orden(
                        str(pedido.get("_id", "")),
                        estado_destino,
                    )
                    if isinstance(resultado, dict) and resultado.get("error"):
                        st.error(f"No se pudo actualizar el pedido: {resultado['error']}")
                    elif not isinstance(resultado, dict) or resultado.get("estado") != estado_destino:
                        st.error("La API no confirmó el cambio de estado del pedido.")
                    else:
                        st.success("Estado del pedido actualizado.")
                        st.rerun()


@st.fragment(run_every="15s")
def _centro_notificaciones():
    response = api.admin_analitica()
    if isinstance(response, dict) and response.get("error"):
        st.error(f"No se pudo cargar la actividad: {response['error']}")
        return

    response = response if isinstance(response, dict) else {}
    metricas = st.columns(4)
    metricas[0].metric("Visitas de hoy", response.get("visitasHoy", 0))
    metricas[1].metric("Ingresos confirmados del mes", formatear_precio_corto(response.get("ingresosMes", 0)))
    notificaciones = response.get("notificaciones", [])
    sin_leer = response.get("alertasSinLeer", 0)
    metricas[2].metric("Alertas sin leer", sin_leer)
    metricas[3].metric("Pedidos por revisar", response.get("pedidosPendientes", 0))
    st.markdown(f"#### :material/notifications: Centro de alertas · {sin_leer} sin leer")

    st.markdown("#### Piezas más consultadas")
    populares = response.get("piezasPopulares", [])
    if populares:
        for pieza in populares:
            st.write(f"{pieza.get('_id', 'Pieza')} · {pieza.get('vistas', 0)} vistas")
    else:
        st.caption("Aún no hay consultas registradas.")

    st.markdown("#### Actividad reciente")
    if not notificaciones:
        st.caption("No hay alertas nuevas.")
        return

    etiquetas = {
        "visita": "Nueva visita",
        "producto": "Pieza consultada",
        "cotizacion": "Solicitud a medida",
        "pedido": "Nuevo pedido",
    }
    for evento in notificaciones[:30]:
        identificador = str(evento.get("id", ""))
        fecha = str(evento.get("fecha", ""))[:19].replace("T", " ")
        detalle = evento.get("productoNombre") or evento.get("ordenId") or evento.get("pagina", "")
        columna_texto, columna_accion = st.columns([5, 1])
        columna_texto.markdown(
            f"**{escape(etiquetas.get(evento.get('tipo'), 'Actividad'))}** · "
            f"{escape(str(detalle))} · {escape(fecha)}"
        )
        if not evento.get("leida") and identificador:
            if columna_accion.button("Leída", key=f"notificacion_{identificador}"):
                result = api.admin_marcar_notificacion_leida(identificador)
                if isinstance(result, dict) and result.get("error"):
                    st.error(result["error"])
                else:
                    st.rerun()


def render():
    user = st.session_state.get("user") or {}
    if not esta_autenticado() or user.get("rol") != "admin":
        st.error("Acceso restringido. Inicia sesión con una cuenta administradora.")
        return

    st.markdown(
        '<div class="sec-head"><div class="sec-eye">Acceso restringido</div>'
        '<div class="sec-title">Administración</div><div class="sec-line"></div></div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Sesión de administración: {user.get('nombre', 'Admin')}")

    secciones = ["Inventario", "Pedidos", "Ventas y ganancias", "Notificaciones"]
    if st.session_state.get("admin_seccion") not in secciones:
        st.session_state["admin_seccion"] = "Inventario"
    seccion = st.segmented_control(
        "Administración",
        options=secciones,
        label_visibility="collapsed",
        key="admin_seccion",
    )

    if seccion == "Inventario":
        resultado = api.admin_productos()
        if isinstance(resultado, dict) and resultado.get("error"):
            st.error(f"No se pudo cargar el inventario: {resultado['error']}")
            return
        productos = resultado if isinstance(resultado, list) else []
        stock_total = sum(int(p.get("stock", 0) or 0) for p in productos)
        valor_total = sum(
            float(p.get("precio", 0) or 0) * int(p.get("stock", 0) or 0)
            for p in productos
        )
        met1, met2, met3 = st.columns(3)
        met1.metric("Piezas", len(productos))
        met2.metric("Unidades disponibles", stock_total)
        met3.metric("Valor en inventario", formatear_precio_corto(valor_total))

        with st.expander("Plantilla rápida · agregar una pieza", expanded=True):
            with st.form("form_nuevo_producto", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    nombre = st.text_input("Nombre", max_chars=120)
                    tipo = st.selectbox(
                        "Categoría",
                        ["anillo", "cadena", "colgante", "dije", "aro", "arete", "pulsera", "manilla", "esmeralda"],
                    )
                    material = st.text_input("Metal", value="Oro 18K", max_chars=80)
                    imagen = st.text_input("Imagen principal (URL)", max_chars=2048)
                    video_url = st.text_input(
                        "Video de la pieza (URL https opcional)",
                        max_chars=2048,
                        help="Pega un enlace https de un video MP4 o YouTube.",
                    )
                    imagenes = st.text_area(
                        "Imágenes para rotación 360° (una URL http(s) por línea)",
                        height=100,
                    )
                with c2:
                    precio = st.number_input("Precio COP", min_value=0, step=50_000)
                    costo_unitario = st.number_input(
                        "Costo de compra o fabricación por unidad (COP)",
                        min_value=0,
                        step=50_000,
                        help="Regístralo para calcular la utilidad; déjalo en 0 si no lo conoces.",
                    )
                    peso = st.number_input("Peso total (g)", min_value=0.0, step=0.1)
                    oro_18k_g = st.number_input("Oro 18K (g)", min_value=0.0, step=0.1)
                    esmeralda_ct = st.number_input("Esmeralda (ct)", min_value=0.0, step=0.05)
                    origen = st.selectbox(
                        "Origen",
                        ["Por confirmar", "Muzo", "Chivor", "Coscuez"],
                    )
                    stock = st.number_input("Stock", min_value=0, step=1)
                    certificado = st.text_input("Certificado gemológico", max_chars=160)
                crear = st.form_submit_button("Crear pieza", type="primary", width="stretch")
            archivos = st.file_uploader(
                "Subir fotos de la pieza (JPG, PNG o WebP; máximo 1 MB cada una)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key=(
                    "imagenes_nueva_pieza_"
                    f"{st.session_state.get('form_producto_version', 0)}"
                ),
            )
            if crear:
                try:
                    imagenes_360 = _imagen_urls(imagenes)
                    video_url = _validar_video_url(video_url)
                except ValueError as error:
                    st.error(str(error))
                else:
                    if not nombre.strip() or precio <= 0:
                        st.error("El nombre y un precio mayor que cero son obligatorios.")
                    elif not imagen.strip() and not archivos and not video_url:
                        st.error("Agrega una imagen principal, sube una foto o pega un video https.")
                    else:
                        response = api.admin_crear_producto({
                            "nombre": nombre.strip(),
                            "tipo": tipo,
                            "material": material.strip(),
                            "precio": precio,
                            "costo_unitario": costo_unitario or None,
                            "peso": peso,
                            "oro_18k_g": oro_18k_g,
                            "esmeralda_ct": esmeralda_ct,
                            "origen": origen if origen != "Por confirmar" else "",
                            "certificado_gemologico": certificado.strip(),
                            "imagen": imagen.strip(),
                            "video_url": video_url,
                            "imagenes_360": imagenes_360,
                            "stock": stock,
                            "activo": True,
                        })
                        if isinstance(response, dict) and response.get("error"):
                            st.error(response["error"])
                        else:
                            imagenes_correctas = True
                            if archivos and isinstance(response, dict) and response.get("_id"):
                                imagenes_correctas = _subir_archivos(
                                    response["_id"],
                                    archivos,
                                )
                            if imagenes_correctas:
                                st.success("Pieza creada.")
                            else:
                                st.warning(
                                    "La pieza quedó creada, pero algunas fotos no se "
                                    "guardaron. Puedes volver a cargarlas al editarla."
                                )
                            st.session_state["form_producto_version"] = (
                                st.session_state.get("form_producto_version", 0) + 1
                            )
                            st.rerun()

        for producto in productos:
            if not producto.get("activo", True):
                continue
            producto_id = str(producto.get("_id", ""))
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 2])
                c1.markdown(f"**{escape(str(producto.get('nombre', 'Pieza')))}**")
                c1.caption(
                    f"{escape(str(producto.get('material', '')))} · "
                    f"{escape(str(producto.get('tipo', '')))} · "
                    f"{formatear_precio(producto.get('precio', 0))}"
                )
                c2.metric("Stock", int(producto.get("stock", 0) or 0))
                c3.metric("Oro 18K", formatear_peso(producto.get("oro_18k_g", producto.get("peso", 0))))
                with c4:
                    acciones = st.columns(2)
                    if acciones[0].button("Editar", key=f"edit_{producto_id}"):
                        _editar_pieza_dialog(producto)
                    if acciones[1].button("Desactivar", key=f"hide_{producto_id}"):
                        response = api.admin_eliminar_producto(producto_id)
                        if isinstance(response, dict) and response.get("error"):
                            st.error(response["error"])
                        else:
                            st.success("Pieza retirada del catálogo.")
                            st.rerun()

    elif seccion == "Pedidos":
        _pedidos()

    elif seccion == "Ventas y ganancias":
        productos = api.admin_productos()
        if isinstance(productos, dict) and productos.get("error"):
            st.error(f"No se pudo cargar el inventario: {productos['error']}")
            return
        disponibles = [
            p for p in (productos if isinstance(productos, list) else [])
            if p.get("activo", True) and int(p.get("stock", 0) or 0) > 0
        ]
        st.subheader("Venta presencial")
        if disponibles:
            opciones = {f"{p.get('nombre', 'Pieza')} · {formatear_precio(p.get('precio', 0))}": p for p in disponibles}
            with st.form("form_agregar_caja"):
                seleccion = st.selectbox("Pieza", list(opciones))
                cantidad = st.number_input("Cantidad", min_value=1, max_value=99, value=1)
                agregar = st.form_submit_button("Añadir a la venta")
            if agregar:
                pieza = opciones[seleccion]
                carrito_caja = st.session_state.setdefault("items_caja", [])
                item = next((x for x in carrito_caja if x["producto_id"] == str(pieza["_id"])), None)
                if item:
                    item["cantidad"] += int(cantidad)
                else:
                    carrito_caja.append({
                        "producto_id": str(pieza["_id"]),
                        "nombre": pieza["nombre"],
                        "precio": pieza["precio"],
                        "cantidad": int(cantidad),
                    })
                st.rerun()
        else:
            st.info("No hay piezas disponibles para una venta presencial.")

        carrito_caja = st.session_state.setdefault("items_caja", [])
        if carrito_caja:
            for item in carrito_caja:
                st.write(
                    f"{item['cantidad']} × {item['nombre']} · "
                    f"{formatear_precio(item['precio'] * item['cantidad'])}"
                )
            pago = st.selectbox(
                "Medio de pago",
                ["Efectivo", "Tarjeta", "Transferencia", "Nequi"],
                key="pago_caja",
            )
            guardar = st.button("Registrar venta", type="primary")
            if guardar:
                response = api.admin_venta_caja({
                    "items": [
                        {"producto_id": item["producto_id"], "cantidad": item["cantidad"]}
                        for item in carrito_caja
                    ],
                    "medioPago": pago,
                })
                if isinstance(response, dict) and response.get("error"):
                    st.error(response["error"])
                else:
                    st.success(f"Venta registrada: {response.get('ventaId', '')}")
                    st.session_state["items_caja"] = []
                    st.rerun()

        st.divider()
        st.subheader("Gastos operativos")
        with st.form("form_gasto"):
            descripcion = st.text_input("Descripción", max_chars=180)
            categoria = st.selectbox(
                "Categoría",
                ["Insumos taller", "Servicios", "Nómina", "Publicidad", "Arriendo", "Otros"],
            )
            monto = st.number_input("Monto COP", min_value=0, step=10_000)
            registrar = st.form_submit_button("Registrar gasto")
        if registrar:
            if not descripcion.strip() or monto <= 0:
                st.error("Ingresa una descripción y un monto mayor que cero.")
            else:
                response = api.admin_registrar_gasto({
                    "descripcion": descripcion.strip(),
                    "categoria": categoria,
                    "monto": monto,
                })
                if isinstance(response, dict) and response.get("error"):
                    st.error(response["error"])
                else:
                    st.success("Gasto registrado.")

        st.subheader("Cierre diario")
        fecha = st.date_input("Fecha del cierre", value=date.today())
        if st.button("Generar cierre", key="generar_cierre"):
            cierre = api.admin_cierre_diario(fecha)
            if isinstance(cierre, dict) and cierre.get("error"):
                st.error(cierre["error"])
            else:
                ventas = cierre.get("ventas", {})
                utilidad = cierre.get("utilidadNeta")
                metricas = st.columns(4)
                metricas[0].metric(
                    "Ingresos confirmados",
                    formatear_precio(cierre.get("totalIngresos", 0)),
                )
                metricas[1].metric(
                    "Costo de piezas",
                    formatear_precio(cierre.get("costoProductos", 0)),
                )
                metricas[2].metric(
                    "Gastos operativos",
                    formatear_precio(cierre.get("totalGastos", 0)),
                )
                metricas[3].metric(
                    "Utilidad neta estimada",
                    formatear_precio(utilidad) if utilidad is not None else "Falta costo",
                )
                st.caption(
                    f"Online: {ventas.get('online', {}).get('cantidad', 0)} órdenes · "
                    f"Caja: {ventas.get('caja', {}).get('cantidad', 0)} ventas"
                )
                if cierre.get("itemsSinCosto", 0):
                    st.warning(
                        f"No se puede calcular la utilidad con precisión: "
                        f"{cierre['itemsSinCosto']} línea(s) vendida(s) no tienen costo "
                        "registrado. Completa el costo unitario en Inventario."
                    )
                else:
                    st.caption(
                        "La utilidad resta costo de piezas y gastos operativos; "
                        "no incluye costos logísticos de envío."
                    )

        st.subheader("Historial de ventas confirmadas")
        respuesta_ordenes = api.admin_ordenes()
        respuesta_caja = api.admin_historial_ventas()
        error_historial = next(
            (
                respuesta.get("error")
                for respuesta in (respuesta_ordenes, respuesta_caja)
                if isinstance(respuesta, dict) and respuesta.get("error")
            ),
            None,
        )
        if error_historial:
            st.error(f"No se pudo cargar el historial: {error_historial}")
        elif not isinstance(respuesta_ordenes, list) or not isinstance(respuesta_caja, list):
            st.error("La API devolvió una respuesta de ventas no válida.")
        else:
            entradas = []
            ordenes = respuesta_ordenes
            ventas_caja = respuesta_caja
            for orden in ordenes:
                if orden.get("estado") in {"procesado", "enviado"}:
                    entradas.append({
                        "fecha": str(orden.get("fecha", "")),
                        "canal": "Pedido en línea",
                        "referencia": orden.get("numero", "Pedido"),
                        "estado": orden.get("estado", ""),
                        "total": orden.get("total", 0),
                    })
            for venta in ventas_caja:
                if venta.get("estado") == "procesado":
                    entradas.append({
                        "fecha": str(venta.get("fecha", "")),
                        "canal": "Venta presencial",
                        "referencia": str(venta.get("_id", "Venta"))[-8:],
                        "estado": venta.get("estado", ""),
                        "total": venta.get("total", 0),
                    })
            entradas.sort(key=lambda entrada: entrada["fecha"], reverse=True)
            if not entradas:
                st.caption("Aún no hay ventas confirmadas.")
            for entrada in entradas[:20]:
                st.write(
                    f"{entrada['fecha'][:19].replace('T', ' ')} · "
                    f"{entrada['canal']} · {entrada['referencia']} · "
                    f"{entrada['estado'].capitalize()} · "
                    f"{formatear_precio(entrada['total'])}"
                )

    else:
        st.caption(
            "Las alertas se actualizan automáticamente cada 15 segundos. "
            "Los pedidos nuevos aparecen aquí y en la sección Pedidos."
        )
        _centro_notificaciones()
