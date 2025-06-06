
import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Smart Timetable Dashboard", layout="wide")

# --- Load Files ---
data_dir = "data"
students_df = pd.read_excel(os.path.join(data_dir, "synthetic_students.xlsx"))
teachers_df = pd.read_excel(os.path.join(data_dir, "synthetic_teachers.xlsx"))
curriculum_df = pd.read_excel(os.path.join(data_dir, "normalized_curriculum.xlsx"))
activities_df = pd.read_excel(os.path.join(data_dir, "activities_table.xlsx"))
final_tt_df = pd.read_csv(os.path.join(data_dir, "final_clean_timetable.csv"))
anomalies_df = pd.read_csv(os.path.join(data_dir, "anomalies_detected.csv"))
healed_df = pd.read_csv(os.path.join(data_dir, "healed_timetable.csv"))
transit_df = pd.read_csv(os.path.join(data_dir, "flagged_transit_violations.csv"))
with open(os.path.join(data_dir, "transit_time.json")) as f:
    transit_map = json.load(f)

# --- Sidebar ---
st.sidebar.title("📊 Timetable Navigator")
section_list = final_tt_df["SectionID"].unique().tolist()
selected_section = st.sidebar.selectbox("Select Section", section_list)

# --- Main Display ---
st.title("📘 Smart Timetable Dashboard")
st.markdown("---")

# Filtered Views
section_tt = final_tt_df[final_tt_df["SectionID"] == selected_section]
section_anomalies = anomalies_df[anomalies_df["SectionID"] == selected_section]
section_healed = healed_df[healed_df["SectionID"] == selected_section]
section_transit = transit_df[transit_df["SectionID"] == selected_section] if "SectionID" in transit_df.columns else pd.DataFrame()

col1, col2 = st.columns(2)
with col1:
    st.subheader("🗓️ Final Timetable")
    st.dataframe(section_tt, use_container_width=True)

with col2:
    st.subheader("🩻 Anomalies Detected")
    st.dataframe(section_anomalies if not section_anomalies.empty else "✅ No anomalies!", use_container_width=True)

st.subheader("🛠️ Healed Timetable (Auto-Reconstructed)")
st.dataframe(section_healed if not section_healed.empty else "✅ No healing needed!", use_container_width=True)

st.subheader("🚦 Transit Time Violations")
st.dataframe(section_transit if not section_transit.empty else "✅ No transit issues!", use_container_width=True)

st.markdown("---")
st.info("To export this timetable or integrate via API, use /models and /utils directories in repo.")
