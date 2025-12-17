import streamlit as st
import pandas as pd
import base64

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="⚽ FootyScope",
    page_icon="⚽",
    layout="wide"
)

# =============================
# BACKGROUND IMAGE
# =============================
def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.82);
            z-index: -1;
        }}

        section[data-testid="stSidebar"] {{
            background-color: #0f172a;
        }}

        h1, h2, h3, h4, h5, h6, p, label {{
            color: #f8fafc !important;
        }}

        div[data-testid="metric-container"] {{
            background-color: #020617;
            border: 1px solid #1e293b;
            border-radius: 16px;
            padding: 18px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background(
    "assets/HD-wallpaper-two-football-players-are-wearing-white-black-dress-football.jpg"
)

# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    return pd.read_csv("FIFA_final_dashboard (2).csv")

df = load_data()

# =============================
# HEADER
# =============================
st.markdown(
    """
    <h1 style='text-align:center; font-size:3.2rem;'>⚽ FootyScope</h1>
    <p style='text-align:center; color:#cbd5f5;'>
    Explore • Filter • Compare FIFA Player Performance
    </p>
    """,
    unsafe_allow_html=True
)

# =============================
# SEARCH BAR (TOP)
# =============================
st.markdown("### 🔍 Search Player")
name = st.text_input("Type player name")

if name:
    result = df[df["Name"].str.contains(name, case=False)]
    st.dataframe(result if not result.empty else pd.DataFrame())

st.divider()

# =============================
# SIDEBAR FILTERS
# =============================
st.sidebar.title("⚙️ Filters")

club = st.sidebar.selectbox(
    "Club", ["All"] + sorted(df["Club"].dropna().unique())
)

position = st.sidebar.selectbox(
    "Position", ["All"] + sorted(df["Position"].dropna().unique())
)

skill = st.sidebar.selectbox(
    "Skill Level", ["All"] + sorted(df["Skill_Level"].unique())
)

filtered_df = df.copy()

if club != "All":
    filtered_df = filtered_df[filtered_df["Club"] == club]

if position != "All":
    filtered_df = filtered_df[filtered_df["Position"] == position]

if skill != "All":
    filtered_df = filtered_df[filtered_df["Skill_Level"] == skill]

# =============================
# METRICS
# =============================
st.subheader("📊 Performance Overview")
c1, c2, c3 = st.columns(3)

c1.metric("Total Players", len(filtered_df))
c2.metric("Avg Overall", round(filtered_df["Overall"].mean(), 2))
c3.metric("Avg Value (£)", round(filtered_df["Value(£)"].mean(), 2))

# =============================
# DATA TABLE
# =============================
st.subheader("📋 Player Dataset")
st.dataframe(filtered_df, use_container_width=True)

# =============================
# CHARTS
# =============================
st.subheader("📈 Overall Rating Distribution")
st.bar_chart(filtered_df["Overall"])

if "Physical_Score" in filtered_df.columns:
    st.subheader("💪 Physical Score Distribution")
    st.bar_chart(filtered_df["Physical_Score"])

