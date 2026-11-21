"""
Utilidades de formato y tablas de precios en COP para joyería a medida.
Precios basados en el mercado colombiano (Bogotá / Medellín, 2026).
"""
from urllib.parse import urlparse

# Tasa de cambio referencial USD → COP
TRM = 4_200  # pesos colombianos por dólar

# --------------------------------------------------------------------------- #
# Precios de metales — COP por gramo (mercado Colombia 2026)
# --------------------------------------------------------------------------- #
PRECIOS_METAL = {
    "oro_18k":   {"nombre": "Oro 18K",       "precio_gramo": 189_000},
    "oro_14k":   {"nombre": "Oro 14K",       "precio_gramo": 147_000},
    "oro_10k":   {"nombre": "Oro 10K",       "precio_gramo": 118_000},
    "plata_925": {"nombre": "Plata Ley 925", "precio_gramo":   3_400},
    "platino":   {"nombre": "Platino 950",   "precio_gramo": 126_000},
}

# --------------------------------------------------------------------------- #
# Precios de gemas — COP por quilate
# Incluye gemas colombianas: esmeralda (Boyacá), cristal de roca, cuarzo rosa
# --------------------------------------------------------------------------- #
PRECIOS_GEMA = {
    "esmeralda_colombiana": {"nombre": "Esmeralda Colombiana (Boyacá)", "precio_quilate": 4_500_000},
    "esmeralda_comercial":  {"nombre": "Esmeralda Comercial",           "precio_quilate": 1_200_000},
    "diamante":             {"nombre": "Diamante",                      "precio_quilate": 21_000_000},
    "rubi":                 {"nombre": "Rubí",                         "precio_quilate": 16_800_000},
    "zafiro":               {"nombre": "Zafiro",                        "precio_quilate":  8_400_000},
    "topacio":              {"nombre": "Topacio Azul",                  "precio_quilate":  2_100_000},
    "cuarzo_rosa":          {"nombre": "Cuarzo Rosa",                   "precio_quilate":    420_000},
    "cristal_roca":         {"nombre": "Cristal de Roca",               "precio_quilate":    210_000},
    "ninguna":              {"nombre": "Sin gema",                      "precio_quilate":          0},
}

# Peso base estimado (gramos) por tipo de joya
PESO_BASE = {
    "anillo":   4.0,
    "cadena":   8.0,
    "manilla": 15.0,
    "pulsera": 12.0,
    "aro":      2.0,
    "colgante": 3.0,
    "dije":     5.0,
}

TALLAS_ANILLO = [str(i) for i in range(8, 25)]
TALLAS_CADENA = ["40 cm", "45 cm", "50 cm", "55 cm", "60 cm", "70 cm"]

COSTO_GRABADO    = 210_000  # COP fijo por grabado
MARGEN_MANO_OBRA = 0.30     # 30 % sobre materiales


# --------------------------------------------------------------------------- #
# Helpers de formato
# --------------------------------------------------------------------------- #

def formatear_precio(valor):
    """Formatea un número como precio en pesos colombianos."""
    return f"$ {valor:,.0f} COP"

def formatear_precio_corto(valor):
    """Versión compacta para tarjetas de producto."""
    if valor >= 1_000_000:
        return f"$ {valor/1_000_000:.1f}M"
    return f"$ {valor:,.0f}"

def formatear_peso(valor):
    """Muestra el peso de una pieza en gramos."""
    peso = float(valor or 0)
    return f"{peso:g} g"

def obtener_imagen_producto(producto, size=600):
    imagen = producto.get("imagen")
    if isinstance(imagen, str):
        parsed = urlparse(imagen.strip())
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return imagen.strip()
    nombre = producto.get("nombre", "Joya")
    tipo   = producto.get("tipo", "joya")
    colores = {
        "anillo":   "1a1a1a/d4af37",
        "cadena":   "1a1a1a/c0a062",
        "manilla":  "1a1a1a/b8860b",
        "pulsera":  "1a1a1a/daa520",
        "aro":      "1a1a1a/e6c200",
        "colgante": "1a1a1a/ccac00",
        "dije":     "1a1a1a/ffd700",
    }
    color = colores.get(tipo, "1a1a1a/d4af37")
    texto = nombre.replace(" ", "+")[:18]
    return f"https://placehold.co/{size}x{size}/{color}?text={texto}"


# --------------------------------------------------------------------------- #
# Cálculo de presupuesto
# --------------------------------------------------------------------------- #

def calcular_presupuesto(tipo_joya, metal, gema, quilates, grabado):
    peso          = PESO_BASE.get(tipo_joya, 4.0)
    precio_metal  = PRECIOS_METAL.get(metal, {}).get("precio_gramo", 0)
    costo_metal   = peso * precio_metal
    precio_gema   = PRECIOS_GEMA.get(gema, {}).get("precio_quilate", 0)
    costo_gema    = quilates * precio_gema
    costo_grabado = COSTO_GRABADO if grabado else 0
    costo_mat     = costo_metal + costo_gema + costo_grabado
    mano_obra     = costo_mat * MARGEN_MANO_OBRA
    total         = costo_mat + mano_obra
    return {
        "peso_estimado":   peso,
        "costo_metal":     costo_metal,
        "costo_gema":      costo_gema,
        "costo_grabado":   costo_grabado,
        "costo_materiales":costo_mat,
        "mano_obra":      mano_obra,
        "total":           total,
    }
