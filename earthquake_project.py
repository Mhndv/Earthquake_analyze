import streamlit as st
import pandas as pd
import plotly.express as px
import reverse_geocoder as rg
import pycountry
from datetime import datetime

# ✅ Streamlit must start with this
st.set_page_config(layout="wide")

# ✅ Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/mohannedalsahaf/Desktop/Tuwaiq Data Science Bootcamp/Earthquakes_Dataset.csv")
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce')
    df = df.dropna(subset=['Datetime'])
    df = df.drop(columns=[
        c for c in [
            "Magnitude Error", "Horizontal Error", "Horizontal Distance",
            "Magnitude Seismic Stations", "Depth Error", "Depth Seismic Stations",
            "Azimuthal Gap"
        ] if c in df.columns
    ])
    df = df[["Datetime", "Latitude", "Longitude", "Depth", "Magnitude", "Magnitude Type", "Type"]]
    df = df.dropna(subset=["Latitude", "Longitude", "Magnitude"])
    return df

# ✅ Reverse geocode to get countries and convert to full names
@st.cache_data
def add_country_names(df):
    coords = list(zip(df['Latitude'], df['Longitude']))
    results = rg.search(coords, mode=1)
    iso_codes = [res['cc'] for res in results]
    df['Country Code'] = iso_codes

    # Convert to full names using pycountry
    def code_to_name(code):
        try:
            return pycountry.countries.get(alpha_2=code).name
        except:
            return code  # fallback
    df['Country'] = df['Country Code'].apply(code_to_name)
    return df

# ✅ Load and enhance data
df = add_country_names(load_data())

# ✅ Sidebar filters
st.sidebar.title("🔍 Filters")
min_date = df['Datetime'].min()
max_date = df['Datetime'].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])
min_mag, max_mag = st.sidebar.slider("Select Magnitude Range", float(df['Magnitude'].min()), float(df['Magnitude'].max()), (4.0, 9.1))

# ✅ Filter data
mask = (
    (df['Datetime'].dt.date >= start_date) &
    (df['Datetime'].dt.date <= end_date) &
    (df['Magnitude'] >= min_mag) &
    (df['Magnitude'] <= max_mag)
)
df = df[mask].copy()
df['Year'] = df['Datetime'].dt.year
df['LatRound'] = df['Latitude'].round(1)
df['LonRound'] = df['Longitude'].round(1)

# ✅ Title
st.title("🌍 Earthquake Data Dashboard")

# ✅ Full-width Map
with st.container():
    fig_map = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Magnitude",
        #size="Magnitude",
        hover_name="Datetime",
        projection="natural earth",
        title="Earthquake Map (Global)",
        height=450
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ✅ Key Metrics
k1, k2, k3 = st.columns(3)
k1.metric("Total Quakes", len(df))
k2.metric("Avg Magnitude", round(df['Magnitude'].mean(), 2))
k3.metric("Max Magnitude", df['Magnitude'].max())

# ✅ Three Charts in One Row
c1, c2, c3 = st.columns([1, 1, 1])

# Earthquakes per Year
with c1:
    yearly = df.groupby('Year').size().reset_index(name='Count')
    fig_year = px.bar(yearly, x='Year', y='Count', title="Earthquakes per Year", height=300)
    st.plotly_chart(fig_year, use_container_width=True)

# Depth vs Magnitude
with c2:
    fig_depth = px.scatter(
        df,
        x="Depth",
        y="Magnitude",
        color="Magnitude",
        title="Depth vs Magnitude",
        height=300
    )
    st.plotly_chart(fig_depth, use_container_width=True)

# Top Earthquake-Prone Countries (full names)
with c3:
    country_counts = df.groupby('Country').size().reset_index(name='Count')
    top_countries = country_counts.sort_values(by='Count', ascending=False).head(5)
    fig_hot = px.bar(
        top_countries,
        x='Count',
        y='Country',
        orientation='h',
        title="Top Earthquake-Prone Countries",
        height=300
    )
    st.plotly_chart(fig_hot, use_container_width=True)

# ✅ Optional: Download Filtered Data
st.download_button("⬇️ Download Filtered Data", df.to_csv(index=False), "filtered_earthquakes.csv")
