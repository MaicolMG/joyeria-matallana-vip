const mongoose = require('mongoose');

const UsuarioSchema = new mongoose.Schema({
    nombre:   { type: String, required: true },
    email:    { type: String, unique: true, required: true },
    password: { type: String, required: true },
    telefono: { type: String, default: '' },
    rol:      { type: String, enum: ['cliente','admin'], default: 'cliente' }
}, { timestamps: true });

module.exports = mongoose.model('Usuario', UsuarioSchema);
