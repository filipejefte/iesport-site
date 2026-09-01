# -*- coding: utf-8 -*-
"""Monta o index.html a partir de src/iesport-v2-src.html embutindo os assets.

Uso:  python src/inject.py   (a partir da raiz do repositorio)
Requer: Pillow  (pip install Pillow)
"""
import base64, io, pathlib, re, sys
from PIL import Image, ImageFilter

REPO = pathlib.Path(__file__).parent.parent
SRC = REPO / 'src' / 'iesport-v2-src.html'
OUT = REPO / 'index.html'
ASSETS = REPO / 'assets'
PHOTOS = ASSETS / 'photos'

PHOTO_MAP = {
    'laraya': 'laraya.jpg',
    'muriano': 'muriano.jpg',
    'toma': 'toma.jpg',  # retrato de 2015: mesmo padrao (jaleco, fundo claro) dos demais
    'fukoshima': 'fukoshima.jpg',
    'jacob': 'jacob.jpg',
    'antoniassi': 'antoniassi.jpg',
}

def photo_data_uri(fname):
    if not fname:
        return None
    p = PHOTOS / fname
    if not p.is_file():
        return None
    im = Image.open(p).convert('RGB')
    w, h = im.size
    if max(w, h) < 300:  # retratos pequenos de 2015: upscale suave + nitidez
        im = im.resize((w * 2, h * 2), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=68, threshold=2))
    elif max(w, h) > 560:
        im.thumbnail((560, 560), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=84, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

html = SRC.read_text(encoding='utf-8')

# logo do nav: fonte 4x recortada no conteudo e reduzida (nitida em telas retina)
lim = Image.open(ASSETS / 'logo_4x.png').convert('RGB')
import PIL.ImageChops as _ch
bbox = _ch.difference(lim, Image.new('RGB', lim.size, (255, 255, 255))).getbbox()
lim = lim.crop(bbox)
lim.thumbnail((2000, 200), Image.LANCZOS)
lbuf = io.BytesIO()
lim.save(lbuf, 'PNG', optimize=True)
html = html.replace('{{LOGO}}', 'data:image/png;base64,' + base64.b64encode(lbuf.getvalue()).decode())
print(f'logo nav {lim.size} ({len(lbuf.getvalue())/1024:.0f} KB)')

b64 = base64.b64encode((ASSETS / 'logo-footer.png').read_bytes()).decode()
html = html.replace('{{LOGOFOOT}}', 'data:image/png;base64,' + b64)

three = (ASSETS / 'three.min.js').read_text(encoding='utf-8')
assert '</script' not in three.lower(), 'three.min.js contem </script>'
html = html.replace('{{THREEJS}}', three)

loader = (ASSETS / 'gltfloader.js').read_text(encoding='utf-8')
assert '</script' not in loader.lower(), 'gltfloader.js contem </script>'
html = html.replace('{{GLTFLOADER}}', loader)

glb_path = ASSETS / 'models' / 'human.glb'
if glb_path.exists():
    glb64 = base64.b64encode(glb_path.read_bytes()).decode()
    print(f'GLB embutido: {len(glb64)/1024:.0f} KB base64')
else:
    glb64 = ''
    print('SEM GLB: usando manequim de primitivas')
html = html.replace('{{GLB}}', glb64)

map_path = ASSETS / 'map.png'
map64 = base64.b64encode(map_path.read_bytes()).decode()
html = html.replace('{{MAP}}', 'data:image/png;base64,' + map64)

fac_path = ASSETS / 'hero.jpg'  # foto diurna do letreiro, usada na secao O Instituto
fim = Image.open(fac_path).convert('RGB')
fim.thumbnail((1500, 1500), Image.LANCZOS)
fbuf = io.BytesIO()
fim.save(fbuf, 'JPEG', quality=80, optimize=True, progressive=True)
fac_uri = 'data:image/jpeg;base64,' + base64.b64encode(fbuf.getvalue()).decode()
print(f'fachada embutida ({len(fbuf.getvalue())/1024:.0f} KB)')
html = html.replace('{{FACHADA_IMG}}', fac_uri)

def img_repl(m):
    slug, alt = m.group(1), m.group(2)
    uri = photo_data_uri(PHOTO_MAP.get(slug, ''))
    if uri is None:
        print('SEM FOTO:', slug)
        return ''  # mantem apenas o monograma
    return f'<img src="{uri}" alt="{alt}">'

html = re.sub(r'\{\{IMG_([a-z]+)\|([^}]*)\}\}', img_repl, html)

leftover = re.findall(r'\{\{[A-Z_]+', html)
assert not leftover, f'placeholders restantes: {leftover}'
OUT.write_text(html, encoding='utf-8')
print('ok', OUT.name, f'{OUT.stat().st_size/1024:.0f} KB')
