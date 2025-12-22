import streamlit as st
import pandas as pd
import base64

st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- FULL BACKGROUND ---------- */
.stApp {
    background: linear-gradient(
        rgba(0,0,0,0.75),
        rgba(0,0,0,0.85)
    ),
    url("assets/HD-wallpaper-two-football-players-are-wearing-white-black-dress-football.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* ---------- TITLES WITH OUTLINE ---------- */
h1 {
    color: white;
    text-align: center;
    font-size: 3.2rem;
    -webkit-text-stroke: 2px black;
    text-shadow: 0px 6px 15px rgba(0,0,0,0.8);
}

h2, h3 {
    color: white;
    -webkit-text-stroke: 1.2px black;
    text-shadow: 0px 4px 10px rgba(0,0,0,0.7);
}

/* ---------- GLASS CARD ---------- */
.glass {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    margin-bottom: 25px;
}

/* ---------- METRIC STYLE ---------- */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.6);
}

/* ---------- SEARCH BAR ---------- */
input {
    border-radius: 14px !important;
    padding: 10px !important;
}

/* ---------- DATAFRAME ---------- */
.stDataFrame {
    background: rgba(0,0,0,0.55);
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

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
    "assets/wp8593981.jpg"
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
st.markdown("""
<div class="glass">
    <h1>⚽ FootyScope</h1>
    <h3 style="text-align:center;">
        Elite Football Analytics Dashboard
    </h3>
</div>
""", unsafe_allow_html=True)


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
    "Skill_Level", ["All"] + sorted(df["Skill_Level"].unique())
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
st.subheader("Performance Overview")
c1, c2, c3 = st.columns(3)

c1.metric("Total Players", len(filtered_df))
c2.metric("Avg Overall", round(filtered_df["Overall"].mean(), 2))
c3.metric("Avg Value (£)", round(filtered_df["Value(£)"].mean(), 2))

# =============================
# DATA TABLE
# =============================
st.subheader("Player Dataset")
st.dataframe(filtered_df, use_container_width=True)

# =============================
# CHARTS
# =============================
st.subheader("Overall Rating Distribution")
st.bar_chart(filtered_df["Overall"])

if "Physical_Score" in filtered_df.columns:
    st.subheader("Physical Score Distribution")
    st.bar_chart(filtered_df["Physical_Score"])

