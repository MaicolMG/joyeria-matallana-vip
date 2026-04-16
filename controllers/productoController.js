const Producto = require('../models/Producto');

exports.crear = async (req, res) => {
    const data = new Producto(req.body);
    await data.save();
    res.json(data);
};

exports.obtener = async (req, res) => {
    const datos = await Producto.find();
    res.json(datos);
};

exports.eliminar = async (req, res) => {
    await Producto.findByIdAndDelete(req.params.id);
    res.json({ mensaje: 'Eliminado' });
};