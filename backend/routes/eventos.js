const express = require('express');
const router = express.Router();
const eventos = require('../controllers/eventosController');

router.post('/', eventos.registrar);

module.exports = router;
