#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 08:24:37 2024

@author: feno
"""
import subprocess
import sys

# Install matplotlib if it isn't already installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt


import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

# Fetch exoplanet data
exoplanet_data = NasaExoplanetArchive.query_criteria(
    table="ps", 
    select="pl_name, pl_orbper, pl_rade, pl_masse, st_mass, st_rad, st_teff"
)

# Save data to CSV
exoplanet_data.to_pandas().to_csv("exoplanet_data_extended.csv", index=False)
# Load the raw exoplanet data
data = pd.read_csv("exoplanet_data_extended.csv")

# Data Cleaning: Remove rows with missing values in essential columns
# Essential columns: 'pl_orbper' (orbital period), 'pl_rade' (planet radius), 'pl_masse' (planet mass), 'st_teff' (star temperature)
cleaned_data = data.dropna(subset=['pl_orbper', 'pl_rade', 'pl_masse', 'st_teff'])

# Save cleaned data to a new CSV
cleaned_data.to_csv("cleaned_exoplanet_data.csv", index=False)

print("Data cleaning complete. Cleaned data saved as 'cleaned_exoplanet_data.csv'.")



# Title and Bio
st.title("Exoplanet Habitability Analysis")
st.write("This app explores exoplanets with criteria potentially indicative of habitability.")

# Bio Section
st.header("About Me")
st.write("""
I am Feno, a researcher interested in the habitability of exoplanets. This app filters exoplanet data based on criteria like size, orbital period, and host star characteristics to identify planets that could be habitable.
""")

# Load Cleaned Data
data = pd.read_csv("cleaned_exoplanet_data.csv")

# Display Data Table
st.header("Exoplanet Data Preview")
st.write(data.head())

# Habitability Filter
st.header("Potentially Habitable Planets")


# Load Cleaned Data
data = pd.read_csv("cleaned_exoplanet_data.csv")

# Habitability Formula: Define boundaries for habitable zones
def is_habitable(row):
    # Stellar flux limits for habitable zone (based on simplified model)
    flux_inner = 0.75 * (row['st_teff'] / 5778)**2
    flux_outer = 1.75 * (row['st_teff'] / 5778)**2
    # Distance calculation in AU
    distance_au = (row['pl_orbper']**2 * row['st_mass'])**(1/3)
    row['distance_au'] = distance_au  # Store the distance in AU
    return flux_inner <= distance_au <= flux_outer and row['pl_rade'] <= 1.6 and row['pl_masse'] <= 5

# Add habitability flag and distance in AU
data['habitable'] = data.apply(is_habitable, axis=1)
data['distance_au'] = data.apply(lambda row: (row['pl_orbper']**2 * row['st_mass'])**(1/3), axis=1)

# Plot: Logarithmic scale for Distance from Star (in AU) vs. Star Temperature
st.header("Log Scale: Distance from Star (AU) vs. Star Temperature")
fig, ax = plt.subplots()
habitable = data[data['habitable']]
non_habitable = data[~data['habitable']]

# Plot habitable and non-habitable planets
ax.scatter(non_habitable['distance_au'], non_habitable['st_teff'], color="gray", alpha=0.5, label="Non-Habitable")
ax.scatter(habitable['distance_au'], habitable['st_teff'], color="green", label="Habitable", edgecolor="black")

# Set axes to log scale
ax.set_xscale("log")
ax.set_xlabel("Distance from Star (AU, Log Scale)")
ax.set_ylabel("Star Temperature (K)")
ax.set_title("Potential Habitability by Distance (AU) and Star Temperature")
ax.legend()
st.pyplot(fig)
