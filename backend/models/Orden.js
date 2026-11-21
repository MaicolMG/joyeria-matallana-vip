const mongoose = require('mongoose');

const ItemSchema = new mongoose.Schema({
    producto_id: { type: mongoose.Schema.Types.ObjectId, ref: 'Producto', required: true },
    nombre: { type: String, trim: true, maxlength: 120 },
    precio: { type: Number, min: 0 },
    costo_unitario: { type: Number, default: null, min: 0 },
    cantidad: { type: Number, required: true, min: 1 }
}, { _id: false });

const OrdenSchema = new mongoose.Schema({
    usuario: { type: mongoose.Schema.Types.ObjectId, ref: 'Usuario', required: true },
    items: [ItemSchema],
    total: { type: Number, required: true },
    numero: { type: String, required: true, unique: true },
    envioAsegurado: { type: Number, default: 0, min: 0 },
    descuento: { type: Number, default: 0, min: 0 },
    codigoPromocional: { type: String, trim: true, maxlength: 40, default: '' },
    metodoPago: {
        type: String,
        enum: ['transferencia', 'pse', 'tarjeta', 'contraentrega', 'reserva_vip'],
        required: true
    },
    datosEnvio: {
        nombre: { type: String, required: true, trim: true, maxlength: 120 },
        email: { type: String, required: true, trim: true, lowercase: true, maxlength: 254 },
        telefono: { type: String, required: true, trim: true, maxlength: 24 },
        direccion: { type: String, required: true, trim: true, maxlength: 180 },
        ciudad: { type: String, required: true, trim: true, maxlength: 80 },
        departamento: { type: String, required: true, trim: true, maxlength: 80 },
        notas: { type: String, trim: true, maxlength: 500, default: '' }
    },
    estado: {
        type: String,
        enum: ['pendiente', 'procesado', 'enviado', 'cancelado'],
        default: 'pendiente'
    },
    confirmadaEn: { type: Date, default: null },
    fecha: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Orden', OrdenSchema);
