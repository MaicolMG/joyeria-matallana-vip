require('dotenv').config();
const mongoose = require('mongoose');
const bcrypt   = require('bcryptjs');
const Usuario  = require('./models/Usuario');

async function crearAdmin() {
    const email = String(process.env.ADMIN_EMAIL || '').trim().toLowerCase();
    const password = process.env.ADMIN_PASSWORD || '';
    if (!process.env.MONGO_URI || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ||
        password.length < 12 || password.length > 128) {
        throw new Error('Configura MONGO_URI, ADMIN_EMAIL válido y ADMIN_PASSWORD de 12 a 128 caracteres.');
    }
    await mongoose.connect(process.env.MONGO_URI);

    const existe = await Usuario.findOne({ email });
    const hash = await bcrypt.hash(password, 12);
    if (existe) {
        existe.rol = 'admin';
        existe.password = hash;
        await existe.save();
        console.log('Rol y contraseña de administrador actualizados para:', email);
    } else {
        const admin = new Usuario({
            nombre: 'Administrador Matallana VIP',
            email,
            password: hash,
            rol: 'admin'
        });

        await admin.save();
        console.log('Administrador creado para:', email);
    }

    const revokeEmail = String(process.env.ADMIN_REVOKE_EMAIL || '').trim().toLowerCase();
    if (revokeEmail && revokeEmail !== email) {
        const revoked = await Usuario.findOneAndUpdate(
            { email: revokeEmail, rol: 'admin' },
            { $set: { rol: 'cliente' } },
            { returnDocument: 'after', runValidators: true }
        );
        if (revoked) {
            console.log('Rol de administrador retirado de:', revokeEmail);
        }
    }
}

crearAdmin()
    .catch((error) => {
        console.error('No se pudo provisionar el administrador:', error.message);
        process.exitCode = 1;
    })
    .finally(async () => {
        if (mongoose.connection.readyState !== 0) {
            await mongoose.connection.close();
        }
    });
