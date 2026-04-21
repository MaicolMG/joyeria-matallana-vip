const jwt = require('jsonwebtoken');

const SECRET = 'joyeria_vip';

module.exports = (req, res, next) => {
    const token = req.headers['authorization'];

    if (!token) return res.status(403).json({ error: 'No token' });

    try {
    const decoded = jwt.verify(token, SECRET);
    req.user = decoded;
    next();
    } catch {
    res.status(401).json({ error: 'Token inválido' });
    }
};