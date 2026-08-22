# 🚚 Nassau Candy Logistics Dashboard

An interactive **Streamlit-based logistics analytics dashboard** for
analyzing shipping performance, route efficiency, geographic patterns,
and ship mode performance.

## 📊 Project Overview

This project provides visibility into:

-   Efficient and inefficient factory-to-customer routes
-   Shipping lead times across U.S. states
-   Shipping performance by region and ship mode
-   Delay frequency using a configurable delay threshold
-   Factory-to-customer route performance through interactive drill-down

## 🎯 Project Objectives

1.  Analyze overall shipping performance.
2.  Identify the Top 10 most efficient routes.
3.  Identify the Bottom 10 least efficient routes.
4.  Compare average shipping lead time by U.S. state.
5.  Compare performance across shipping modes.
6.  Analyze delay frequency using a configurable threshold.
7.  Provide factory, customer-state, and ship-mode drill-down analysis.
8.  Enable interactive filtering by date, region, state, factory, and
    ship mode.

## 🖥️ Dashboard Sections

### 🚚 Route Efficiency

Includes:

-   Top 10 Most Efficient Routes
-   Bottom 10 Least Efficient Routes
-   Route-level average shipping lead time
-   Factory-to-customer route comparison

### 🗺️ Geographic Analysis

Includes:

-   Average Shipping Lead Time by State
-   Interactive U.S. map
-   State-level shipment information
-   Average lead time
-   Delay frequency

Users can hover over states to inspect detailed information.

### 🚢 Ship Mode Analysis

The dashboard compares:

-   First Class
-   Same Day
-   Second Class
-   Standard Class

Visualizations include:

-   Average Lead Time by Ship Mode
-   Delay Frequency by Ship Mode
-   Cost vs Shipping Time

### 🔎 Route Drill-Down

Users can select:

-   Factory
-   Customer State
-   Ship Mode

The dashboard then displays:

-   Shipments
-   Average Lead Time
-   Median Lead Time
-   Delay Frequency
-   Shipment Lead-Time Distribution

## 🎛️ Interactive Filters

-   Order Date Range
-   Region
-   State
-   Factory
-   Ship Mode
-   Delay Threshold (Days)

The delay threshold controls the lead-time threshold used for
delay-frequency analysis.

## 📈 Key KPIs

-   Total Shipments
-   Average Lead Time
-   Delay Frequency
-   Number of Routes
-   Average Cost

## 🛠️ Technologies Used

-   Python
-   Pandas
-   Plotly Express
-   Plotly Graph Objects
-   Streamlit

## 📂 Project Structure

``` text
Nassau-Candy-Logistics-Dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── Nassu_Candy_Final_Analytical_Dataset
└── screenshots/
    ├── route_efficiency.png
    ├── geographic_analysis.png
    ├── ship_mode_analysis.png
    └── route_drilldown.png
```

> Replace `dataset.csv` with your actual dataset filename if it is
> different.

## ⚙️ Installation & Usage

### 1. Clone the repository

``` bash
git clone https://github.com/sakshidhumane/Nassau-Candy-Logistics-Dashboard.git
```

### 2. Open the project folder

``` bash
cd Nassau-Candy-Logistics-Dashboard
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Run the dashboard

``` bash
streamlit run app.py
```

The dashboard will normally open at:

``` text
http://localhost:8501
```

## 🔍 Analysis Workflow

``` text
Raw Shipping Data
       ↓
Data Preparation
       ↓
Interactive Filters
       ↓
KPI Calculation
       ↓
Route Efficiency Analysis
       ↓
Geographic Analysis
       ↓
Ship Mode Analysis
       ↓
Route Drill-Down
       ↓
Logistics Insights
```

## 💡 Insights Supported by the Dashboard

The dashboard can be used to identify:

-   Routes with lower and higher average lead times
-   States with relatively higher shipping lead times
-   Differences between shipping modes
-   Ship modes with higher delay frequency
-   Factory-to-state combinations requiring investigation
-   Potential logistics bottlenecks

Exact results depend on the selected filters and underlying data.

## 🧪 Dashboard Testing

The application was tested for:

-   ✅ Route Efficiency
-   ✅ Geographic Analysis
-   ✅ Ship Mode Analysis
-   ✅ Route Drill-Down
-   ✅ Date filtering
-   ✅ Region filtering
-   ✅ State filtering
-   ✅ Factory filtering
-   ✅ Ship Mode filtering
-   ✅ Delay Threshold slider
-   ✅ Interactive charts
-   ✅ Factory/State/Ship Mode drill-down

## 🚀 Future Enhancements

-   Monthly and yearly shipping trends
-   Automated anomaly detection
-   Route-level recommendations
-   Predictive delay analysis
-   Expanded cost optimization analysis
-   Online deployment

## 👩‍💻 Author

**Sakshi Dhumane**

Data Analytics \| Python \| SQL \| Power BI \| Excel \| Streamlit

## ⭐ Skills Demonstrated

-   Data Analysis
-   Exploratory Data Analysis
-   Data Visualization
-   Interactive Dashboard Development
-   KPI Analysis
-   Logistics Analytics
-   Python
-   Pandas
-   Plotly
-   Streamlit
