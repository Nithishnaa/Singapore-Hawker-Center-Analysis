"""
SINGAPORE HAWKER CENTRE ANALYTICS — Step 3: Streamlit Dashboard
================================================================
HOW TO RUN:
    pip install streamlit plotly pandas folium streamlit-folium
    streamlit run 03_streamlit_app.py

DEPLOY:
    Push to GitHub → share.streamlit.io → live in 2 mins

INTERVIEW TALKING POINT:
"The dashboard has three views — an executive overview for senior stakeholders,
an interactive Singapore map showing every hawker centre colour-coded by
accessibility, and a deep-dive explorer for analysts. I deliberately designed
it so a non-technical audience like an urban planner or policy maker could
draw insights without any data background."
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="SG Hawker Centre Analytics",
    page_icon="🍜",
    layout="wide"
)

ACCENT   = "#B85C38"
RED      = "#D94F3D"
GREEN    = "#2E8B57"
BLUE     = "#2C6FAC"

st.markdown("""
<style>
    .kpi-card {
        background: #fdf8f5;
        border-left: 5px solid #B85C38;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .kpi-card h2 { margin: 0; color: #B85C38; font-size: 1.9rem; }
    .kpi-card p  { margin: 4px 0 0 0; color: #555; font-size: 0.85rem; }
    .insight-box {
        background: #f0f7f0;
        border-left: 4px solid #2E8B57;
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 0.88rem;
        color: #1a4a2a;
    }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("hawker_centres.csv")
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/noodles.png", width=55)
st.sidebar.title("🇸🇬 SG Hawker Analytics")
st.sidebar.markdown(f"**{len(df)} hawker centres · {df['no_of_food_stalls'].sum():,} food stalls**")
st.sidebar.divider()

page = st.sidebar.radio("Navigate", [
    "📊 Executive Overview",
    "🗺️ Singapore Map",
    "🔍 Deep Dive Explorer",
    "📍 Find Nearest Hawker"
])

region_filter = st.sidebar.multiselect(
    "Filter by Region",
    options=sorted(df['region'].unique()),
    default=sorted(df['region'].unique())
)
df_filtered = df[df['region'].isin(region_filter)]


# ════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "📊 Executive Overview":
    st.title("🍜 Singapore Hawker Centre Analytics")
    st.markdown("*Analysing Singapore's hawker culture through data — locations, accessibility, and regional distribution.*")
    st.caption("📡 Data source: data.gov.sg (Hawker Centres Dataset) + OneMap Singapore API")
    st.divider()

    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""<div class="kpi-card"><h2>{len(df_filtered)}</h2>
            <p>Hawker Centres</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-card"><h2>{df_filtered['no_of_food_stalls'].sum():,}</h2>
            <p>Food Stalls</p></div>""", unsafe_allow_html=True)
    with col3:
        walkable = df_filtered['mrt_walkable'].mean()
        st.markdown(f"""<div class="kpi-card"><h2>{walkable:.0%}</h2>
            <p>Within 500m of MRT</p></div>""", unsafe_allow_html=True)
    with col4:
        avg_acc = df_filtered['accessibility_score'].mean()
        st.markdown(f"""<div class="kpi-card"><h2>{avg_acc:.1f}/10</h2>
            <p>Avg Accessibility Score</p></div>""", unsafe_allow_html=True)
    with col5:
        avg_dist = df_filtered['nearest_mrt_km'].mean()
        st.markdown(f"""<div class="kpi-card"><h2>{avg_dist:.2f}km</h2>
            <p>Avg Distance to MRT</p></div>""", unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Food Stalls by Region")
        region_data = df_filtered.groupby('region').agg(
            Centres=('hawker_name','count'),
            Food_Stalls=('no_of_food_stalls','sum'),
            Avg_Accessibility=('accessibility_score','mean')
        ).reset_index().sort_values('Food_Stalls', ascending=True)

        fig = px.bar(region_data, x='Food_Stalls', y='region', orientation='h',
                     color='Avg_Accessibility', color_continuous_scale=['#E8C4B0','#B85C38'],
                     text='Food_Stalls', title="Total Food Stalls by Region")
        fig.update_traces(textposition='outside')
        fig.update_layout(plot_bgcolor='white', coloraxis_colorbar_title="Accessibility")
        fig.update_xaxes(gridcolor='#eee')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div class="insight-box">
            💡 <b>Insight:</b> Central Singapore has the most stalls and best accessibility.
            The North has fewer centres and lower accessibility — a potential gap for urban planners.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.subheader("Hawker Centre Size Distribution")
        size_counts = df_filtered['size_category'].value_counts().reset_index()
        size_counts.columns = ['Size', 'Count']
        fig2 = px.pie(size_counts, values='Count', names='Size',
                      color_discrete_sequence=['#B85C38','#D4896A','#E8C4B0','#F5E6DC'],
                      title="Distribution by Size Category")
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""<div class="insight-box">
            💡 <b>Insight:</b> Most hawker centres are Small or Medium sized,
            serving neighbourhood catchments. Only a handful are Mega centres (80+ stalls).
        </div>""", unsafe_allow_html=True)

    st.subheader("Top 15 Largest Hawker Centres")
    top15 = df_filtered.nlargest(15, 'no_of_food_stalls')[
        ['hawker_name','region','no_of_food_stalls','nearest_mrt_station',
         'nearest_mrt_km','accessibility_score','popularity_score']
    ].reset_index(drop=True)
    top15.index += 1
    top15.columns = ['Name','Region','Food Stalls','Nearest MRT','MRT Dist (km)','Accessibility','Popularity']
    st.dataframe(top15.style.background_gradient(subset=['Food Stalls'], cmap='Oranges')
                            .background_gradient(subset=['Accessibility'], cmap='Greens'),
                 use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 2 — SINGAPORE MAP
# ════════════════════════════════════════════════════════════
elif page == "🗺️ Singapore Map":
    st.title("🗺️ Singapore Hawker Centre Map")
    st.markdown("*Every hawker centre plotted by location, sized by stall count, coloured by accessibility.*")
    st.divider()

    color_by = st.radio("Colour markers by:", [
        "Accessibility Score", "Number of Food Stalls", "Region", "Popularity Score"
    ], horizontal=True)

    col_map = {
        "Accessibility Score": "accessibility_score",
        "Number of Food Stalls": "no_of_food_stalls",
        "Region": "region",
        "Popularity Score": "popularity_score"
    }
    col = col_map[color_by]
    is_categorical = col == 'region'

    fig = px.scatter_mapbox(
        df_filtered,
        lat="latitude", lon="longitude",
        size="no_of_food_stalls",
        color=col,
        color_continuous_scale="Oranges" if not is_categorical else None,
        color_discrete_sequence=px.colors.qualitative.Set2 if is_categorical else None,
        hover_name="hawker_name",
        hover_data={
            "region": True,
            "no_of_food_stalls": True,
            "nearest_mrt_station": True,
            "nearest_mrt_km": ":.2f",
            "accessibility_score": ":.1f",
            "popularity_score": ":.1f",
            "latitude": False, "longitude": False
        },
        zoom=10.8,
        center={"lat": 1.3521, "lon": 103.8198},
        mapbox_style="carto-positron",
        height=580,
        title=f"Singapore Hawker Centres — coloured by {color_by}"
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Most Accessible", df_filtered.loc[df_filtered['accessibility_score'].idxmax(), 'hawker_name'])
    with col2:
        st.metric("Least Accessible", df_filtered.loc[df_filtered['accessibility_score'].idxmin(), 'hawker_name'])
    with col3:
        st.metric("Largest Centre", df_filtered.loc[df_filtered['no_of_food_stalls'].idxmax(), 'hawker_name'])


# ════════════════════════════════════════════════════════════
# PAGE 3 — DEEP DIVE
# ════════════════════════════════════════════════════════════
elif page == "🔍 Deep Dive Explorer":
    st.title("🔍 Deep Dive Explorer")
    st.markdown("*Explore correlations and patterns across all hawker centres.*")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Accessibility vs Stall Count")
        fig = px.scatter(df_filtered,
                         x='nearest_mrt_km', y='no_of_food_stalls',
                         color='region', size='total_stalls',
                         hover_name='hawker_name',
                         labels={'nearest_mrt_km': 'Distance to MRT (km)',
                                 'no_of_food_stalls': 'Number of Food Stalls'},
                         title="MRT Distance vs Food Stall Count")
        fig.add_vline(x=0.5, line_dash="dash", line_color="gray",
                      annotation_text="500m walkable threshold")
        fig.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div class="insight-box">
            💡 Larger centres tend to cluster near MRT stations — confirming deliberate
            urban planning. Outliers (large + far from MRT) are worth investigating
            as potential improvement targets.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.subheader("Accessibility Score Distribution by Region")
        fig2 = px.box(df_filtered, x='region', y='accessibility_score',
                      color='region',
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      title="Accessibility Score Spread by Region")
        fig2.update_layout(plot_bgcolor='white', showlegend=False)
        fig2.update_yaxes(gridcolor='#eee')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""<div class="insight-box">
            💡 Central has the tightest distribution — consistently high accessibility.
            North shows the widest spread — some centres are well-connected,
            others are quite remote.
        </div>""", unsafe_allow_html=True)

    st.subheader("Correlation Heatmap — Hawker Centre Features")
    num_cols = ['no_of_food_stalls', 'no_of_mkt_produce_stalls',
                'total_stalls', 'nearest_mrt_km', 'accessibility_score', 'popularity_score']
    corr = df_filtered[num_cols].corr().round(2)
    fig3 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                     title="Feature Correlation Matrix", aspect="auto")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""<div class="insight-box">
        💡 Strong negative correlation between <b>nearest_mrt_km</b> and <b>accessibility_score</b>
        (expected — confirms our scoring logic). Moderate positive correlation between
        <b>total_stalls</b> and <b>popularity_score</b> — bigger centres attract more footfall.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 4 — NEAREST HAWKER FINDER
# ════════════════════════════════════════════════════════════
elif page == "📍 Find Nearest Hawker":
    st.title("📍 Find Nearest Hawker Centre")
    st.markdown("*Enter your location coordinates to find the closest hawker centres.*")
    st.divider()

    st.info("💡 To get your coordinates: Google Maps → long press your location → copy the numbers shown")

    col1, col2 = st.columns(2)
    with col1:
        user_lat = st.number_input("Your Latitude", value=1.3521, format="%.4f", step=0.001)
    with col2:
        user_lon = st.number_input("Your Longitude", value=103.8198, format="%.4f", step=0.001)

    n_results = st.slider("Show nearest N hawker centres", 3, 15, 5)

    if st.button("🔍 Find Nearest Hawker Centres", type="primary"):
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
            a = np.sin((lat2-lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2-lon1)/2)**2
            return R * 2 * np.arcsin(np.sqrt(a))

        df['dist_from_user'] = df.apply(
            lambda r: haversine(user_lat, user_lon, r['latitude'], r['longitude']), axis=1
        )
        nearest = df.nsmallest(n_results, 'dist_from_user')[
            ['hawker_name','region','no_of_food_stalls','dist_from_user',
             'nearest_mrt_station','accessibility_score','popularity_score']
        ].reset_index(drop=True)
        nearest.index += 1
        nearest['dist_from_user'] = nearest['dist_from_user'].round(3).astype(str) + ' km'
        nearest.columns = ['Name','Region','Food Stalls','Distance from You',
                           'Nearest MRT','Accessibility','Popularity']

        st.success(f"✅ Found {n_results} nearest hawker centres to your location")
        st.dataframe(nearest, use_container_width=True)

        # Mini map
        map_df = df.nsmallest(n_results, 'dist_from_user')
        user_point = pd.DataFrame([{
            'latitude': user_lat, 'longitude': user_lon,
            'hawker_name': '📍 Your Location', 'no_of_food_stalls': 5,
            'region': '', 'accessibility_score': 0, 'popularity_score': 0
        }])
        map_combined = pd.concat([map_df, user_point], ignore_index=True)

        fig = px.scatter_mapbox(
            map_combined, lat='latitude', lon='longitude',
            hover_name='hawker_name', size='no_of_food_stalls',
            color='hawker_name',
            zoom=13, mapbox_style='carto-positron', height=400
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
