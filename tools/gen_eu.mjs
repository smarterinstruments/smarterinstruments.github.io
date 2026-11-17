import fs from 'fs';
import * as topojson from 'topojson-client';
import { geoConicConformal, geoPath, geoCentroid, geoBounds } from 'd3-geo';
import countries from 'i18n-iso-countries';
const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const geo = topojson.feature(topo, topo.objects.countries);
const W = 1000, H = 640;
// frame polygon for Europe
const ring = [];
for (let lon = -10; lon <= 39; lon += 1) ring.push([lon, 34.8]);     // bottom edge along the parallel (dense, so fitSize sees the parallel's sag)
for (let lat = 34.8; lat <= 65; lat += 1) ring.push([39, lat]);
for (let lon = 39; lon >= -10; lon -= 1) ring.push([lon, 65]);
for (let lat = 65; lat >= 34.8; lat -= 1) ring.push([-10, lat]);
ring.push([-10, 34.8]);
const frame = { type: 'Polygon', coordinates: [ring.reverse()] };
const proj = geoConicConformal().parallels([40, 65]).rotate([-14, 0]).fitSize([W, H], frame).clipExtent([[0, 0], [W, H]]);
const path = geoPath(proj);
const out = [];
for (const f of geo.features) {
  const [[x0, y0], [x1, y1]] = geoBounds(f);
  // crude pre-filter: bbox intersects Europe/near region
  if (x1 < -30 || x0 > 60 || y1 < 25 || y0 > 82) continue;
  if (f.properties.name === 'Antarctica') continue;
  let d = path(f) || '';
  const num = String(f.id).padStart(3, '0');
  const a2 = countries.numericToAlpha2(num) || '';
  // centroid: for countries with far-flung parts (France, Norway, Russia), use largest polygon in frame
  let best = null, bestA = -1;
  const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  for (const p of polys) {
    const g = { type: 'Polygon', coordinates: p };
    const c = proj(geoCentroid(g)); if (!c) continue;
    if (c[0] < 0 || c[0] > W || c[1] < 0 || c[1] > H) continue;
    const a = Math.abs(geoPath(proj).area(g));
    if (a > bestA) { bestA = a; best = c; }
  }
  if (!best) { const cc = proj(geoCentroid(f)); if (cc && cc[0] >= 0 && cc[0] <= W && cc[1] >= 0 && cc[1] <= H) best = cc; }
  if (!d && !best) continue;
  const area = Math.abs(geoPath(proj).area(f));
  out.push({ id: num, a2, d: d.replace(/(\d+\.\d{1})\d+/g, '$1'), c: best ? best.map(v => +v.toFixed(1)) : null, pt: (!d || area < 12) && best ? best.map(v => +v.toFixed(1)) : undefined });
}
const states = JSON.parse(fs.readFileSync('de_states.geojson'));
const st = states.features.map(f => ({ id: f.properties.id, d: path(f).replace(/(\d+\.\d{1})\d+/g, '$1'), c: proj(geoCentroid(f)).map(v => +v.toFixed(1)) }));
fs.writeFileSync('europe.json', JSON.stringify({ W, H, countries: out, states: st }));
console.log('eu countries', out.length, 'size', fs.statSync('europe.json').size);
console.log(out.filter(c => ['CZ', 'DE', 'FR', 'NL', 'BE', 'AT', 'PL', 'IT', 'ES', 'IE', 'FI', 'SE', 'GB', 'CH', 'NO', 'PT', 'HU', 'SK', 'RO', 'GR', 'TR', 'IL'].includes(c.a2)).map(c => c.a2 + ':' + c.c).join(' '));
console.log(st.map(s => s.id + ':' + s.c).join(' '));
