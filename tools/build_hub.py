#!/usr/bin/env python3
"""Public hub of the Global and EU Semiconductor Value Chain Radar.
map template (global/map/template.html) + world/europe geometry + global_index.json (+ per-region meta.json) -> hub/index.html
Public rules: no private (claude.ai) links; click = country card when one exists, else public radar; regions without a public page show numbers only."""
import json, pathlib, re, sys, urllib.request
HUB = pathlib.Path(__file__).resolve().parent.parent
DATA = HUB / 'tools' / 'data'                      # world.json, europe.json, esra.json (gen_eu.mjs / gen_esra.mjs in the sandbox global/map), global_index_src.json
BRAND = 'Global and EU Semiconductor Value Chain Radar'
CARDS = {'DE-SN': 'https://smarterinstruments.github.io/sn/'}          # regions with a published country card
META = {'DE-SN': '/home/claude/saxony-radar/meta.json'}                 # per-region meta.json written by the radar builds (local path or URL)

# ESRA – European Semiconductor Regions Alliance, member regions per country (esra-org.eu, read 17 Nov 2026; 44 regions)
ESRA_URL = 'https://www.esra-org.eu/'
ESRA = {
 'DE': ['Baden-Württemberg', 'Bavaria', 'Hamburg', 'Hesse', 'Lower Saxony', 'North Rhine-Westphalia', 'Saarland', 'Saxony', 'Saxony-Anhalt', 'Schleswig-Holstein', 'Thuringia'],
 'ES': ['Andalusia', 'Basque Country', 'Catalonia', 'Madrid', 'Valencia'],
 'FR': ['Auvergne-Rhône-Alpes', 'Île-de-France', 'Occitanie', 'Région SUD – Provence-Alpes-Côte d\'Azur'],
 'NL': ['Flevoland', 'Gelderland', 'North Brabant', 'Overijssel'],
 'IT': ['Lombardy', 'Piemonte', 'Sicily'], 'CZ': ['South Moravia', 'Pilsen', 'Zlín'], 'FI': ['Helsinki', 'Tampere', 'Oulu'],
 'AT': ['Carinthia', 'Styria'], 'PT': ['Centro', 'Norte'], 'SE': ['Östergötland', 'Skåne'],
 'BE': ['Flanders'], 'SK': ['Bratislava'], 'PL': ['Pomerania'], 'IE': ['Ireland'], 'GB': ['Wales'],
}
ESRA_STATE = {'DE-SN': {'member': True, 'since': 2023, 'role': 'initiator'}, 'DE-BY': {'member': True, 'since': 2023}, 'DE-BW': {'member': True, 'since': 2023}}
idx = json.loads((DATA / 'global_index_src.json').read_text(encoding='utf-8'))
idx['esra'] = {'url': ESRA_URL, 'total': sum(len(v) for v in ESRA.values()), 'chair2026': 'Catalonia', 'byCountry': ESRA}
for r in idx['regions']:
    u = r.get('url') or ''
    if 'claude.ai' in u or not r.get('public'):            # private artifacts / internal previews: numbers only
        r['url'] = None; r.pop('preview', None)
    r['card'] = CARDS.get(r['id'])
    if r.get('level') == 'state': r['esra'] = ESRA_STATE.get(r['id'], {'member': False})
    else: r['esra'] = {'n': len(ESRA.get(r['a2'], [])), 'regions': ESRA.get(r['a2'], [])}
    m = META.get(r['id'])
    if m:                                                   # refresh counts from the radar's own meta.json
        mj = json.loads(pathlib.Path(m).read_text(encoding='utf-8')) if not m.startswith('http') else json.load(urllib.request.urlopen(m))
        for k in ('edition', 'updated', 'orgs', 'verified', 'active31', 'news', 'events', 'ipcei', 'ipcei_ast', 'chipsact', 'seg'):
            if k in mj: r[k] = mj[k]
        if mj.get('url'): r['url'] = mj['url']
idx['brand'] = BRAND
(HUB / 'global_index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding='utf-8')

T = (HUB / 'tools' / 'template.html').read_text(encoding='utf-8')
def J(o): return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
for tok, f in [('/*__WORLD__*/', 'world.json'), ('/*__EUROPE__*/', 'europe.json'), ('/*__ESRA__*/', 'esra.json'), ('/*__POINTS__*/', 'points.json')]:
    assert T.count(tok) == 1, tok; T = T.replace(tok, J(json.loads((DATA / f).read_text(encoding='utf-8'))))
assert T.count('/*__INDEX__*/') == 1; T = T.replace('/*__INDEX__*/', J(idx))
import re as _re
assert not _re.search(r'chipdiplo|\bceias\b|claude\.ai', T, _re.I), 'forbidden string in hub page'
(HUB / 'index.html').write_text(T, encoding='utf-8')
print('hub written', (HUB / 'index.html').stat().st_size, 'bytes;', sum(1 for r in idx['regions'] if r.get('url')), 'public radars,', sum(1 for r in idx['regions'] if r.get('card')), 'cards')
