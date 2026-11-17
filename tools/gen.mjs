import fs from 'fs';
import * as topojson from 'topojson-client';
import { geoNaturalEarth1, geoPath, geoCentroid, geoBounds } from 'd3-geo';
import countries from 'i18n-iso-countries';
import cs from 'i18n-iso-countries/langs/cs.json' with { type: 'json' };
import de from 'i18n-iso-countries/langs/de.json' with { type: 'json' };
import en from 'i18n-iso-countries/langs/en.json' with { type: 'json' };
countries.registerLocale(cs); countries.registerLocale(de); countries.registerLocale(en);
const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-110m.json'));
const geo = topojson.feature(topo, topo.objects.countries);
const W = 1000, H = 520;
const proj = geoNaturalEarth1().fitSize([W, H], { type: 'Sphere' });
const path = geoPath(proj);
const out = [];
for (const f of geo.features) {
  const num = String(f.id).padStart(3, '0');
  const a2 = countries.numericToAlpha2(num) || '';
  const d = path(f); if (!d) continue;
  const c = proj(geoCentroid(f));
  out.push({ id: num, a2, n: { en: countries.getName(num, 'en') || f.properties.name, de: countries.getName(num, 'de') || f.properties.name, cs: countries.getName(num, 'cs') || f.properties.name }, d: d.replace(/(\d+\.\d{1})\d+/g, '$1'), c: c ? c.map(v => +v.toFixed(1)) : null });
}
// micro-states missing from 110m (Malta, Singapore, Liechtenstein, ...): take centroid points from 50m
const topo50 = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const geo50 = topojson.feature(topo50, topo50.objects.countries);
const have = new Set(out.map(o => o.id));
for (const f of geo50.features) {
  const num = String(f.id).padStart(3, '0'); if (have.has(num)) continue;
  const a2 = countries.numericToAlpha2(num) || ''; if (!a2) continue;
  const c = proj(geoCentroid(f)); if (!c) continue;
  out.push({ id: num, a2, n: { en: countries.getName(num, 'en') || f.properties.name, de: countries.getName(num, 'de') || f.properties.name, cs: countries.getName(num, 'cs') || f.properties.name }, d: '', pt: c.map(v => +v.toFixed(1)), c: c.map(v => +v.toFixed(1)) });
}
const states = JSON.parse(fs.readFileSync('de_states.geojson'));
const st = [];
for (const f of states.features) {
  const d = path(f); const c = proj(geoCentroid(f));
  st.push({ id: f.properties.id, n: f.properties.name, d: d.replace(/(\d+\.\d{2})\d+/g, '$1'), c: c.map(v => +v.toFixed(1)) });
}
// Europe view box in projected coords
const eu = [proj([-12, 72]), proj([42, 34])];
const sphere = path({ type: 'Sphere' });
fs.writeFileSync('world.json', JSON.stringify({ W, H, sphere, eu: [eu[0][0], eu[0][1], eu[1][0] - eu[0][0], eu[1][1] - eu[0][1]].map(v => +v.toFixed(1)), countries: out, states: st }));
console.log('countries', out.length, 'states', st.length, 'eu', eu, 'size', fs.statSync('world.json').size);
