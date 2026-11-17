#!/usr/bin/env python3
"""Public hub of the Global and EU Semiconductor Value Chain Radar.
map template (global/map/template.html) + world/europe geometry + global_index.json (+ per-region meta.json) -> hub/index.html
Public rules: no private (claude.ai) links; click = country card when one exists, else public radar; regions without a public page show numbers only."""
import json, pathlib, re, sys, urllib.request
HUB = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path('/home/claude/global/map')
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
idx = json.loads((SRC / 'global_index.json').read_text(encoding='utf-8'))
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

T = (SRC / 'template.html').read_text(encoding='utf-8')
def J(o): return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
for tok, f in [('/*__WORLD__*/', 'world.json'), ('/*__EUROPE__*/', 'europe.json')]:
    assert T.count(tok) == 1, tok; T = T.replace(tok, J(json.loads((SRC / f).read_text(encoding='utf-8'))))
assert T.count('/*__INDEX__*/') == 1; T = T.replace('/*__INDEX__*/', J(idx))

# --- public naming ---
T = T.replace('<title>Global Semiconductor Value Chain Radar – CNSC</title>', f'<title>{BRAND} – alpha</title><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Which countries and regions already have a weekly radar of public activity in the semiconductor value chain – one taxonomy, one metric. Click a country for its card and live radar.">')
T = T.replace("title: 'Globální radar polovodičového hodnotového řetězce',", f"title: '{BRAND}',")
T = T.replace("title: 'Global Semiconductor Value Chain Radar',", f"title: '{BRAND}',")
T = T.replace("title: 'Globaler Radar der Halbleiter-Wertschöpfungskette',", f"title: '{BRAND}',")
# --- click target: country card first, then public radar ---
rep = [
 ("if (t.kind === 'region') { const r = regById[t.id]; if (r.url) window.open(r.url, '_blank', 'noopener'); return; }",
  "if (t.kind === 'region') { const r = regById[t.id]; const u = r.card || r.url; if (u) window.open(u, '_blank', 'noopener'); return; }"),
 ("if (t.kind === 'group') { const g = ALL.find(r => r.group === t.group && r.url); if (g) window.open(g.url, '_blank', 'noopener'); return; }",
  "if (t.kind === 'group') { const g = ALL.find(r => r.group === t.group && (r.card || r.url)); if (g) window.open(g.card || g.url, '_blank', 'noopener'); return; }"),
 ("if (rs.length === 1 && rs[0].level === 'country') { window.open(rs[0].url, '_blank', 'noopener'); return; }",
  "if (rs.length === 1 && rs[0].level === 'country') { const u = rs[0].card || rs[0].url; if (u) window.open(u, '_blank', 'noopener'); return; }"),
 ("class: 'state ' + r.status + (r.url ? ' pointer' : '')", "class: 'state ' + r.status + ((r.card || r.url) ? ' pointer' : '')"),
 # region list card: country card button + radar button
 ("""<div class="links"><a class="btn" href="${esc(r.url)}" target="_blank" rel="noopener">${esc(t.open)}${r.public ? '' : ' · ' + esc(t.internal)}</a>""",
  """<div class="links">${r.card ? `<a class="btn" href="${esc(r.card)}" target="_blank" rel="noopener">${esc(t.openCard)}</a>` : ''}${r.url ? `<a class="btn${r.card ? ' sec' : ''}" href="${esc(r.url)}" target="_blank" rel="noopener">${esc(t.open)}</a>` : (r.card ? '' : `<span class="btn sec" style="opacity:.6;cursor:default">${esc(t.internal)}</span>`)}"""),
]
for a, b in rep:
    assert T.count(a) == 1, a[:60]; T = T.replace(a, b)
# hover hint: card vs radar
T = T.replace("""${r.url ? `<div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : tr.clickOpen)} ↗</div>` : ''}`;
    return `<h4>""", """${(r.card || r.url) ? `<div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : (r.card ? tr.clickCard : tr.clickOpen))} ↗</div>` : ''}`;
    return `<h4>""")
assert 'tr.clickCard' in T
# strings
T = T.replace("open: 'Otevřít radar', repo: 'Data (GitHub)',", "open: 'Živý radar', openCard: 'Karta regionu', clickCard: 'Klik → karta regionu a živý radar', repo: 'Data (GitHub)',")
T = T.replace("open: 'Open radar', repo: 'Data (GitHub)',", "open: 'Live radar', openCard: 'Country card', clickCard: 'Click → country card & live radar', repo: 'Data (GitHub)',")
T = T.replace("open: 'Radar öffnen', repo: 'Daten (GitHub)',", "open: 'Live-Radar', openCard: 'Regionskarte', clickCard: 'Klick → Regionskarte & Live-Radar', repo: 'Daten (GitHub)',")
T = T.replace("internal: 'interní přístup'", "internal: 'interní náhled – zatím bez veřejné stránky'").replace("internal: 'internal access'", "internal: 'internal preview – no public page yet'").replace("internal: 'interner Zugang'", "internal: 'interne Vorschau – noch keine öffentliche Seite'")
T = T.replace("hint: 'Najeďte na zemi · klik otevře plný radar'", "hint: 'Najeďte na zemi · klik otevře kartu regionu a živý radar'").replace("hint: 'Hover a country · click opens the full radar'", "hint: 'Hover a country · click opens the country card and live radar'").replace("hint: 'Land überfahren · Klick öffnet den vollständigen Radar'", "hint: 'Land überfahren · Klick öffnet Regionskarte und Live-Radar'")
T = T.replace("klik otevře plný radar regionu.'", "klik otevře kartu regionu a jeho živý radar.'").replace("click opens the full radar of the region.'", "click opens the region's card and live radar.'")
assert 'chipdiplo' not in T.lower() and 'ceias' not in T.lower() and 'claude.ai' not in T
# the hover tip's generic clickOpen for regions with card is handled above; also the non-collecting tip uses tr.clickOpen – patch generically
T = T.replace("""${r.url ? `<div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : tr.clickOpen)} ↗</div>` : ''}""", """${(r.card || r.url) ? `<div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : (r.card ? tr.clickCard : tr.clickOpen))} ↗</div>` : ''}""")

# remaining strings: tip for live regions, lede, eyebrow
T = T.replace("""      <div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : tr.clickOpen)} ↗</div>`;""", """      <div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : (r.card ? tr.clickCard : tr.clickOpen))} ↗</div>`;""")
T = T.replace("click opens the region\\'s full radar.'", "click opens the region\\'s card and live radar.'")
T = T.replace("Klick öffnet den vollständigen Radar der Region.'", "Klick öffnet Regionskarte und Live-Radar.'")
T = T.replace("tapAgain: 'Klepněte znovu → plný radar'", "tapAgain: 'Klepněte znovu → otevřít'").replace("tapAgain: 'Tap again → full radar'", "tapAgain: 'Tap again → open'").replace("tapAgain: 'Erneut tippen → vollständiger Radar'", "tapAgain: 'Erneut tippen → öffnen'")
T = T.replace("let VIEW = q.get('view') === 'europe' ? 'europe' : 'world';", "let VIEW = q.get('view') ? (q.get('view') === 'europe' ? 'europe' : 'world') : (window.innerWidth < 640 ? 'europe' : 'world');")
assert "window.innerWidth < 640" in T
T = T.replace('<div class="kicker">CNSC · Global Value Chain Radar</div>', '<div class="kicker">Alpha · weekly editions · public sources only</div>')
assert 'kicker">Alpha' in T
# --- ESRA + IPCEI AST lines in tooltips and region cards ---
T = T.replace("function tipHtml(t) {", """function esraLine(r, tr) {
  const e = r.esra; if (!e) return '';
  if (r.level === 'state') return e.member ? `<div class="seglist esra">${esc(tr.esraMember)}${e.role === 'initiator' ? ' · ' + esc(tr.esraInit) : ''} (${e.since})</div>` : '';
  if (!e.n) return `<div class="seglist esra">${esc(tr.esraNone)}</div>`;
  return `<div class="seglist esra">ESRA: ${e.n} ${esc(e.n === 1 ? tr.esraRegion : tr.esraRegions)} – ${esc(e.regions.join(', '))}</div>`;
}
function esraCountry(a2, tr) { const l = (IDX.esra && IDX.esra.byCountry[a2]) || []; return l.length ? `<div class="seglist esra">ESRA: ${l.length} ${esc(l.length === 1 ? tr.esraRegion : tr.esraRegions)} – ${esc(l.join(', '))}</div>` : `<div class="seglist esra">${esc(tr.esraNone)}</div>`; }
function astLine(r, tr) { return r.ipcei_ast ? `<div class="seglist">${esc(tr.ipceiAst)}: <b>${fmt(r.ipcei_ast)}</b> · ${esc(tr.ipceiAstNote)}</div>` : ''; }
function tipHtml(t) {""", 1)
# live/preview region tip: after the edition line
T = T.replace("""      <div class="seglist" style="margin-top:4px">${esc(tr.edition)} ${esc(r.edition)} · ${esc(tr.updated)} ${fd(r.updated)}</div>
      <div class="act">""", """      <div class="seglist" style="margin-top:4px">${esc(tr.edition)} ${esc(r.edition)} · ${esc(tr.updated)} ${fd(r.updated)}</div>
      ${astLine(r, tr)}${esraLine(r, tr)}
      <div class="act">""", 1)
# collecting region tip
T = T.replace("""      <div class="seglist">${esc(tr.collectLine(fmt(r.orgs), r.batches))} · ${fd(r.updated)}</div>""", """      <div class="seglist">${esc(tr.collectLine(fmt(r.orgs), r.batches))} · ${fd(r.updated)}</div>
      ${esraLine(r, tr)}""", 1)
# parent country tip (DE): ESRA regions of the country
T = T.replace("""    <div class="act">${esc(VIEW === 'world' ? tr.clickZoom : tr.clickOpen)} ↗</div>`;
}""", """    ${esraCountry(t.a2, tr)}
    <div class="act">${esc(VIEW === 'world' ? tr.clickZoom : tr.clickOpen)} ↗</div>`;
}""", 1)
# not covered country: still show ESRA regions (context)
T = T.replace("""<span class="st none">${esc(tr.notCovered)}</span><div class="seglist">${esc(tr.join)}</div>`;""", """<span class="st none">${esc(tr.notCovered)}</span>${esraCountry(t.a2, tr)}<div class="seglist">${esc(tr.join)}</div>`;""", 1)
# region cards: after .meta
T = T.replace("""${r.verified ? `<span>${fmt(r.verified)} ${esc(t.verified)}</span>` : ''}</div>""", """${r.verified ? `<span>${fmt(r.verified)} ${esc(t.verified)}</span>` : ''}</div>
      ${astLine(r, t)}${esraLine(r, t)}""", 1)
assert T.count('esraLine(r, t)') == 1 and T.count('esraLine(r, tr)') == 3 and T.count('esraCountry(t.a2, tr)') == 2, 'esra patches'
T = T.replace("</style>", ".seglist.esra{color:var(--blue);font-weight:500}\n</style>", 1)
for lang, d in {'cs': ("esraMember: 'členský region ESRA', esraInit: 'iniciátor aliance', esraRegion: 'region', esraRegions: 'regiony', esraNone: 'ESRA: žádný členský region', ipceiAst: 'IPCEI AST', ipceiAstNote: 'vyhlédnuto k podpoře (BMWE, 30. 6. 2026), schválení Komise probíhá',"),
                'en': ("esraMember: 'ESRA member region', esraInit: 'initiator of the alliance', esraRegion: 'region', esraRegions: 'regions', esraNone: 'ESRA: no member region', ipceiAst: 'IPCEI AST', ipceiAstNote: 'earmarked for funding (BMWE, 30 Jun 2026), Commission approval pending',"),
                'de': ("esraMember: 'ESRA-Mitgliedsregion', esraInit: 'Initiator der Allianz', esraRegion: 'Region', esraRegions: 'Regionen', esraNone: 'ESRA: keine Mitgliedsregion', ipceiAst: 'IPCEI AST', ipceiAstNote: 'zur Förderung vorgesehen (BMWE, 30.06.2026), Genehmigung der Kommission läuft',")}.items():
    key = {'cs': "regions: 'Sledované regiony',", 'en': "regions: 'Tracked regions',", 'de': "regions: 'Erfasste Regionen',"}[lang]
    assert T.count(key) == 1, key; T = T.replace(key, key + ' ' + d, 1)
# no click hint for regions without a public page (internal pilot)
T = T.replace("""      ${astLine(r, tr)}${esraLine(r, tr)}
      <div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : (r.card ? tr.clickCard : tr.clickOpen))} ↗</div>`;""", """      ${astLine(r, tr)}${esraLine(r, tr)}
      ${(r.card || r.url) ? `<div class="act">${esc(pinned && pinned.touch ? tr.tapAgain : (r.card ? tr.clickCard : tr.clickOpen))} ↗</div>` : `<div class="seglist">${esc(tr.internal)}</div>`}`;""", 1)
assert '`<div class="seglist">${esc(tr.internal)}</div>`' in T
(HUB / 'index.html').write_text(T, encoding='utf-8')
print('hub written', (HUB / 'index.html').stat().st_size, 'bytes;', sum(1 for r in idx['regions'] if r.get('url')), 'public radars,', sum(1 for r in idx['regions'] if r.get('card')), 'cards')
