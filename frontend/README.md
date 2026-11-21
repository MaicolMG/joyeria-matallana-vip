# Matallana VIP · Streamlit

## Ejecutar localmente

1. Configura `API_BASE_URL` en `frontend/.env` usando `frontend/.env.example` como referencia.
2. Configura `MONGO_URI`, `JWT_SECRET` (mínimo 32 caracteres) y `PUBLIC_API_ORIGIN` en `backend/.env`, tomando `backend/.env.example` como plantilla.
3. Inicia el backend: `cd backend` y `npm run dev`.
4. Inicia la tienda: `cd frontend` y `streamlit run app.py` (o ejecuta `run.bat`).

No compartas ni subas los archivos `.env`. El servidor no inicia si faltan `MONGO_URI` o un `JWT_SECRET` adecuado.

## Órdenes y pagos

El checkout crea una orden `pendiente` y no procesa pagos. PSE, tarjeta, transferencia, contraentrega y reserva VIP son preferencias para coordinar con el equipo; integrar un cobro real requiere credenciales y configuración del proveedor. El precio y el stock se vuelven a verificar en el backend. El envío asegurado se configura con `ENVIO_ASEGURADO_COP`; con `0`, su costo se confirma con el asesor antes de cobrar.

Los códigos promocionales se configuran en `PROMO_CODES_JSON` como JSON, por ejemplo `{"VIP10":{"tipo":"porcentaje","valor":10}}`. El servidor calcula el descuento; nunca confía en un total enviado por el navegador.

## Imágenes y analítica

El panel admin acepta imágenes JPG, PNG y WebP de hasta 1 MB cada una; se guardan en GridFS de MongoDB y se sirven desde `/media`. Configura `PUBLIC_API_ORIGIN` con la URL pública del backend. Los archivos no se guardan en el disco local.

La analítica guarda hora, página/producto y un UUID aleatorio de sesión durante un máximo de 180 días. No conserva IP, agente de usuario ni huella de dispositivo. El panel actualiza las alertas periódicamente.
