"""
Vista de autenticación de cliente y administrador.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from api.client import api
from utils.session import agregar_al_carrito, esta_autenticado, iniciar_sesion, cerrar_sesion


_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def render():
    st.markdown(
        '<div class="sec-head"><div class="sec-eye">Atención privada</div>'
        '<div class="sec-title">Mi cuenta</div><div class="sec-line"></div></div>',
        unsafe_allow_html=True,
    )

    if esta_autenticado():
        user = st.session_state.get("user") or {}
        with st.container(border=True):
            st.subheader(user.get("nombre", "Cliente"))
            st.caption(user.get("email", ""))
            st.caption("Administrador" if user.get("rol") == "admin" else "Cliente")
            if user.get("rol") == "admin" and st.button(
                "Abrir panel de administración",
                key="abrir_panel_admin_cuenta",
                type="primary",
                width="stretch",
            ):
                st.query_params["page"] = "admin"
                st.rerun()
            if st.button("Cerrar sesión", type="secondary"):
                cerrar_sesion()
        return

    vista = st.segmented_control(
        "Acceso",
        options=["login", "registro"],
        format_func=lambda value: "Iniciar sesión" if value == "login" else "Crear cuenta",
        default=st.session_state.get("auth_view", "login"),
        label_visibility="collapsed",
        key=f"auth_view_selector_{st.session_state.get('auth_view', 'login')}",
    )
    st.session_state["auth_view"] = vista

    if vista == "login":
        compra_pendiente = st.session_state.get("compra_pendiente")
        if compra_pendiente:
            st.info(
                f"Inicia sesión para continuar con la compra de "
                f"«{compra_pendiente.get('nombre', 'tu joya')}»."
            )
        st.subheader("Bienvenido de nuevo")
        with st.form("form_login", clear_on_submit=False):
            email = st.text_input("Correo electrónico", max_chars=254)
            password = st.text_input("Contraseña", type="password", max_chars=128)
            submitted = st.form_submit_button("Ingresar", type="primary", width="stretch")

        if submitted:
            email_limpio = email.strip().lower()
            if not _EMAIL.fullmatch(email_limpio) or not password:
                st.error("Ingresa un correo y una contraseña válidos.")
                return

            with st.spinner("Verificando tus datos..."):
                response = api.login(email_limpio, password)

            if isinstance(response, dict) and response.get("error"):
                st.error(response["error"])
            elif isinstance(response, dict) and response.get("token"):
                user_info = {
                    "nombre": response.get("nombre", "Cliente"),
                    "email": response.get("email", email_limpio),
                    "rol": response.get("rol", "cliente"),
                }
                iniciar_sesion(response["token"], user_info)
                compra_pendiente = st.session_state.pop("compra_pendiente", None)
                if user_info["rol"] == "admin":
                    st.query_params["page"] = "admin"
                elif compra_pendiente:
                    agregar_al_carrito(compra_pendiente)
                    st.query_params["page"] = "carrito"
                st.rerun()
            else:
                st.error("El servidor devolvió una respuesta de acceso no válida.")
        return

    st.subheader("Crear cuenta")
    with st.form("form_registro", clear_on_submit=False):
        nombre = st.text_input("Nombre completo", max_chars=120)
        email = st.text_input("Correo electrónico", max_chars=254)
        password = st.text_input(
            "Contraseña",
            type="password",
            max_chars=128,
            help="Usa al menos 12 caracteres.",
        )
        confirmar = st.text_input("Confirmar contraseña", type="password", max_chars=128)
        with st.expander("Autorización de tratamiento de datos"):
            st.markdown(
                "Usaremos tus datos para administrar la cuenta, gestionar pedidos y "
                "atender solicitudes relacionadas con tus compras. Puedes solicitar "
                "acceso, rectificación o supresión escribiendo a contacto@matallanavip.com."
            )
        acepta = st.checkbox(
            "Autorizo el tratamiento de mis datos personales para estos fines."
        )
        submitted = st.form_submit_button(
            "Crear cuenta",
            type="primary",
            width="stretch",
        )

    if not submitted:
        return

    errores = []
    nombre_limpio = nombre.strip()
    email_limpio = email.strip().lower()
    if not nombre_limpio or len(nombre_limpio) > 120:
        errores.append("Ingresa tu nombre completo.")
    if not _EMAIL.fullmatch(email_limpio):
        errores.append("Ingresa un correo electrónico válido.")
    if len(password) < 12:
        errores.append("La contraseña debe tener al menos 12 caracteres.")
    if password != confirmar:
        errores.append("Las contraseñas no coinciden.")
    if not acepta:
        errores.append("Debes autorizar el tratamiento de datos para continuar.")

    if errores:
        for error in errores:
            st.error(error)
        return

    with st.spinner("Creando tu cuenta..."):
        response = api.registrar(nombre_limpio, email_limpio, password)

    if isinstance(response, dict) and response.get("error"):
        st.error(response["error"])
    elif isinstance(response, dict) and response.get("mensaje"):
        login_response = api.login(email_limpio, password)
        if isinstance(login_response, dict) and login_response.get("token"):
            iniciar_sesion(login_response["token"], {
                "nombre": login_response.get("nombre", nombre_limpio),
                "email": login_response.get("email", email_limpio),
                "rol": login_response.get("rol", "cliente"),
            })
            compra_pendiente = st.session_state.pop("compra_pendiente", None)
            if compra_pendiente:
                agregar_al_carrito(compra_pendiente)
                st.query_params["page"] = "carrito"
            st.success("Tu cuenta quedó creada y la sesión inició correctamente.")
            st.rerun()
        else:
            st.success("Tu cuenta quedó creada. Selecciona «Iniciar sesión» para acceder.")
    else:
        st.error("El servidor devolvió una respuesta de registro no válida.")
