# ⚡ Campus Energy Management System (CampusEMS)

### Smart Campus Energy Monitoring, Analytics and Management Dashboard

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75?logo=plotly)
![Status](https://img.shields.io/badge/Project-Development-orange)

---

## 🌐 Live Application

**CampusEMS Dashboard:** https://campus-energy-management.streamlit.app/

**FastAPI Backend:** https://campus-energy-monitoring-5ed86988.fastapicloud.dev/

**API Documentation:** https://campus-energy-monitoring-5ed86988.fastapicloud.dev/docs

**GitHub Repository:** https://github.com/KaushikShelam/Campus-Energy-Management

---

## 📌 1. Project Overview

The **Campus Energy Management System (CampusEMS)** is a smart energy monitoring and analytics platform designed to monitor, analyze and visualize electrical energy consumption across different buildings within a campus.

The system provides a centralized dashboard to observe important electrical parameters, compare building-wise energy consumption, analyze solar and grid power utilization, and identify abnormal electrical conditions.

The platform aims to improve energy awareness, support efficient electricity utilization, and provide insights for better campus energy management.

The current version uses simulated electrical readings for demonstration. Future development will integrate IoT-based energy meters for actual real-time monitoring.

---

## 🎯 2. Project Objectives

- Develop a centralized campus energy monitoring platform.
- Monitor essential electrical parameters.
- Analyze building-wise electricity consumption.
- Compare solar generation with grid power consumption.
- Visualize energy usage through interactive charts.
- Identify abnormal electrical readings.
- Generate downloadable energy reports.
- Support future IoT-based energy monitoring and automation.

---

## 🚀 3. Key Features

### 3.1 Campus Overview Dashboard

Provides a centralized view of the campus electrical performance.

- Campus-level electrical parameter summaries.
- Building-wise power consumption comparison.
- Energy distribution visualization.
- Solar generation overview.
- Grid power consumption analysis.

### 3.2 Electrical Parameter Monitoring

The system monitors seven major electrical parameters:

| Parameter | Unit | Description |
|---|---|---|
| Voltage | V | Electrical supply voltage |
| Current | A | Electrical current consumption |
| Active Power | kW | Actual electrical power consumed |
| Energy Consumption | kWh | Electrical energy usage |
| Frequency | Hz | Supply frequency |
| Power Factor | PF | Electrical power utilization factor |
| Apparent Power | kVA | Total apparent electrical power |

Additional monitoring indicators include:

- Solar Power Generation (kW)
- Grid Power Consumption (kW)
- Temperature (°C)

### 3.3 Building-wise Monitoring

The dashboard supports monitoring of five demonstration campus buildings:

1. Engineering Block
2. Library
3. Administrative Block
4. Laboratories
5. Hostel Block

Users can select individual buildings and view their electrical readings and power distribution.

### 3.4 Interactive Energy Analytics

The dashboard provides interactive visualizations for:

- Building-wise energy distribution.
- Active power comparison.
- Energy consumption analysis.
- Solar versus grid power distribution.

Charts are developed using Plotly.

### 3.5 Solar and Grid Analysis

Provides an overview of campus solar generation and grid power utilization.

The dashboard visualizes the contribution of solar and grid power using interactive charts.

### 3.6 Alerts and Reports

The system includes basic abnormal-reading checks for:

- High or low voltage.
- Low power factor.

Users can also download campus energy readings in CSV format for further analysis.

---

## 🖥️ 4. Dashboard Modules

| Module | Functionality |
|---|---|
| Overview | Campus-wide energy summary |
| Live Monitoring | Building-specific electrical parameters |
| Building Analysis | Individual building energy analysis |
| Energy Analytics | Energy distribution and consumption charts |
| Solar & Grid | Solar generation and grid utilization |
| Alerts & Reports | Abnormal-reading checks and CSV reports |

---

## 🏗️ 5. System Architecture

The current application follows a Python-based dashboard architecture.

```text
          USER
            |
            v
      WEB BROWSER
            |
            v
     STREAMLIT FRONTEND
            |
            v
      PYTHON APPLICATION
            |
       +----+----+
       |         |
       v         v
    PANDAS     PLOTLY
   DATA       CHARTS
   PROCESSING    |
       |         |
       +----+----+
            |
            v
    CAMPUS ENERGY
     DASHBOARD
```

**Future IoT Integration:**

```text
Electrical Energy Meter
        |
        v
   ESP32 / NodeMCU
        |
        v
 Communication Network
        |
        v
 Python Backend / Database
        |
        v
 CampusEMS Dashboard
```

---

## 🛠️ 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Streamlit | Web dashboard development |
| Pandas | Data processing and analysis |
| Plotly | Interactive data visualization |
| HTML / CSS | Dashboard styling concepts |
| GitHub | Source code management |
| Streamlit Community Cloud | Application deployment |

### Development Environment

- Visual Studio Code
- Python 3.12
- Windows 11
- Google Chrome

---

## 📂 7. Project Structure

```text
Campus-Energy-Management/
│
├── streamlit_app.py
│       Main Streamlit dashboard application
│
├── requirements.txt
│       Python dependencies
│
├── README.md
│       Project documentation
│
├── app.py
│       Earlier FastAPI backend prototype
│
├── static/
│       CSS resources from the earlier web interface
│
└── templates/
        HTML dashboard from the earlier web interface
```

---

## ⚙️ 8. Installation and Local Setup

Follow these steps to run CampusEMS locally.

### Step 1: Clone the repository

```bash
git clone https://github.com/KaushikShelam/Campus-Energy-Management.git
```

### Step 2: Navigate to the project directory

```bash
cd Campus-Energy-Management
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the application

```bash
streamlit run streamlit_app.py
```

### Step 7: Open the dashboard

Visit:

```text
http://localhost:8501
```

---

## 📦 9. Dependencies

The application uses the following Python libraries:

```text
streamlit
pandas
plotly
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## ☁️ 10. Cloud Deployment

CampusEMS is deployed using **Streamlit Community Cloud**.

Deployment workflow:

1. Maintain the application source code in GitHub.
2. Connect the GitHub repository to Streamlit Community Cloud.
3. Select the `main` branch.
4. Configure `streamlit_app.py` as the main application file.
5. Deploy the application.
6. Access the dashboard through its public URL.

**Live Dashboard:**

https://campus-energy-management.streamlit.app/

Updates committed to the connected GitHub repository can trigger automatic application redeployment.

---

## 📊 11. Current Implementation Status

| Component | Status |
|---|---|
| Streamlit dashboard | Completed |
| Professional dark interface | Implemented |
| KPI monitoring cards | Implemented |
| Building-wise analysis | Implemented |
| Interactive Plotly charts | Implemented |
| Solar and grid visualization | Implemented |
| Basic abnormal-reading checks | Implemented |
| CSV report download | Implemented |
| Cloud deployment | Configured |
| Real-time IoT integration | Future enhancement |
| Persistent cloud database | Future enhancement |
| Historical energy analytics | Future enhancement |

**Note:** Current electrical readings are simulated demonstration values. The application is not yet connected to physical energy meters.

---

## 🔮 12. Future Enhancements

The following improvements are planned for future development:

- Integration with ESP32 and NodeMCU controllers.
- Integration with PZEM-004T energy measurement modules.
- Real-time voltage, current and power acquisition.
- Database integration for persistent energy records.
- Historical energy consumption analysis.
- Automatic abnormal-condition notifications.
- Building-wise energy efficiency analysis.
- Solar generation forecasting.
- AI-based energy consumption prediction.
- Automated energy-saving recommendations.
- User authentication and role-based access.
- PDF and Excel report generation.

---

## 🌱 13. Expected Benefits

- Improved campus energy visibility.
- Better understanding of electricity consumption.
- Identification of abnormal electrical conditions.
- Improved solar energy utilization awareness.
- Support for energy conservation initiatives.
- Centralized energy information for campus management.

---

## 👨‍💻 14. Project Information

**Project Name:** Campus Energy Management System (CampusEMS)

**Category:** Smart Energy Management / Web Application / Data Analytics

**Framework:** Streamlit

**Programming Language:** Python

**Deployment Platform:** Streamlit Community Cloud

**Developer:** Shelam Kaushik

**GitHub:** [KaushikShelam](https://github.com/KaushikShelam)

---

## 📜 15. License

This project is developed for educational, demonstration and academic purposes.

---

### ⚡ CampusEMS

**Smarter Monitoring. Better Energy Management. Sustainable Campus.**
