const Orden = require('../models/Orden');
const Producto = require('../models/Producto');
const Evento = require('../models/Evento');
const mongoose = require('mongoose');

const METODOS_PAGO = new Set([
    'transferencia', 'pse', 'tarjeta', 'contraentrega', 'reserva_vip'
]);
const EMAIL_VALIDO = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const TELEFONO_VALIDO = /^\+?[\d\s()-]{7,24}$/;

function obtenerPromocion(codigo, subtotal) {
    if (!codigo) return { descuento: 0, codigo: '' };
    let promociones;
    try {
        promociones = JSON.parse(process.env.PROMO_CODES_JSON || '{}');
    } catch (error) {
        throw new Error('La configuración de promociones no es válida.');
    }
    const promo = promociones[String(codigo).trim().toUpperCase()];
    if (!promo || !Number.isFinite(Number(promo.valor)) || Number(promo.valor) <= 0) {
        throw new Error('El código promocional no es válido.');
    }
    const valor = Number(promo.valor);
    const descuento = promo.tipo === 'porcentaje'
        ? Math.round(subtotal * Math.min(valor, 100) / 100)
        : Math.min(Math.round(valor), subtotal);
    return { descuento, codigo: String(codigo).trim().toUpperCase() };
}

// 💾 Crear orden — descuenta stock automáticamente
exports.crear = async (req, res) => {
    const ajustesInventario = [];
    try {
        const {
            items, metodoPago, codigoPromocional = '',
            datosEnvio = {}, sesionAnonima
        } = req.body;
        const usuarioId = req.user.id;   // inyectado por authMiddleware

        if (!Array.isArray(items) || items.length === 0 || items.length > 30) {
            return res.status(400).json({ error: 'La orden no tiene items' });
        }
        if (!METODOS_PAGO.has(metodoPago)) {
            return res.status(400).json({ error: 'Selecciona un método de pago válido' });
        }
        const envio = {
            nombre: String(datosEnvio.nombre || '').trim(),
            email: String(datosEnvio.email || '').trim().toLowerCase(),
            telefono: String(datosEnvio.telefono || '').trim(),
            direccion: String(datosEnvio.direccion || '').trim(),
            ciudad: String(datosEnvio.ciudad || '').trim(),
            departamento: String(datosEnvio.departamento || '').trim(),
            notas: String(datosEnvio.notas || '').trim()
        };
        if (!envio.nombre || envio.nombre.length > 120 ||
            !EMAIL_VALIDO.test(envio.email) || envio.email.length > 254 ||
            !TELEFONO_VALIDO.test(envio.telefono) ||
            !envio.direccion || envio.direccion.length > 180 ||
            !envio.ciudad || envio.ciudad.length > 80 ||
            !envio.departamento || envio.departamento.length > 80 ||
            envio.notas.length > 500) {
            return res.status(400).json({ error: 'Revisa los datos de envío' });
        }

        const cantidades = new Map();
        for (const item of items) {
            if (!mongoose.isValidObjectId(item.producto_id) ||
                !Number.isInteger(item.cantidad) || item.cantidad < 1 || item.cantidad > 99) {
                return res.status(400).json({ error: 'El carrito contiene un artículo inválido' });
            }
            const productoId = String(item.producto_id);
            const nuevaCantidad = (cantidades.get(productoId) || 0) + item.cantidad;
            if (nuevaCantidad > 99) {
                return res.status(400).json({ error: 'La cantidad máxima por pieza es 99' });
            }
            cantidades.set(productoId, nuevaCantidad);
        }

        let subtotal = 0;
        const itemsVerificados = [];
        for (const [productoId, cantidad] of cantidades) {
            const producto = await Producto.findOneAndUpdate(
                { _id: productoId, activo: true, stock: { $gte: cantidad } },
                { $inc: { stock: -cantidad } },
                { new: true }
            );
            if (!producto) {
                for (const ajuste of ajustesInventario) {
                    await Producto.updateOne(
                        { _id: ajuste.productoId },
                        { $inc: { stock: ajuste.cantidad } }
                    );
                }
                ajustesInventario.length = 0;
                return res.status(409).json({
                    error: 'Una pieza ya no tiene stock suficiente. Actualiza el carrito.'
                });
            }
            ajustesInventario.push({ productoId, cantidad });
            subtotal += producto.precio * cantidad;
            itemsVerificados.push({
                producto_id: producto._id,
                nombre: producto.nombre,
                precio: producto.precio,
                costo_unitario: producto.costo_unitario,
                cantidad
            });
        }

        const { descuento, codigo } = obtenerPromocion(codigoPromocional, subtotal);
        const envioAsegurado = Math.max(
            0,
            Math.round(Number(process.env.ENVIO_ASEGURADO_COP || 0))
        );
        if (!Number.isFinite(envioAsegurado)) {
            throw new Error('La configuración del envío asegurado no es válida.');
        }
        const total = subtotal + envioAsegurado - descuento;
        const numero = `MVIP-${new mongoose.Types.ObjectId().toString().slice(-6).toUpperCase()}`;
        const orden = new Orden({
            usuario: usuarioId,
            items: itemsVerificados,
            numero,
            total,
            envioAsegurado,
            descuento,
            codigoPromocional: codigo,
            metodoPago,
            datosEnvio: envio
        });

        await orden.save();
        ajustesInventario.length = 0;

        if (typeof sesionAnonima === 'string' && /^[0-9a-f-]{36}$/i.test(sesionAnonima)) {
            try {
                await Evento.create({
                    tipo: 'pedido',
                    pagina: 'carrito',
                    sesionAnonima,
                    ordenId: numero
                });
            } catch (eventError) {
                console.error('No se pudo registrar la notificación de pedido:', eventError);
            }
        }

        res.status(201).json({
            mensaje: 'Orden creada con éxito',
            ordenId: orden._id,
            numero: orden.numero,
            total: orden.total,
            envioAsegurado: orden.envioAsegurado,
            descuento: orden.descuento,
            fecha: orden.fecha,
            estado: orden.estado
        });

    } catch (error) {
        for (const ajuste of ajustesInventario) {
            try {
                await Producto.updateOne(
                    { _id: ajuste.productoId },
                    { $inc: { stock: ajuste.cantidad } }
                );
            } catch (rollbackError) {
                console.error('No se pudo restaurar stock tras error de orden:', rollbackError);
            }
        }
        console.error('Error al crear orden:', error);
        if (error.message.includes('código promocional')) {
            return res.status(400).json({ error: error.message });
        }
        res.status(500).json({ error: 'Error al procesar la orden' });
    }
};

// 📋 Obtener órdenes del usuario autenticado
exports.obtener = async (req, res) => {
    try {
        const ordenes = await Orden.find({ usuario: req.user.id })
            .select('-items.costo_unitario')
            .sort({ fecha: -1 });
        res.json(ordenes);
    } catch (error) {
        console.error('Error al obtener órdenes:', error);
        res.status(500).json({ error: 'Error al obtener órdenes' });
    }
};

// 🔍 Obtener una orden por ID
exports.obtenerPorId = async (req, res) => {
    try {
        if (!mongoose.isValidObjectId(req.params.id)) {
            return res.status(404).json({ error: 'Orden no encontrada' });
        }
        const orden = await Orden.findOne({
            _id: req.params.id,
            usuario: req.user.id
        }).select('-items.costo_unitario');
        if (!orden) return res.status(404).json({ error: 'Orden no encontrada' });
        res.json(orden);
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener la orden' });
    }
};
