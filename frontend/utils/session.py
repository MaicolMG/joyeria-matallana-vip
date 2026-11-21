"""
Gestión del estado de sesión de la aplicación (token JWT, usuario, carrito).
Centraliza toda la lógica de autenticación y del carrito de compras.
"""
import streamlit as st


def init_session():
    """Inicializa las claves de session_state con valores por defecto."""
    defaults = {
        "token": None,          # JWT recibido del backend
        "user": None,           # {"nombre": ..., "rol": ...}
        "carrito": [],          # [{"producto_id", "nombre", "precio", "peso", "material", "cantidad"}]
        "auth_view": "login",   # "login" | "registro"
        "compra_pendiente": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# --------------------------------------------------------------------------- #
# Autenticación
# --------------------------------------------------------------------------- #

def esta_autenticado():
    """True si hay un token JWT vigente en sesión."""
    return st.session_state.get("token") is not None


def iniciar_sesion(token, user_info=None):
    """Guarda el token y la info de usuario tras un login exitoso."""
    st.session_state["token"] = token
    st.session_state["user"] = user_info or {}
    st.toast("¡Bienvenido! Sesión iniciada correctamente.", icon="✅")


def cerrar_sesion():
    """Elimina token, datos de usuario y vacía el carrito."""
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.session_state["carrito"] = []
    st.toast("Sesión cerrada.", icon="👋")
    st.rerun()


# --------------------------------------------------------------------------- #
# Carrito de compras
# --------------------------------------------------------------------------- #

def agregar_al_carrito(producto, cantidad=1):
    """Agrega un producto al carrito o incrementa su cantidad si ya existe."""
    carrito = st.session_state["carrito"]
    pid = str(producto.get("_id", producto.get("producto_id", "")))

    item = next((i for i in carrito if i["producto_id"] == pid), None)
    if item:
        item["cantidad"] = min(99, item["cantidad"] + max(1, int(cantidad)))
    else:
        carrito.append({
            "producto_id": pid,
            "nombre": producto.get("nombre", "Producto"),
            "precio": producto.get("precio", 0),
            "peso": producto.get("peso", 0),
            "oro_18k_g": producto.get("oro_18k_g", producto.get("peso", 0)),
            "esmeralda_ct": producto.get("esmeralda_ct", 0),
            "material": producto.get("material", ""),
            "tipo": producto.get("tipo", ""),
            "cantidad": cantidad,
        })
    st.session_state["carrito"] = carrito


def actualizar_cantidad(producto_id, cantidad):
    """Actualiza la cantidad de un item (mínimo 1)."""
    for item in st.session_state["carrito"]:
        if item["producto_id"] == producto_id:
            item["cantidad"] = max(1, int(cantidad))
            break


def eliminar_del_carrito(producto_id):
    """Elimina un item del carrito por su producto_id."""
    st.session_state["carrito"] = [
        i for i in st.session_state["carrito"] if i["producto_id"] != producto_id
    ]


def vaciar_carrito():
    """Elimina todos los items del carrito."""
    st.session_state["carrito"] = []


def contar_items_carrito():
    """Devuelve el número total de unidades en el carrito."""
    return sum(i["cantidad"] for i in st.session_state.get("carrito", []))
