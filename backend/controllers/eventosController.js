const Evento = require('../models/Evento');
const ventanasPorIp = new Map();

const TIPOS_PERMITIDOS = new Set(['visita', 'producto', 'cotizacion']);
const PAGINAS_PERMITIDAS = new Set([
    'inicio', 'catalogo', 'a_medida', 'carrito', 'mi_cuenta'
]);

exports.registrar = async (req, res) => {
    try {
        const ahora = Date.now();
        const ip = req.ip || req.socket.remoteAddress || 'unknown';
        let ventana = ventanasPorIp.get(ip);
        if (!ventana || ventana.renueva <= ahora) {
            if (ventanasPorIp.size >= 5000) {
                const primeraIp = ventanasPorIp.keys().next().value;
                if (primeraIp) ventanasPorIp.delete(primeraIp);
            }
            ventana = { cantidad: 0, renueva: ahora + 60_000 };
        }
        ventana.cantidad += 1;
        ventanasPorIp.set(ip, ventana);
        if (ventana.cantidad > 60) {
            return res.status(429).json({ error: 'Límite de eventos alcanzado' });
        }

        const { tipo, pagina, sesionAnonima, productoId = '', productoNombre = '' } = req.body;
        if (!TIPOS_PERMITIDOS.has(tipo) || !PAGINAS_PERMITIDAS.has(pagina) ||
            typeof sesionAnonima !== 'string' || !/^[0-9a-f-]{36}$/i.test(sesionAnonima)) {
            return res.status(400).json({ error: 'Evento inválido' });
        }

        await Evento.create({
            tipo,
            pagina,
            sesionAnonima,
            productoId: String(productoId).slice(0, 80),
            productoNombre: String(productoNombre).slice(0, 120)
        });
        res.status(201).json({ registrado: true });
    } catch (error) {
        console.error('Error al registrar evento anónimo:', error);
        res.status(500).json({ error: 'No se pudo registrar el evento' });
    }
};
