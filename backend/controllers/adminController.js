/**
 * adminController.js
 * Control total de inventario, caja presencial y cierre diario.
 * Solo accesible para usuarios con rol 'admin'.
 */
const Producto       = require('../models/Producto');
const Orden          = require('../models/Orden');
const Venta          = require('../models/Venta');
const GastoOperativo = require('../models/GastoOperativo');
const Evento = require('../models/Evento');
const mongoose = require('mongoose');

// ─────────────────────────────────────────────────────────────────
// INVENTARIO
// ─────────────────────────────────────────────────────────────────

/** GET /api/admin/productos — Lista completa con stock y pesaje */
exports.listarProductos = async (req, res) => {
    try {
        const productos = await Producto.find().sort({ createdAt: -1 });
        res.json(productos);
    } catch (e) {
        res.status(500).json({ error: 'Error al obtener inventario' });
    }
};

/** POST /api/admin/productos — Crear joya con pesaje real e imágenes HD */
exports.crearProducto = async (req, res) => {
    try {
        const p = new Producto(req.body);
        await p.save();
        res.status(201).json(p);
    } catch (e) {
        console.error(e);
        res.status(400).json({ error: e.message || 'Error al crear producto' });
    }
};

/** PUT /api/admin/productos/:id — Editar / reabastecer stock */
exports.editarProducto = async (req, res) => {
    try {
        const p = await Producto.findByIdAndUpdate(
            req.params.id, req.body, { new: true, runValidators: true }
        );
        if (!p) return res.status(404).json({ error: 'Producto no encontrado' });
        res.json(p);
    } catch (e) {
        res.status(400).json({ error: e.message || 'Error al editar' });
    }
};

/** DELETE /api/admin/productos/:id — Desactivación lógica */
exports.eliminarProducto = async (req, res) => {
    try {
        const p = await Producto.findByIdAndUpdate(
            req.params.id,
            { activo: false },
            { new: true }
        );
        if (!p) return res.status(404).json({ error: 'Producto no encontrado' });
        res.json({ mensaje: 'Producto desactivado del catálogo', id: p._id });
    } catch (e) {
        res.status(500).json({ error: 'Error al eliminar' });
    }
};

/** GET /api/admin/ordenes — Pedidos de clientes, incluidos los pendientes */
exports.listarOrdenes = async (req, res) => {
    try {
        const ordenes = await Orden.find()
            .sort({ fecha: -1 })
            .limit(200)
            .lean();
        res.json(ordenes);
    } catch (error) {
        console.error('Error al listar pedidos:', error);
        res.status(500).json({ error: 'Error al obtener los pedidos' });
    }
};

/** PATCH /api/admin/ordenes/:id/estado — Confirma y avanza el pedido */
exports.actualizarEstadoOrden = async (req, res) => {
    try {
        if (!mongoose.isValidObjectId(req.params.id)) {
            return res.status(404).json({ error: 'Pedido no encontrado' });
        }
        const transiciones = {
            pendiente: 'procesado',
            procesado: 'enviado'
        };
        const estadoActual = String((req.body || {}).estado || '');
        const pedido = await Orden.findById(req.params.id);
        if (!pedido) return res.status(404).json({ error: 'Pedido no encontrado' });
        if (transiciones[pedido.estado] !== estadoActual) {
            return res.status(409).json({
                error: 'El pedido cambió de estado o la transición no está permitida.'
            });
        }
        const actualizado = await Orden.findOneAndUpdate(
            { _id: pedido._id, estado: pedido.estado },
            {
                $set: {
                    estado: estadoActual,
                    ...(estadoActual === 'procesado' ? { confirmadaEn: new Date() } : {})
                }
            },
            { returnDocument: 'after', runValidators: true }
        );
        if (!actualizado) {
            return res.status(409).json({ error: 'El pedido cambió de estado. Actualiza la lista.' });
        }
        res.json(actualizado);
    } catch (error) {
        console.error('Error al actualizar pedido:', error);
        res.status(500).json({ error: 'No se pudo actualizar el pedido' });
    }
};

// ─────────────────────────────────────────────────────────────────
// VENTAS EN CAJA PRESENCIAL
// ─────────────────────────────────────────────────────────────────

/**
 * POST /api/admin/ventas/caja
 * Registra venta física, descuenta stock y guarda en colección Ventas.
 * Body: { items: [{producto_id, cantidad}], medioPago }
 */
exports.ventaCaja = async (req, res) => {
    try {
        const { items, medioPago } = req.body;

        if (!items || items.length === 0)
            return res.status(400).json({ error: 'La venta no tiene artículos' });
        if (!['Efectivo','Tarjeta','Transferencia','Nequi'].includes(medioPago))
            return res.status(400).json({ error: 'Medio de pago inválido' });

        let total = 0;
        const itemsCompletos = [];

        // Verificar stock de cada producto
        for (const item of items) {
            const prod = await Producto.findById(item.producto_id);
            if (!prod) return res.status(404).json({ error: `Producto ${item.producto_id} no encontrado` });
            if (prod.stock > 0 && prod.stock < item.cantidad)
                return res.status(400).json({
                    error: `Stock insuficiente para "${prod.nombre}". Disponible: ${prod.stock}`
                });

            const subtotal = prod.precio * item.cantidad;
            total += subtotal;
            itemsCompletos.push({
                producto:   prod._id,
                nombre:     prod.nombre,
                cantidad:   item.cantidad,
                precioUnit: prod.precio,
                costoUnit:  prod.costo_unitario,
                subtotal
            });
        }

        // Descontar stock
        for (const item of items) {
            const prod = await Producto.findById(item.producto_id);
            if (prod.stock > 0) {
                prod.stock -= item.cantidad;
                await prod.save();
            }
        }

        // Guardar venta
        const venta = new Venta({
            items:         itemsCompletos,
            total,
            medioPago,
            canal:         'caja',
            registradoPor: req.user.id,
            estado:        'procesado'
        });
        await venta.save();

        res.status(201).json({
            mensaje:  'Venta en caja registrada',
            ventaId:  venta._id,
            total,
            medioPago,
            fecha:    venta.fecha
        });

    } catch (e) {
        console.error(e);
        res.status(500).json({ error: 'Error al registrar venta en caja' });
    }
};

// ─────────────────────────────────────────────────────────────────
// GASTOS OPERATIVOS
// ─────────────────────────────────────────────────────────────────

/** POST /api/admin/gastos */
exports.registrarGasto = async (req, res) => {
    try {
        const { descripcion, categoria, monto } = req.body;
        if (!monto || monto <= 0)
            return res.status(400).json({ error: 'El monto debe ser mayor a 0' });

        const gasto = new GastoOperativo({
            descripcion, categoria, monto,
            registradoPor: req.user.id
        });
        await gasto.save();
        res.status(201).json({ mensaje: 'Gasto registrado', gasto });
    } catch (e) {
        res.status(500).json({ error: 'Error al registrar gasto' });
    }
};

/** GET /api/admin/gastos */
exports.listarGastos = async (req, res) => {
    try {
        const gastos = await GastoOperativo.find()
            .populate('registradoPor', 'nombre email')
            .sort({ fecha: -1 });
        res.json(gastos);
    } catch (e) {
        res.status(500).json({ error: 'Error al obtener gastos' });
    }
};

// ─────────────────────────────────────────────────────────────────
// CIERRE DE CAJA DIARIO
// ─────────────────────────────────────────────────────────────────

/**
 * GET /api/admin/caja/cierre-diario
 * Calcula ventas confirmadas, costos de piezas, gastos y utilidad estimada.
 * Query param opcional: ?fecha=2026-11-04
 */
exports.cierreDiario = async (req, res) => {
    try {
        // Rango del día solicitado (o hoy por defecto)
        const fechaStr = req.query.fecha;
        const inicio   = fechaStr ? new Date(fechaStr) : new Date();
        inicio.setHours(0, 0, 0, 0);
        const fin = new Date(inicio);
        fin.setHours(23, 59, 59, 999);

        // Ventas online (colección Orden)
        const ordenesDelDia = await Orden.find({
            estado: { $in: ['procesado', 'enviado'] },
            $or: [
                { confirmadaEn: { $gte: inicio, $lte: fin } },
                { confirmadaEn: null, fecha: { $gte: inicio, $lte: fin } }
            ]
        }).select('total envioAsegurado items').lean();
        const totalOnline = ordenesDelDia.reduce((s, o) => s + o.total, 0);
        const countOnline = ordenesDelDia.length;
        const ingresosPiezasOnline = ordenesDelDia.reduce(
            (total, orden) => total + Math.max(0, orden.total - (orden.envioAsegurado || 0)),
            0
        );

        // Ventas caja
        const ventasCaja = await Venta.find({
            fecha:  { $gte: inicio, $lte: fin },
            canal:  'caja',
            estado: 'procesado'
        }).select('total items').lean();
        const totalCaja  = ventasCaja.reduce((s, v) => s + v.total, 0);
        const countCaja  = ventasCaja.length;
        const costosItems = [
            ...ordenesDelDia.flatMap((orden) => orden.items || [])
                .map((item) => ({ cantidad: item.cantidad, costo: item.costo_unitario })),
            ...ventasCaja.flatMap((venta) => venta.items || [])
                .map((item) => ({ cantidad: item.cantidad, costo: item.costoUnit }))
        ];
        const itemsSinCosto = costosItems.filter(
            (item) => item.costo === null || item.costo === undefined ||
                !Number.isFinite(Number(item.costo))
        ).length;
        const costoProductos = costosItems.reduce(
            (total, item) => total + (Number(item.costo) || 0) * item.cantidad,
            0
        );
        const ingresosPiezas = ingresosPiezasOnline + totalCaja;

        // Desglose por medio de pago (caja)
        const desglosePago = {};
        for (const v of ventasCaja) {
            desglosePago[v.medioPago] = (desglosePago[v.medioPago] || 0) + v.total;
        }

        // Gastos del día
        const gastosDelDia = await GastoOperativo.find({
            fecha: { $gte: inicio, $lte: fin }
        });
        const totalGastos = gastosDelDia.reduce((s, g) => s + g.monto, 0);

        // Cálculo final
        const totalIngresos = totalOnline + totalCaja;
        const saldoNeto     = totalIngresos - totalGastos;
        const utilidadBruta = itemsSinCosto ? null : ingresosPiezas - costoProductos;
        const utilidadNeta = utilidadBruta === null ? null : utilidadBruta - totalGastos;

        res.json({
            fecha:          inicio.toISOString().split('T')[0],
            ventas: {
                online:     { cantidad: countOnline,  total: totalOnline  },
                caja:       { cantidad: countCaja,    total: totalCaja    },
                desgloseMedioPago: desglosePago
            },
            totalIngresos,
            totalGastos,
            saldoNeto,
            ingresosPiezas,
            costoProductos,
            itemsSinCosto,
            utilidadBruta,
            utilidadNeta,
            estado:         saldoNeto >= 0 ? 'POSITIVO ✅' : 'NEGATIVO ⚠️',
            generadoEn:     new Date().toISOString()
        });

    } catch (e) {
        console.error(e);
        res.status(500).json({ error: 'Error al generar cierre de caja' });
    }
};

/** GET /api/admin/caja/ventas — Historial de ventas presenciales */
exports.historialVentas = async (req, res) => {
    try {
        const { desde, hasta, canal } = req.query;
        const filtro = {};
        if (desde || hasta) {
            filtro.fecha = {};
            if (desde) filtro.fecha.$gte = new Date(desde);
            if (hasta) { const h = new Date(hasta); h.setHours(23,59,59,999); filtro.fecha.$lte = h; }
        }
        if (canal) filtro.canal = canal;

        const ventas = await Venta.find(filtro)
            .populate('registradoPor', 'nombre')
            .sort({ fecha: -1 })
            .limit(200);
        res.json(ventas);
    } catch (e) {
        res.status(500).json({ error: 'Error al obtener historial' });
    }
};

exports.analitica = async (req, res) => {
    try {
        const ahora = new Date();
        const fechaBogota = new Date(ahora.getTime() - 5 * 60 * 60 * 1000)
            .toISOString()
            .slice(0, 10);
        const [anio, mes] = fechaBogota.split('-');
        const inicioHoy = new Date(`${fechaBogota}T00:00:00-05:00`);
        const finHoy = new Date(inicioHoy.getTime() + 24 * 60 * 60 * 1000);
        const inicioMes = new Date(`${anio}-${mes}-01T00:00:00-05:00`);
        const finMes = new Date(inicioMes);
        finMes.setUTCMonth(finMes.getUTCMonth() + 1);
        const [
            visitasHoy,
            alertasSinLeer,
            pedidosPendientes,
            eventos,
            piezasPopulares,
            ordenesMes,
            ventasMes
        ] = await Promise.all([
            Evento.countDocuments({
                tipo: 'visita',
                createdAt: { $gte: inicioHoy, $lt: finHoy }
            }),
            Evento.countDocuments({ leida: false }),
            Orden.countDocuments({ estado: 'pendiente' }),
            Evento.find().sort({ createdAt: -1 }).limit(50).lean(),
            Evento.aggregate([
                { $match: { tipo: 'producto', productoNombre: { $ne: '' } } },
                { $group: { _id: '$productoNombre', vistas: { $sum: 1 } } },
                { $sort: { vistas: -1 } },
                { $limit: 5 }
            ]),
            Orden.find({
                estado: { $in: ['procesado', 'enviado'] },
                $or: [
                    { confirmadaEn: { $gte: inicioMes, $lt: finMes } },
                    { confirmadaEn: null, fecha: { $gte: inicioMes, $lt: finMes } }
                ]
            }).select('total').lean(),
            Venta.find({
                fecha: { $gte: inicioMes, $lt: finMes },
                estado: 'procesado'
            }).select('total').lean()
        ]);
        const ingresosMes = [...ordenesMes, ...ventasMes]
            .reduce((total, venta) => total + (Number(venta.total) || 0), 0);

        res.json({
            visitasHoy,
            alertasSinLeer,
            pedidosPendientes,
            ingresosMes,
            piezasPopulares,
            notificaciones: eventos.map((evento) => ({
                id: evento._id,
                tipo: evento.tipo,
                pagina: evento.pagina,
                productoNombre: evento.productoNombre,
                ordenId: evento.ordenId,
                leida: evento.leida,
                fecha: evento.createdAt
            }))
        });
    } catch (error) {
        console.error('Error al obtener analítica:', error);
        res.status(500).json({ error: 'Error al obtener las notificaciones' });
    }
};

exports.marcarEventoLeido = async (req, res) => {
    try {
        const evento = await Evento.findByIdAndUpdate(
            req.params.id,
            { leida: true },
            { new: true, runValidators: true }
        );
        if (!evento) return res.status(404).json({ error: 'Notificación no encontrada' });
        res.json({ leida: true });
    } catch (error) {
        res.status(400).json({ error: 'No se pudo actualizar la notificación' });
    }
};

exports.subirImagen = async (req, res) => {
    const tiposPermitidos = new Set(['image/jpeg', 'image/png', 'image/webp']);
    const tipo = req.get('content-type');
    if (!tiposPermitidos.has(tipo) || !Buffer.isBuffer(req.body) ||
        req.body.length === 0 || req.body.length > 1_000_000) {
        return res.status(400).json({ error: 'Imagen inválida; usa JPG, PNG o WebP de hasta 1 MB.' });
    }
    const firmaValida = tipo === 'image/jpeg'
        ? req.body.length >= 3 &&
          req.body[0] === 0xff && req.body[1] === 0xd8 && req.body[2] === 0xff
        : tipo === 'image/png'
            ? req.body.length >= 8 &&
              req.body.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))
            : req.body.length >= 12 &&
              req.body.toString('ascii', 0, 4) === 'RIFF' &&
              req.body.toString('ascii', 8, 12) === 'WEBP';
    if (!firmaValida) {
        return res.status(400).json({ error: 'El contenido no coincide con el tipo de imagen declarado.' });
    }

    let archivoId;
    try {
        if (!mongoose.isValidObjectId(req.params.id)) {
            return res.status(404).json({ error: 'Producto no encontrado' });
        }
        const producto = await Producto.findById(req.params.id);
        if (!producto) return res.status(404).json({ error: 'Producto no encontrado' });
        if ((producto.imagenes_360 || []).length >= 36) {
            return res.status(400).json({ error: 'La pieza ya tiene el máximo de 36 imágenes.' });
        }

        const extensiones = {
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/webp': 'webp'
        };
        const bucket = new mongoose.mongo.GridFSBucket(mongoose.connection.db, {
            bucketName: 'joya_media'
        });
        const upload = bucket.openUploadStream(
            `${new mongoose.Types.ObjectId().toString()}.${extensiones[tipo]}`,
            { metadata: { contentType: tipo } }
        );
        archivoId = upload.id;
        await new Promise((resolve, reject) => {
            upload.once('error', reject);
            upload.once('finish', resolve);
            upload.end(req.body);
        });

        const origen = (process.env.PUBLIC_API_ORIGIN ||
            `${req.protocol}://${req.get('host')}`).replace(/\/+$/, '');
        const url = `${origen}/media/${archivoId.toString()}`;
        producto.imagenes_360 = [...(producto.imagenes_360 || []), url];
        if (!producto.imagen) producto.imagen = url;
        await producto.save();
        res.status(201).json({ url, imagenes_360: producto.imagenes_360 });
    } catch (error) {
        if (archivoId) {
            try {
                const bucket = new mongoose.mongo.GridFSBucket(mongoose.connection.db, {
                    bucketName: 'joya_media'
                });
                await bucket.delete(archivoId);
            } catch (cleanupError) {
                console.error('No se pudo limpiar una imagen incompleta:', cleanupError);
            }
        }
        console.error('Error al subir imagen de producto:', error);
        res.status(500).json({ error: 'No se pudo guardar la imagen' });
    }
};
