# 🏭 Industrial Human Resource Geo-Visualization

This project visualizes and analyzes India's industrial workforce distribution using data science and NLP techniques. It categorizes detailed industry classifications (`nic_name`) into broad sectors and presents insights in an interactive Streamlit dashboard.

---

## 📌 Problem Statement

In India, understanding the classification of main and marginal workers (excluding cultivators and agricultural laborers) is critical for employment planning and policy making. However, the available data is outdated and fragmented. This project aims to:

- Merge and preprocess industrial workforce data
- Classify industry types into broader economic sectors
- Perform exploratory data analysis
- Build an interactive dashboard for visualization

---

## 🛠 Tools & Technologies

- **Python**, **Pandas**, **NumPy**
- **Natural Language Processing (NLP)** for sector classification
- **Matplotlib**, **Plotly**, **Seaborn** for visualization
- **Streamlit** for interactive dashboard
- **scikit-learn** for optional ML/NLP
- **Git** for version control

---

## 🧠 Project Workflow

### 1. Data Preprocessing
- Multiple CSVs merged into a single dataframe
- Null values cleaned, column names standardized
- Gender and worker type aggregates computed

### 2. NLP Classification
- `nic_name` column preprocessed (lowercase, stripped)
- Custom keyword-based classifier maps jobs into sectors like:
  - **Agriculture**
  - **Manufacturing**
  - **Retail**
  - **Healthcare**
  - **IT / Services**, etc.

### 3. Exploratory Data Analysis (EDA)
- Gender-wise and sector-wise aggregation
- State-level comparisons
- Worker type distributions

### 4. Dashboard (Streamlit)
- Sidebar filters: `State`, `Sector`
- Visuals:
  - Bar chart (Workers by Sector)
  - Pie chart (Gender distribution)
  - Data table with filtered results

---

## 🚀 How to Run

### 1. Clone this repo
```powershell
     cd industrial-human-resource-geovisualization
**Then run this **
```powershell
     streamlit run app.py


