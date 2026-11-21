const Usuario = require('../models/Usuario');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const failedLogins = new Map();
const MAX_LOGIN_ATTEMPTS = 5;
const LOGIN_WINDOW_MS = 15 * 60 * 1000;

function loginKey(req, email) {
    return {
        ip: `ip:${req.ip || req.socket.remoteAddress}`,
        account: `account:${email}`
    };
}

function recordFailedLogin(key) {
    const now = Date.now();
    for (const [entryKey, entry] of failedLogins) {
        if (entry.expiresAt <= now) failedLogins.delete(entryKey);
    }
    const entry = failedLogins.get(key);
    if (!entry || entry.expiresAt <= now) {
        if (failedLogins.size >= 10000) {
            const oldestKey = failedLogins.keys().next().value;
            if (oldestKey) failedLogins.delete(oldestKey);
        }
        failedLogins.set(key, { attempts: 1, expiresAt: now + LOGIN_WINDOW_MS });
    } else {
        entry.attempts += 1;
    }
}

exports.registro = async (req, res) => {
    try {
        const { nombre, email, password } = req.body;
        const nombreLimpio = typeof nombre === 'string' ? nombre.trim() : '';
        const emailLimpio = typeof email === 'string' ? email.trim().toLowerCase() : '';

        if (!nombreLimpio || nombreLimpio.length > 120 ||
            !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailLimpio) ||
            emailLimpio.length > 254 ||
            typeof password !== 'string' || password.length < 12 || password.length > 128) {
            return res.status(400).json({ error: 'Todos los campos son obligatorios' });
        }

        const existe = await Usuario.findOne({ email: emailLimpio });
        if (existe)
            return res.status(400).json({ error: 'Este correo ya está registrado' });

        const hash = await bcrypt.hash(password, 12);
        const usuario = new Usuario({ nombre: nombreLimpio, email: emailLimpio, password: hash });
        await usuario.save();

        res.json({ mensaje: 'Registro exitoso' });

    } catch (error) {
        console.error('Error registro:', error);
        if (error.code === 11000) {
            return res.status(409).json({ error: 'Este correo ya está registrado' });
        }
        res.status(500).json({ error: 'Error interno al registrar' });
    }
};

exports.login = async (req, res) => {
    try {
        const { email, password } = req.body;
        const emailLimpio = typeof email === 'string' ? email.trim().toLowerCase() : '';
        const claves = loginKey(req, emailLimpio);
        const bloqueado = Object.values(claves).some((key) => {
            const rate = failedLogins.get(key);
            return rate && rate.expiresAt > Date.now() &&
                rate.attempts >= MAX_LOGIN_ATTEMPTS;
        });
        if (bloqueado) {
            return res.status(429).json({
                error: 'Demasiados intentos. Espera 15 minutos antes de volver a intentarlo.'
            });
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailLimpio) ||
            typeof password !== 'string' || !password || password.length > 128) {
            Object.values(claves).forEach(recordFailedLogin);
            return res.status(401).json({ error: 'Correo o contraseña incorrectos' });
        }

        const user = await Usuario.findOne({ email: emailLimpio });
        if (!user) {
            Object.values(claves).forEach(recordFailedLogin);
            return res.status(401).json({ error: 'Correo o contraseña incorrectos' });
        }

        const valido = await bcrypt.compare(password, user.password);
        if (!valido) {
            Object.values(claves).forEach(recordFailedLogin);
            return res.status(401).json({ error: 'Correo o contraseña incorrectos' });
        }

        Object.values(claves).forEach((key) => failedLogins.delete(key));
        const token = jwt.sign(
            { id: user._id, rol: user.rol },
            process.env.JWT_SECRET,
            { expiresIn: '8h' }
        );

        // Devolvemos nombre y rol para que el frontend pueda mostrarlos
        res.json({
            token,
            rol: user.rol,
            nombre: user.nombre,
            email: user.email
        });

    } catch (error) {
        console.error('Error login:', error);
        res.status(500).json({ error: 'Error interno al iniciar sesión' });
    }
};
