import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import os
from tqdm import tqdm

# 1. Load the Shapefiles (GIS Data)
# Using your 2020+ shapefile as it matches your recent coordinates
gdf = gpd.read_file('interventions-sim2020.shp')

# 2. Re-project to Web Mercator for OpenStreetMap compatibility
gdf = gdf.to_crs(epsg=3857)

# 3. Clean dates and filter for the 3 main types
gdf['datetime'] = pd.to_datetime(gdf['CREATION_DATE_TIME'], errors='coerce')
gdf['year_month'] = gdf['datetime'].dt.to_period('M')

# Filter for specific call types seen in your previous bar charts
target_types = ['1-REPOND', 'SANS FEU', 'INCENDIE']
gdf = gdf[gdf['DESCRIPTION_GROUPE'].isin(target_types)]

timeline = sorted(gdf['year_month'].unique())

def create_map_frame(month):
    fig, ax = plt.subplots(figsize=(12, 12))
    month_data = gdf[gdf['year_month'] == month]
    
    # Plot heatmap/density using a hexbin or scatter with alpha
    if not month_data.empty:
        month_data.plot(ax=ax, column='DESCRIPTION_GROUPE', categorical=True, 
                        legend=True, markersize=5, alpha=0.5, cmap='Set1')
    
    # Add OpenStreetMap background
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    
    ax.set_title(f'Montreal Fire Dept Activity: {month}', fontsize=15)
    ax.set_axis_off()
    
    plt.savefig(f'frames/map_{month}.png', dpi=120)
    plt.close()

print("Generating map frames...")
for m in tqdm(timeline[-24:]): # Starting with last 24 months for speed
    create_map_frame(m)