import io
import zipfile
import requests
import pandas as pd
import geopandas as gpd
import folium

# -------------------------
# 1) CONFIG
# -------------------------
API_KEY = None   # optional
YEAR = 2023
BASE_URL = f"https://api.census.gov/data/{YEAR}/acs/acs5"

VARS = [
    "NAME",
    "B15003_001E",  # total pop 25+
    "B15003_022E",  # bachelor's
    "B15003_023E",  # master's
    "B15003_024E",  # professional school degree (JD/MD/etc.)
    "B15003_025E",  # doctorate degree (PhD/EdD/etc.)
]

south_bay_zips = {
    "San Jose": [
        95110,95111,95112,95113,95116,95117,95118,95119,95120,
        95121,95122,95123,95124,95125,95126,95127,95128,95129,
        95130,95131,95132,95133,95134,95135,95136,95138,95139,
        95140,95141,95148
    ],
    "Cupertino": [95014, 95015],
    "Los Gatos": [95030, 95032, 95033],
    "Saratoga": [95070, 95071],
    "Mountain View": [94040, 94041, 94043],
    "Palo Alto": [94301, 94303, 94304, 94305, 94306],
    "Los Altos": [94022, 94023, 94024],
    "Sunnyvale": [94085, 94086, 94087, 94088, 94089],
    "Santa Clara": [95050, 95051, 95053, 95054],
    "Campbell": [95008, 95009, 95011],
    "Milpitas": [95035, 95036],
}

# ZCTA shapefile (2023 TIGER/Line nationwide ZCTAs)
ZCTA_SHP_URL = "https://www2.census.gov/geo/tiger/TIGER2023/ZCTA5/tl_2023_us_zcta520.zip"

# -------------------------
# 2) FETCH ACS DATA BY ZIP
# -------------------------
zip_to_city = {z: city for city, zs in south_bay_zips.items() for z in zs}
zip_list = sorted(zip_to_city.keys())

def fetch_zcta(z):
    params = {"get": ",".join(VARS), "for": f"zip code tabulation area:{z}"}
    if API_KEY:
        params["key"] = API_KEY
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    header, row = r.json()
    return dict(zip(header, row))

records = []
for z in zip_list:
    try:
        rec = fetch_zcta(z)
        rec["city"] = zip_to_city[z]
        records.append(rec)
    except Exception as e:
        print(f"Failed for {z}: {e}")

df = pd.DataFrame(records)

num_cols = ["B15003_001E","B15003_022E","B15003_023E","B15003_024E","B15003_025E"]
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

df["pct_bachelor"]     = df["B15003_022E"] / df["B15003_001E"] * 100
df["pct_master"]       = df["B15003_023E"] / df["B15003_001E"] * 100
df["pct_professional"] = df["B15003_024E"] / df["B15003_001E"] * 100
df["pct_doctorate"]    = df["B15003_025E"] / df["B15003_001E"] * 100

# (1) Combined Bachelor's or higher
df["pct_bachelor_or_higher"] = (
    (df["B15003_022E"] + df["B15003_023E"] + df["B15003_024E"] + df["B15003_025E"])
    / df["B15003_001E"] * 100
)

# (2) "No bachelor's" (a clean, commonly used "no college degree" proxy)
df["pct_no_bachelors"] = 100 - df["pct_bachelor_or_higher"]

out = df[[
    "city",
    "zip code tabulation area",
    "NAME",
    "B15003_001E",
    "pct_bachelor",
    "pct_master",
    "pct_professional",
    "pct_doctorate",
    "pct_bachelor_or_higher",
    "pct_no_bachelors"
]].rename(columns={
    "zip code tabulation area": "zip",
    "B15003_001E": "total_pop_25plus"
}).sort_values(["city","zip"])

out.to_csv("south_bay_education.csv", index=False)
print("Wrote CSV: south_bay_education.csv")

# -------------------------
# 3) LOAD ZCTA SHAPEFILE + MERGE
# -------------------------
# Download ZIPped shapefile to memory and read with GeoPandas
shp_bytes = requests.get(ZCTA_SHP_URL, timeout=60).content
with zipfile.ZipFile(io.BytesIO(shp_bytes)) as zf:
    # geopandas can read from a virtual zip path by extracting to a temp folder;
    # easiest is extract into memory-backed temp dir via /vsizip/
    # We'll write to a temp folder on disk:
    zf.extractall("zcta_shp")

zcta_gdf = gpd.read_file("zcta_shp/tl_2023_us_zcta520.shp")

# ZCTA field is ZCTA5CE20 (5-digit string)
zcta_gdf["zip"] = zcta_gdf["ZCTA5CE20"].astype(int)

southbay_gdf = zcta_gdf[zcta_gdf["zip"].isin(zip_list)].merge(out, on="zip", how="left")

# Reproject to WGS84 for Folium
southbay_gdf = southbay_gdf.to_crs(epsg=4326)

# -------------------------
# 4) INTERACTIVE HOVER MAP (FOLIUM)
# -------------------------
# Center map roughly on South Bay
m = folium.Map(location=[37.35, -121.9], zoom_start=10, tiles="cartodbpositron")

# Choropleth on Bachelor's-or-higher
folium.Choropleth(
    geo_data=southbay_gdf,
    data=southbay_gdf,
    columns=["zip", "pct_bachelor_or_higher"],
    key_on="feature.properties.zip",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Bachelor's or higher (%)"
).add_to(m)

# Tooltip fields
tooltip = folium.features.GeoJsonTooltip(
    fields=[
        "city", "zip",
        "pct_bachelor", "pct_master",
        "pct_professional", "pct_doctorate",
        "pct_bachelor_or_higher", "pct_no_bachelors"
    ],
    aliases=[
        "City", "ZIP",
        "% Bachelor's",
        "% Master's",
        "% Professional degree",
        "% Doctorate",
        "% Bachelor's or higher",
        "% No Bachelor's"
    ],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: white;
        border: 1px solid gray;
        border-radius: 3px;
        box-shadow: 2px 2px 2px rgba(0,0,0,0.2);
        padding: 4px;
    """
)

folium.GeoJson(
    southbay_gdf,
    name="South Bay ZCTAs",
    tooltip=tooltip
).add_to(m)

folium.LayerControl().add_to(m)

m.save("output/south_bay_education_map_folium.html")
print("Wrote interactive map: output/south_bay_education_map_folium.html")
