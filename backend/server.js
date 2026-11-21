require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

if (!process.env.JWT_SECRET || process.env.JWT_SECRET.length < 32) {
    throw new Error('JWT_SECRET debe estar configurado y tener al menos 32 caracteres.');
}
if (!process.env.MONGO_URI) {
    throw new Error('MONGO_URI debe configurarse mediante variables de entorno.');
}

const origins = (process.env.CORS_ORIGINS || '')
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean);
app.use(cors({
    origin: origins.length ? origins : false,
    credentials: false
}));
app.use(express.json({ limit: '1mb' }));

// 🔥 RUTAS
const authRoutes    = require('./routes/auth');
const productoRoutes = require('./routes/productos');
const ordenRoutes   = require('./routes/ordenes');
const adminRoutes   = require('./routes/admin');
const eventosRoutes = require('./routes/eventos');
const mediaRoutes = require('./routes/media');

app.use('/api/auth',      authRoutes);
app.use('/api/productos', productoRoutes);
app.use('/api/ordenes',   ordenRoutes);
app.use('/api/admin',     adminRoutes);
app.use('/api/eventos',   eventosRoutes);
app.use('/media',         mediaRoutes);

// 🔥 PUERTO
const PORT = process.env.PORT || 3000;

mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        console.log('MongoDB conectado');
        app.listen(PORT, () => console.log(`Servidor corriendo en puerto ${PORT}`));
    })
    .catch((error) => {
        console.error('No se pudo conectar a MongoDB:', error.message);
        process.exit(1);
    });