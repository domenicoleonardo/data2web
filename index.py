import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("datasets/Climate_historical_data_RSBrasil.csv")

st.set_page_config(layout="wide")

# Title
st.title("Rainfall Analysis in Rio Grande do Sul - 64 Years of Historical Data")
st.markdown("### Visualize total rainfall by city and month over the years")

# Year range from dataset
year_min = int(df["Year"].min())
year_max = int(df["Year"].max())

# Year range slider
year_range = st.sidebar.slider(
    "Select the year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# Filter by selected year range
df_year_range = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# Station selection
station = st.sidebar.selectbox("Select the weather station", df_year_range["Station"].unique())

# Filter by station
df_filtered = df_year_range[df_year_range["Station"] == station]

# Group by Year and Month, calculating total rainfall and temperature averages
df_summary = df_filtered.groupby(["Year", "Month"]).agg({
    "Total Rainfall (mm)": "sum",
    "Max Temperature (°C)": "mean",
    "Min Temperature (°C)": "mean"
}).reset_index()

# Display summary table
st.markdown(f"### Summary data for: {station}")
st.markdown("Showing up to 20 results")
st.table(df_summary.head(20))

# Group by Month to get total rainfall across all stations for the selected year range
df_monthly_rainfall = df_year_range.groupby("Month")["Total Rainfall (mm)"].sum().reset_index()

# Create bar chart
fig = px.bar(
    df_monthly_rainfall,
    x="Month",
    y="Total Rainfall (mm)",
    title=f"Total Rainfall by Month from {year_range[0]} to {year_range[1]}",
    labels={"Month": "Month", "Total Rainfall (mm)": "Total Rainfall (mm)"},
    color="Month",
    text_auto=True
)

# Customize chart appearance
fig.update_layout(
    title_font_size=24,
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title_font_size=18,
    yaxis_title_font_size=18,
    font=dict(size=14),
    bargap=0.2,
    showlegend=False
)

fig.update_traces(marker_line_color='black', marker_line_width=1.5)

# Display chart
st.plotly_chart(fig, use_container_width=True)

# Calculate the month with the most rainfall
month_most_rain = df_monthly_rainfall.loc[df_monthly_rainfall["Total Rainfall (mm)"].idxmax()]

# Display insight with station name highlighted in orange
st.markdown(
    f"<h3>The month with the most rainfall in <span style='color:orange;'>{station}</span> from {year_range[0]} to {year_range[1]} was <b>{month_most_rain['Month']}</b>.</h3>",
    unsafe_allow_html=True
)
