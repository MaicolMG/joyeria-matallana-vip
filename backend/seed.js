/**
 * seed.js — Catálogo de Joyería Matallana VIP
 * Imágenes del Metropolitan Museum of Art (dominio público) y Wikimedia Commons.
 * Uso: node seed.js
 */
require('dotenv').config();
const mongoose = require('mongoose');
const Producto = require('./models/Producto');

const MET = "https://upload.wikimedia.org/wikipedia/commons/thumb";

const productos = [
    // ── ANILLOS · MUJER ──────────────────────────────────────────────
    {
        nombre: "Anillo solitario de oro blanco con diamantes", tipo: "anillo",
        precio: 10500000, peso: 5.2, diametro: 18, material: "Oro 18K",
        stock: 10, genero: "mujer",
        imagen: `${MET}/b/bb/Starlight_-_white_gold_ring_with_diamonds.jpg/960px-Starlight_-_white_gold_ring_with_diamonds.jpg`,
        gema: "Diamante",
        certificado: { autenticidad: true, calidad: "VS1" }
    },
    {
        nombre: "Anillo sello de oro con escarabajo", tipo: "anillo",
        precio: 7560000, peso: 4.5, diametro: 16, material: "Oro",
        stock: 8, genero: "mujer",
        imagen: `${MET}/b/b7/Gold_ring_MET_DP109248.jpg/960px-Gold_ring_MET_DP109248.jpg`,
        certificado: { autenticidad: true, calidad: "Autenticidad de referencia" }
    },
    {
        nombre: "Anillo de oro con cornalina", tipo: "anillo",
        precio: 1470000, peso: 3.8, diametro: 15, material: "Oro",
        stock: 20, genero: "mujer",
        imagen: `${MET}/1/1a/Gold_ring_with_carnelian_ring_stone_MET_DP135918.jpg/960px-Gold_ring_with_carnelian_ring_stone_MET_DP135918.jpg`,
        gema: "Cornalina",
        certificado: { autenticidad: true, calidad: "Cornalina" }
    },

    // ── ANILLOS · HOMBRE ─────────────────────────────────────────────
    {
        nombre: "Anillo de caballero con diamante negro", tipo: "anillo",
        precio: 13440000, peso: 8.5, diametro: 22, material: "Oro 18K",
        stock: 6, genero: "hombre",
        imagen: `${MET}/e/e9/Domed_gold_ring_with_a_black_diamond.jpg/960px-Domed_gold_ring_with_a_black_diamond.jpg`,
        gema: "Diamante negro",
        certificado: { autenticidad: true, calidad: "18K" }
    },
    {
        nombre: "Anillo sello de oro con escarabajo de cornalina", tipo: "anillo",
        precio: 18900000, peso: 9.0, diametro: 22, material: "Oro",
        stock: 4, genero: "hombre",
        imagen: `${MET}/c/c0/Gold_ring_with_plain_carnelian_scaraboid_MET_DP135914.jpg/960px-Gold_ring_with_plain_carnelian_scaraboid_MET_DP135914.jpg`,
        gema: "Cornalina",
        certificado: { autenticidad: true, calidad: "Cornalina" }
    },
    {
        nombre: "Anillo de oro con escarabajo", tipo: "anillo",
        precio: 1890000, peso: 6.0, diametro: 20, material: "Oro",
        stock: 15, genero: "hombre",
        imagen: `${MET}/b/b7/Gold_ring_MET_DP109248.jpg/960px-Gold_ring_MET_DP109248.jpg`,
        certificado: { autenticidad: true, calidad: "Autenticidad de referencia" }
    },

    // ── CADENAS · MUJER ──────────────────────────────────────────────
    {
        nombre: "Cadena Oro 18K 50cm", tipo: "cadena",
        precio: 15960000, peso: 12, diametro: 0, material: "Oro 18K",
        stock: 5, genero: "mujer",
        imagen: `${MET}/c/ce/Gold_chain_in_three_strands_MET_DP257487.jpg/960px-Gold_chain_in_three_strands_MET_DP257487.jpg`,
        certificado: { autenticidad: true, calidad: "18K" }
    },
    {
        nombre: "Cadena Plata 925 45cm", tipo: "cadena",
        precio: 1176000, peso: 8, diametro: 0, material: "Plata 925",
        stock: 25, genero: "mujer",
        imagen: `${MET}/6/6d/Necklace%2C_chain_MET_SF2213969.jpg/960px-Necklace%2C_chain_MET_SF2213969.jpg`,
        certificado: { autenticidad: true, calidad: "Plata Ley" }
    },

    // ── CADENAS · HOMBRE ─────────────────────────────────────────────
    {
        nombre: "Cadena Oro 14K 55cm", tipo: "cadena",
        precio: 17640000, peso: 18, diametro: 0, material: "Oro 14K",
        stock: 4, genero: "hombre",
        imagen: `${MET}/8/8a/Necklace%2C_chain_MET_sf9515260.jpg/960px-Necklace%2C_chain_MET_sf9515260.jpg`,
        certificado: { autenticidad: true, calidad: "14K" }
    },
    {
        nombre: "Cadena Plata 925 60cm Hombre", tipo: "cadena",
        precio: 1470000, peso: 15, diametro: 0, material: "Plata 925",
        stock: 20, genero: "hombre",
        imagen: `${MET}/a/ae/Silver_necklace_875.JPG/960px-Silver_necklace_875.JPG`,
        certificado: { autenticidad: true, calidad: "Plata Ley" }
    },
    {
        nombre: "Cadena Platino 950 50cm", tipo: "cadena",
        precio: 23100000, peso: 14, diametro: 0, material: "Platino 950",
        stock: 3, genero: "unisex",
        imagen: `${MET}/f/f3/Necklace%2C_chain_MET_sf951617color.jpg/960px-Necklace%2C_chain_MET_sf951617color.jpg`,
        certificado: { autenticidad: true, calidad: "Pt950" }
    },

    // ── MANILLAS · MUJER ─────────────────────────────────────────────
    {
        nombre: "Manilla Oro 18K Mujer", tipo: "manilla",
        precio: 11760000, peso: 10, diametro: 60, material: "Oro 18K",
        stock: 7, genero: "mujer",
        imagen: `${MET}/6/64/Gold_bracelet_MET_DT333008.jpg/960px-Gold_bracelet_MET_DT333008.jpg`,
        certificado: { autenticidad: true, calidad: "18K" }
    },
    {
        nombre: "Manilla Plata 925 Mujer", tipo: "manilla",
        precio: 924000, peso: 12, diametro: 60, material: "Plata 925",
        stock: 30, genero: "mujer",
        imagen: `${MET}/4/4c/Gold_bracelet_MET_DT333008edited3.jpg/960px-Gold_bracelet_MET_DT333008edited3.jpg`,
        certificado: { autenticidad: true, calidad: "Plata Ley" }
    },

    // ── MANILLAS · HOMBRE ────────────────────────────────────────────
    {
        nombre: "Manilla Oro 14K Hombre", tipo: "manilla",
        precio: 14700000, peso: 20, diametro: 70, material: "Oro 14K",
        stock: 5, genero: "hombre",
        imagen: `${MET}/8/85/Gold_bracelet_with_a_carnelian_stone_MET_262377.jpg/960px-Gold_bracelet_with_a_carnelian_stone_MET_262377.jpg`,
        certificado: { autenticidad: true, calidad: "14K" }
    },
    {
        nombre: "Manilla Plata 925 Hombre", tipo: "manilla",
        precio: 1260000, peso: 18, diametro: 70, material: "Plata 925",
        stock: 25, genero: "hombre",
        imagen: `${MET}/1/1f/Electrotype_copy_of_a_gold_bracelet_MET_sf74513553rod.jpg/960px-Electrotype_copy_of_a_gold_bracelet_MET_sf74513553rod.jpg`,
        certificado: { autenticidad: true, calidad: "Plata Ley" }
    },
    {
        nombre: "Manilla Oro 18K Hombre", tipo: "manilla",
        precio: 16800000, peso: 22, diametro: 72, material: "Oro 18K",
        stock: 3, genero: "hombre",
        imagen: `${MET}/6/64/Gold_bracelet_MET_DT333008.jpg/960px-Gold_bracelet_MET_DT333008.jpg`,
        certificado: { autenticidad: true, calidad: "18K" }
    },

    // ── PULSERAS · MUJER ─────────────────────────────────────────────
    {
        nombre: "Pulsera Oro 18K", tipo: "pulsera",
        precio: 9240000, peso: 8, diametro: 0, material: "Oro 18K",
        stock: 8, genero: "mujer",
        imagen: `${MET}/4/4c/Gold_bracelet_MET_DT333008edited3.jpg/960px-Gold_bracelet_MET_DT333008edited3.jpg`,
        certificado: { autenticidad: true, calidad: "18K" }
    },
    {
        nombre: "Pulsera Plata 925", tipo: "pulsera",
        precio: 756000, peso: 10, diametro: 0, material: "Plata 925",
        stock: 28, genero: "mujer",
        imagen: `${MET}/8/85/Gold_bracelet_with_a_carnelian_stone_MET_262377.jpg/960px-Gold_bracelet_with_a_carnelian_stone_MET_262377.jpg`,
        certificado: { autenticidad: true, calidad: "Plata Ley" }
    },

    // ── AROS · MUJER ─────────────────────────────────────────────────
    {
        nombre: "Aros Oro 18K", tipo: "aro",
        precio: 6300000, peso: 3, diametro: 12, material: "Oro 18K",
        stock: 12, genero: "mujer",
        imagen: `${MET}/0/07/Gold_necklace_with_pendants_MET_sf74513396.jpg/960px-Gold_necklace_with_pendants_MET_sf74513396.jpg`,
        certificado: { autenticidad: true, calidad: "18K" }
    },
    {
        nombre: "Aros Plata 925", tipo: "aro",
        precio: 504000, peso: 2.5, diametro: 10, material: "Plata 925",
        stock: 35, genero: "mujer",
        imagen: `${MET}/a/ae/Silver_necklace_875.JPG/960px-Silver_necklace_875.JPG`,
        certificado: { autenticidad: true, calidad: "Plata Ley" }
    },

    // ── DIJES ────────────────────────────────────────────────────────
    {
        nombre: "Dije Oro 18K con Esmeralda", tipo: "dije",
        precio: 5040000, peso: 4, diametro: 25, material: "Oro 18K",
        stock: 10, genero: "mujer",
        imagen: `${MET}/2/2f/Gold_necklace_with_crescent-shaped_pendant_MET_DP160653.jpg/960px-Gold_necklace_with_crescent-shaped_pendant_MET_DP160653.jpg`,
        certificado: { autenticidad: true, calidad: "18K" }
    },
    {
        nombre: "Dije Plata 925 Unisex", tipo: "dije",
        precio: 378000, peso: 3, diametro: 22, material: "Plata 925",
        stock: 40, genero: "unisex",
        imagen: `${MET}/5/56/Necklace_with_gold_beads_and_pendants_attached_to_agate_in_box_setting_MET_sf74513398.jpg/960px-Necklace_with_gold_beads_and_pendants_attached_to_agate_in_box_setting_MET_sf74513398.jpg`,
        certificado: { autenticidad: true, calidad: "Plata Ley" }
    },

    // ── COLGANTES ────────────────────────────────────────────────────
    {
        nombre: "Colgante Oro 14K Luna", tipo: "colgante",
        precio: 7560000, peso: 5, diametro: 20, material: "Oro 14K",
        stock: 6, genero: "mujer",
        imagen: `${MET}/5/5f/Necklace_of_gold_and_carnelian_beads%2C_with_gold-capped_carnelian_pendant_MET_sf74513389.jpg/960px-Necklace_of_gold_and_carnelian_beads%2C_with_gold-capped_carnelian_pendant_MET_sf74513389.jpg`,
        certificado: { autenticidad: true, calidad: "14K" }
    },
];

async function seed() {
    try {
        if (!process.env.MONGO_URI) {
            throw new Error('MONGO_URI debe configurarse mediante variables de entorno.');
        }
        await mongoose.connect(process.env.MONGO_URI);
        console.log('✅ Conectado a MongoDB');

        await Producto.deleteMany({});
        console.log('🗑️  Productos anteriores eliminados');

        await Producto.insertMany(productos);
        console.log(`✅ ${productos.length} productos insertados`);

        const stats = {
            hombre: await Producto.countDocuments({ genero: 'hombre' }),
            mujer:  await Producto.countDocuments({ genero: 'mujer'  }),
            unisex: await Producto.countDocuments({ genero: 'unisex' }),
            conImg: await Producto.countDocuments({ imagen: { $exists: true, $ne: '' } }),
        };
        console.log(`📊 Hombre: ${stats.hombre} | Mujer: ${stats.mujer} | Unisex: ${stats.unisex}`);
        console.log(`🖼️  Con imagen: ${stats.conImg}/${productos.length}`);

        await mongoose.connection.close();
        console.log('✅ Listo');
        process.exit(0);
    } catch (e) {
        console.error('❌', e);
        process.exit(1);
    }
}

seed();
