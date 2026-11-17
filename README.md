# Global and EU Semiconductor Value Chain Radar – hub (alpha)

Entry point of the radar family: an interactive world / Europe map with a number on every tracked country or region, a hover card with the key figures, and a click that opens the region's **country card** and from there its **live radar**.

```
/            map (World / Europe, CS · EN · DE, metric switch, region list)
/sn/         Saxony – country card (web), card PNG + PDF for LinkedIn, links to the live radar, data and GitHub
/global_index.json   one record per region: status, edition, counts, top segments, public URLs
```

Map layers: countries from Natural Earth (world-atlas), German states from deutschlandGeoJSON (© GeoBasis-DE/BKG), ESRA member regions from Eurostat Nuts2json (NUTS 2021; Wales NUTS 2016; © EuroGeographics) – `tools/gen_eu.mjs`, `tools/gen.mjs`, `tools/gen_esra.mjs` regenerate `tools/data/*.json` (needs `npm i d3-geo topojson-client world-atlas i18n-iso-countries` and the Nuts2json files `pub/v2/2021/4326/10M/nutsrg_{0..3}.json`, `pub/v2/2016/4326/10M/nutsrg_1.json` in `tools/nuts/`). The map zooms with the mouse wheel, drag, pinch or the +/−/⟲ buttons; numbers are shown on hover, ESRA regions as a hatched layer (toggle). Point layers (Europe view, `tools/data/pillar_src.json` → `tools/gen_points.mjs` → `tools/data/points.json`): 30 Chips competence centres (list acccess.eu/network, host organisations from the centres' websites), 11 Chips Act pilot lines at their coordinator's site, 9 EuroCDP design enablement teams, 4 first-of-a-kind fabs with IPF/OEF status (Commission, 16 Oct 2025) and the 14 + 2 Silicon Europe Alliance clusters (silicon-europe.eu). Each marker has a hover card and links to the organisation's website; markers of one layer at the same place are spread outwards. First-of-a-kind fabs are drawn as a bold "1" badge. Clicking a pilot-line marker expands all its participant sites (hollow triangles + connectors to the coordinator; `tools/make_pl_sites.py` → `tools/data/pl_sites_src.json`, participants and legal seats from the CORDIS fact sheets, 225 entries for 11 lines; a panel on the map lists the open lines with website and CORDIS links). `tools/gen_points.mjs` needs `d3-geo` (symlink `tools/node_modules` or `npm i d3-geo`).

Live radars stay in their own repositories (one per region, so a partner cluster can get access to its own): `Saxony-Radar`, `Bavaria-Radar`, … Each radar build writes a small `meta.json` (aggregate counts only); `tools/build_hub.py` collects them into `global_index.json` and rebuilds the map. Regions without a public page (internal pilot, data collection) show numbers only – no links.

Public sources only; no personal data. Status **alpha**: organisation lists and value-chain segment assignments are provisional until the partner cluster of each region has validated them. Corrections: info@semicz.cz.

© 2026 Czech National Semiconductor Cluster, z.s. · background IP of CNSC / Smarter Instruments s.r.o.
