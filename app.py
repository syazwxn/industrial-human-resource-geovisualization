import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Industrial Human Resource Dashboard", layout="wide")

# -------------------------------
# 🔹 Load Data
# -------------------------------
df = pd.read_csv("classified_by_sector.csv")

# Clean columns
df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
df.rename(columns={'india/states': 'state'}, inplace=True)

# Clean nic_name
df['nic_name'] = df['nic_name'].str.strip().str.lower()

# -------------------------------
# 🔹 Train ML Model
# -------------------------------
@st.cache_resource
def train_model():
    X_raw = df['nic_name']
    y = df['sector']
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    X = vectorizer.fit_transform(X_raw)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model, vectorizer

model, vectorizer = train_model()

# -------------------------------
# 🔹 Title
# -------------------------------
st.title("🧠 Industrial Human Resource Geo-Visualization Dashboard")
st.markdown("Visualizing workforce data across sectors, states, gender, rural/urban, with ML prediction support.")

# -------------------------------
# 🔍 Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filter Options")
selected_state = st.sidebar.multiselect("Select State(s):", sorted(df['state'].unique()))
selected_sector = st.sidebar.multiselect("Select Sector(s):", sorted(df['sector'].unique()))

# Filter data based on sidebar selection
filtered_df = df.copy()
if selected_state:
    filtered_df = filtered_df[filtered_df['state'].isin(selected_state)]
if selected_sector:
    filtered_df = filtered_df[filtered_df['sector'].isin(selected_sector)]

# Add new calculated columns
filtered_df['total_rural'] = (
    filtered_df['main_workers_-_rural_-__persons'] +
    filtered_df['marginal_workers_-_rural_-__persons']
)
filtered_df['total_urban'] = (
    filtered_df['main_workers_-_urban_-__persons'] +
    filtered_df['marginal_workers_-_urban_-__persons']
)
filtered_df['total_male'] = (
    filtered_df['main_workers_-_total_-_males'] +
    filtered_df['marginal_workers_-_total_-_males']
)
filtered_df['total_female'] = (
    filtered_df['main_workers_-_total_-_females'] +
    filtered_df['marginal_workers_-_total_-_females']
)
filtered_df['total_workers'] = filtered_df['total_male'] + filtered_df['total_female']

# -------------------------------
# 🧩 Tabs Layout (4 tabs)
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Insights", "🔎 Search NIC", "🧠 Predict Sector", "📥 Download Data"])

# -------------------------------
# 📊 Tab 1: Insights
# -------------------------------
with tab1:
    st.header("📊 Insights on Industrial Workforce")

    # Rural vs Urban Bar Chart
    rural_urban_summary = filtered_df.groupby('sector')[['total_rural', 'total_urban']].sum().reset_index()

    fig_rural_urban = go.Figure([
        go.Bar(name="Rural", x=rural_urban_summary['sector'], y=rural_urban_summary['total_rural']),
        go.Bar(name="Urban", x=rural_urban_summary['sector'], y=rural_urban_summary['total_urban'])
    ])
    fig_rural_urban.update_layout(title="👥 Rural vs Urban Workforce by Sector", barmode='group')
    st.plotly_chart(fig_rural_urban, use_container_width=True)

    # Total Workers by Sector Bar Chart
    sector_totals = filtered_df.groupby('sector')['total_workers'].sum().sort_values(ascending=False)
    fig_sector = px.bar(
        sector_totals,
        x=sector_totals.index,
        y=sector_totals.values,
        labels={'x': 'Sector', 'y': 'Total Workers'},
        title="🏭 Total Workers by Sector"
    )
    st.plotly_chart(fig_sector, use_container_width=True)

    # Gender Distribution Pie Chart
    gender_total = filtered_df[['total_male', 'total_female']].sum()
    fig_gender = px.pie(
        names=['Male', 'Female'],
        values=gender_total.values,
        title="🧑‍🤝‍🧑 Overall Gender Distribution"
    )
    st.plotly_chart(fig_gender, use_container_width=True)

    # Top 10 States by Total Workforce
    top_states = filtered_df.groupby('state')['total_workers'].sum().sort_values(ascending=False).head(10)
    fig_top_states = px.bar(
        top_states,
        x=top_states.values,
        y=top_states.index,
        orientation='h',
        title="🏆 Top 10 States by Total Workforce",
        labels={'x': 'Total Workers', 'y': 'State'}
    )
    st.plotly_chart(fig_top_states, use_container_width=True)

# -------------------------------
# 🔎 Tab 2: NIC Search (Contains search)
# -------------------------------
with tab2:
    st.header("🔎 Search NIC Descriptions (Contains)")

    keyword = st.text_input("Type any word to search NIC description:")

    if keyword:
        matches = filtered_df[filtered_df['nic_name'].str.contains(keyword.lower(), na=False)]
        st.write(f"🧾 Found {matches.shape[0]} NIC descriptions containing **'{keyword}'**")
        st.dataframe(matches[['state', 'nic_name', 'sector']].drop_duplicates().head(100))
    else:
        st.info("Type a word to search NIC descriptions.")

# -------------------------------
# 🧠 Tab 3: Predict Sector
# -------------------------------
with tab3:
    st.header("🧠 Predict Sector from NIC Description")

    user_input = st.text_input("✏️ Enter NIC/Industry Description:")

    if user_input:
        vec = vectorizer.transform([user_input.lower()])
        pred = model.predict(vec)[0]
        st.success(f"🔮 Predicted Sector: **{pred}**")

# -------------------------------
# 📥 Tab 4: Download Data
# -------------------------------
with tab4:
    st.header("📥 Download Filtered Workforce Data")

    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(filtered_df)

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name='filtered_industrial_workforce.csv',
        mime='text/csv'
    )

    st.subheader("📋 View Filtered Data Table")
    st.dataframe(filtered_df[['state', 'nic_name', 'sector', 'total_male', 'total_female', 'total_rural', 'total_urban', 'total_workers']].head(100))
