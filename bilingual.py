import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import cv2
from tqdm import tqdm
from matplotlib.colors import LinearSegmentedColormap
from shapely.geometry import Point
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import matplotlib.cm as cm

print("Starting Montreal SIM Intervention Animation Generator (Bilingual Version)")

# Set up directories for temporary frames and output
os.makedirs('frames', exist_ok=True)
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Define color mapping for incident types
color_mapping = {
    "Building fires / Incendies de bâtiments": 'red',
    "Other fires / Autres incendies": 'orange',
    "Non-fire / Sans incendie": 'blue',
    "Fire alarms / Alarmes-incendie": 'yellow',
    "First responders / Premiers répondants": 'green',
    "False alarms/cancellations / Fausses alertes/annulations": 'gray',
    "Other / Autres": 'purple'
}

# Bilingual mapping for incident types
incident_type_bilingual = {
    "Incendies de bâtiments": "Building fires / Incendies de bâtiments",
    "Autres incendies": "Other fires / Autres incendies",
    "Sans incendie": "Non-fire / Sans incendie",
    "Alarmes-incendie": "Fire alarms / Alarmes-incendie",
    "Premiers répondants": "First responders / Premiers répondants",
    "Fausses alertes/annulations": "False alarms/cancellations / Fausses alertes/annulations",
    "Autres": "Other / Autres"
}

# Function to normalize incident types across different datasets
def normalize_incident_type(incident_type):
    if not isinstance(incident_type, str):
        return "Autres"
    
    incident_type = incident_type.upper()
    
    if any(term in incident_type for term in ["INCENDIE BATIMENT", "BÂTIMENT", "BUILDING"]):
        return "Incendies de bâtiments"
    elif any(term in incident_type for term in ["INCENDIE", "AUTRE FEU", "FEU"]):
        return "Autres incendies"
    elif any(term in incident_type for term in ["SANS FEU", "SANS INCENDIE"]):
        return "Sans incendie"
    elif any(term in incident_type for term in ["ALARME", "ALARM"]):
        return "Alarmes-incendie"
    elif any(term in incident_type for term in ["PREMIER", "1-REPOND", "RÉPONDANT", "MEDICAL"]):
        return "Premiers répondants"
    elif any(term in incident_type for term in ["FAUSSE", "ANNUL", "CANCEL"]):
        return "Fausses alertes/annulations"
    else:
        return "Autres"

# Load CSV data
print("Loading data files...")
csv_files = [
    'donneesouvertes-interventions-sim.csv',
    'donneesouvertes-interventions-sim_2015_2022.csv',
    'donneesouvertes-interventions-sim_2005-2014.csv'
]

all_dfs = []
for file in csv_files:
    try:
        df = pd.read_csv(file)
        print(f"Loaded {file} with {len(df)} records")
        all_dfs.append(df)
    except Exception as e:
        print(f"Error loading {file}: {e}")

# Combine CSV data
if all_dfs:
    interventions_df = pd.concat(all_dfs, ignore_index=True)
    print(f"Combined {len(interventions_df)} records from CSV files")
else:
    print("No CSV data loaded. Exiting.")
    exit(1)

# Parse dates and add derived date components
print("Processing dates...")
if 'CREATION_DATE_TIME' in interventions_df.columns:
    # Parse dates with flexible format handling
    interventions_df['datetime'] = pd.to_datetime(
        interventions_df['CREATION_DATE_TIME'], 
        errors='coerce',
        format='mixed'
    )
    
    # Only keep records with valid dates
    interventions_df = interventions_df.dropna(subset=['datetime'])
    print(f"Retained {len(interventions_df)} records with valid dates")
    
    # Extract date components
    interventions_df['year'] = interventions_df['datetime'].dt.year
    interventions_df['month'] = interventions_df['datetime'].dt.month
    interventions_df['year_month'] = interventions_df['datetime'].dt.strftime('%Y-%m')
    
    # Filter for suspicious midnight timestamps
    suspicious_times = (
        (interventions_df['datetime'].dt.hour == 0) & 
        (interventions_df['datetime'].dt.minute == 0) & 
        (interventions_df['datetime'].dt.second == 0)
    )
    
    print(f"Found {suspicious_times.sum()} records with suspicious 00:00:00 timestamps")
    # We'll keep these records but mark them
    interventions_df['exact_time_known'] = ~suspicious_times
    
    # Add normalized incident category 
    if 'DESCRIPTION_GROUPE' in interventions_df.columns:
        interventions_df['INCIDENT_CATEGORY'] = interventions_df['DESCRIPTION_GROUPE'].apply(normalize_incident_type)
    else:
        # Try alternative column names
        for col in ['INCIDENT_TYPE_DESC', 'DESCRIPTIO']:
            if col in interventions_df.columns:
                interventions_df['INCIDENT_CATEGORY'] = interventions_df[col].apply(normalize_incident_type)
                break
        else:
            interventions_df['INCIDENT_CATEGORY'] = 'Autres'
    
    # Get the year range
    years = sorted(interventions_df['year'].unique())
    start_year = min(years)
    end_year = max(years)
    print(f"Data covers {start_year} to {end_year}")
    
    # Count records by year-month to identify gaps
    year_month_counts = interventions_df['year_month'].value_counts().sort_index()
    
    # Create year-month sequence for complete timeline
    # But only include months that actually have data
    year_month_range = list(year_month_counts.index)
    print(f"Found {len(year_month_range)} months with data")
    
    # Add a note about the data coverage
    data_note_en = "Note: Animation includes only months with available data."
    data_note_fr = "Remarque: L'animation inclut uniquement les mois avec des données disponibles."
    data_note = f"{data_note_en} / {data_note_fr}"
else:
    print("No date column found. Exiting.")
    exit(1)

# Prepare the animation
print("Preparing animation...")

# Create month names in French
month_names_fr = {
    1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril',
    5: 'mai', 6: 'juin', 7: 'juillet', 8: 'août',
    9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
}

# Create a function to generate frames
def create_frame(year_month, frame_number, total_frames):
    # Parse year and month
    year, month = map(int, year_month.split('-'))
    month_name_fr = month_names_fr[month]
    
    # Filter data for the current month and all preceding months in the rolling window
    # Use a 12-month rolling window
    window_start_idx = max(0, frame_number - 11)
    window_months = year_month_range[window_start_idx:frame_number + 1]
    
    window_data = interventions_df[interventions_df['year_month'].isin(window_months)]
    current_month_data = interventions_df[interventions_df['year_month'] == year_month]
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 9), dpi=120)
    
    # Set up the layout with GridSpec
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1])
    
    # Bilingual title for the whole figure - split into two lines
    plt.suptitle(
        f'Montreal Fire Department Interventions: created by Mycole Brown\nInterventions du Service d\'incendie de Montréal: créé par Mycole Brown\n{year}-{month:02d} ({month_name_fr} {year})', 
        fontsize=18, fontweight='bold', y=0.98
    )
    
    # Subplot 1: Monthly trend line over time
    ax1 = plt.subplot(gs[0, :])
    
    # Prepare data for the trend line
    monthly_counts = []
    plot_dates = []
    
    for ym in year_month_range[:frame_number+1]:
        count = len(interventions_df[interventions_df['year_month'] == ym])
        monthly_counts.append(count)
        plot_dates.append(datetime.strptime(ym, '%Y-%m'))
    
    # Plot the trend line
    ax1.plot(plot_dates, monthly_counts, 'b-', linewidth=2)
    ax1.set_title('Monthly Intervention Trend / Tendance mensuelle des interventions', fontsize=16)
    ax1.set_ylabel('Number of Interventions / Nombre d\'interventions', fontsize=13)
    
    # Format the x-axis to show only years
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    
    # Highlight the current month
    current_date = datetime.strptime(year_month, '%Y-%m')
    current_count = monthly_counts[-1]
    ax1.plot(current_date, current_count, 'ro', markersize=8)
    
    # Add a bilingual text label for the current month
    ax1.text(current_date, current_count + (max(monthly_counts) * 0.05),
             f'{year}-{month:02d}: {current_count:,} interventions',
             ha='center', va='bottom', fontsize=12, fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))
    
    # Set y-axis limit with some headroom
    ax1.set_ylim(0, max(monthly_counts) * 1.2)
    
    # Add grid
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Subplot 2: Incident type breakdown for current month (pie chart)
    ax2 = plt.subplot(gs[1, 0])
    
    # Convert incident categories to bilingual versions
    current_month_data_bilingual = current_month_data.copy()
    current_month_data_bilingual['INCIDENT_CATEGORY_BILINGUAL'] = current_month_data_bilingual['INCIDENT_CATEGORY'].map(incident_type_bilingual)
    
    # Count incidents by category for the current month
    category_counts = current_month_data_bilingual['INCIDENT_CATEGORY'].value_counts()
    
    # Only include categories that have data
    categories = []
    bilingual_categories = []
    counts = []
    colors = []
    
    for cat, count in category_counts.items():
        if count > 0:
            categories.append(cat)
            bilingual_categories.append(incident_type_bilingual[cat])
            counts.append(count)
            colors.append(color_mapping.get(incident_type_bilingual[cat], 'purple'))
    
    # Create the pie chart
    if counts:  # Only if we have data
        wedges, texts, autotexts = ax2.pie(
            counts, 
            labels=None,  # We'll add a legend instead
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        
        # Make the percentage labels more readable
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Add a bilingual legend
        ax2.legend(
            wedges, 
            [f"{bicat} ({count:,})" for bicat, count in zip(bilingual_categories, counts)],
            title="Incident Types / Types d'incidents",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=9
        )
    
    ax2.set_title(f'Incident Types / Types d\'incidents: {year}-{month:02d}', fontsize=15)
    
    # Subplot 3: Bar chart showing 12-month rolling average by incident type
    ax3 = plt.subplot(gs[1, 1])
    
    # Group by incident category for the rolling window and convert to bilingual
    rolling_category_counts = window_data['INCIDENT_CATEGORY'].value_counts()
    
    # Convert to bilingual display names
    bilingual_rolling_categories = {}
    for cat, count in rolling_category_counts.items():
        bilingual_cat = incident_type_bilingual[cat]
        bilingual_rolling_categories[bilingual_cat] = count
    
    # Convert to Series and sort
    rolling_bilingual_series = pd.Series(bilingual_rolling_categories)
    rolling_bilingual_series = rolling_bilingual_series.sort_values(ascending=True)  # Ascending for horizontal bar
    
    # Plot horizontal bar chart
    bars = ax3.barh(
        range(len(rolling_bilingual_series)),
        rolling_bilingual_series.values,
        color=[color_mapping.get(cat, 'purple') for cat in rolling_bilingual_series.index]
    )
    
    # Add value labels to the bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax3.text(
            width + (rolling_bilingual_series.max() * 0.02),
            bar.get_y() + bar.get_height()/2,
            f'{int(width):,}',
            ha='left', va='center', fontsize=10
        )
    
    # Set labels and title
    ax3.set_yticks(range(len(rolling_bilingual_series)))
    ax3.set_yticklabels(rolling_bilingual_series.index, fontsize=8)
    ax3.set_title('12-Month Rolling Total / Total mobile sur 12 mois', fontsize=15)
    ax3.set_xlabel('Number of Interventions / Nombre d\'interventions', fontsize=13)
    
    # Add grid
    ax3.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Add timestamp, data info and note about coverage
    plt.figtext(
        0.01, 0.01,
        f'Created / Créé: {datetime.now().strftime("%Y-%m-%d")} | Data source / Source des données: Service d\'incendie de Montréal (SIM) | {data_note}',
        fontsize=8, color='gray'
    )
    
    # Save the frame
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to accommodate the suptitle
    frame_path = f'frames/frame_{frame_number:04d}.png'
    plt.savefig(frame_path, dpi=120)
    plt.close()
    
    return frame_path

# Generate all frames
print("Generating animation frames...")
frame_paths = []

# Generate frames with progress bar
for idx, year_month in enumerate(tqdm(year_month_range, desc="Creating frames")):
    frame_path = create_frame(year_month, idx, len(year_month_range))
    frame_paths.append(frame_path)

# Compile frames into a video
print("Compiling video...")
output_video_path = os.path.join(output_dir, 'montreal_sim_interventions_bilingual.mp4')

# Get frame dimensions from the first image
first_frame = cv2.imread(frame_paths[0])
height, width, layers = first_frame.shape

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v codec
fps = 2  # Frames per second - adjust for slower/faster playback
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Add each frame to the video
for frame_path in tqdm(frame_paths, desc="Adding frames to video"):
    frame = cv2.imread(frame_path)
    out.write(frame)

# Release the video writer
out.release()

print(f"Video saved to {output_video_path}")

# Optionally, add the final 3 seconds pause on the last frame
print("Adding pause on final frame...")
last_frame = cv2.imread(frame_paths[-1])
pause_video_path = os.path.join(output_dir, 'montreal_sim_interventions_bilingual_with_pause.mp4')
out_pause = cv2.VideoWriter(pause_video_path, fourcc, fps, (width, height))

# Add all regular frames
for frame_path in frame_paths:
    frame = cv2.imread(frame_path)
    out_pause.write(frame)

# Add 3 seconds of the final frame (3 seconds * fps frames)
for _ in range(3 * fps):
    out_pause.write(last_frame)

out_pause.release()

print(f"Video with pause saved to {pause_video_path}")

print("Bilingual animation creation completed!")