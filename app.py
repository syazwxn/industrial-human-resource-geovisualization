import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("classified_by_sector.csv")

# Clean columns
df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
df.rename(columns={'india/states': 'state'}, inplace=True)

# Title
st.title("Industrial Human Resource Dashboard")
st.markdown("Visualizing workforce data across sectors, states, and gender")

# Sidebar filters
st.sidebar.header("Filter Options")
selected_state = st.sidebar.multiselect("Select State(s):", sorted(df['state'].unique()))
selected_sector = st.sidebar.multiselect("Select Sector(s):", sorted(df['sector'].unique()))

# Filter data based on selection
filtered_df = df.copy()
if selected_state:
    filtered_df = filtered_df[filtered_df['state'].isin(selected_state)]
if selected_sector:
    filtered_df = filtered_df[filtered_df['sector'].isin(selected_sector)]

# Gender Totals
filtered_df['total_male'] = (
    filtered_df['main_workers_-_total_-_males'] + 
    filtered_df['marginal_workers_-_total_-_males']
)
filtered_df['total_female'] = (
    filtered_df['main_workers_-_total_-_females'] + 
    filtered_df['marginal_workers_-_total_-_females']
)
filtered_df['total_workers'] = filtered_df['total_male'] + filtered_df['total_female']

# Sector distribution
sector_totals = filtered_df.groupby('sector')['total_workers'].sum().sort_values(ascending=False)
fig_sector = px.bar(
    sector_totals, 
    x=sector_totals.index, 
    y=sector_totals.values, 
    labels={'x': 'Sector', 'y': 'Total Workers'},
    title="Total Workers by Sector"
)
st.plotly_chart(fig_sector)

# Gender Pie Chart
gender_total = filtered_df[['total_male', 'total_female']].sum()
fig_gender = px.pie(
    names=['Male', 'Female'],
    values=gender_total.values,
    title="Overall Gender Distribution"
)
st.plotly_chart(fig_gender)

# Display filtered table
st.subheader("Filtered Data Table")
st.dataframe(filtered_df[['state', 'nic_name', 'sector', 'total_male', 'total_female', 'total_workers']].head(100))
