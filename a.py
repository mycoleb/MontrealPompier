import os
import pandas as pd

def summarize_files():
    print("--- Montreal Fire Department Data Summary ---")
    files = os.listdir('.')
    csv_files = [f for f in files if f.endswith('.csv')]
    shapefiles = [f for f in files if f.endswith('.shp')]
    
    print(f"\nFound {len(csv_files)} CSV data files:")
    for csv in csv_files:
        try:
            # Check row count and date range for each file
            df = pd.read_csv(csv, usecols=['CREATION_DATE_TIME'])
            df['dt'] = pd.to_datetime(df['CREATION_DATE_TIME'], errors='coerce', format='mixed')
            start = df['dt'].min()
            end = df['dt'].max()
            print(f"- {csv}: {len(df):,} records | Range: {start.date()} to {end.date()}")
        except:
            print(f"- {csv}: Could not parse date info.")

    print(f"\nFound {len(shapefiles)} Shapefile sets (GIS Data):")
    for shp in shapefiles:
        print(f"- {shp} (Requires accompanying .dbf, .shx, and .prj)")

if __name__ == "__main__":
    summarize_files()