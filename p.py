import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from tqdm import tqdm

# Setup
os.makedirs('histogram_frames', exist_ok=True)
csv_files = [
    'donneesouvertes-interventions-sim.csv',
    'donneesouvertes-interventions-sim_2015_2022.csv',
    'donneesouvertes-interventions-sim_2005-2014.csv'
]

print("Loading and cleaning data for hourly analysis...")
all_dfs = []
for file in csv_files:
    if os.path.exists(file):
        df = pd.read_csv(file, usecols=['CREATION_DATE_TIME'])
        all_dfs.append(df)

df = pd.concat(all_dfs, ignore_index=True)
df['datetime'] = pd.to_datetime(df['CREATION_DATE_TIME'], errors='coerce', format='mixed')
df = df.dropna(subset=['datetime'])

# FILTER: Exclude the suspicious 00:00:00 timestamps to see real hourly trends
# If we keep them, there will be a massive fake spike at midnight.
df = df[~((df['datetime'].dt.hour == 0) & (df['datetime'].dt.minute == 0))]

df['year_month'] = df['datetime'].dt.to_period('M')
df['hour'] = df['datetime'].dt.hour
timeline = sorted(df['year_month'].unique())

fig, ax = plt.subplots(figsize=(10, 6))

def animate(i):
    ax.clear()
    current_month = timeline[i]
    month_data = df[df['year_month'] == current_month]
    
    ax.hist(month_data['hour'], bins=24, range=(0, 24), color='skyblue', edgecolor='black')
    ax.set_title(f'Montreal Interventions: Hourly Distribution ({current_month})', fontsize=14)
    ax.set_xlabel('Hour of Day (0-23)', fontsize=12)
    ax.set_ylabel('Number of Incidents', fontsize=12)
    ax.set_xlim(0, 23)
    ax.set_xticks(range(0, 24))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

print("Generating histogram animation...")
ani = animation.FuncAnimation(fig, animate, frames=len(timeline), interval=200)
ani.save('output/hourly_histogram_2005_2026.mp4', writer='ffmpeg', fps=5)
print("Animation saved to output/hourly_histogram_2005_2026.mp4")