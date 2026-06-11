import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Config & Data Setup
st.set_page_config(page_title="Feminist Archive", layout="wide")

@st.cache_data
def load_data():
    # Load your final model CSV
    df = pd.read_csv("journals_model_final.csv")
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    return df

df = load_data()

# 2. Historical Context Engine
# Defining waves to educate while filtering
WAVES = {
    "Pre-Wave (1814–1847)": (1814, 1847, "Proto-feminist philosophers, early dissent."),
    "First Wave (1848–1928)": (1848, 1928, "Suffrage movement and foundational rights."),
    "Inter-Wave (1929–1962)": (1929, 1962, "Philosophical deepening, The Second Sex."),
    "Second Wave (1963–1989)": (1963, 1989, "The personal is political, intersectionality."),
    "Third Wave (1990–2011)": (1990, 2011, "Gender performativity, post-structuralism."),
    "Fourth Wave (2012–Present)": (2012, 2026, "Digital feminism, climate justice, #MeToo.")
}

# 3. Sidebar Interaction
st.sidebar.title("Explore the Archive")
wave_choice = st.sidebar.selectbox("Feminist Historical Waves", list(WAVES.keys()))
start_yr, end_yr, context = WAVES[wave_choice]

st.sidebar.info(context)
only_oa = st.sidebar.checkbox("Open Access Only")

# Apply Filter
filtered = df[(df['year'] >= start_yr) & (df['year'] <= end_yr)]
if only_oa:
    filtered = filtered[filtered['openaccess'] == 1]

# 4. Main Interface
st.title(f"📚 Feminist Literature: {wave_choice.split('(')[0]}")

# Metrics Row
m1, m2, m3 = st.columns(3)
m1.metric("Archive Size", len(filtered))
m2.metric("Open Access %", f"{(filtered['openaccess'].mean()*100):.1f}%")
m3.metric("Avg. Citations", f"{filtered['citations'].mean():.1f}")

# Visuals
# A treemap is the most "information-dense" way to visualize fields without clutter
fig_tree = px.treemap(filtered.dropna(subset=['main_field', 'title_category']), 
                     path=['main_field', 'title_category'], 
                     color='year', color_continuous_scale='RdPu')
fig_tree.update_layout(margin=dict(t=0, l=0, r=0, b=0))
st.plotly_chart(fig_tree, use_container_width=True)

# Results Table
st.subheader("Research Papers")
st.dataframe(filtered[['year', 'title', 'authors', 'openaccess', 'citations']], use_container_width=True)

# Community Link
st.markdown("---")
col1, col2 = st.columns([2, 1])
col1.write("Explore more at [The Feminist Park](https://www.feminist-park.org).")
col2.link_button("Listen to 'Un/Seen Spaces'", "https://open.spotify.com/show/1eBAcX8qxijrvAI6a90AyR?si=4ad0babaad5f4f0e ")