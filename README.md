# GatiPredict: India Logistics Performance Diagnostics and Risk Engine

GatiPredict is an end-to-end data analytics and predictive diagnostics framework built to track carrier SLA compliance, identify supply chain bottlenecks, and forecast transit risks across multi-regional Indian transport corridors.

Utilizing a dataset of 25,000 shipment profiles, this project integrates a robust SQL relational data staging layer with a machine learning classification engine to convert raw freight records into actionable, data-driven operational insights.

---

## Core System Architecture

* **Relational Warehousing Layer (`src/data_pipeline.py`)**: Cleans timestamp representations into explicit numeric indicators and stages records into an optimized analytical schema.
* **SQL Diagnostic Workspace (`database/`)**: Computes complex multi-tier matrices to isolate localized performance gaps across major 3PL providers (including Delhivery, Blue Dart, XpressBees, Shadowfax, DHL, FedEx, Ekart, and Ecom Express).
* **Predictive Risk Engine (`src/train.py`)**: Employs an optimized multi-tree Ensemble Classifier to predict shipment delays before deployment, evaluating real-world factors like weather anomalies, distance, payload mass, and route types.

---

## Repository Structure

```text
GatiPredict-India-Logistics/
│
├── data/
│   ├── raw/                  # Directory for the raw Delivery_Logistics.csv file
│   └── processed/            # Holds delivery_logistics_cleaned.csv after pipeline run
│
├── database/
│   ├── schema.sql            # Core SQL Data Warehouse Staging definitions
│   └── analytical_queries.sql# Advanced SQL performance matrix and KPI queries
│
├── src/
│   ├── __init__.py
│   ├── data_pipeline.py      # Cleans time metrics and handles SQLite ETL
│   ├── feature_engineering.py# Maps logistics risk indicators to ML arrays
│   ├── train.py              # Fits the Random Forest model and prints diagnostic scores
│   └── visualize.py          # Programmatic multi-pane Seaborn chart script
│
├── notebooks/                # Production-ready visual reports (.png exports)
│   ├── carrier_sla_breach_rate.png
│   ├── weather_delay_impact.png
│   └── bottleneck_feature_importance.png
│
├── requirements.txt          # Explicit package version lock file
└── README.md                 # Project configuration and summary documentation

```

---

## Step-by-Step Local Deployment

### 1. Initialize Environment and Dependencies

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/GatiPredict-India-Logistics.git
cd GatiPredict-India-Logistics
pip install -r requirements.txt

```

### 2. Stage the Data Source

Ensure your raw data file is named exactly `Delivery_Logistics.csv` and placed in the root directory.

### 3. Run Ingestion and SQL Analytics

Execute the database initialization pipeline to clean raw records, apply standard DDL schemas, migrate logs to SQLite (`logistics_warehouse.db`), and execute diagnostic validation queries:

```bash
python src/data_pipeline.py

```

### 4. Execute Feature Engineering and Machine Learning

Run the training module to extract predictive weight arrays and evaluate overall validation accuracy. This process outputs the `delivery_logistics_cleaned.csv` file:

```bash
python src/train.py

```

### 5. Generate Production Visualizations

Produce and save high-resolution analytical charts to the workspace:

```bash
python src/visualize.py

```

---

## Key Diagnostic and Performance Insights

### 1. Carrier Service Reliability Matrix (SQL)

Relational queries mapping cross-regional performance reveal specific bottleneck clusters. For example, within the central economic corridor:

* **Xpressbees** and **Amazon Logistics** exhibited the highest vulnerabilities, with SLA breach rates peaking at **29.35%** and **28.23%** respectively.
* **Delhivery** maintained an optimized service ceiling, keeping its breach rate to a low of **24.75%** under identical conditions.

### 2. Environmental Degradation Impact

Analyzing severe weather disruptions proves that atmospheric hurdles create major delivery friction across the highway network:

* **Stormy Conditions:** Leads system-wide risk profiles with an SLA breach rate of **41.42%**.
* **Rainy and Foggy Conditions:** Maintain critical friction benchmarks, forcing delay rates to **37.28%** and **30.34%** respectively.

### 3. Machine Learning Predictive Accuracy

The underlying predictive model demonstrates high precision and robustness across unseen evaluation sets:

* **Area Under the ROC Curve (ROC-AUC):** **0.9625**
* **Global Model Accuracy:** **89.00%**
* **Sensitivity (Recall) for Delayed Runs:** **83.00%** (enabling robust proactive scheduling adjustments).

### 4. Root-Cause Bottleneck Signatures

By measuring the cumulative reduction in Gini Impurity across tree structures, the engine establishes that a shipment's delivery mode and expected time duration dictate the largest drops in variance, accounting for over **50.3%** of overall delay predictability. The node impurity is calculated formally as:

$$H(X_m) = 1 - \sum_{k=0}^{1} p_{mk}^2$$

---

## Saved Visual Reports

The programmatic visualization execution script automatically builds and saves presentation-ready graphics to the root or `notebooks/` directory:

* `carrier_sla_breach_rate.png` - Comprehensive ranking of 3PL providers mapped against systemic SLA breach probabilities.
* `weather_delay_impact.png` - Categorical distribution of environmental factors and their structural impact on network reliability.
* `bottleneck_feature_importance.png` - Information-gain summary illustrating the exact operational features driving model choices.
