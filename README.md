# South Bay Education Analysis

Interactive visualizations of educational attainment across South Bay Area ZIP codes, using 2023 American Community Survey (ACS) data from the U.S. Census Bureau.

**Cities covered**: San Jose, Cupertino, Palo Alto, Mountain View, Los Altos, Sunnyvale, Santa Clara, Campbell, Milpitas, Los Gatos, Saratoga (54 ZIP codes)

---

## Inspiration

This project was inspired by the San Francisco Chronicle article ["Where are the Bay Area's most educated residents?"](https://www.sfchronicle.com/sf/article/most-educated-residents-data-21199765.php) by Hanna Zakharenko and Danielle Echeverria. Their data journalism raised the question of what the same picture looks like at ZIP code resolution across the South Bay.

---

## Key Findings

From the 2023 ACS data:

- **Highest**: Palo Alto 94305 (Stanford area) — 90.9% with a bachelor's degree or higher
- **Lowest**: San Jose 95122 — 17.9% with a bachelor's degree or higher
- **South Bay average**: ~60% with a bachelor's degree or higher (vs. ~35% nationally)
- **Highest PhD concentration**: Palo Alto 94304 — 31% of adults hold a doctorate

---

## Project Structure

```
education_by_area/
├── code.py                    # Fetch data from Census API; generates south_bay_education.csv
├── geo_map.py                 # Generate interactive choropleth maps (Folium + Plotly)
├── visualize.py               # Generate statistical charts (bar, stacked bar, scatter)
├── south_bay_education.csv    # Education data by ZIP code (committed for reference)
├── requirements.txt           # Python dependencies
├── SETUP.md                   # Quick setup guide
├── LICENSE
└── output/
    └── south_bay_education_map_interactive.html   # Main interactive map (committed)
    # Other HTML outputs are generated locally (see .gitignore)
```

---

## Quick Start

```bash
pip install -r requirements.txt
```

Run in order:

```bash
# 1. Fetch Census data
python3 code.py

# 2. Generate the interactive geographic map (recommended)
python3 geo_map.py

# 3. Generate statistical charts
python3 visualize.py
```

All outputs are saved to the `output/` folder as standalone HTML files.

---

## Data Sources

- **Education data**: [ACS 2023, Table B15003](https://www.census.gov/programs-surveys/acs) — Educational Attainment for the Population 25 Years and Over
- **Geographic boundaries**: [TIGER/Line Shapefiles (ZCTAs)](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)

All data is publicly available from the U.S. Census Bureau.

---

## Tech Stack

- Python 3.9+
- pandas, geopandas
- plotly, folium
- Census API (key optional)

---

## Notes

- The ZCTA shapefile (~500MB) is downloaded automatically on first run of `geo_map.py`
- A Census API key is optional but recommended for higher rate limits (set in `code.py`)
- Generated HTML files are standalone and require no server to open

---

## License

MIT. See [LICENSE](LICENSE).

---

*Ritwik Sinha — [ritwik.sinha@gmail.com](mailto:ritwik.sinha@gmail.com)*
