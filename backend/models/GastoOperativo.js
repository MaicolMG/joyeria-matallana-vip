const mongoose = require('mongoose');

const GastoOperativoSchema = new mongoose.Schema({
    descripcion:    { type: String, required: true },
    categoria:      {
        type: String,
        enum: ['Insumos taller', 'Servicios', 'Nómina', 'Publicidad', 'Arriendo', 'Otros'],
        default: 'Otros'
    },
    monto:          { type: Number, required: true, min: 0 },
    registradoPor:  { type: mongoose.Schema.Types.ObjectId, ref: 'Usuario', required: true },
    fecha:          { type: Date, default: Date.now }
});

module.exports = mongoose.model('GastoOperativo', GastoOperativoSchema);
