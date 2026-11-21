const express = require('express');
const router = express.Router();
const media = require('../controllers/mediaController');

router.get('/:id', media.obtener);

module.exports = router;
