
# 🌍 Earthquake Data Analysis Dashboard

This project is a **Streamlit-powered interactive dashboard** that analyzes global earthquake data. Users can explore seismic activity visually and filter earthquakes by date, magnitude, and more.

---

## 📊 Features

- 🌍 **Interactive World Map** of earthquakes with magnitude-based color and size
- 📅 **Date Range Selector** to explore historical earthquakes
- **Magnitude Range** to explore all ranges of magnitudes
- **Magnitude Type Selector** to select specific types of the magnitudes
- 🗺️ **Country Selection** to explore specific country historical earthquakes
- 📈 **Charts**:
  - Earthquakes per year
  - Depth vs Magnitude
  - Top Earthquake-Prone Countries (using full country names)
- 📌 **Key Metrics**:
  - Total Earthquakes
  - Average Magnitude
  - Strongest Earthquake
- ⬇️ **Downloadable CSV** of filtered results
- 🌐 **Reverse Geocoding**: Country names from coordinates
- 💡 Optimized layout with large full-width map and organized charts

---

## 📁 Dataset

The dashboard uses a CSV file from kaggle:  
**[`Earthquakes_Dataset.csv`](https://www.kaggle.com/datasets/usgs/earthquake-database?resource=download)**

Minimum required columns:
- `Date`
- `Time`
- `Latitude`
- `Longitude`
- `Magnitude`
- `Magnitude Type`
- `Depth`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Mhndv/earthquake-dashboard.git
cd earthquake-dashboard
```

### 2. Install Dependencies

Install from the `requirements.txt`:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pandas plotly reverse_geocoder pycountry
```

### 3. Run the App

```bash
streamlit run app.py
```

Then open the local URL (usually http://localhost:8501) to view the dashboard.

---

## 🧠 Insights You Can Gain

- 🌍 Where in the world earthquakes occur most frequently
- ⛏️ The relationship between earthquake depth and magnitude
- 📈 Trends in earthquake activity over time
- 🧭 The most active seismic regions by country

---

## 📦 Requirements

- `streamlit`
- `pandas`
- `plotly`
- `reverse_geocoder`
- `pycountry`

See `requirements.txt` for full details.

---


## Screeshot

<img width="1728" alt="Screenshot 1446-11-05 at 2 49 23 PM" src="https://github.com/user-attachments/assets/15fd8968-98cf-437b-ad45-9b0195b12830" />


---


## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
