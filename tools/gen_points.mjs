// Project the Pillar-I / Silicon Europe points (tools/data/pillar_src.json) into the Europe view (same projection as gen_eu.mjs)
import fs from 'fs';
import { geoConicConformal } from 'd3-geo';
const W = 1000, H = 640;
const ring = [];
for (let lon = -10; lon <= 39; lon += 1) ring.push([lon, 34.8]);
for (let lat = 34.8; lat <= 65; lat += 1) ring.push([39, lat]);
for (let lon = 39; lon >= -10; lon -= 1) ring.push([lon, 65]);
for (let lat = 65; lat >= 34.8; lat -= 1) ring.push([-10, lat]);
ring.push([-10, 34.8]);
const frame = { type: 'Polygon', coordinates: [ring.reverse()] };
const proj = geoConicConformal().parallels([40, 65]).rotate([-14, 0]).fitSize([W, H], frame);
const src = JSON.parse(fs.readFileSync('data/pillar_src.json'));
const out = src.points.map(p => { const [x, y] = proj([p.lon, p.lat]); return Object.assign({}, p, { x: +x.toFixed(1), y: +y.toFixed(1) }); });
fs.writeFileSync('data/points.json', JSON.stringify({ read: src.read, layers: src.layers, points: out }));
const c = {}; out.forEach(p => c[p.l] = (c[p.l] || 0) + 1);
console.log('points', out.length, c, out.filter(p => p.x < 0 || p.x > W || p.y < 0 || p.y > H).map(p => p.id));
