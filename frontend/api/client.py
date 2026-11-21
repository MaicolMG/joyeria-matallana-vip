"""
Cliente HTTP para la API REST de Joyería Matallana VIP.
Envía el token JWT con el esquema estándar Bearer.
"""
import logging

import requests
import streamlit as st
from config import API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _handle(self, resp):
        try:
            data = resp.json()
        except ValueError:
            data = {}
        if resp.status_code >= 400:
            msg = data.get("error") or data.get("mensaje") or f"Error HTTP {resp.status_code}"
            return {"error": msg, "status": resp.status_code}
        return data

    @staticmethod
    def _connection_error(error):
        _LOGGER.error("API request failed (%s)", type(error).__name__)
        return {"error": "No se pudo conectar con la API."}

    # ── Métodos genéricos ──────────────────────────────────────────────
    def get(self, endpoint, params=None):
        try:
            r = requests.get(f"{self.base_url}{endpoint}",
                             headers=self._headers(), params=params, timeout=15)
            return self._handle(r)
        except requests.exceptions.RequestException as error:
            return self._connection_error(error)

    def post(self, endpoint, data=None):
        try:
            r = requests.post(f"{self.base_url}{endpoint}",
                              headers=self._headers(), json=data, timeout=15)
            return self._handle(r)
        except requests.exceptions.RequestException as error:
            return self._connection_error(error)

    def put(self, endpoint, data=None):
        """Petición PUT con token JWT — para actualizar recursos."""
        try:
            r = requests.put(f"{self.base_url}{endpoint}",
                             headers=self._headers(), json=data, timeout=15)
            return self._handle(r)
        except requests.exceptions.RequestException as error:
            return self._connection_error(error)

    def delete(self, endpoint):
        try:
            r = requests.delete(f"{self.base_url}{endpoint}",
                                headers=self._headers(), timeout=15)
            return self._handle(r)
        except requests.exceptions.RequestException as error:
            return self._connection_error(error)

    def patch(self, endpoint, data=None):
        try:
            r = requests.patch(f"{self.base_url}{endpoint}",
                               headers=self._headers(), json=data, timeout=15)
            return self._handle(r)
        except requests.exceptions.RequestException as error:
            return self._connection_error(error)

    # ── Auth ───────────────────────────────────────────────────────────
    def registrar(self, nombre, email, password):
        return self.post("/auth/registro", {"nombre": nombre, "email": email, "password": password})

    def login(self, email, password):
        return self.post("/auth/login", {"email": email, "password": password})

    # ── Productos (catálogo público) ───────────────────────────────────
    def obtener_productos(self):
        return self.get("/productos")

    def eliminar_producto(self, producto_id):
        return self.delete(f"/productos/{producto_id}")

    # ── Órdenes ────────────────────────────────────────────────────────
    def crear_orden(self, orden_data):
        """POST /api/ordenes/crear — procesa compra y descuenta stock."""
        return self.post("/ordenes/crear", orden_data)

    def registrar_evento(self, data):
        try:
            response = requests.post(
                f"{self.base_url}/eventos",
                json=data,
                timeout=2,
            )
            return self._handle(response)
        except requests.exceptions.RequestException as error:
            return self._connection_error(error)

    # ── Cotizaciones a medida (va al admin, no al catálogo público) ────
    def enviar_cotizacion(self, data):
        """POST /api/admin/productos — crea cotización (requiere admin).
        Para clientes normales solo guarda localmente."""
        return self.post("/admin/productos", data)

    # ── Admin ──────────────────────────────────────────────────────────
    def admin_productos(self):
        return self.get("/admin/productos")

    def admin_crear_producto(self, data):
        return self.post("/admin/productos", data)

    def admin_editar_producto(self, pid, data):
        """PUT /api/admin/productos/:id — editar o reabastecer stock."""
        return self.put(f"/admin/productos/{pid}", data)

    def admin_eliminar_producto(self, pid):
        return self.delete(f"/admin/productos/{pid}")

    def admin_ordenes(self):
        return self.get("/admin/ordenes")

    def admin_actualizar_estado_orden(self, order_id, estado):
        return self.patch(f"/admin/ordenes/{order_id}/estado", {"estado": estado})

    def admin_historial_ventas(self, params=None):
        return self.get("/admin/caja/ventas", params=params)

    def admin_subir_imagen(self, pid, contenido, tipo):
        headers = self._headers()
        headers["Content-Type"] = tipo
        try:
            response = requests.post(
                f"{self.base_url}/admin/productos/{pid}/imagenes",
                headers=headers,
                data=contenido,
                timeout=30,
            )
            return self._handle(response)
        except requests.exceptions.RequestException as error:
            return self._connection_error(error)

    def admin_venta_caja(self, data):
        return self.post("/admin/ventas/caja", data)

    def admin_gastos(self):
        return self.get("/admin/gastos")

    def admin_registrar_gasto(self, data):
        return self.post("/admin/gastos", data)

    def admin_cierre_diario(self, fecha=None):
        params = {"fecha": str(fecha)} if fecha else None
        return self.get("/admin/caja/cierre-diario", params=params)

    def admin_analitica(self):
        return self.get("/admin/analitica")

    def admin_marcar_notificacion_leida(self, event_id):
        return self.patch(f"/admin/notificaciones/{event_id}/leida")

    # ── Health check ───────────────────────────────────────────────────
    def health(self):
        """Verifica que la API esté respondiendo."""
        try:
            r = requests.get(f"{self.base_url}/productos", timeout=5)
            return r.status_code == 200
        except requests.exceptions.RequestException as error:
            self._connection_error(error)
            return False


api = APIClient()
