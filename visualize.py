import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Read the CSV data
df = pd.read_csv("south_bay_education.csv")

# -------------------------
# 1) INTERACTIVE BAR CHART - Bachelor's or Higher by ZIP
# -------------------------
df_sorted = df.sort_values('pct_bachelor_or_higher', ascending=True)

fig1 = go.Figure()

# Create color scale based on percentage
colors = df_sorted['pct_bachelor_or_higher']

fig1.add_trace(go.Bar(
    y=[f"{row['city']} ({row['zip']})" for _, row in df_sorted.iterrows()],
    x=df_sorted['pct_bachelor_or_higher'],
    orientation='h',
    marker=dict(
        color=colors,
        colorscale='RdYlGn',
        showscale=True,
        colorbar=dict(title="% Bachelor's+")
    ),
    text=[f"{val:.1f}%" for val in df_sorted['pct_bachelor_or_higher']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>' +
                  'Bachelor\'s or Higher: %{x:.2f}%<br>' +
                  '<extra></extra>'
))

fig1.update_layout(
    title="South Bay Education: Bachelor's Degree or Higher by ZIP Code (2023)",
    xaxis_title="Percentage with Bachelor's Degree or Higher",
    yaxis_title="City (ZIP Code)",
    height=1200,
    showlegend=False,
    font=dict(size=10),
    plot_bgcolor='rgba(240,240,240,0.5)',
    xaxis=dict(gridcolor='white', range=[0, 105])
)

fig1.write_html("output/education_by_zip.html")
print("✓ Created: output/education_by_zip.html")

# -------------------------
# 2) STACKED BAR CHART - Degree Breakdown
# -------------------------
fig2 = go.Figure()

df_sorted2 = df.sort_values('pct_bachelor_or_higher', ascending=True)
zip_labels = [f"{row['city']} ({row['zip']})" for _, row in df_sorted2.iterrows()]

# Stack the degrees in order
fig2.add_trace(go.Bar(
    name="Bachelor's",
    y=zip_labels,
    x=df_sorted2['pct_bachelor'],
    orientation='h',
    marker=dict(color='#3498db')
))

fig2.add_trace(go.Bar(
    name="Master's",
    y=zip_labels,
    x=df_sorted2['pct_master'],
    orientation='h',
    marker=dict(color='#2ecc71')
))

fig2.add_trace(go.Bar(
    name="Professional",
    y=zip_labels,
    x=df_sorted2['pct_professional'],
    orientation='h',
    marker=dict(color='#f39c12')
))

fig2.add_trace(go.Bar(
    name="Doctorate",
    y=zip_labels,
    x=df_sorted2['pct_doctorate'],
    orientation='h',
    marker=dict(color='#e74c3c')
))

fig2.update_layout(
    title="South Bay Education: Degree Type Breakdown by ZIP Code (2023)",
    xaxis_title="Percentage of Population (25+)",
    yaxis_title="City (ZIP Code)",
    barmode='stack',
    height=1200,
    font=dict(size=10),
    plot_bgcolor='rgba(240,240,240,0.5)',
    legend=dict(x=0.7, y=0.02),
    xaxis=dict(gridcolor='white')
)

fig2.write_html("output/education_breakdown.html")
print("✓ Created: output/education_breakdown.html")

# -------------------------
# 3) CITY-LEVEL SUMMARY
# -------------------------
# Aggregate by city (weighted by population)
city_agg = df.groupby('city').apply(
    lambda x: pd.Series({
        'pct_bachelor_or_higher': (x['pct_bachelor_or_higher'] * x['total_pop_25plus']).sum() / x['total_pop_25plus'].sum(),
        'total_pop': x['total_pop_25plus'].sum(),
        'num_zips': len(x)
    })
).reset_index()

city_agg = city_agg.sort_values('pct_bachelor_or_higher', ascending=True)

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    y=city_agg['city'],
    x=city_agg['pct_bachelor_or_higher'],
    orientation='h',
    marker=dict(
        color=city_agg['pct_bachelor_or_higher'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="% Bachelor's+")
    ),
    text=[f"{val:.1f}%" for val in city_agg['pct_bachelor_or_higher']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>' +
                  'Bachelor\'s or Higher: %{x:.2f}%<br>' +
                  'Total Pop 25+: %{customdata[0]:,}<br>' +
                  'Number of ZIPs: %{customdata[1]}<br>' +
                  '<extra></extra>',
    customdata=city_agg[['total_pop', 'num_zips']].values
))

fig3.update_layout(
    title="South Bay Education: Average by City (Population-Weighted, 2023)",
    xaxis_title="Percentage with Bachelor's Degree or Higher",
    yaxis_title="City",
    height=600,
    showlegend=False,
    font=dict(size=12),
    plot_bgcolor='rgba(240,240,240,0.5)',
    xaxis=dict(gridcolor='white', range=[0, 95])
)

fig3.write_html("output/education_by_city.html")
print("✓ Created: output/education_by_city.html")

# -------------------------
# 4) SCATTER PLOT - Population vs Education
# -------------------------
fig4 = px.scatter(
    df,
    x='total_pop_25plus',
    y='pct_bachelor_or_higher',
    color='city',
    size='total_pop_25plus',
    hover_data=['zip', 'pct_bachelor', 'pct_master', 'pct_doctorate'],
    title="Population vs Education Level by ZIP Code",
    labels={
        'total_pop_25plus': 'Total Population (Age 25+)',
        'pct_bachelor_or_higher': 'Bachelor\'s Degree or Higher (%)',
        'city': 'City'
    },
    height=700
)

fig4.update_layout(
    plot_bgcolor='rgba(240,240,240,0.5)',
    xaxis=dict(gridcolor='white'),
    yaxis=dict(gridcolor='white')
)

fig4.write_html("output/education_scatter.html")
print("✓ Created: output/education_scatter.html")

# -------------------------
# 5) COMBINED DASHBOARD
# -------------------------
fig5 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Top 10 Most Educated ZIPs",
        "Bottom 10 Least Educated ZIPs",
        "City Averages",
        "Degree Type Distribution (Top 10)"
    ),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# Top 10
top10 = df.nlargest(10, 'pct_bachelor_or_higher')
fig5.add_trace(
    go.Bar(
        y=[f"{row['city']}<br>({row['zip']})" for _, row in top10.iterrows()],
        x=top10['pct_bachelor_or_higher'],
        orientation='h',
        marker=dict(color='#2ecc71'),
        text=[f"{val:.1f}%" for val in top10['pct_bachelor_or_higher']],
        textposition='outside',
        showlegend=False
    ),
    row=1, col=1
)

# Bottom 10
bottom10 = df.nsmallest(10, 'pct_bachelor_or_higher')
fig5.add_trace(
    go.Bar(
        y=[f"{row['city']}<br>({row['zip']})" for _, row in bottom10.iterrows()],
        x=bottom10['pct_bachelor_or_higher'],
        orientation='h',
        marker=dict(color='#e74c3c'),
        text=[f"{val:.1f}%" for val in bottom10['pct_bachelor_or_higher']],
        textposition='outside',
        showlegend=False
    ),
    row=1, col=2
)

# City averages
fig5.add_trace(
    go.Bar(
        y=city_agg['city'],
        x=city_agg['pct_bachelor_or_higher'],
        orientation='h',
        marker=dict(color='#3498db'),
        text=[f"{val:.1f}%" for val in city_agg['pct_bachelor_or_higher']],
        textposition='outside',
        showlegend=False
    ),
    row=2, col=1
)

# Degree breakdown for top 10
degree_data = top10[['city', 'zip', 'pct_bachelor', 'pct_master', 'pct_professional', 'pct_doctorate']]
zip_labels_top10 = [f"{row['city']}<br>({row['zip']})" for _, row in degree_data.iterrows()]

fig5.add_trace(go.Bar(name="Bachelor's", x=degree_data['pct_bachelor'], y=zip_labels_top10, 
                       orientation='h', marker=dict(color='#3498db')), row=2, col=2)
fig5.add_trace(go.Bar(name="Master's", x=degree_data['pct_master'], y=zip_labels_top10,
                       orientation='h', marker=dict(color='#2ecc71')), row=2, col=2)
fig5.add_trace(go.Bar(name="Professional", x=degree_data['pct_professional'], y=zip_labels_top10,
                       orientation='h', marker=dict(color='#f39c12')), row=2, col=2)
fig5.add_trace(go.Bar(name="Doctorate", x=degree_data['pct_doctorate'], y=zip_labels_top10,
                       orientation='h', marker=dict(color='#e74c3c')), row=2, col=2)

fig5.update_xaxes(title_text="% Bachelor's+", row=1, col=1)
fig5.update_xaxes(title_text="% Bachelor's+", row=1, col=2)
fig5.update_xaxes(title_text="% Bachelor's+", row=2, col=1)
fig5.update_xaxes(title_text="Percentage", row=2, col=2)

fig5.update_layout(
    height=1000,
    title_text="South Bay Education Dashboard (2023 ACS Data)",
    showlegend=True,
    barmode='stack',
    font=dict(size=9)
)

fig5.write_html("output/education_dashboard.html")
print("✓ Created: output/education_dashboard.html")

print("\n" + "="*60)
print("All visualizations created successfully!")
print("="*60)
print("\nOpen these HTML files in your browser:")
print("  1. output/education_dashboard.html    - Complete overview")
print("  2. output/education_by_zip.html       - All ZIPs ranked")
print("  3. output/education_by_city.html      - City-level summary")
print("  4. output/education_breakdown.html    - Degree type breakdown")
print("  5. output/education_scatter.html      - Population vs Education")

