import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Logistics Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
}

.dashboard-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 25px;
}

.kpi-card {
    background-color: white;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.kpi-title {
    font-size: 14px;
    color: #6b7280;
}

.kpi-value {
    font-size: 27px;
    font-weight: 700;
    margin-top: 5px;
}

.section-title {
    font-size: 22px;
    font-weight: 650;
    margin-top: 25px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = "Nassau_Candy_Final_Analytical_Dataset_Corrected.xlsx"
FILE_PATH = BASE_DIR / FILE_NAME

@st.cache_data
  def load_data():
      try:
          if not FILE_PATH.exists():
              st.error(f"Excel file not found: {FILE_PATH}")
              return None

          excel_file = pd.ExcelFile(FILE_PATH)
          st.write("Available sheets:", excel_file.sheet_names)

          df = pd.read_excel(
              FILE_PATH,
              sheet_name="Cleaned_Data"
          )

          return df

      except Exception as e:
          st.error(f"Excel loading error: {e}")
          return None

    # Convert dates
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )

    # Calculate Shipping Lead Time
    df["Shipping Lead Time"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    # Remove invalid lead times
    df = df[
        df["Shipping Lead Time"].notna()
    ]

    df = df[
        df["Shipping Lead Time"] >= 0
    ]

    # Factory mapping
    factory_mapping = {

        "Wonka Bar - Nutty Crunch Surprise":
            "Lot's O' Nuts",

        "Wonka Bar - Fudge Mallows":
            "Lot's O' Nuts",

        "Wonka Bar -Scrumdiddlyumptious":
            "Lot's O' Nuts",

        "Wonka Bar - Milk Chocolate":
            "Wicked Choccy's",

        "Wonka Bar - Triple Dazzle Caramel":
            "Wicked Choccy's",

        "Laffy Taffy":
            "Sugar Shack",

        "SweeTARTS":
            "Sugar Shack",

        "Nerds":
            "Sugar Shack",

        "Fun Dip":
            "Sugar Shack",

        "Fizzy Lifting Drinks":
            "Sugar Shack",

        "Everlasting Gobstopper":
            "Secret Factory",

        "Hair Toffee":
            "The Other Factory",

        "Lickable Wallpaper":
            "Secret Factory",

        "Wonka Gum":
            "Secret Factory",

        "Kazookles":
            "The Other Factory"
    }

    if "Factory" not in df.columns:

        df["Factory"] = df["Product Name"].map(
            factory_mapping
        )

    return df


try:

    df = load_data()

except Exception as e:

    st.error(
        "Unable to load the Excel dataset."
    )

    st.info(
       "Make sure Nassau_Candy_Final_Analytical_Dataset_Corrected.xlsx "
       "is in the same folder as app.py."
) 

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '🚚 Nassau Candy Logistics Performance Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Data-driven analysis of shipping routes, geographic bottlenecks, '
    'factory performance and shipping modes'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")

# Date filter

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region filter

regions = sorted(
    df["Region"].dropna().unique()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

# State filter

states = sorted(
    df["State/Province"].dropna().unique()
)

selected_states = st.sidebar.multiselect(
    "State",
    states
)

# Factory filter

factories = sorted(
    df["Factory"].dropna().unique()
)

selected_factories = st.sidebar.multiselect(
    "Factory",
    factories
)

# Ship mode filter

ship_modes = sorted(
    df["Ship Mode"].dropna().unique()
)

selected_ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    ship_modes,
    default=ship_modes
)

# Lead-time threshold

max_lead = int(
    min(
        max(df["Shipping Lead Time"].max(), 1),
        5000
    )
)

default_threshold = min(
    1200,
    max_lead
)

lead_threshold = st.sidebar.slider(
    "Delay Threshold (Days)",
    min_value=0,
    max_value=max_lead,
    value=default_threshold,
    step=1
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

# Date filter

if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date)
        &
        (filtered_df["Order Date"] <= end_date)
    ]


# Region filter

if selected_regions:  

    filtered_df = filtered_df[
        filtered_df["Region"].isin(
            selected_regions
        )
    ]


# State filter

if selected_states:

    filtered_df = filtered_df[
        filtered_df["State/Province"].isin(
            selected_states
        )
    ]


# Factory filter

if selected_factories:

    filtered_df = filtered_df[
        filtered_df["Factory"].isin(
            selected_factories
        )
    ]


# Ship mode filter

if selected_ship_modes:

    filtered_df = filtered_df[
        filtered_df["Ship Mode"].isin(
            selected_ship_modes
        )
    ]


# Delay flag

filtered_df["Delayed"] = (
    filtered_df["Shipping Lead Time"]
    > lead_threshold
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 Logistics Performance Overview'
    '</div>',
    unsafe_allow_html=True
)

total_shipments = len(
    filtered_df
)

avg_lead_time = (
    filtered_df["Shipping Lead Time"].mean()
    if total_shipments > 0
    else 0
)

delay_rate = (
    filtered_df["Delayed"].mean() * 100
    if total_shipments > 0
    else 0
)

unique_routes = (
    filtered_df["Route"].nunique()
    if "Route" in filtered_df.columns
    else 0
)

avg_cost = (
    filtered_df["Cost"].mean()
    if total_shipments > 0
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "Total Shipments",
        f"{total_shipments:,}"
    )

with col2:

    st.metric(
        "Average Lead Time",
        f"{avg_lead_time:.1f} days"
    )

with col3:

    st.metric(
        "Delay Frequency",
        f"{delay_rate:.1f}%"
    )

with col4:

    st.metric(
        "Routes",
        f"{unique_routes:,}"
    )

with col5:

    st.metric(
        "Average Cost",
        f"${avg_cost:,.2f}"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🚚 Route Efficiency",
        "🗺️ Geographic Analysis",
        "🚢 Ship Mode Analysis",
        "🔎 Route Drill-Down"
    ]
)


# ============================================================
# TAB 1 — ROUTE EFFICIENCY
# ============================================================

with tab1:

    st.subheader(
        "Route Efficiency Overview"
    )

    if len(filtered_df) == 0:

        st.warning(
            "No data available for the selected filters."
        )

    else:

        route_group = (
            filtered_df
            .groupby(
                [
                    "Factory",
                    "Region",
                    "State/Province"
                ],
                as_index=False
            )
            .agg(
                Total_Shipments=(
                    "Order ID",
                    "count"
                ),

                Average_Lead_Time=(
                    "Shipping Lead Time",
                    "mean"
                ),

                Median_Lead_Time=(
                    "Shipping Lead Time",
                    "median"
                ),

                Lead_Time_Variability=(
                    "Shipping Lead Time",
                    "std"
                ),

                Delayed_Shipments=(
                    "Delayed",
                    "sum"
                )
            )
        )

        route_group[
            "Lead_Time_Variability"
        ] = route_group[
            "Lead_Time_Variability"
        ].fillna(0)

        route_group[
            "Delay_Frequency_%"
        ] = (
            route_group["Delayed_Shipments"]
            /
            route_group["Total_Shipments"]
            * 100
        )

        route_group["Route"] = (
            route_group["Factory"]
            + " → "
            + route_group["State/Province"]
        )

        # Efficiency score

        min_time = route_group[
            "Average_Lead_Time"
        ].min()

        max_time = route_group[
            "Average_Lead_Time"
        ].max()

        if max_time == min_time:

            route_group[
                "Route_Efficiency_Score"
            ] = 100

        else:

            route_group[
                "Route_Efficiency_Score"
            ] = (
                (
                    max_time
                    -
                    route_group[
                        "Average_Lead_Time"
                    ]
                )
                /
                (
                    max_time
                    -
                    min_time
                )
                * 100
            )

        # ----------------------------------------------------
        # TOP AND BOTTOM ROUTES
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        top_routes = (
            route_group
            .sort_values(
                "Average_Lead_Time"
            )
            .head(10)
        )

        bottom_routes = (
            route_group
            .sort_values(
                "Average_Lead_Time",
                ascending=False
            )
            .head(10)
        )

        with col1:

            st.markdown(
                "### 🏆 Top 10 Most Efficient Routes"
            )

            fig_top = px.bar(
                top_routes.sort_values(
                    "Average_Lead_Time",
                    ascending=True
                ),
                x="Average_Lead_Time",
                y="Route",
                orientation="h",
                text="Average_Lead_Time",
                labels={
                    "Average_Lead_Time":
                    "Average Lead Time (Days)"
                }
            )

            fig_top.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside"
            )

            fig_top.update_layout(
                height=500
            )

            st.plotly_chart(
                fig_top,
                use_container_width=True
            )

        with col2:

            st.markdown(
                "### ⚠️ Bottom 10 Least Efficient Routes"
            )

            fig_bottom = px.bar(
                bottom_routes,
                x="Average_Lead_Time",
                y="Route",
                orientation="h",
                text="Average_Lead_Time",
                labels={
                    "Average_Lead_Time":
                    "Average Lead Time (Days)"
                }
            )

            fig_bottom.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside"
            )

            fig_bottom.update_layout(
                height=500
            )

            st.plotly_chart(
                fig_bottom,
                use_container_width=True
            )


        # ----------------------------------------------------
        # ROUTE TABLE
        # ----------------------------------------------------

        st.markdown(
            "### 📋 Route Performance Leaderboard"
        )

        display_routes = route_group[
            [
                "Route",
                "Total_Shipments",
                "Average_Lead_Time",
                "Median_Lead_Time",
                "Lead_Time_Variability",
                "Delay_Frequency_%",
                "Route_Efficiency_Score"
            ]
        ].sort_values(
            "Average_Lead_Time"
        )

        st.dataframe(
            display_routes.style.format(
                {
                    "Average_Lead_Time":
                        "{:.2f}",

                    "Median_Lead_Time":
                        "{:.2f}",

                    "Lead_Time_Variability":
                        "{:.2f}",

                    "Delay_Frequency_%":
                        "{:.2f}%",

                    "Route_Efficiency_Score":
                        "{:.1f}"
                }
            ),
            use_container_width=True,
            height=450
        )


# ============================================================
# TAB 2 — GEOGRAPHIC ANALYSIS
# ============================================================

with tab2:

    st.subheader(
        "🗺️ Geographic Shipping Performance"
    )

    if len(filtered_df) == 0:

        st.warning(
            "No data available."
        )

    else:

        state_group = (
            filtered_df
            .groupby(
                "State/Province",
                as_index=False
            )
            .agg(
                Total_Shipments=(
                    "Order ID",
                    "count"
                ),

                Average_Lead_Time=(
                    "Shipping Lead Time",
                    "mean"
                ),

                Median_Lead_Time=(
                    "Shipping Lead Time",
                    "median"
                ),

                Delayed_Shipments=(
                    "Delayed",
                    "sum"
                )
            )
        )

        state_group[
            "Delay_Frequency_%"
        ] = (
            state_group[
                "Delayed_Shipments"
            ]
            /
            state_group[
                "Total_Shipments"
            ]
            * 100
        )

        # ----------------------------------------------------
        # STATE MAP
        # ----------------------------------------------------

        st.markdown(
            "### 🇺🇸 Average Shipping Lead Time by State"
        )

        # State name conversion

        state_abbreviations = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY"
        }

        state_group["State_Code"] = (
            state_group[
                "State/Province"
            ]
            .map(state_abbreviations)
        )

        map_data = state_group.dropna(
            subset=["State_Code"]
        )

        if len(map_data) > 0:

            fig_map = px.choropleth(
                map_data,
                locations="State_Code",
                locationmode="USA-states",
                color="Average_Lead_Time",
                scope="usa",
                hover_name="State/Province",
                hover_data={
                    "Total_Shipments": True,
                    "Average_Lead_Time": ":.1f",
                    "Delay_Frequency_%": ":.1f",
                    "State_Code": False
                },
                labels={
                    "Average_Lead_Time":
                        "Avg Lead Time"
                }
            )

            fig_map.update_layout(
                height=600
            )

            st.plotly_chart(
                fig_map,
                use_container_width=True
            )

        else:

            st.info(
                "The state names in the dataset could not "
                "be matched to standard US state names."
            )


        # ----------------------------------------------------
        # BOTTLENECK ANALYSIS
        # ----------------------------------------------------

        st.markdown(
            "### 🚨 Geographic Bottleneck Analysis"
        )

        median_volume = state_group[
            "Total_Shipments"
        ].median()

        median_lead = state_group[
            "Average_Lead_Time"
        ].median()

        bottlenecks = state_group[
            (
                state_group[
                    "Total_Shipments"
                ] >= median_volume
            )
            &
            (
                state_group[
                    "Average_Lead_Time"
                ] >= median_lead
            )
        ].sort_values(
            "Average_Lead_Time",
            ascending=False
        )

        if len(bottlenecks) > 0:

            st.dataframe(
                bottlenecks.style.format(
                    {
                        "Average_Lead_Time":
                            "{:.2f}",

                        "Median_Lead_Time":
                            "{:.2f}",

                        "Delay_Frequency_%":
                            "{:.2f}%"
                    }
                ),
                use_container_width=True
            )

        else:

            st.success(
                "No high-volume/high-lead-time bottleneck "
                "states detected for the current filters."
            )


# ============================================================
# TAB 3 — SHIP MODE ANALYSIS
# ============================================================

with tab3:

    st.subheader(
        "🚢 Ship Mode Performance Analysis"
    )

    if len(filtered_df) == 0:

        st.warning(
            "No data available."
        )

    else:

        mode_group = (
            filtered_df
            .groupby(
                "Ship Mode",
                as_index=False
            )
            .agg(
                Total_Shipments=(
                    "Order ID",
                    "count"
                ),

                Average_Lead_Time=(
                    "Shipping Lead Time",
                    "mean"
                ),

                Median_Lead_Time=(
                    "Shipping Lead Time",
                    "median"
                ),

                Lead_Time_Variability=(
                    "Shipping Lead Time",
                    "std"
                ),

                Delayed_Shipments=(
                    "Delayed",
                    "sum"
                ),

                Average_Cost=(
                    "Cost",
                    "mean"
                ),

                Average_Sales=(
                    "Sales",
                    "mean"
                ),

                Average_Gross_Profit=(
                    "Gross Profit",
                    "mean"
                )
            )
        )

        mode_group[
            "Delay_Frequency_%"
        ] = (
            mode_group[
                "Delayed_Shipments"
            ]
            /
            mode_group[
                "Total_Shipments"
            ]
            * 100
        )

        mode_group[
            "Lead_Time_Variability"
        ] = mode_group[
            "Lead_Time_Variability"
        ].fillna(0)


        # ----------------------------------------------------
        # CHARTS
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### ⏱️ Average Lead Time by Ship Mode"
            )

            fig_mode_time = px.bar(
                mode_group,
                x="Ship Mode",
                y="Average_Lead_Time",
                text="Average_Lead_Time",
                labels={
                    "Average_Lead_Time":
                    "Average Lead Time (Days)"
                }
            )

            fig_mode_time.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside"
            )

            fig_mode_time.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_mode_time,
                use_container_width=True
            )


        with col2:

            st.markdown(
                "### 🚨 Delay Frequency by Ship Mode"
            )

            fig_delay = px.bar(
                mode_group,
                x="Ship Mode",
                y="Delay_Frequency_%",
                text="Delay_Frequency_%",
                labels={
                    "Delay_Frequency_%":
                    "Delay Frequency (%)"
                }
            )

            fig_delay.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside"
            )

            fig_delay.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_delay,
                use_container_width=True
            )


        # ----------------------------------------------------
        # COST VS LEAD TIME
        # ----------------------------------------------------

        st.markdown(
            "### 💰 Cost vs Shipping Time"
        )

        fig_cost = px.scatter(
            mode_group,
            x="Average_Lead_Time",
            y="Average_Cost",
            size="Total_Shipments",
            color="Ship Mode",
            hover_data=[
                "Delay_Frequency_%",
                "Average_Gross_Profit"
            ],
            labels={
                "Average_Lead_Time":
                    "Average Lead Time (Days)",

                "Average_Cost":
                    "Average Cost"
            }
        )

        fig_cost.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_cost,
            use_container_width=True
        )


        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        st.markdown(
            "### 📋 Ship Mode Performance Table"
        )

        st.dataframe(
            mode_group.style.format(
                {
                    "Average_Lead_Time":
                        "{:.2f}",

                    "Median_Lead_Time":
                        "{:.2f}",

                    "Lead_Time_Variability":
                        "{:.2f}",

                    "Delay_Frequency_%":
                        "{:.2f}%",

                    "Average_Cost":
                        "${:,.2f}",

                    "Average_Sales":
                        "${:,.2f}",

                    "Average_Gross_Profit":
                        "${:,.2f}"
                }
            ),
            use_container_width=True
        )


# ============================================================
# TAB 4 — ROUTE DRILL-DOWN
# ============================================================

with tab4:

    st.subheader(
        "🔎 Route Drill-Down Analysis"
    )

    # Factory selector

    drill_factories = sorted(
        filtered_df[
            "Factory"
        ].dropna().unique()
    )

    if len(drill_factories) == 0:

        st.warning(
            "No factories available."
        )

    else:

        selected_drill_factory = st.selectbox(
            "Select Factory",
            drill_factories
        )

        drill_df = filtered_df[
            filtered_df[
                "Factory"
            ] == selected_drill_factory
        ].copy()


        # State selector

        drill_states = sorted(
            drill_df[
                "State/Province"
            ].dropna().unique()
        )

        if len(drill_states) > 0:

            selected_drill_state = st.selectbox(
                "Select Customer State",
                ["All"] + drill_states
            )

            if selected_drill_state != "All":

                drill_df = drill_df[
                    drill_df[
                        "State/Province"
                    ] == selected_drill_state
                ]


        # Ship mode selector

        drill_modes = sorted(
            drill_df[
                "Ship Mode"
            ].dropna().unique()
        )

        if len(drill_modes) > 0:

            selected_drill_mode = st.selectbox(
                "Select Ship Mode",
                ["All"] + drill_modes
            )

            if selected_drill_mode != "All":

                drill_df = drill_df[
                    drill_df[
                        "Ship Mode"
                    ] == selected_drill_mode
                ]


        # ----------------------------------------------------
        # DRILL-DOWN KPIs
        # ----------------------------------------------------

        if len(drill_df) > 0:

            drill_shipments = len(
                drill_df
            )

            drill_avg = drill_df[
                "Shipping Lead Time"
            ].mean()

            drill_median = drill_df[
                "Shipping Lead Time"
            ].median()

            drill_delay = (
                drill_df["Delayed"].mean()
                * 100
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Shipments",
                    f"{drill_shipments:,}"
                )

            with col2:

                st.metric(
                    "Avg Lead Time",
                    f"{drill_avg:.1f} days"
                )

            with col3:

                st.metric(
                    "Median Lead Time",
                    f"{drill_median:.1f} days"
                )

            with col4:

                st.metric(
                    "Delay Frequency",
                    f"{drill_delay:.1f}%"
                )


            # ------------------------------------------------
            # LEAD TIME DISTRIBUTION
            # ------------------------------------------------

            st.markdown(
                "### 📈 Shipment Lead-Time Distribution"
            )

            fig_hist = px.histogram(
                drill_df,
                x="Shipping Lead Time",
                nbins=30,
                labels={
                    "Shipping Lead Time":
                    "Shipping Lead Time (Days)"
                }
            )

            fig_hist.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_hist,
                use_container_width=True
            )


            # ------------------------------------------------
            # ORDER LEVEL DETAILS
            # ------------------------------------------------

            st.markdown(
                "### 📦 Order-Level Shipment Details"
            )

            available_columns = [

                "Order ID",
                "Order Date",
                "Ship Date",
                "Ship Mode",
                "Customer ID",
                "State/Province",
                "Region",
                "Product Name",
                "Factory",
                "Shipping Lead Time",
                "Sales",
                "Cost",
                "Gross Profit"

            ]

            existing_columns = [
                c for c in available_columns
                if c in drill_df.columns
            ]

            order_details = drill_df[
                existing_columns
            ].sort_values(
                "Shipping Lead Time",
                ascending=False
            )

            st.dataframe(
                order_details,
                use_container_width=True,
                height=500
            )

        else:

            st.warning(
                "No orders match the selected route."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Nassau Candy Logistics Performance Dashboard | "
    "Built with Python, Pandas, Plotly and Streamlit"
)
