const Usuario = require('../models/Usuario');

module.exports = async (req, res, next) => {
    if (!req.user || !req.user.id) {
        return res.status(403).json({ error: 'Acceso denegado. Se requiere rol de administrador.' });
    }

    try {
        const usuario = await Usuario.findById(req.user.id).select('rol');
        if (!usuario || usuario.rol !== 'admin') {
            return res.status(403).json({
                error: 'Acceso denegado. Se requiere rol de administrador.'
            });
        }
        next();
    } catch (error) {
        console.error('No se pudo verificar el rol de administrador:', error);
        res.status(500).json({ error: 'No se pudo verificar el acceso administrativo' });
    }
};
