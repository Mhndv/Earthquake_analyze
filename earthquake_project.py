import streamlit as st
import pandas as pd
import plotly.express as px
import reverse_geocoder as rg
import pycountry
from datetime import datetime


st.set_page_config(layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("Earthquakes_Dataset.csv")
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce')
    df = df.dropna(subset=['Datetime'])
    df = df[["Datetime", "Latitude", "Longitude", "Depth", "Magnitude", "Magnitude Type"]]
    df = df.dropna()
    return df


@st.cache_data
def add_country_names(df):
    #adding country names according to the coodinates
    coords = list(zip(df['Latitude'], df['Longitude']))
    results = rg.search(coords, mode=1)
    iso_codes = [res['cc'] for res in results]
    df['Country Code'] = iso_codes

    # convert to full country names
    def code_to_name(code):
        try:
            return pycountry.countries.get(alpha_2=code).name
        except:
            return code  
    df['Country'] = df['Country Code'].apply(code_to_name)
    return df


df = add_country_names(load_data())

#SIDEBAR

#date and magnitude filter
st.sidebar.title("🔍 Filters")
min_date = df['Datetime'].min()
max_date = df['Datetime'].max()
start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

min_mag, max_mag = st.sidebar.slider("Select Magnitude Range", float(df['Magnitude'].min()), float(df['Magnitude'].max()), (4.0, 9.1))

#magnitude types filter
magnitude_types = ["All"] + sorted(df['Magnitude Type'].unique().tolist())
selected_mag_type = st.sidebar.selectbox(
    "Select Magnitude Type", 
    magnitude_types,
    index=0  # Default to "All"
)
#country filter
available_countries = sorted(df["Country"].dropna().unique().tolist())
available_countries.insert(0, "All")  
selected_country = st.sidebar.selectbox("🌍 Select Country", available_countries, index=0)


#change the data according to the filters
mask = (
    (df['Datetime'].dt.date >= start_date) &
    (df['Datetime'].dt.date <= end_date) &
    (df['Magnitude'] >= min_mag) &
    (df['Magnitude'] <= max_mag)&
    ((df['Magnitude Type'] == selected_mag_type) if selected_mag_type != "All" else True)
)
if selected_country != "All":
    mask = mask & (df["Country"] == selected_country)

df = df[mask].copy()
df['Year'] = df['Datetime'].dt.year
df['LatRound'] = df['Latitude'].round(1)
df['LonRound'] = df['Longitude'].round(1)


st.title("🌍 Earthquake Data Dashboard")

#map
with st.container():
    fig_map = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Magnitude",
        hover_name="Datetime",
        projection="natural earth",
        title="Earthquake Map (Global)",
        height=450
    )
    st.plotly_chart(fig_map, use_container_width=True)

#data summary
k1, k2, k3 = st.columns(3)
k1.metric("Total Quakes", len(df))
k2.metric("Avg Magnitude", round(df['Magnitude'].mean(), 2))
k3.metric("Max Magnitude", df['Magnitude'].max())


c1, c2, c3 = st.columns([1, 1, 1])

# earthquakes per Year
with c1:
    yearly = df.groupby('Year').size().reset_index(name='Count')
    fig_year = px.bar(yearly, x='Year', y='Count', title="Earthquakes per Year", height=300)
    st.plotly_chart(fig_year, use_container_width=True)

# depth vs magnitude
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

# top earthquake countries 
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

# download filtered data option 
st.download_button("⬇️ Download Filtered Data", df.to_csv(index=False), "filtered_earthquakes.csv")
