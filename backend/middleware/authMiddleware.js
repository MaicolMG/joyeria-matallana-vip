const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
    const authorization = req.headers.authorization || '';
    const token = authorization.startsWith('Bearer ')
        ? authorization.slice(7).trim()
        : authorization.trim();

    if (!token) return res.status(401).json({ error: 'Token requerido' });

    try {
        if (!process.env.JWT_SECRET) {
            return res.status(500).json({ error: 'Autenticación no configurada' });
        }
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        res.status(401).json({ error: 'Token inválido o expirado' });
    }
};
