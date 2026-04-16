const mongoose = require('mongoose');

const ProductoSchema = new mongoose.Schema({
    nombre: String,
    tipo: String,
    precio: Number,
    peso: Number,
    diametro: Number,
    material: String,
    certificado: {
    autenticidad: Boolean,
    calidad: String
    }
});

module.exports = mongoose.model('Producto', ProductoSchema);