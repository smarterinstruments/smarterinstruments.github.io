// Project the Pillar-I / Silicon Europe points (tools/data/pillar_src.json) into the Europe view (same projection as gen_eu.mjs)
import fs from 'fs';
import { geoConicConformal } from 'd3-geo';
const W = 1000, H = 760;   // frame −10..39° E / 34.8..71.5° N (North Cape), fitted by height; side margins show the clipped world
const ring = [];
for (let lon = -10; lon <= 39; lon += 1) ring.push([lon, 34.8]);
for (let lat = 34.8; lat <= 71.5; lat += 1) ring.push([39, lat]);
for (let lon = 39; lon >= -10; lon -= 1) ring.push([lon, 71.5]);
for (let lat = 71.5; lat >= 34.8; lat -= 1) ring.push([-10, lat]);
ring.push([-10, 34.8]);
const frame = { type: 'Polygon', coordinates: [ring.reverse()] };
const proj = geoConicConformal().parallels([40, 65]).rotate([-14, 0]).fitSize([W, H], frame);
const src = JSON.parse(fs.readFileSync('data/pillar_src.json'));
const sites = JSON.parse(fs.readFileSync('data/pl_sites_src.json'));
const out = src.points.map(p => {
  const [x, y] = proj([p.lon, p.lat]); const o = Object.assign({}, p, { x: +x.toFixed(1), y: +y.toFixed(1) });
  const L = p.l === 'pl' && sites.lines[p.id];
  if (L) {   // participant sites (CORDIS legal seats); off = outside the Europe frame (listed, not drawn)
    o.cordis = L.cordis; o.acronym = L.acronym;
    o.sites = L.parts.map(q => { const [sx, sy] = proj([q.lon, q.lat]); const off = sx < 0 || sx > W || sy < 0 || sy > H;   // outside the drawn Europe box
      return { n: q.n, city: q.city, a2: q.a2, role: q.role, x: +sx.toFixed(1), y: +sy.toFixed(1), off }; });
  }
  return o;
});
fs.writeFileSync('data/points.json', JSON.stringify({ read: src.read, layers: src.layers, sitesSrc: sites.src, sitesNote: sites.note, sitesRead: sites.read, points: out }));
console.log('sites', out.filter(p => p.sites).map(p => p.id + ':' + p.sites.length + (p.sites.some(s => s.off) ? '(' + p.sites.filter(s => s.off).length + ' off)' : '')).join(' '));
const c = {}; out.forEach(p => c[p.l] = (c[p.l] || 0) + 1);
console.log('points', out.length, c, out.filter(p => p.x < 0 || p.x > W || p.y < 0 || p.y > H).map(p => p.id));
