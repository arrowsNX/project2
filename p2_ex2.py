#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 08:24:37 2024

@author: feno
"""
import streamlit as st
#import matplotlib.pyplot as plt
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


