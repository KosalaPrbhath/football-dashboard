import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("FIFA_final_dashboard.csv")

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
st.title("⚽ FIFA Player Stats Dashboard")
st.write("Analyze player performance and compare players easily.")

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

# -----------------------------
# PLAYER SEARCH
# -----------------------------
st.subheader("🔍 Search Player")
name = st.text_input("Enter player name")

if name:
    result = df[df['Name'].str.contains(name, case=False)]
    st.dataframe(result if len(result) > 0 else pd.DataFrame())
