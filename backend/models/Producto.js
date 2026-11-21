const mongoose = require('mongoose');

const ProductoSchema = new mongoose.Schema({
    nombre:   { type: String, required: true, trim: true, maxlength: 120 },
    tipo:     { type: String, trim: true, maxlength: 40 },
    precio:   { type: Number, required: true, min: 0 },
    costo_unitario: { type: Number, default: null, min: 0 },
    peso:     { type: Number, default: 0, min: 0 },
    diametro: { type: Number, default: 0 },
    material: { type: String, trim: true, maxlength: 80 },
    imagen:   { type: String, trim: true, maxlength: 2048 },
    video_url: {
        type: String,
        trim: true,
        maxlength: 2048,
        match: /^(?:https:\/\/\S+)?$/i
    },
    imagen_referencial: { type: Boolean, default: false },
    imagenes_360: [{ type: String, trim: true, maxlength: 2048 }],
    oro_18k_g: { type: Number, default: 0, min: 0 },
    esmeralda_ct: { type: Number, default: 0, min: 0 },
    gema: { type: String, trim: true, maxlength: 80 },
    origen: { type: String, trim: true, maxlength: 40 },
    certificado_gemologico: { type: String, trim: true, maxlength: 160 },
    stock:    { type: Number, default: 0, min: 0 },
    activo:   { type: Boolean, default: true },
    genero:   { type: String, enum: ['hombre','mujer','unisex'], default: 'unisex' },
    certificado: {
        autenticidad: { type: Boolean, default: false },
        calidad: String
    }
}, { timestamps: true });

module.exports = mongoose.model('Producto', ProductoSchema);
