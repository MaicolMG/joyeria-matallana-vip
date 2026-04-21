const Usuario = require('../models/Usuario');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const SECRET = 'joyeria_vip';

exports.registro = async (req, res) => {
    try {
    const { nombre, email, password } = req.body;

    const existe = await Usuario.findOne({ email });
    if (existe) return res.status(400).json({ error: 'Ya existe' });

    const hash = await bcrypt.hash(password, 10);

    const usuario = new Usuario({
        nombre,
        email,
        password: hash
    });

    await usuario.save();

    res.json({ mensaje: 'Registrado' });

    } catch (error) {
    console.log(error);
    res.status(400).json({ error: 'Error registro' });
    }
};

exports.login = async (req, res) => {
    const { email, password } = req.body;

    const user = await Usuario.findOne({ email });
    if (!user) return res.status(400).json({ error: 'No existe' });

    const valido = await bcrypt.compare(password, user.password);
    if (!valido) return res.status(400).json({ error: 'Incorrecto' });

    const token = jwt.sign(
    { id: user._id, rol: user.rol },
    SECRET
    );

    res.json({ token, rol: user.rol });
};