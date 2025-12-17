import streamlit as st
import pandas as pd
import base64

# ---------------- BACKGROUND IMAGE ----------------
def set_background("assets/HD-wallpaper-two-football-players-are-wearing-white-black-dress-football.jpg"):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <h1 style='text-align:center; font-weight:800;'>⚽ FootyScope</h1>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Dark overlay */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.78);
            z-index: -1;
        }}

        /* Sidebar dark */
        section[data-testid="stSidebar"] {{
            background-color: #0e0e0e;
        }}

        h1, h2, h3, h4, h5, h6, p {{
            color: white;
        }}
        <p style='text-align:center; font-size:18px; color:#bbbbbb;'>Advanced FIFA Player Performance Analytics</p>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("FIFA_final_dashboard (2).csv")

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("⚽ Player Filters")

clubs = ["All"] + sorted(df['Club'].dropna().unique().tolist())
club_select = st.sidebar.selectbox("Club", clubs)

positions = ["All"] + sorted(df['Position'].dropna().unique().tolist())
position_select = st.sidebar.selectbox("Position", positions)

skills = ["All"] + sorted(df['Skill_Level'].unique().tolist())
skill_select = st.sidebar.selectbox("Skill Level", skills)

# Apply filters
filtered_df = df.copy()
if club_select != "All":
    filtered_df = filtered_df[filtered_df["Club"] == club_select]

if position_select != "All":
    filtered_df = filtered_df[filtered_df["Position"] == position_select]

if skill_select != "All":
    filtered_df = filtered_df[filtered_df["Skill_Level"] == skill_select]

# -----------------------------
# MAIN TITLE
# -----------------------------
st.title("⚽ FootyScope")
st.write("Analyze player performance and compare players easily.")

# PLAYER SEARCH
# -----------------------------
name = st.text_input("Enter player name")

if name:
    result = df[df['Name'].str.contains(name, case=False)]
    st.dataframe(result if len(result) > 0 else pd.DataFrame())

# -----------------------------
# METRIC CARDS
# -----------------------------
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Total Players", len(filtered_df))
col2.metric("Avg Overall", round(filtered_df["Overall"].mean(), 2))
col3.metric("Avg Value", round(filtered_df["Value(£)"].mean(), 2))

# -----------------------------
# SHOW TABLE
# -----------------------------
st.subheader("📋 Player Data")
st.dataframe(filtered_df)

# -----------------------------
# VISUALS
# -----------------------------
st.subheader("📈 Overall Rating Distribution")
st.bar_chart(filtered_df["Overall"])

st.subheader("💪 Physical Score Distribution")
st.bar_chart(filtered_df["Physical_Score"])


    
