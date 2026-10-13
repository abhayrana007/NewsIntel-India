# 🛡️ NewsIntel India

### 🇮🇳 Cyber Threat Intelligence & Incident Visualization Dashboard

<p align="center">
  <strong>Turning cyber incident data into actionable visual insights.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Domain-Cyber%20Threat%20Intelligence-00A86B" alt="Cyber Threat Intelligence" />
</p>

---

## 🔍 About the Project

**NewsIntel India** is a Python-powered **Cyber Threat Intelligence (CTI) dashboard** designed to explore, analyze, and visualize cyber incident data through an interactive interface.

The project combines a dark-themed incident map, analytical charts, timeline visualization, and searchable incident records to make cyber incident information easier to explore and understand.

Whether you're exploring attack patterns, examining affected sectors, or analyzing incident trends, NewsIntel India brings multiple perspectives together in one dashboard.

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗺️ **Interactive Incident Map** | Explore incident locations using a dark-themed map. |
| 📊 **Incident Overview** | Get a quick snapshot of key incident metrics. |
| 🎯 **Attack-Type Analysis** | Explore the distribution of different attack types. |
| 🏢 **Sector Analysis** | Examine incidents across affected sectors. |
| 📈 **Timeline Analysis** | Explore monthly incident trends from July 2024 to July 2026. |
| 🎛️ **Interactive Filters** | Filter records by country, sector, attack type, and verification status. |
| 🔎 **Incident Explorer** | Search and examine individual incident records. |
| 🌑 **Cybersecurity-Inspired UI** | Navigate the dashboard through a dark, security-focused interface. |

## 🖥️ Technology Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
</p>

- **Python** — Core programming language
- **Streamlit** — Interactive dashboard and user interface
- **Pandas** — Data cleaning, processing, and analysis
- **Plotly** — Interactive charts and data visualization

## ⚙️ Getting Started

Follow these steps to run NewsIntel India locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/abhayrana007/NewsIntel-India.git
cd NewsIntel-India
```

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4️⃣ Add the Dataset

Ensure the dataset is available at the following location:

```text
data/raw/NewsIntel_final.csv
```

If the dataset is not included in the repository, place your authorized copy at that path.

### 5️⃣ Launch the Dashboard 🚀

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in your terminal. Open that URL in your browser to explore the dashboard.

## 📂 Project Structure

```text
NewsIntel-India/
│
├── app.py                      # Main Streamlit dashboard
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Files excluded from Git
│
├── data/
│   └── raw/
│       └── NewsIntel_final.csv # Incident dataset (if included)
│
├── reports/                    # Reports and analysis outputs
└── src/                        # Supporting source code
```

## 🎯 Project Goals

- 🧠 Explore cyber threat intelligence through data visualization.
- 🌍 Understand the geographic distribution of reported incidents.
- 📉 Analyze incident trends over time.
- 🏭 Examine patterns across attack types and sectors.
- 🔎 Make incident records easier to search and investigate.
- 💻 Build practical skills in Python, OSINT-oriented analysis, and security analytics.

## ⚠️ Data Limitations & Responsible Use

- Incident records may originate from sources with different levels of reliability.
- Verification labels reflect the underlying dataset and should not be treated as independent confirmation.
- Map coordinates may be approximate and do not necessarily establish the exact location of an incident.
- A plotted record does **not** independently prove that an attack occurred.
- Only publish datasets you are authorized to share. Remove confidential, restricted, or sensitive information before making the repository public.

**This dashboard is intended for educational, analytical, and research purposes.**

## 🔮 Future Improvements

Potential enhancements include:

- 📡 Integration of additional authorized threat-intelligence sources.
- 🧹 Improved data validation and normalization.
- 📊 More advanced trend analysis and visualizations.
- 🧭 Additional filtering and incident investigation capabilities.
- 📥 Exportable summaries and analytical reports.

## 👨‍💻 Author

**Cybersecurity Student | Cyber Threat Intelligence | OSINT | Security Analytics**

Interested in exploring cyber threats, analyzing security-related data, and building practical tools that make complex information easier to understand.

🔗 **GitHub:** [@abhayrana007](https://github.com/abhayrana007)

---

<p align="center">
  <strong>🛡️ Explore. Analyze. Understand.</strong>
  <br/>
  <em>NewsIntel India — Visualizing the cyber threat landscape.</em>
</p>
