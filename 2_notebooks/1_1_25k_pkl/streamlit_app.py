import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(page_title="Feminist Literature Archive", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_and_prep_data():
    # Replace with your actual paths
    df = pd.read_csv("journals_model_final.csv") 
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    return df

df = load_and_prep_data()

# --- SIDEBAR: CONTEXTUAL FILTERS ---
st.sidebar.title("🔍 Explore the Archive")

# Feminist History Context
history_periods = {
    "The Progenitors (1814–1920)": (1814, 1920),
    "Second Wave (1960–1985)": (1960, 1985),
    "Intersectionality (1986–2010)": (1986, 2010),
    "Cyber & Digital (2011–2026)": (2011, 2026)
}

selected_period = st.sidebar.selectbox("Feminist Historical Eras", list(history_periods.keys()))
start_yr, end_yr = history_periods[selected_period]

st.sidebar.info(f"**Context:** Currently exploring the era of {selected_period.split('(')[0]}. This period focused on {'foundational suffrage' if 'Progenitors' in selected_period else 'digital equity and algorithmic justice'}.")

# Filters
year_range = st.sidebar.slider("Fine-tune Year Range", 1814, 2026, (start_yr, end_yr))
only_oa = st.sidebar.checkbox("Only Open Access Papers", value=False)

# --- FILTER LOGIC ---
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
if only_oa:
    filtered_df = filtered_df[filtered_df['openaccess'] == 1]

# --- MAIN UI ---
st.title("📚 Feminist Scientific Paper Recommender")
st.markdown("A living intellectual archive mapping the evolution of feminist discourse.")

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🌐 Topic Evolution", "📑 Search Results"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Papers in View", len(filtered_df))
        fig = px.histogram(filtered_df, x="year", nbins=50, title="Publication Trend", color_discrete_sequence=['#FF7F3E'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### About The Feminist Park")
        st.write("The Feminist Park is a transdisciplinary research initiative. We design for liberation by unseeing the constraints of traditional academic structures.")
        st.link_button("Listen to 'Un/Seen Spaces' Podcast", "https://open.spotify.com/show/1eBAcX8qxijrvAI6a90AyR?si=4ad0babaad5f4f0e ")

with tab2:
    st.subheader("Topic Distribution")
    # Using a Sunburst to represent hierarchical categorizations
    fig_sun = px.sunburst(filtered_df.dropna(subset=['main_field', 'title_category']), 
                          path=['main_field', 'title_category'], 
                          title="Intersectional Topic Hierarchy")
    st.plotly_chart(fig_sun, use_container_width=True)

with tab3:
    st.dataframe(filtered_df[['title', 'authors', 'year', 'openaccess']], use_container_width=True)
    
    with st.expander("💡 Suggest a Paper / Provide Feedback"):
        with st.form("feedback"):
            st.text_input("Paper Title")
            st.text_area("Why this should be included...")
            if st.form_submit_button("Submit"):
                st.success("Contribution logged.")

# --- FOOTER ---
st.divider()
st.caption("Feminist Literature Engine | Built for scholarly liberation.")