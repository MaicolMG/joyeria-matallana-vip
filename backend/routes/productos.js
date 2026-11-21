const express = require('express');
const router = express.Router();
const Producto = require('../models/Producto');
const verifyToken = require('../middleware/authMiddleware');

// 🔍 Obtener productos (público — para el catálogo)
router.get('/', async (req, res) => {
    try {
    const productos = await Producto.find().select('-costo_unitario');
    res.json(productos);
    } catch (error) {
    res.status(500).json({ error: 'Error al obtener productos' });
    }
});

// 💾 Crear producto — SOLO ADMIN (cotizaciones van a /api/admin/productos)
router.post('/', verifyToken, async (req, res) => {
    // Verificar que sea admin para crear productos en el catálogo público
    if (req.user.rol !== 'admin') {
        return res.status(403).json({
            error: 'Solo administradores pueden crear productos en el catálogo.'
        });
    }
    try {
        const nuevo = new Producto(req.body);
        await nuevo.save();
        res.json(nuevo);
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: 'Error al guardar producto' });
    }
});

// ❌ Eliminar producto (solo admin)
router.delete('/:id', verifyToken, async (req, res) => {
    if (req.user.rol !== 'admin') {
        return res.status(403).json({ error: 'Solo administradores pueden eliminar productos.' });
    }
    try {
        await Producto.findByIdAndDelete(req.params.id);
        res.json({ msg: 'Producto eliminado' });
    } catch (error) {
        res.status(500).json({ error: 'Error al eliminar' });
    }
});

module.exports = router;