const Producto = require('../models/Producto');

exports.crear = async (req, res) => {
    try {
        const data = new Producto(req.body);
        await data.save();
        res.json(data);
    } catch (error) {
        res.status(400).json({ error: error.message || 'Error al crear producto' });
    }
};

exports.obtener = async (req, res) => {
    try {
        const datos = await Producto.find({ activo: true });
        res.json(datos);
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener productos' });
    }
};

exports.eliminar = async (req, res) => {
    try {
        await Producto.findByIdAndDelete(req.params.id);
        res.json({ mensaje: 'Eliminado' });
    } catch (error) {
        res.status(500).json({ error: 'Error al eliminar producto' });
    }
};