const mongoose = require('mongoose');

const EventoSchema = new mongoose.Schema({
    tipo: {
        type: String,
        enum: ['visita', 'producto', 'cotizacion', 'pedido'],
        required: true
    },
    pagina: {
        type: String,
        enum: ['inicio', 'catalogo', 'a_medida', 'carrito', 'mi_cuenta'],
        required: true
    },
    sesionAnonima: {
        type: String,
        required: true,
        match: /^[0-9a-f-]{36}$/i
    },
    productoId: { type: String, maxlength: 80, default: '' },
    productoNombre: { type: String, maxlength: 120, default: '' },
    ordenId: { type: String, maxlength: 80, default: '' },
    leida: { type: Boolean, default: false }
}, { timestamps: true });

EventoSchema.index({ createdAt: -1 });
EventoSchema.index({ tipo: 1, createdAt: -1 });
EventoSchema.index({ createdAt: 1 }, { expireAfterSeconds: 15_552_000 });

module.exports = mongoose.model('Evento', EventoSchema);
