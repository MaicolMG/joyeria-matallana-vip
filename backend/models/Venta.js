const mongoose = require('mongoose');

const ItemVentaSchema = new mongoose.Schema({
    producto:   { type: mongoose.Schema.Types.ObjectId, ref: 'Producto', required: true },
    nombre:     String,
    cantidad:   { type: Number, required: true, min: 1 },
    precioUnit: { type: Number, required: true },
    costoUnit:  { type: Number, default: null, min: 0 },
    subtotal:   { type: Number, required: true }
}, { _id: false });

const VentaSchema = new mongoose.Schema({
    items:          [ItemVentaSchema],
    total:          { type: Number, required: true },
    medioPago:      {
        type: String,
        enum: ['Efectivo', 'Tarjeta', 'Transferencia', 'Nequi'],
        required: true
    },
    canal:          {
        type: String,
        enum: ['online', 'caja'],
        default: 'online'
    },
    cliente:        { type: mongoose.Schema.Types.ObjectId, ref: 'Usuario' },
    registradoPor:  { type: mongoose.Schema.Types.ObjectId, ref: 'Usuario' },
    estado:         {
        type: String,
        enum: ['pendiente', 'procesado', 'cancelado'],
        default: 'pendiente'
    },
    fecha:          { type: Date, default: Date.now }
});

module.exports = mongoose.model('Venta', VentaSchema);
