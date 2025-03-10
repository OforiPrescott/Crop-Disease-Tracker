import streamlit as st
import pandas as pd
import sqlalchemy as sa
import folium
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(page_title="Crop Disease Tracker", layout="wide", initial_sidebar_state="expanded")

# Theme toggle in sidebar
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"], index=0)

# Custom CSS for styling and responsiveness
st.markdown("""
    <style>
    .main { max-width: 1200px; margin: 0 auto; padding: 10px; }
    .stTitle { font-family: 'Arial', sans-serif; margin-top: 10px; }
    h2 { font-family: 'Arial', sans-serif; }
    .stForm { padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 5px; }
    @media (max-width: 768px) {
        .stTitle { font-size: 24px; }
        .stColumn { width: 100% !important; margin-bottom: 20px; }
    }
    </style>
""", unsafe_allow_html=True)

# Theme-specific CSS
if theme == "Dark":
    st.markdown("""
        <style>
        body { background-color: #1E1E1E; color: #E0E0E0; }
        .stTitle { color: #4CAF50; }
        h2 { color: #66BB6A; }
        .css-1d391kg { background-color: #2D2D2D; }
        .stForm { background-color: #333333; }
        .stButton>button { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body { background-color: #FFFFFF; color: #212121; }
        .stTitle { color: #2E7D32; }
        h2 { color: #388E3C; }
        .css-1d391kg { background-color: #F1F8E9; }
        .stForm { background-color: #E8F5E9; }
        .stButton>button { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Database connection with fallback
try:
    engine = sa.create_engine('mssql+pyodbc://@PresHacks/AgriDiseaseDB?driver=SQL+Server&trusted_connection=yes')
    st.write("Connected to SQL Server")
except Exception as e:
    st.warning("SQL Server connection failed. Using mock data for demo.")
    # Mock data
    farms_df = pd.DataFrame({
        "farm_id": [1, 2, 3],
        "farm_name": ["Farm_1", "Farm_2", "Farm_3"],
        "latitude": [41.0, 41.1, 41.2],
        "longitude": [-99.0, -98.9, -98.8]
    })
    disease_df = pd.DataFrame({
        "report_id": [1, 2, 3],
        "farm_id": [1, 2, 3],
        "crop_id": [1, 2, 3],
        "disease_name": ["Blight", "Rust", "Mildew"],
        "report_date": pd.to_datetime(["2024-03-01", "2024-03-02", "2024-03-03"]),
        "severity": [5, 7, 3],
        "description": ["Yellow spots", "Wilting", "Gray patches"],
        "latitude": [41.0, 41.1, 41.2],
        "longitude": [-99.0, -98.9, -98.8],
        "crop_type": ["Wheat", "Corn", "Soybean"]
    })
else:
    # Load data from SQL Server
    @st.cache_data(ttl=300)
    def load_data():
        farms_df = pd.read_sql("SELECT * FROM Farms", engine)
        disease_df = pd.read_sql("""
            SELECT d.*, f.latitude, f.longitude, c.crop_type 
            FROM DiseaseReports d
            JOIN Farms f ON d.farm_id = f.farm_id
            JOIN Crops c ON d.crop_id = c.crop_id
        """, engine)
        disease_df["report_date"] = pd.to_datetime(disease_df["report_date"])
        return farms_df, disease_df

    farms_df, disease_df = load_data()

# Header with logo and title
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("gi-kace logo.jpg", width=150, caption="GI-KACE")
with col_title:
    st.title("AI-Powered Crop Disease Tracker")
    st.markdown("Visualize and report crop diseases across farms in real-time.")

# Sidebar filters
st.sidebar.header("Filters")
disease_options = ["All"] + sorted(disease_df["disease_name"].unique().tolist())
selected_disease = st.sidebar.selectbox("Disease", disease_options)
date_range = st.sidebar.date_input("Date Range", 
                                   [disease_df["report_date"].min(), disease_df["report_date"].max()],
                                   min_value=disease_df["report_date"].min(),
                                   max_value=disease_df["report_date"].max())

# Filter data
filtered_df = disease_df.copy()
if selected_disease != "All":
    filtered_df = filtered_df[filtered_df["disease_name"] == selected_disease]
filtered_df = filtered_df[
    (filtered_df["report_date"] >= pd.to_datetime(date_range[0])) &
    (filtered_df["report_date"] <= pd.to_datetime(date_range[1]))
]

# Main content
with st.container():
    col1, col2 = st.columns([2, 1], gap="medium")
    with col1:
        st.subheader("Disease Map")
        m = folium.Map(location=[41.0, -99.0], zoom_start=6, 
                       tiles="CartoDB Positron" if theme == "Light" else "CartoDB Dark Matter")
        for _, row in filtered_df.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=row["severity"] * 2,
                popup=f"{row['crop_type']} - {row['disease_name']} (Severity: {row['severity']})",
                color="red" if row["severity"] > 5 else "orange",
                fill=True,
                fill_opacity=0.7
            ).add_to(m)
        st_folium(m, width=None, height=400, returned_objects=[])
    with col2:
        st.subheader("Severity Trend")
        trend_data = filtered_df.groupby("report_date")["severity"].mean().reset_index()
        fig = px.line(trend_data, x="report_date", y="severity", 
                      title="Average Severity Over Time",
                      labels={"report_date": "Date", "severity": "Avg Severity"},
                      color_discrete_sequence=["#4CAF50" if theme == "Light" else "#81C784"])
        fig.update_layout(
            height=400, 
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#FFFFFF" if theme == "Light" else "#1E1E1E",
            plot_bgcolor="#FFFFFF" if theme == "Light" else "#1E1E1E",
            font_color="#212121" if theme == "Light" else "#E0E0E0"
        )
        st.plotly_chart(fig, use_container_width=True)

# Report Form (disabled for demo if using mock data)
st.subheader("Submit Disease Report")
if 'engine' in globals():
    with st.form("report_form"):
        farm_id = st.selectbox("Farm", farms_df["farm_id"].tolist())
        crops_df = pd.read_sql(f"SELECT crop_id, crop_type FROM Crops WHERE farm_id = {farm_id}", engine)
        crop_id = st.selectbox("Crop", crops_df["crop_id"].tolist(),
                               format_func=lambda x: crops_df[crops_df["crop_id"] == x]["crop_type"].values[0])
        disease_name = st.text_input("Disease Name", max_chars=50)
        severity = st.slider("Severity", 1, 10, 5)
        description = st.text_area("Description", max_chars=255)
        submitted = st.form_submit_button("Submit")
        if submitted:
            with engine.connect() as conn:
                conn.execute(sa.text("""
                    INSERT INTO DiseaseReports (farm_id, crop_id, disease_name, report_date, severity, description)
                    VALUES (:farm_id, :crop_id, :disease_name, :report_date, :severity, :description)
                """), {
                    "farm_id": farm_id, "crop_id": crop_id, "disease_name": disease_name,
                    "report_date": datetime.now(), "severity": severity, "description": description
                })
                conn.commit()
            st.success("Report submitted successfully!")
            st.cache_data.clear()
else:
    st.info("Reporting disabled in demo mode with mock data.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & SQL Server | Data refreshes every 5 minutes")