
# 📘 Best Cities for Workation Dashboard

## 🌍 Overview
This Streamlit dashboard helps users discover and compare the **best global cities for a “workation”** — a mix of *work* and *vacation*. It evaluates cities based on factors such as WiFi speed, rent cost, sunshine hours, and social appeal, and is intended for digital nomads, remote workers, and travel enthusiasts.

---

## 📊 Dataset
The dataset used in this dashboard comes from **[Kaggle: The Best Cities for a Workation](https://www.kaggle.com/datasets/)**. It contains 50+ global cities and includes variables such as:
- `WiFi Speed (Mbps)`
- `Monthly Rent (USD)`
- `Sunshine Hours per Year`
- `Coworking Spaces`
- `Meal, Coffee, Beer, Taxi Prices`
- `Instagram Photos` (as a proxy for social media appeal)

Derived columns:
- `Sunshine per Day (hrs)`
- `Workation Score` = `WiFi Speed × 2 + Sunshine Hours − (Rent × 0.01)`
- `Composite Score` = normalized average of WiFi, coworking, rent (inverted), sunshine/day, Instagram popularity

---

## 🖥️ Features

- **Filtering Panel**:
  - Select by Country or City
  - Adjust WiFi speed, rent, and sunshine preferences

- **Key Visualizations**:
  - 📊 Top Workation Cities (Bar chart)
  - 🌍 Composite Score by Country (Map & Pie)
  - ☀️ Sunniest Cities (Treemap)
  - 💰 Daily Cost Breakdown (Pie and Bar Chart)
  - ⚠️ Worst Cities by Workation Score

- **User Segments Tabs**:
  - 💼 Remote Workers (score: WiFi + coworking)
  - 💸 Budget Travelers (total daily cost)
  - 📸 Social Explorers (Instagram + attractions)

- **Download Options**: Export filtered data as `.csv`

---

## ⚙️ How to Run

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/Dashboard-Workation.git
   cd Dashboard-Workation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the app**:
   ```bash
   streamlit run main_app.py
   ```

---

## 📥 Folder Structure

```
📁 workation-dashboard
├── 📄 main_app.py                ← Main Streamlit dashboard
├── 📁 Dataset/              ← Contains cleaned dataset (workation_cleaned.csv)
├── 📁 .streamlit/              ← Contains config (config.toml)
├── 📄 requirements.txt      ← Required packages
└── 📄 README.md             ← You're here!
```
=======
# Dashboard-Workation
