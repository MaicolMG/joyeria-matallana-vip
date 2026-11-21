const mongoose = require('mongoose');

const TIPOS_PERMITIDOS = new Set(['image/jpeg', 'image/png', 'image/webp']);

exports.obtener = async (req, res) => {
    if (!mongoose.isValidObjectId(req.params.id)) {
        return res.status(404).json({ error: 'Imagen no encontrada' });
    }

    try {
        const id = new mongoose.Types.ObjectId(req.params.id);
        const bucket = new mongoose.mongo.GridFSBucket(mongoose.connection.db, {
            bucketName: 'joya_media'
        });
        const archivo = await bucket.find({ _id: id }).next();
        if (!archivo) return res.status(404).json({ error: 'Imagen no encontrada' });
        const tipo = archivo.metadata && archivo.metadata.contentType;
        if (!TIPOS_PERMITIDOS.has(tipo)) {
            return res.status(415).json({ error: 'Formato de imagen no permitido' });
        }

        res.set({
            'Content-Type': tipo,
            'Content-Length': String(archivo.length),
            'Cache-Control': 'public, max-age=31536000, immutable',
            'X-Content-Type-Options': 'nosniff',
            'Content-Security-Policy': "default-src 'none'; sandbox"
        });
        const descarga = bucket.openDownloadStream(id);
        descarga.on('error', (error) => {
            console.error('Error al descargar imagen:', error);
            if (!res.headersSent) res.status(500).end();
            else res.destroy(error);
        });
        descarga.pipe(res);
    } catch (error) {
        console.error('Error al consultar imagen:', error);
        if (!res.headersSent) res.status(500).json({ error: 'No se pudo obtener la imagen' });
    }
};
