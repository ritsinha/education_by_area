# 🎓 South Bay Education Analysis

Interactive visualizations of education levels across South Bay Area ZIP codes using 2023 American Community Survey (ACS) data from the U.S. Census Bureau.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📊 Overview

This project analyzes and visualizes educational attainment data for cities in the San Francisco Bay Area's South Bay region, including:
- San Jose
- Cupertino
- Palo Alto
- Mountain View
- Los Altos
- Sunnyvale
- Santa Clara
- Campbell
- Milpitas
- Los Gatos
- Saratoga

### 💡 Inspiration

This project was inspired by the San Francisco Chronicle article ["Where are the Bay Area's most educated residents? This map shows the latest Census data"](https://www.sfchronicle.com/sf/article/most-educated-residents-data-21199765.php) by [Hanna Zakharenko](https://www.sfchronicle.com/author/hanna-zakharenko/) and [Danielle Echeverria](https://www.sfchronicle.com/author/danielle-echeverria/). Their data journalism sparked the question of what this data looks like for the South Bay ZIP codes.

All data used in this project is publicly available from the U.S. Census Bureau and can be freely accessed and analyzed by anyone.

## ✨ Features

### 🗺️ Interactive Geographic Maps
- **Choropleth map** with ZIP code boundaries
- **Dropdown menu** to switch between different education metrics:
  - No Bachelor's Degree
  - Bachelor's or Higher
  - Master's Degree
  - Professional Degree
  - Master's, Professional or PhD
  - PhD Degree
- **Hover tooltips** showing complete education breakdown for each ZIP
- **Zoom, pan, and explore** the South Bay area

### 📈 Statistical Visualizations
- **Interactive dashboard** with multiple panels
- **Bar charts** ranking all ZIP codes and cities
- **Stacked bar charts** showing degree type distribution
- **Scatter plots** comparing population vs education levels

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Scripts

#### 1. Fetch Data and Create Basic Visualizations
```bash
python3 code.py
```
This will:
- Fetch education data from Census API for South Bay ZIP codes
- Generate `south_bay_education.csv` with all statistics
- Attempt to create a basic Folium map (may fail on shapefile download)

#### 2. Generate Interactive Charts
```bash
python3 visualize.py
```
This creates 5 Plotly visualizations:
- `education_dashboard.html` - Complete overview
- `education_by_zip.html` - All ZIPs ranked
- `education_by_city.html` - City-level summary
- `education_breakdown.html` - Degree type breakdown
- `education_scatter.html` - Population vs Education

#### 3. Create Interactive Geographic Map ⭐ **Recommended**
```bash
python3 geo_map.py
```
This creates:
- `south_bay_education_map_interactive.html` - **Main interactive map with dropdown**
- `south_bay_education_map.html` - Simple version with ZIP labels

## 📁 Project Structure

```
education_by_zip/
├── code.py                          # Main data fetching script
├── visualize.py                     # Statistical charts generator
├── geo_map.py                       # Geographic map generator
├── south_bay_education.csv          # Generated data file
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
└── output/                          # Generated HTML visualizations (not in repo)
    ├── education_dashboard.html
    ├── education_by_zip.html
    ├── education_by_city.html
    ├── education_breakdown.html
    ├── education_scatter.html
    ├── south_bay_education_map_interactive.html
    └── south_bay_education_map.html
```

## 📊 Data Sources

- **Education Data**: [U.S. Census Bureau American Community Survey (ACS) 2023](https://www.census.gov/programs-surveys/acs)
  - Table B15003: Educational Attainment for the Population 25 Years and Over
- **Geographic Boundaries**: [TIGER/Line Shapefiles - ZIP Code Tabulation Areas (ZCTAs)](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)

## 🎯 Education Metrics

The project analyzes the following educational attainment levels for population 25 years and older:

- **Bachelor's Degree**: 4-year college degree
- **Master's Degree**: Graduate degree beyond bachelor's
- **Professional Degree**: JD, MD, DDS, DVM, etc.
- **Doctorate Degree**: PhD, EdD, etc.
- **Bachelor's or Higher**: Combined percentage with any 4-year degree or above
- **No Bachelor's**: Percentage without a 4-year degree

## 📈 Key Findings

Based on 2023 ACS data:
- **Highest Education**: Palo Alto ZIP 94305 (Stanford area) - **90.9%** with Bachelor's+
- **Lowest Education**: San Jose ZIP 95122 - **17.9%** with Bachelor's+
- **Average Across South Bay**: ~60% with Bachelor's degree or higher
- **54 ZIP Codes** analyzed across **11 cities**

## 🛠️ Technologies Used

- **Python 3.9+**
- **pandas** - Data manipulation
- **geopandas** - Geographic data processing
- **plotly** - Interactive visualizations
- **folium** - Alternative mapping library
- **requests** - API data fetching

## 📝 Notes

- **All data is publicly available** from the U.S. Census Bureau and free to use
- Census API key is optional but recommended for higher rate limits
- Shapefile downloads are ~500MB (automatically downloaded when running `geo_map.py`)
- Generated HTML files are standalone and can be shared without dependencies
- This project was developed with assistance from LLMs and AI Coding tools

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to:
- **[Hanna Zakharenko](https://www.sfchronicle.com/author/hanna-zakharenko/)** and **[Danielle Echeverria](https://www.sfchronicle.com/author/danielle-echeverria/)** at the San Francisco Chronicle for their inspiring [data journalism article](https://www.sfchronicle.com/sf/article/most-educated-residents-data-21199765.php) on Bay Area education patterns
- **U.S. Census Bureau** for providing comprehensive, publicly available ACS data

## 📧 Contact

**Ritwik Sinha** | [ritwik.sinha@gmail.com](mailto:ritwik.sinha@gmail.com)

For questions or suggestions feel free to reach out. 

---

**Note**: This project is for those who are curious. Census data is subject to sampling error and other limitations detailed in the ACS documentation.

