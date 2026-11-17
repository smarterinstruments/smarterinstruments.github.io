# Global and EU Semiconductor Value Chain Radar – hub (alpha)

Entry point of the radar family: an interactive world / Europe map with a number on every tracked country or region, a hover card with the key figures, and a click that opens the region's **country card** and from there its **live radar**.

```
/            map (World / Europe, CS · EN · DE, metric switch, region list)
/sn/         Saxony – country card (web), card PNG + PDF for LinkedIn, links to the live radar, data and GitHub
/global_index.json   one record per region: status, edition, counts, top segments, public URLs
```

Live radars stay in their own repositories (one per region, so a partner cluster can get access to its own): `Saxony-Radar`, `Bavaria-Radar`, … Each radar build writes a small `meta.json` (aggregate counts only); `tools/build_hub.py` collects them into `global_index.json` and rebuilds the map. Regions without a public page (internal pilot, data collection) show numbers only – no links.

Public sources only; no personal data. Status **alpha**: organisation lists and value-chain segment assignments are provisional until the partner cluster of each region has validated them. Corrections: info@semicz.cz.

© 2026 Czech National Semiconductor Cluster, z.s. · background IP of CNSC / Smarter Instruments s.r.o.
