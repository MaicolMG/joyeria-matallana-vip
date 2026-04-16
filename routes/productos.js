const express = require('express');
const router = express.Router();
const Producto = require('../models/Producto');

// 🔍 Obtener productos
router.get('/', async (req, res) => {
    try {
    const productos = await Producto.find();
    res.json(productos);
    } catch (error) {
    res.status(500).json({ error: 'Error al obtener productos' });
    }
});

// 💾 Crear producto
router.post('/', async (req, res) => {
    try {
    const nuevo = new Producto(req.body);
    await nuevo.save();
    res.json(nuevo);
    } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error al guardar producto' });
    }
});

// ❌ Eliminar producto
router.delete('/:id', async (req, res) => {
    try {
    await Producto.findByIdAndDelete(req.params.id);
    res.json({ msg: 'Producto eliminado' });
    } catch (error) {
    res.status(500).json({ error: 'Error al eliminar' });
    }
});

module.exports = router;