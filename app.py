import streamlit as st
import pandas as pd

st.set_page_config(page_title="FIFA Player Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("FIFA_with_features.csv")

df = load_data()

st.title("⚽ FIFA Player Performance Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

club = st.sidebar.selectbox(
    "Select Club",
    ["All"] + sorted(df["Club"].dropna().unique().tolist())
)

position = st.sidebar.selectbox(
    "Select Position",
    ["All"] + sorted(df["Position"].dropna().unique().tolist())
)


filtered_df = df.copy()
if club != "All":
    filtered_df = filtered_df[filtered_df["Club"] == club]
if position != "All":
    filtered_df = filtered_df[filtered_df["Position"] == position]

# Metrics
c1, c2, = st.columns(2)
c1.metric("Total Players", len(filtered_df))
c2.metric("Average Overall", round(filtered_df["Overall"].mean(), 2))

# Table
st.subheader("Player Data")
st.dataframe(filtered_df)

# Charts
st.subheader("Overall Rating Distribution")
st.bar_chart(filtered_df["Overall"])

# Search
st.subheader("Search Player")
name = st.text_input("Enter player name")
if name:
    st.dataframe(df[df["Name"].str.contains(name, case=False)])

