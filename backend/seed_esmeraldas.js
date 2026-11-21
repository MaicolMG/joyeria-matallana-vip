/**
 * Carga aditiva de joyas con esmeralda para el catálogo.
 * No elimina ni modifica productos existentes.
 * Uso: npm run catalogo:esmeraldas
 */
require('dotenv').config();
const mongoose = require('mongoose');
const Producto = require('./models/Producto');

const imagenes = {
    anillo: 'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d9/Gold_ring_set_with_an_emerald_MET_DT283.jpg/960px-Gold_ring_set_with_an_emerald_MET_DT283.jpg',
    aretes: 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/07/Pair_of_Earrings%2C_600s_AD%2C_Early_Byzantine%2C_gold%2C_pearls%2C_glass%2C_and_emeralds_-_Cleveland_Museum_of_Art_-_DSC08327.JPG/960px-Pair_of_Earrings%2C_600s_AD%2C_Early_Byzantine%2C_gold%2C_pearls%2C_glass%2C_and_emeralds_-_Cleveland_Museum_of_Art_-_DSC08327.JPG',
    dije: 'https://thumb.wikimedia.org/wikipedia/commons/thumb/7/74/Spanish_jewellery-Gold_and_emerald_pendant_at_VAM-01.jpg/960px-Spanish_jewellery-Gold_and_emerald_pendant_at_VAM-01.jpg',
    manilla: 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ad/Byzantine_necklace_with_cross_pendant_and_ring%2C_6th-7th_centuries%2C_gold%2C_emerald%2C_amethyst%2C_sapphire%2C_pearls%2C_niello%2C_in_the_Neues_Museum%2C_Berlin.jpg/960px-Byzantine_necklace_with_cross_pendant_and_ring%2C_6th-7th_centuries%2C_gold%2C_emerald%2C_amethyst%2C_sapphire%2C_pearls%2C_niello%2C_in_the_Neues_Museum%2C_Berlin.jpg',
};

const piezas = [
    { nombre: 'Anillo de esmeralda en oro 18K', tipo: 'anillo', material: 'Oro 18K', precio: 4850000, imagen: imagenes.anillo },
    { nombre: 'Anillo de esmeralda en plata 925', tipo: 'anillo', material: 'Plata 925', precio: 1480000, imagen: imagenes.anillo },
    { nombre: 'Aretes de esmeralda en oro 18K', tipo: 'arete', material: 'Oro 18K', precio: 6250000, imagen: imagenes.aretes },
    { nombre: 'Aretes de esmeralda en plata 925', tipo: 'arete', material: 'Plata 925', precio: 1850000, imagen: imagenes.aretes },
    { nombre: 'Dije de esmeralda en oro 18K', tipo: 'dije', material: 'Oro 18K', precio: 3950000, imagen: imagenes.dije },
    { nombre: 'Dije de esmeralda en plata 925', tipo: 'dije', material: 'Plata 925', precio: 1250000, imagen: imagenes.dije },
    { nombre: 'Manilla de esmeralda en oro 18K', tipo: 'manilla', material: 'Oro 18K', precio: 7950000, imagen: imagenes.manilla },
    { nombre: 'Manilla de esmeralda en plata 925', tipo: 'manilla', material: 'Plata 925', precio: 2350000, imagen: imagenes.manilla },
].map((pieza) => ({
    ...pieza,
    gema: 'Esmeralda',
    imagen_referencial: true,
    peso: 0,
    oro_18k_g: 0,
    esmeralda_ct: 0,
    certificado_gemologico: 'Por confirmar',
    stock: 1,
    genero: 'unisex',
    activo: true,
}));

async function cargarCatalogo() {
    if (!process.env.MONGO_URI) {
        throw new Error('MONGO_URI debe configurarse mediante variables de entorno.');
    }

    await mongoose.connect(process.env.MONGO_URI);
    let agregadas = 0;
    let existentes = 0;

    for (const pieza of piezas) {
        const yaExiste = await Producto.exists({ nombre: pieza.nombre });
        if (yaExiste) {
            existentes += 1;
            continue;
        }
        await Producto.create(pieza);
        agregadas += 1;
    }

    console.log(`Catálogo de esmeraldas listo: ${agregadas} agregadas, ${existentes} ya existentes.`);
}

cargarCatalogo()
    .catch((error) => {
        console.error('No se pudo cargar el catálogo de esmeraldas:', error.message);
        process.exitCode = 1;
    })
    .finally(async () => {
        await mongoose.disconnect();
    });
