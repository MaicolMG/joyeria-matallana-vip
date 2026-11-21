# Joyería Matallana VIP

## ¿De qué trata esta aplicación?

Joyería Matallana VIP es una aplicación web para presentar y administrar una tienda de alta joyería colombiana, con énfasis en esmeraldas. Reúne en un mismo proyecto la vitrina que visitan los clientes, el proceso de compra y las herramientas internas que necesita el equipo para gestionar el negocio.

Los clientes pueden explorar el catálogo, conocer las características de cada pieza, crear una cuenta, iniciar sesión y enviar una orden desde el carrito. El panel privado permite al administrador gestionar productos e inventario, revisar pedidos, actualizar su estado, consultar ventas y notificaciones, y llevar un registro de costos para obtener una utilidad estimada cuando se cuenta con esa información.

La aplicación tiene una interfaz construida con Streamlit, una API en Node.js y una base de datos MongoDB. La API valida nuevamente el precio y la disponibilidad al crear una orden. Las imágenes de los productos se almacenan en GridFS; también se pueden registrar enlaces de video para las piezas.

**Importante:** el checkout registra pedidos pendientes, pero no cobra ni procesa pagos reales. Los medios de pago que aparecen en la tienda sirven para coordinar el pago con el equipo.

## ¿Qué incluye?

- **Tienda para clientes:** inicio, catálogo, fichas de producto, personalización de joyas, carrito y cuenta de usuario.
- **Administración:** productos, características y peso, inventario, imágenes y enlaces de video.
- **Gestión de pedidos:** consulta de órdenes y actualización de sus estados.
- **Ventas y utilidad:** seguimiento de ventas y cálculo de utilidad estimada a partir de los costos registrados; no se inventan costos faltantes.
- **Notificaciones y gastos:** avisos para el administrador y registro de gastos operativos.
- **API y datos:** servicios REST, autenticación, MongoDB y almacenamiento de imágenes mediante GridFS.
- **Privacidad básica de analítica:** registra páginas o productos vistos con un identificador aleatorio de sesión; no almacena IP ni huella del dispositivo.

## Funcionalidades principales

- Catálogo de productos y personalización de joyas.
- Registro e inicio de sesión de clientes.
- Carrito y creación de órdenes.
- Panel de administración para productos, inventario, pedidos, ventas, costos y notificaciones.
- Carga de imágenes y configuración de videos para productos.

## Tecnologías

- **Interfaz:** Python y Streamlit.
- **API:** Node.js, Express y MongoDB.
- **Imágenes:** GridFS de MongoDB.

## Requisitos

- Windows, para usar los archivos BAT incluidos.
- Node.js y npm.
- Python y pip.
- Una instancia de MongoDB accesible desde la aplicación.

## Configuración local

Desde la carpeta raíz del repositorio, crea los archivos de configuración locales:

```powershell
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env
```

Edita `backend\.env` y configura, como mínimo:

- `MONGO_URI`: conexión a MongoDB.
- `JWT_SECRET`: secreto aleatorio de al menos 32 caracteres.
- `ADMIN_EMAIL`: correo que usarás para administrar la tienda.
- `ADMIN_PASSWORD`: contraseña de administrador de 12 a 128 caracteres.
- `CORS_ORIGINS` y `PUBLIC_API_ORIGIN`: direcciones de la interfaz y la API para tu entorno.

En `frontend\.env`, confirma que `API_BASE_URL` apunte a la API; para desarrollo local normalmente es `http://localhost:3000`.

Instala las dependencias y crea el usuario administrador:

```powershell
cd backend
npm install
npm run admin

cd ..\frontend
python -m pip install -r requirements.txt

cd ..
```

## Iniciar y detener

Con las dependencias y los archivos `.env` configurados, ejecuta desde la raíz:

```powershell
.\iniciar.bat
```

La tienda estará disponible en <http://localhost:8501> y la API en <http://localhost:3000>. Para detener los servicios administrados por este proyecto:

```powershell
.\detener.bat
```

Los registros y datos temporales del controlador se guardan en `.runtime\`.

### Inicio manual

Si prefieres no usar los BAT, ejecuta el backend y la interfaz en terminales separadas:

```powershell
cd backend
npm run dev
```

```powershell
cd frontend
python -m streamlit run app.py --server.port 8501
```

## Estructura

```text
backend/      API y acceso a MongoDB
frontend/     Tienda y panel de administración en Streamlit
landing/      Página de aterrizaje estática
scripts/      Control de servicios para Windows
iniciar.bat   Inicia la API y la tienda
detener.bat   Detiene los servicios administrados
```

## Seguridad

- No subas `backend\.env`, `frontend\.env`, contraseñas ni secretos.
- Usa los archivos `.env.example` como plantillas y reemplaza sus valores de ejemplo.
- Protege las credenciales de MongoDB y utiliza un `JWT_SECRET` aleatorio.-
