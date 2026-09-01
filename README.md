# IESPORT — Instituto de Especialidades Ortopédicas

Site institucional de página única para o IESPORT (Marília/SP): oito ortopedistas,
um subespecialista para cada região do corpo.

O site inteiro é **um único arquivo HTML** (`index.html`) com todos os recursos
embutidos como data URIs — sem dependências externas além do Google Fonts (Raleway).
Isso permite hospedar em qualquer serviço de arquivos estáticos (GitHub Pages,
Netlify, Cloudflare Pages, ou a hospedagem que a clínica já usa) sem build no servidor.

## Destaques

- **Mapa 3D interativo do corpo** (Three.js + modelo GLB embutido): cada ponto
  colorido leva ao card da subespecialidade; arraste para girar, toque para navegar.
  Se WebGL não estiver disponível, cai para uma silhueta SVG estática.
- **Hero com a identidade da marca**: silhueta com os seis pontos das regiões
  (clicáveis) sobre anéis dourados, no navy institucional.
- **Google Maps nativo com fallback**: a página tenta carregar o embed oficial do
  Google Maps; em ambientes que bloqueiam iframes externos, mantém um mapa
  estático OpenStreetMap gerado no build.
- **Agendamento via WhatsApp** com mensagens pré-preenchidas por especialidade e
  por médico (`wa.me`).
- Paleta e tipografia recuperadas da identidade original da clínica
  (navy `#0F2243`, dourado `#D9A441`, Raleway).

## Estrutura

```
index.html              site final (gerado — não editar à mão)
src/
  iesport-v2-src.html   fonte editável, com placeholders {{...}}
  inject.py             build: embute logos, fotos, 3D e mapa no HTML
  build_map.py          gera assets/map.png a partir de tiles OpenStreetMap
assets/                 logos, fotos, Three.js, modelo 3D, mapa
```

## Build

```bash
pip install Pillow
python src/inject.py     # gera index.html na raiz
```

Para atualizar o mapa estático (só é preciso se o endereço mudar):

```bash
python src/build_map.py  # regenera assets/map.png
```

## Conteúdo e manutenção

- Telefones, WhatsApp, endereço e horários estão no HTML fonte — busque pelo
  valor atual para trocar (aparecem no topo, no hero, em Contato e no rodapé;
  os links `wa.me` usam o número com DDI: `5514997122181`).
- O e-mail `iesport@outlook.com` veio do material público da clínica e tem fonte
  única — vale confirmar com a clínica antes de manter em produção.
- As fotos da fachada e do letreiro vieram da ficha pública da clínica no Google
  Maps — para produção, vale a autorização formal da clínica. Os cards dos
  médicos usam monogramas por decisão editorial (ver pendências abaixo).

### Pendências para produção (conformidade CFM)

Corpo clínico atualizado em 01/09/2026 conforme lista da própria clínica
(9 especialistas; saíram Yanasse e Ferro, entraram Salgado, Reinas e Baldissera).

- Exibir no rodapé o **nome e CRM do diretor técnico médico** da clínica.
- Obter o **RQE** dos Drs. Muriano e Antoniassi (não publicado em fonte alguma).
- Obter a **formação acadêmica** dos Drs. Laraya e Reinas (sem fonte pública;
  as bios no ar contêm apenas o que é verificável).
- Confirmar se o Dr. Antoniassi atende **joelho** além de quadril, os convênios
  aceitos além da Unimed e a composição societária atual.
- **Fotos**: retratos vindos da melhor fonte pública de cada médico (site
  próprio: Antoniassi e Fukoshima; diretoria da SBMEE: Laraya; Doctoralia:
  Salgado; Instagram profissional: Baldissera; site 2015 da própria clínica:
  Muriano, Jacob e Toma). O Dr. Reinas não tem retrato público — fica com
  monograma até a clínica enviar. Para produção, formalizar a **autorização de
  imagem** com cada médico (art. 20 do Código Civil); um ensaio fotográfico
  padronizado dos nove é o upgrade ideal.
  Há um comentário com essa lista no HTML fonte, antes do rodapé.

## Créditos e licenças de terceiros

- [Three.js](https://threejs.org) r147 e `GLTFLoader` — licença MIT.
- Modelo 3D "Human Base Mesh" de **Arthur Migranov**, via
  [Poly Pizza](https://poly.pizza/m/eWGDnQ0jzmH) — licença
  [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). A atribuição também
  está em comentário no HTML; a licença pede crédito visível de forma razoável,
  então mantenha esta seção (ou um crédito equivalente) ao redistribuir.
- Mapa estático montado com tiles © colaboradores do
  [OpenStreetMap](https://www.openstreetmap.org/copyright) (crédito visível no site).
- Fonte [Raleway](https://fonts.google.com/specimen/Raleway) via Google Fonts — OFL.
