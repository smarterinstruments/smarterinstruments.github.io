// ESRA member regions (esra-org.eu, 17 Nov 2026) as projected SVG paths in the Europe view (same projection as gen_eu.mjs)
import fs from 'fs';
import { geoConicConformal, geoPath, geoCentroid } from 'd3-geo';
const W = 1000, H = 760;   // frame −10..39° E / 34.8..71.5° N (North Cape), fitted by height; side margins show the clipped world
const ring = [];
for (let lon = -10; lon <= 39; lon += 1) ring.push([lon, 34.8]);
for (let lat = 34.8; lat <= 71.5; lat += 1) ring.push([39, lat]);
for (let lon = 39; lon >= -10; lon -= 1) ring.push([lon, 71.5]);
for (let lat = 71.5; lat >= 34.8; lat -= 1) ring.push([-10, lat]);
ring.push([-10, 34.8]);
const frame = { type: 'Polygon', coordinates: [ring.reverse()] };
const proj = geoConicConformal().parallels([40, 65]).rotate([-14, 0]).fitSize([W, H], frame).clipExtent([[0, 0], [W, H]]);
const path = geoPath(proj);
// NUTS 2021 ids (level in brackets); Wales from NUTS 2016 (UK left NUTS 2021)
const MEMBERS = [
 ['DE1','Baden-Württemberg','DE'],['DE2','Bavaria','DE'],['DE6','Hamburg','DE'],['DE7','Hesse','DE'],['DE9','Lower Saxony','DE'],['DEA','North Rhine-Westphalia','DE'],['DEC','Saarland','DE'],['DED','Saxony','DE'],['DEE','Saxony-Anhalt','DE'],['DEF','Schleswig-Holstein','DE'],['DEG','Thuringia','DE'],
 ['ES61','Andalusia','ES'],['ES21','Basque Country','ES'],['ES51','Catalonia','ES'],['ES30','Madrid','ES'],['ES52','Valencia','ES'],
 ['FRK','Auvergne-Rhône-Alpes','FR'],['FR1','Île-de-France','FR'],['FRJ','Occitanie','FR'],['FRL',"Région SUD – Provence-Alpes-Côte d'Azur",'FR'],
 ['NL23','Flevoland','NL'],['NL22','Gelderland','NL'],['NL41','North Brabant','NL'],['NL21','Overijssel','NL'],
 ['ITC4','Lombardy','IT'],['ITC1','Piemonte','IT'],['ITG1','Sicily','IT'],
 ['CZ064','South Moravia','CZ'],['CZ032','Pilsen','CZ'],['CZ072','Zlín','CZ'],
 ['FI1B','Helsinki (Helsinki-Uusimaa)','FI'],['FI197','Tampere (Pirkanmaa)','FI'],['FI1D9','Oulu (Pohjois-Pohjanmaa)','FI'],
 ['AT21','Carinthia','AT'],['AT22','Styria','AT'],['PT16','Centro','PT'],['PT11','Norte','PT'],['SE123','Östergötland','SE'],['SE224','Skåne','SE'],
 ['BE2','Flanders','BE'],['SK01','Bratislava','SK'],['PL63','Pomerania','PL'],['IE','Ireland','IE'],['UKL','Wales','GB'],
];
const feats = {};
for (const [lvl, file] of [[0,'nuts/nutsrg_0.json'],[1,'nuts/nutsrg_1.json'],[2,'nuts/nutsrg_2.json'],[3,'nuts/nutsrg_3.json'],[1,'nuts/uk16_1.json']]) {
  for (const f of JSON.parse(fs.readFileSync(file)).features) if (!feats[f.properties.id]) feats[f.properties.id] = f;
}
const out = [], missing = [];
for (const [id, name, a2] of MEMBERS) {
  const f = feats[id]; if (!f) { missing.push(id); continue; }
  const d = path(f) || ''; const c = proj(geoCentroid(f));
  if (!d) { missing.push(id + ' (outside frame)'); continue; }
  out.push({ id, name, a2, d: d.replace(/(\d+\.\d{1})\d+/g, '$1'), c: c ? c.map(v => +v.toFixed(1)) : null, nuts: f.properties.na });
}
fs.writeFileSync('data/esra.json', JSON.stringify({ W, H, url: 'https://www.esra-org.eu/', read: '2026-11-17', total: MEMBERS.length, regions: out }));
console.log('esra regions', out.length, 'missing', missing, 'size', fs.statSync('esra.json').size);
console.log(out.map(r => r.id + '=' + r.nuts).join(' | '));
