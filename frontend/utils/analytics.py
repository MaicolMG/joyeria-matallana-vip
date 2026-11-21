import concurrent.futures
import logging
import uuid

import streamlit as st

from api.client import api

_LOGGER = logging.getLogger(__name__)


@st.cache_resource
def _event_executor():
    return concurrent.futures.ThreadPoolExecutor(max_workers=2)


def sesion_anonima():
    if "sesion_anonima" not in st.session_state:
        st.session_state["sesion_anonima"] = str(uuid.uuid4())
    return st.session_state["sesion_anonima"]


def registrar_evento(tipo, pagina, producto=None):
    if st.session_state.get("ultima_pagina_analitica") == pagina and tipo == "visita":
        return
    producto = producto or {}
    payload = {
        "tipo": tipo,
        "pagina": pagina,
        "sesionAnonima": sesion_anonima(),
        "productoId": str(producto.get("_id", "")),
        "productoNombre": str(producto.get("nombre", "")),
    }
    if tipo == "visita":
        st.session_state["ultima_pagina_analitica"] = pagina

    future = _event_executor().submit(api.post, "/eventos", payload)

    def report_error(completed):
        try:
            response = completed.result()
            if isinstance(response, dict) and response.get("error"):
                _LOGGER.error("No se pudo registrar la analítica: %s", response["error"])
        except Exception:
            _LOGGER.exception("Falló el registro asíncrono de analítica")

    future.add_done_callback(report_error)
