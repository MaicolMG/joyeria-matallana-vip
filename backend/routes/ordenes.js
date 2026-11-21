const express = require('express');
const router = express.Router();
const verifyToken = require('../middleware/authMiddleware');
const ordenController = require('../controllers/ordenController');

// 💾 Crear orden (requiere autenticación) — descuenta stock
router.post('/crear', verifyToken, ordenController.crear);

// 📋 Obtener órdenes del usuario (requiere autenticación)
router.get('/', verifyToken, ordenController.obtener);

// 🔍 Obtener orden por ID (requiere autenticación)
router.get('/:id', verifyToken, ordenController.obtenerPorId);

module.exports = router;
