const express   = require('express');
const router    = express.Router();
const auth      = require('../middleware/authMiddleware');
const esAdmin   = require('../middleware/adminMiddleware');
const ctrl      = require('../controllers/adminController');

// Todos los endpoints requieren token válido + rol admin
router.use(auth, esAdmin);

// ── Inventario ────────────────────────────────────────────
router.get   ('/productos',          ctrl.listarProductos);
router.post  ('/productos',          ctrl.crearProducto);
router.put   ('/productos/:id',      ctrl.editarProducto);
router.delete('/productos/:id',      ctrl.eliminarProducto);
router.get   ('/ordenes',            ctrl.listarOrdenes);
router.patch ('/ordenes/:id/estado', ctrl.actualizarEstadoOrden);
router.post  (
    '/productos/:id/imagenes',
    express.raw({ type: ['image/jpeg', 'image/png', 'image/webp'], limit: '1mb' }),
    ctrl.subirImagen
);

// ── Ventas caja presencial ─────────────────────────────────
router.post  ('/ventas/caja',        ctrl.ventaCaja);
router.get   ('/caja/ventas',        ctrl.historialVentas);

// ── Gastos operativos ──────────────────────────────────────
router.post  ('/gastos',             ctrl.registrarGasto);
router.get   ('/gastos',             ctrl.listarGastos);

// ── Cierre de caja ─────────────────────────────────────────
router.get   ('/caja/cierre-diario', ctrl.cierreDiario);
router.get   ('/analitica',          ctrl.analitica);
router.patch ('/notificaciones/:id/leida', ctrl.marcarEventoLeido);

module.exports = router;
