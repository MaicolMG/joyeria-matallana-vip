const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());

// 🔥 CONEXIÓN A MONGODB
mongoose.connect('mongodb://localhost:27017/joyeria')
    .then(() => console.log('✅ MongoDB conectado'))
    .catch(err => console.log('❌ Error MongoDB:', err));

// 🔥 RUTAS
const authRoutes = require('./routes/auth');
const productoRoutes = require('./routes/productos');

app.use('/api/auth', authRoutes);
app.use('/api/productos', productoRoutes);

// 🔥 PUERTO
const PORT = 3000;

app.listen(PORT, () => {
    console.log(`🚀 Servidor corriendo en puerto ${PORT}`);
});