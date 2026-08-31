# -*- coding: utf-8 -*-
"""Gera mapa estatico OSM da clinica com marcador, para embutir como data URI."""
import io, math, urllib.request, pathlib
from PIL import Image, ImageDraw

LAT, LON = -22.2216043, -49.9378541
Z = 17
W, H = 660, 420
OUT = pathlib.Path(__file__).parent.parent / 'assets' / 'map.png'

def deg2num(lat, lon, z):
    lat_r = math.radians(lat)
    n = 2.0 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n
    return x, y

xf, yf = deg2num(LAT, LON, Z)
cx, cy = int(xf), int(yf)

# monta 4x3 tiles ao redor
tiles_x = range(cx - 2, cx + 2)
tiles_y = range(cy - 1, cy + 2)
mosaic = Image.new('RGB', (256 * 4, 256 * 3))
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'IESPORT-site-build/1.0 (+https://github.com/iesport-site)')]
for i, tx in enumerate(tiles_x):
    for j, ty in enumerate(tiles_y):
        url = f'https://tile.openstreetmap.org/{Z}/{tx}/{ty}.png'
        data = opener.open(url, timeout=30).read()
        mosaic.paste(Image.open(io.BytesIO(data)).convert('RGB'), (i * 256, j * 256))

# posicao do ponto no mosaico
px = (xf - (cx - 2)) * 256
py = (yf - (cy - 1)) * 256
# recorte centrado no ponto
left = int(px - W / 2)
top = int(py - H / 2)
crop = mosaic.crop((left, top, left + W, top + H))

d = ImageDraw.Draw(crop)
mx, my = W / 2, H / 2
# pino: circulo navy com borda branca + ponto branco
r = 13
d.ellipse([mx - r - 3, my - r - 3, mx + r + 3, my + r + 3], fill=(255, 255, 255))
d.ellipse([mx - r, my - r, mx + r, my + r], fill=(15, 34, 67))
d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(255, 255, 255))

crop.save(OUT, 'PNG', optimize=True)
print('ok', OUT.name, crop.size, f'{OUT.stat().st_size/1024:.0f} KB')
