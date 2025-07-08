
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="🌍 Best Workation Cities", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("Dataset/workation_cleaned.csv")
    df["Sunshine per Day (hrs)"] = df["Sunshine Hours"] / 365
    df["Workation Score"] = df["WiFi Speed"] * 2 + df["Sunshine Hours"] - df["Rent"] * 0.01
    df["Total Cost"] = df["Meal Price"] + df["Rent"] / 30 + df["Coffee Price"] + df["Beer Price"] + df["Taxi Price"]
    df["Rent_inv"] = df["Rent"].max() - df["Rent"]
    from sklearn.preprocessing import MinMaxScaler
    features = ["WiFi Speed", "Coworking Spaces", "Rent_inv", "Sunshine per Day (hrs)", "Instagram Photos"]
    df["Composite Score"] = MinMaxScaler().fit_transform(df[features]).mean(axis=1)
    df["Continent"] = df["Country"].map({
        "Portugal": "Europe", "Spain": "Europe", "Thailand": "Asia", "India": "Asia",
        "Argentina": "South America", "Vietnam": "Asia", "Indonesia": "Asia",
        "Germany": "Europe", "USA": "North America", "Mexico": "North America",
        "Colombia": "South America", "Brazil": "South America", "France": "Europe"
    }).fillna("Other")
    return df

df = load_data()
filtered_df = df.copy()  # penting: definisikan sebelum digunakan

# Sekarang buat variabel turunan
all_countries = sorted(df["Country"].unique())
all_cities = sorted(df["City"].unique())

# === SIDEBAR ===
with st.sidebar:
    st.markdown("""
        <style>
            /* Ubah warna background sidebar */
            section[data-testid="stSidebar"] > div:first-child {
                background: linear-gradient(135deg, #1f2937, #111827);  /* Gradient abu gelap */
                padding: 20px;
                color: white;
            }

            /* Perhalus warna teks sidebar */
            .css-qbe2hs, .css-1cpxqw2, .css-1v0mbdj {
                color: #f3f4f6 !important;  /* Teks abu terang */
            }

            /* Style header sidebar */
            .sidebar-title {
                font-size: 24px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 5px;
            }

            .sidebar-subtext {
                font-size: 14px;
                color: #d1d5db;
                margin-bottom: 20px;
            }

            /* Atur garis batas antar bagian */
            .sidebar-section {
                border-bottom: 1px solid #374151;
                margin-bottom: 20px;
                padding-bottom: 10px;
            }
        </style>
        <div class="sidebar-title">🌴 Workation Explorer</div>
        <div class="sidebar-subtext">Find your perfect balance between work & travel 🌍</div>
    """, unsafe_allow_html=True)

    with st.expander("📍 Location Filter", expanded=True):
        selected_countries = st.multiselect("🌐 Countries:", ["All"] + all_countries, default=["All"])
        selected_city_only = st.selectbox("🏙️ Specific City (Optional):", ["All"] + all_cities)

    with st.expander("📶 Environment Preferences", expanded=True):
        wifi_range = st.slider("📡 WiFi Speed (Mbps):", float(df["WiFi Speed"].min()), float(df["WiFi Speed"].max()),
                               (float(df["WiFi Speed"].min()), float(df["WiFi Speed"].max())))
        rent_range = st.slider("🏠 Rent (USD):", int(df["Rent"].min()), int(df["Rent"].max()),
                               (int(df["Rent"].min()), int(df["Rent"].max())))
        sunshine_range = st.slider("🌞 Sunshine Hours:", int(df["Sunshine Hours"].min()), int(df["Sunshine Hours"].max()),
                                   (int(df["Sunshine Hours"].min()), int(df["Sunshine Hours"].max())))

    st.markdown("---")
    st.markdown("📥 **Download Your Selection**")
    if not filtered_df.empty:
        st.download_button(
            label="⬇️ Download CSV",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='filtered_workation_cities.csv',
            mime='text/csv'
        )

    st.markdown("📌 **Looking for recommendations?**")
    st.markdown("""
        <a href='#audience-section'>
            <button style='
                padding: 0.5rem 1rem;
                font-size: 14px;
                border: 1px solid rgba(250, 250, 250, 0.2);
                background-color: transparent;
                border-radius: 0.25rem;
                color: #FFFFFF;
                transition: background-color 0.3s, color 0.3s;
            ' onmouseover="this.style.backgroundColor='#FFFFFF'; this.style.color='#000000';"
            onmouseout="this.style.backgroundColor='transparent'; this.style.color='#FFFFFF';">
                Explore Now
            </button>
        </a>
    """, unsafe_allow_html=True)

# === Apply filters ===
if "All" not in selected_countries:
    filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
if selected_city_only != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city_only]
filtered_df = filtered_df[
    (filtered_df["WiFi Speed"].between(*wifi_range)) &
    (filtered_df["Rent"].between(*rent_range)) &
    (filtered_df["Sunshine Hours"].between(*sunshine_range))
]

# === HEADER & METRICS ===
st.title("🌍 Best Workation Cities Dashboard")

st.markdown("This dashboard helps you discover the world's best cities for combining work and leisure. Use the filters on the left to narrow down by country, internet speed, rent, and sunshine hours.")

with st.expander("ℹ️ About the Data & Scoring"):
    st.markdown(f"""
- **Workation Score** = `WiFi × 2 + Sunshine Hours − (Rent × 0.01)`
- **Composite Score** = Normalized mix of:
    - WiFi Speed  
    - Coworking Spaces  
    - Sunshine per Day  
    - Inverse Rent  
    - Instagram Popularity
- **Rent is divided by 30** to approximate daily cost.
- Dataset contains **{df['Country'].nunique()} countries** and **{len(df)} cities**.
    """)


col0, col1, col2, col3, col4 = st.columns(5)
col0.metric("🌐 Countries", filtered_df["Country"].nunique())
col1.metric("🏙️ Cities", len(filtered_df))
col2.metric("📶 Avg WiFi", f"{filtered_df['WiFi Speed'].mean():.1f} Mbps")
avg_rent = filtered_df['Rent'].mean()
rent_trend = "🟢 Low" if avg_rent < 500 else "🟡 Moderate" if avg_rent < 800 else "🔴 High"
col3.metric("💸 Avg Rent", f"${avg_rent:.0f}", rent_trend)
col4.metric("☀️ Avg Sunshine", f"{filtered_df['Sunshine Hours'].mean():.0f} hrs")

col5, col6, col7, col8, col9 = st.columns(5)
with col5:
    st.markdown("📥 Download Filtered Data")  
    if not filtered_df.empty:
        
        st.download_button(
            label="Download CSV",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='filtered_workation_cities.csv',
            mime='text/csv'
        )
        
with col6:
    st.markdown("📌 **Looking for recommendations?**")
    st.markdown("""
        <a href='#audience-section'>
            <button style='
                padding: 0.5rem 1rem;
                font-size: 14px;
                border: 1px solid rgba(250, 250, 250, 0.2);
                background-color: transparent;
                border-radius: 0.25rem;
                color: #FFFFFF;
                transition: background-color 0.3s, color 0.3s;
            ' onmouseover="this.style.backgroundColor='#FFFFFF'; this.style.color='#000000';"
            onmouseout="this.style.backgroundColor='transparent'; this.style.color='#FFFFFF';">
                Explore Now
            </button>
        </a>
    """, unsafe_allow_html=True)
    
st.markdown("---")
# === ROW 1 ===
c1, c2 = st.columns(2)
with c1:
    st.subheader("🏆 Best Workation Cities")
    top_score = filtered_df.sort_values("Workation Score", ascending=False).head(10)
    fig1 = px.bar(top_score, x="Workation Score", y="City", color="Country", orientation="h", hover_data=["WiFi Speed", "Rent"])
    fig1.update_yaxes(categoryorder="total ascending")
    st.caption(
        "Ranking of cities based on a combination of fast internet, plenty of sunshine, and lower apartment rental costs. "
        "A higher Workation Score means the city is more suitable for remote work."
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("🌍 Average Score by Continent")
    continent_avg = filtered_df.groupby("Continent")["Composite Score"].mean().reset_index()
    fig2 = px.pie(continent_avg, names="Continent", values="Composite Score", hole=0.4)
    st.caption("Average composite score of cities grouped by continent.")
    st.plotly_chart(fig2, use_container_width=True)

# === ROW 2 ===
c3, c4 = st.columns(2)
with c3:
    st.subheader("☀️ Sunniest Cities")
    sun_top = filtered_df.sort_values("Sunshine Hours", ascending=False).head(10)
    fig3 = px.treemap(sun_top, path=["Country", "City"], values="Sunshine Hours", color="Sunshine Hours", color_continuous_scale="YlOrRd")
    st.caption(
        "Cities with the most hours of sunshine per year. "
        "Ideal for those who prefer bright and sunny environments while working."
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("💰 Daily Cost Breakdown")
    st.caption(
        "This pie chart shows the estimated share of daily spending for the selected city. "
        "Rent costs are divided by 30 to approximate daily expenses."
    )
    city = st.selectbox("Select City:", filtered_df["City"].unique())
    cost_data = filtered_df[filtered_df["City"] == city].iloc[0]
    cost_items = {
        "Meal": cost_data["Meal Price"],
        "Coffee": cost_data["Coffee Price"],
        "Beer": cost_data["Beer Price"],
        "Taxi": cost_data["Taxi Price"],
        "Rent (Daily)": cost_data["Rent"] / 30
    }
    cost_df = pd.DataFrame(list(cost_items.items()), columns=["Expense", "Cost"])
    color_map = {
        "Meal": "#1f77b4",
        "Coffee": "#ff7f0e",
        "Beer": "#2ca02c",
        "Taxi": "#d62728",
        "Rent (Daily)": "#9467bd",
    }
    fig4 = px.pie(cost_df, names="Expense", values="Cost", hole=0.4,
                color="Expense", color_discrete_map=color_map)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown(f"**Total Estimated Daily Cost in {city}:** ${sum(cost_items.values()):.2f}")


# === ROW 3 ===
c5, c6 = st.columns(2)
with c5:
    st.subheader("📊 Composite Score Viewer")
    st.caption(
    "The Composite Score combines normalized values of WiFi speed, coworking spaces, sunshine per day, inverse rent cost, and Instagram popularity. "
    "Higher scores indicate an overall better destination for a balanced workation experience."
)
    view_mode = st.radio("View Mode:", ["Top Cities", "By Country Average"], horizontal=True, 
        index=1 )
    if view_mode == "Top Cities":
        top_cities = filtered_df.sort_values("Composite Score", ascending=False).head(10)
        fig5 = px.bar(top_cities, x="Composite Score", y="City", color="Country", orientation="h")
        fig5.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        avg_by_country = filtered_df.groupby("Country")["Composite Score"].mean().reset_index()
        fig5 = px.choropleth(avg_by_country, locations="Country", locationmode="country names",
                             color="Composite Score", color_continuous_scale="Oranges")
        st.plotly_chart(fig5, use_container_width=True)

with c6:
    st.subheader("🔍 Explore Other Insights")
    st.markdown("<div id='insight-section'></div>", unsafe_allow_html=True)
    insight_option = st.selectbox("Select Insight:", [
        "📸 Most Instagrammed Cities",
        "🏢 Avg Coworking Spaces per Country",
        "💳 Daily Expense Breakdown (Top 5 Cities)",
        "⚠️ Worst Cities (Low Workation Score)"
    ])

    if insight_option == "📸 Most Instagrammed Cities":
        top_ig = filtered_df.sort_values("Instagram Photos", ascending=True).head(10)
        fig = px.bar(top_ig, x="Instagram Photos", y="City", color="Country", orientation="h")
        st.caption("Top cities with the highest number of Instagram photos, reflecting social media popularity.")
        st.plotly_chart(fig, use_container_width=True)

    elif insight_option == "🏢 Avg Coworking Spaces per Country":
        avg_cowork = filtered_df.groupby("Country")["Coworking Spaces"].mean().reset_index()
        fig = px.bar(avg_cowork.sort_values("Coworking Spaces", ascending=True),
                     x="Coworking Spaces", y="Country", orientation="h",
                     color="Coworking Spaces", color_continuous_scale="Blues")
        st.caption("Average number of coworking spaces per country to assess digital nomad infrastructure.")
        st.plotly_chart(fig, use_container_width=True)

    elif insight_option == "💳 Daily Expense Breakdown (Top 5 Cities)":
            top5 = filtered_df.sort_values("Workation Score", ascending=False).head(5).copy()
            top5["Rent (Daily)"] = top5["Rent"] / 30

            # Buat kolom dengan label konsisten
            top5["Meal"] = top5["Meal Price"]
            top5["Coffee"] = top5["Coffee Price"]
            top5["Beer"] = top5["Beer Price"]
            top5["Taxi"] = top5["Taxi Price"]

            cost_cols = ["Meal", "Rent (Daily)", "Coffee", "Beer", "Taxi"]

            # Melt untuk visualisasi
            melted = top5[["City"] + cost_cols].melt(id_vars="City", var_name="Expense", value_name="Cost")

            # Warna konsisten
            color_map = {
                "Meal": "#1f77b4",
                "Coffee": "#ff7f0e",
                "Beer": "#2ca02c",
                "Taxi": "#d62728",
                "Rent (Daily)": "#9467bd",
            }

            fig = px.bar(melted, x="City", y="Cost", color="Expense", barmode="group",
                            color_discrete_map=color_map)
            st.caption("Comparison of estimated **daily** living costs across top 5 cities with the highest Workation Score.")
            st.plotly_chart(fig, use_container_width=True)


    elif insight_option == "⚠️ Worst Cities (Low Workation Score)":
        worst = filtered_df.sort_values("Workation Score").head(10)
        fig = px.bar(worst, x="Workation Score", y="City", color="Country", orientation="h")
        fig.update_yaxes(categoryorder="total descending")
        st.caption("These cities have the lowest Workation Scores due to a combination of low WiFi, high rent, or poor weather conditions.")
        st.plotly_chart(fig, use_container_width=True)

# === TABS FOR USER SEGMENTS ===
st.markdown("---")
st.markdown("<div id='audience-section'></div>", unsafe_allow_html=True)
st.subheader("👥 Explore recommendations based on different traveler profiles")
tab1, tab2, tab3 = st.tabs(["💼 Remote Workers", "💸 Budget Travelers", "📸 Social Explorers"])

with tab1:
    st.subheader("Top Cities for Remote Workers")
    df_remote = filtered_df.copy()
    df_remote["Remote Score"] = df_remote["WiFi Speed"] * 2 + df_remote["Coworking Spaces"]
    top_remote = df_remote.sort_values("Remote Score", ascending=False).head(10)
    fig = px.bar(top_remote, x="Remote Score", y="City", color="Country", orientation="h")
    fig.update_yaxes(categoryorder="total ascending")
    st.caption("Top cities with high internet speed and coworking availability, ideal for remote workers.")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Top Cities for Budget Travelers")
    top_budget = filtered_df.sort_values("Total Cost").head(10)
    fig = px.bar(top_budget, x="Total Cost", y="City", color="Country", orientation="h")
    fig.update_yaxes(categoryorder="total descending")
    st.caption("Most affordable cities based on total daily living cost, great for budget-conscious travelers.")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Top Cities for Social Media Lovers")
    df_social = filtered_df.copy()
    df_social["Social Score"] = df_social["Instagram Photos"] * 0.7 + df_social["Things To Do"] * 10
    top_social = df_social.sort_values("Social Score", ascending=False).head(10)
    fig = px.bar(top_social, x="Social Score", y="City", color="Country", orientation="h")
    fig.update_yaxes(categoryorder="total ascending")
    st.caption("Top cities with strong social appeal, based on Instagram activity and number of attractions.")
    st.plotly_chart(fig, use_container_width=True)


# === MAP ===
st.subheader("🗺️ World Map of Workation Cities")
st.caption("This map shows city locations by country with bubble sizes based on Composite Score.")
fig_map = px.scatter_geo(filtered_df, locations="Country", locationmode="country names",
                         hover_name="City", size="Composite Score", color="Composite Score",
                         projection="natural earth", template="plotly", title="Workation City Map")
fig_map.update_layout(geo=dict(showframe=False, showcoastlines=True))
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.markdown("📊 **Data source:** Kaggle *The Best Cities for a Workation*")

