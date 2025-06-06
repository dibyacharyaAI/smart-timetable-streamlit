# 📘 Smart Timetable Streamlit Dashboard

An AI-powered interactive dashboard to visualize, validate, and auto-correct academic timetables using RNN-based anomaly detection and OR-Tools-based healing.

---

## 🚀 Features

- 🧠 Autoencoder-based anomaly detection
- 🔧 Constraint-driven self-healing (via OR-Tools)
- 📥 Drag-and-drop timetable updates via CSV
- 🔁 Pipeline auto-triggered on upload
- 👨‍🎓 Student View: personal section schedule
- 👩‍🏫 Teacher View: subject-wise teaching slots
- 👨‍💼 Admin View: full timetable + anomalies + transit violations
- 📊 Transit time violation detection using custom JSON map

---

## 📁 Project Structure

```
smart-timetable-streamlit/
├── app.py                       # Streamlit dashboard
├── pipeline_runner.py          # AI pipeline runner
├── data/                       # Timetable, model outputs, constraints
├── models/                     # Trained autoencoder model
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Installation

```bash
git clone https://github.com/dibyacharyaAI/smart-timetable-streamlit.git
cd smart-timetable-streamlit
pip install -r requirements.txt
```

---

## 🖥️ Run the Streamlit App

```bash
streamlit run app.py
```

> Open browser at: http://localhost:8501

---

## 📂 Upload Workflow (Admin Panel)

1. Upload a new `.csv` timetable (from drag-and-drop UI)
2. Click “🔁 Run Timetable Pipeline”
3. Behind the scenes:
   - Anomalies detected
   - Timetable healed
   - Transit time constraints applied
4. All updated views appear live

---

## 🔗 API + Automation (Optional)

Run backend pipeline directly:

```bash
python pipeline_runner.py data/uploaded_timetable_<timestamp>.csv
```

---

## 🧪 Requirements

- Python 3.9+
- streamlit, pandas, openpyxl, json, datetime

---

## 🧠 Model Architecture

- Bi-LSTM Autoencoder
- CrossEntropy-based reconstruction loss
- Outlier thresholding (mean + 3σ)
- Constraint Solver: Google OR-Tools CP-SAT

---

## 📌 License

This project is internal and part of the **Dhamm.AI Smart Scheduling System**.
