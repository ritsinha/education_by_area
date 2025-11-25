import io
import zipfile
import requests
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

print("Loading CSV data...")
df = pd.read_csv("south_bay_education.csv")

# -------------------------
# Download and Load ZCTA Shapefile
# -------------------------
print("Downloading ZCTA shapefile (this may take a minute)...")

# Try the 2023 ZCTA shapefile
ZCTA_SHP_URL = "https://www2.census.gov/geo/tiger/TIGER2023/ZCTA520/tl_2023_us_zcta520.zip"

try:
    response = requests.get(ZCTA_SHP_URL, timeout=120)
    response.raise_for_status()
    print(f"Downloaded {len(response.content)} bytes")
    
    # Check if it's actually a zip file
    if response.content[:4] != b'PK\x03\x04':
        print("Error: Downloaded file is not a valid ZIP file")
        print("First 100 bytes:", response.content[:100])
        raise Exception("Invalid ZIP file")
    
    # Extract the shapefile
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall("zcta_shp")
    print("✓ Shapefile extracted successfully")
    
except Exception as e:
    print(f"Error downloading shapefile: {e}")
    print("\nTrying alternative method - downloading to file first...")
    
    # Alternative: Download to file first
    response = requests.get(ZCTA_SHP_URL, stream=True, timeout=120)
    response.raise_for_status()
    
    with open("zcta_temp.zip", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print("✓ Downloaded to file")
    
    with zipfile.ZipFile("zcta_temp.zip", "r") as zf:
        zf.extractall("zcta_shp")
    
    print("✓ Shapefile extracted successfully")

# -------------------------
# Load and Process Shapefile
# -------------------------
print("Loading shapefile into GeoPandas...")
zcta_gdf = gpd.read_file("zcta_shp/tl_2023_us_zcta520.shp")
print(f"Loaded {len(zcta_gdf)} ZCTAs nationwide")

# Convert ZCTA to integer for matching
zcta_gdf["zip"] = zcta_gdf["ZCTA5CE20"].astype(int)

# Filter to only South Bay ZIPs
south_bay_zips = df['zip'].astype(int).unique()
southbay_gdf = zcta_gdf[zcta_gdf["zip"].isin(south_bay_zips)].copy()
print(f"Filtered to {len(southbay_gdf)} South Bay ZCTAs")

# Merge with education data
southbay_gdf = southbay_gdf.merge(df, on="zip", how="left")

# Convert to WGS84 (lat/lon) for Plotly
southbay_gdf = southbay_gdf.to_crs(epsg=4326)

# -------------------------
# Create Interactive Plotly Map
# -------------------------
print("Creating interactive map...")

# Create hover text with all education details
southbay_gdf['hover_text'] = southbay_gdf.apply(
    lambda row: f"<b>{row['city']} - ZIP {row['zip']}</b><br>" +
                f"Population (25+): {row['total_pop_25plus']:,.0f}<br>" +
                f"<br><b>Education Levels:</b><br>" +
                f"Bachelor's: {row['pct_bachelor']:.1f}%<br>" +
                f"Master's: {row['pct_master']:.1f}%<br>" +
                f"Professional: {row['pct_professional']:.1f}%<br>" +
                f"Doctorate: {row['pct_doctorate']:.1f}%<br>" +
                f"<br><b>Total Bachelor's+: {row['pct_bachelor_or_higher']:.1f}%</b><br>" +
                f"No Bachelor's: {row['pct_no_bachelors']:.1f}%",
    axis=1
)

# Create the choropleth map using Plotly
fig = px.choropleth_mapbox(
    southbay_gdf,
    geojson=southbay_gdf.geometry.__geo_interface__,
    locations=southbay_gdf.index,
    color='pct_bachelor_or_higher',
    hover_name='city',
    hover_data={
        'zip': True,
        'pct_bachelor': ':.1f',
        'pct_master': ':.1f',
        'pct_professional': ':.1f',
        'pct_doctorate': ':.1f',
        'pct_bachelor_or_higher': ':.1f',
        'total_pop_25plus': ':,.0f'
    },
    color_continuous_scale='RdYlGn',
    range_color=[0, 100],
    mapbox_style="carto-positron",
    center={"lat": 37.35, "lon": -121.9},
    zoom=9,
    opacity=0.7,
    labels={
        'pct_bachelor_or_higher': "Bachelor's+ (%)",
        'pct_bachelor': "Bachelor's (%)",
        'pct_master': "Master's (%)",
        'pct_professional': 'Professional (%)',
        'pct_doctorate': 'Doctorate (%)',
        'total_pop_25plus': 'Population 25+',
        'zip': 'ZIP Code'
    }
)

fig.update_layout(
    title={
        'text': "South Bay Education Map: Bachelor's Degree or Higher by ZIP Code (2023)",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#333'}
    },
    height=800,
    margin={"r": 0, "t": 60, "l": 0, "b": 0}
)

# Add ZIP code labels
for idx, row in southbay_gdf.iterrows():
    # Get centroid for label placement
    centroid = row.geometry.centroid
    fig.add_trace(go.Scattermapbox(
        lon=[centroid.x],
        lat=[centroid.y],
        mode='text',
        text=[str(row['zip'])],
        textfont=dict(size=8, color='black'),
        showlegend=False,
        hoverinfo='skip'
    ))

fig.write_html("output/south_bay_education_map.html")
print("✓ Created: output/south_bay_education_map.html")

# -------------------------
# Create Interactive Map with Dropdown Menu
# -------------------------
print("Creating interactive map with dropdown menu...")

# Get centroids for each ZIP
centroids = southbay_gdf.geometry.centroid
southbay_gdf['lat'] = centroids.y
southbay_gdf['lon'] = centroids.x

# Calculate new combined metric: Masters, Professional or PhD
southbay_gdf['pct_graduate_degree'] = (
    southbay_gdf['pct_master'] + 
    southbay_gdf['pct_professional'] + 
    southbay_gdf['pct_doctorate']
)

# Create figure with multiple traces (one for each education metric)
fig2 = go.Figure()

# Define education metrics to visualize
education_metrics = [
    {
        'column': 'pct_no_bachelors',
        'label': "No Bachelor's Degree",
        'colorbar_title': "No Bachelor's<br>(%)"
    },
    {
        'column': 'pct_bachelor_or_higher',
        'label': "Bachelor's or Higher",
        'colorbar_title': "Bachelor's+<br>(%)"
    },
    {
        'column': 'pct_master',
        'label': "Master's Degree",
        'colorbar_title': "Master's<br>(%)"
    },
    {
        'column': 'pct_professional',
        'label': "Professional Degree",
        'colorbar_title': "Professional<br>(%)"
    },
    {
        'column': 'pct_graduate_degree',
        'label': "Master's, Professional or PhD",
        'colorbar_title': "Graduate<br>Degree (%)"
    },
    {
        'column': 'pct_doctorate',
        'label': "PhD Degree",
        'colorbar_title': "PhD<br>(%)"
    }
]

# Create a trace for each education metric
for i, metric in enumerate(education_metrics):
    fig2.add_trace(go.Choroplethmapbox(
        geojson=southbay_gdf.geometry.__geo_interface__,
        locations=southbay_gdf.index,
        z=southbay_gdf[metric['column']],
        colorscale='RdYlGn' if metric['column'] != 'pct_no_bachelors' else 'RdYlGn_r',
        zmin=0,
        zmax=100,
        marker_opacity=0.7,
        marker_line_width=1.5,
        marker_line_color='white',
        colorbar=dict(
            title=metric['colorbar_title'],
            x=1.02,
            thickness=15,
            len=0.7
        ),
        visible=(i == 0),  # Only first trace visible by default
        name=metric['label'],
        hovertemplate='<b>%{customdata[0]} - ZIP %{customdata[1]}</b><br>' +
                      'Population (25+): %{customdata[2]:,.0f}<br>' +
                      '<br><b>Education Breakdown:</b><br>' +
                      'Bachelor\'s: %{customdata[3]:.1f}%<br>' +
                      'Master\'s: %{customdata[4]:.1f}%<br>' +
                      'Professional: %{customdata[5]:.1f}%<br>' +
                      'Doctorate: %{customdata[6]:.1f}%<br>' +
                      '<br><b>Total Bachelor\'s+: %{customdata[7]:.1f}%</b><br>' +
                      'No Bachelor\'s: %{customdata[8]:.1f}%<br>' +
                      '<br><b>Current View: ' + metric['label'] + '</b><br>' +
                      'Value: %{z:.1f}%<br>' +
                      '<extra></extra>',
        customdata=southbay_gdf[[
            'city', 'zip', 'total_pop_25plus',
            'pct_bachelor', 'pct_master', 'pct_professional', 'pct_doctorate',
            'pct_bachelor_or_higher', 'pct_no_bachelors'
        ]].values
    ))

# Create dropdown menu buttons
buttons = []
for i, metric in enumerate(education_metrics):
    visible = [False] * len(education_metrics)
    visible[i] = True
    buttons.append(
        dict(
            label=metric['label'],
            method="update",
            args=[
                {"visible": visible},
                {
                    "title": f"South Bay Education Map: {metric['label']} by ZIP Code (2023)"
                }
            ]
        )
    )

# Update layout with dropdown menu
fig2.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.01,
            xanchor="left",
            y=0.99,
            yanchor="top",
            bgcolor="white",
            bordercolor="#333",
            borderwidth=2,
            font=dict(size=12)
        )
    ],
    mapbox_style="carto-positron",
    mapbox_center={"lat": 37.35, "lon": -121.9},
    mapbox_zoom=9,
    title={
        'text': f"South Bay Education Map: {education_metrics[0]['label']} by ZIP Code (2023)",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18, 'color': '#333'}
    },
    height=900,
    margin={"r": 0, "t": 80, "l": 0, "b": 0},
    annotations=[
        dict(
            text="<b>Select Education Metric:</b>",
            showarrow=False,
            x=0.01,
            y=1.05,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="bottom",
            font=dict(size=14, color="#333")
        )
    ]
)

fig2.write_html("output/south_bay_education_map_interactive.html")
print("✓ Created: output/south_bay_education_map_interactive.html")

print("\n" + "="*70)
print("Geographic visualizations created successfully!")
print("="*70)
print("\nOpen these HTML files in your browser:")
print("  1. output/south_bay_education_map_interactive.html ⭐ RECOMMENDED")
print("     - Interactive map with dropdown menu to switch metrics")
print("  2. output/south_bay_education_map.html")
print("     - Simple choropleth with ZIP labels")
print("\n📍 MAIN FEATURES (Interactive Map):")
print("  • Dropdown menu to select education metric:")
print("    - No Bachelor's Degree")
print("    - Bachelor's or Higher")
print("    - Master's Degree")
print("    - Professional Degree")
print("    - Master's, Professional or PhD")
print("    - PhD Degree")
print("  • Hover over any ZIP code to see ALL education statistics")
print("  • Color-coded by selected metric (Green=high, Red=low)")
print("  • Zoom and pan to explore the South Bay area")

