#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 08:24:37 2024

@author: feno
"""
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

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

# Define Habitability Criteria
habitable_planets = data[
    (data['pl_rade'] <= 1.6) &                    # Radius close to Earth's
    (data['pl_masse'] <= 5) &                     # Mass similar to Earth
    (data['pl_orbper'] >= 100) & (data['pl_orbper'] <= 500) &  # Reasonable orbital period for habitability
    (data['st_teff'] >= 2400) & (data['st_teff'] <= 7600)     # Temperature range of host star
]

st.write("Planets meeting habitability criteria:")
st.write(habitable_planets)

# Visualization for Habitability Metrics
st.header("Visualizing Potential Habitability")

# Orbital Period Distribution (Filtered for Habitability)
st.subheader("Orbital Period of Potentially Habitable Exoplanets")
fig, ax = plt.subplots()
ax.hist(habitable_planets['pl_orbper'].dropna(), bins=15, color="lightblue", edgecolor="black")
ax.set_xlabel("Orbital Period (days)")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Orbital Periods for Potentially Habitable Planets")
st.pyplot(fig)

# Radius vs Mass Scatter Plot (Filtered for Habitability)
st.subheader("Potentially Habitable Planet Radius vs. Mass")
fig, ax = plt.subplots()
ax.scatter(habitable_planets['pl_rade'], habitable_planets['pl_masse'], color='green', alpha=0.7)
ax.set_xlabel("Planet Radius (Earth radii)")
ax.set_ylabel("Planet Mass (Earth masses)")
ax.set_title("Radius vs. Mass of Potentially Habitable Planets")
st.pyplot(fig)

# Star Temperature Distribution (Filtered for Habitability)
st.subheader("Host Star Effective Temperature of Potentially Habitable Planets")
fig, ax = plt.subplots()
ax.hist(habitable_planets['st_teff'].dropna(), bins=10, color="orange", edgecolor="black")
ax.set_xlabel("Effective Temperature (K)")
ax.set_ylabel("Frequency")
ax.set_title("Host Star Temperature for Potentially Habitable Planets")
st.pyplot(fig)