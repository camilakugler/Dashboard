import pandas as pd
import plotly.express as px
import streamlit as st
import time

# Compatibility: define experimental_rerun fallback for Streamlit versions without it
if not hasattr(st, "experimental_rerun"):
    def experimental_rerun():
        # Fallback: update query params to force a rerun when possible
        try:
            st.experimental_set_query_params(_rerun=str(time.time()))
        except Exception:
            pass
    st.experimental_rerun = experimental_rerun

# Load the data
car_data = pd.read_csv('vehicles.csv')

# Extract manufacturer from model (assuming first word is manufacturer)
car_data['manufacturer'] = car_data['model'].str.split().str[0].str.lower()

# Calculate ad counts per manufacturer
ad_counts = car_data['manufacturer'].value_counts()

# Streamlit app title
st.title("Vehicle Ads Dashboard")

# Section 1: Data Viewer
st.header("Data Viewer")
include_less_than_1000 = st.checkbox("Include manufacturers with less than 1000 ads")

# Filter data based on checkbox
if include_less_than_1000:
    filtered_data = car_data
else:
    manufacturers_with_1000_plus = ad_counts[ad_counts >= 1000].index
    filtered_data = car_data[car_data['manufacturer'].isin(manufacturers_with_1000_plus)]

# Display interactive table
st.dataframe(filtered_data, use_container_width=True)

# Section 2: Vehicle Types by Manufacturer
st.header("Vehicle Types by Manufacturer")
# Create a crosstab for types by manufacturer
type_by_manuf = pd.crosstab(car_data['manufacturer'], car_data['type'])
# Plot as stacked bar chart
fig_types = px.bar(type_by_manuf, barmode='stack', title="Vehicle Types by Manufacturer")
st.plotly_chart(fig_types, use_container_width=True)

# Section 3: Histogram of Condition vs Model Year
st.header("Histogram of Condition vs Model Year")
# Group by condition and model_year, count occurrences
condition_year_counts = car_data.groupby(['condition', 'model_year']).size().reset_index(name='count')
# Histogram (bar chart) of counts
fig_condition = px.bar(condition_year_counts, x='model_year', y='count', color='condition',
                       title="Condition vs Model Year", barmode='group')
st.plotly_chart(fig_condition, use_container_width=True)

# Section 4: Compare Price Distribution Between Manufacturers
st.header("Compare Price Distribution Between Manufacturers")
# Get unique manufacturers
unique_manufacturers = sorted(car_data['manufacturer'].unique())

# Select boxes for two manufacturers
col1, col2 = st.columns(2)
with col1:
    manuf1 = st.selectbox("Select Manufacturer 1", unique_manufacturers)
with col2:
    manuf2 = st.selectbox("Select Manufacturer 2", unique_manufacturers, index=1 if len(unique_manufacturers) > 1 else 0)

# Filter data for selected manufacturers
data_manuf1 = car_data[car_data['manufacturer'] == manuf1]
data_manuf2 = car_data[car_data['manufacturer'] == manuf2]

# Combine for plotting
combined_data = pd.concat([data_manuf1.assign(manufacturer=manuf1), data_manuf2.assign(manufacturer=manuf2)])

# Plot price distribution as histogram
if not combined_data.empty:
    # Define distinct colors for each manufacturer
    color_map = {
        manuf1: '#FF6347',  # Tomato red for manufacturer 1
        manuf2: '#4682B4'   # Steel blue for manufacturer 2
    }
    fig_price = px.histogram(
        combined_data,
        x='price',
        color='manufacturer',
        marginal='box',
        title=f"Price Distribution: {manuf1} vs {manuf2}",
        barmode='overlay',
        opacity=0.5,  # Reduced opacity for better overlap visibility
        color_discrete_map=color_map  # Assign custom colors
    )
    st.plotly_chart(fig_price, use_container_width=True)
else:
    st.write("No data available for the selected manufacturers.")

# Retain some of the original code for histogram and scatter if desired
st.header("Additional Visualizations")
hist_checkbox = st.checkbox("Exibir histograma de Odometer")
if hist_checkbox:
    fig_hist = px.histogram(car_data, x="odometer", title="Histogram of Odometer")
    st.plotly_chart(fig_hist, use_container_width=True)

scatter_checkbox = st.checkbox("Exibir gráfico de dispersão Odometer vs Price")
if scatter_checkbox:
    fig_scatter = px.scatter(car_data, x="odometer", y="price", title="Scatter Plot: Odometer vs Price")
    st.plotly_chart(fig_scatter, use_container_width=True)