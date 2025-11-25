# 🚀 Quick Setup Guide

## Initial Setup

1. **Install Dependencies**
```bash
pip3 install -r requirements.txt
```

2. **Run Scripts in Order**

### Step 1: Fetch Census Data
```bash
python3 code.py
```
Creates: `south_bay_education.csv`

### Step 2: Generate Statistical Charts
```bash
python3 visualize.py
```
Creates 5 HTML files in `output/` folder

### Step 3: Create Geographic Map (Recommended)
```bash
python3 geo_map.py
```
Creates interactive map with dropdown menu in `output/` folder

## 📂 Output Files

All visualizations are saved to the `output/` folder:
- `south_bay_education_map_interactive.html` ⭐ Main interactive map
- `education_dashboard.html` - Statistical dashboard
- Plus 6 more visualization files

## 💡 Tips

- The shapefile download (~500MB) happens automatically in `geo_map.py`
- Census API key is optional (add to `code.py` line 11 if you have one)
- HTML files can be opened directly in any browser
- All outputs are in `.gitignore` and won't be pushed to GitHub

## 🔧 Troubleshooting

**Issue: pip install fails**
- Try: `pip3 install --user -r requirements.txt`

**Issue: Shapefile download slow**
- The ZCTA shapefile is ~500MB, first run takes a few minutes
- Subsequent runs reuse the downloaded file

**Issue: Missing output folder**
- Run: `mkdir -p output`
