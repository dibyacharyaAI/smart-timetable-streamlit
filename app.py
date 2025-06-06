# smart-timetable-streamlit/app.py
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
st.sidebar.title("📊 Filters")
view_type = st.sidebar.radio("View As", ["Student", "Teacher", "Admin"])
campus_filter = st.sidebar.multiselect("Campus", ["Campus A", "Campus B", "Campus C"], default=["Campus A"])
batch_filter = st.sidebar.multiselect("Batch", ["A", "B", "C"], default=["A"])

if view_type == "Student":
    section_list = final_tt_df["SectionID"].dropna().unique().tolist()
    selected_section = st.sidebar.selectbox("Section", section_list)
    st.title("📘 Student Timetable")
    section_tt = final_tt_df[final_tt_df["SectionID"] == selected_section]
    section_anomalies = anomalies_df[anomalies_df["SectionID"] == selected_section]
    section_healed = healed_df[healed_df["SectionID"] == selected_section]
    section_transit = transit_df[transit_df["SectionID"] == selected_section] if "SectionID" in transit_df.columns else pd.DataFrame()

    st.subheader("🗓️ Final Timetable")
    st.dataframe(section_tt, use_container_width=True)

    st.subheader("🩻 Anomalies Detected")
    st.dataframe(section_anomalies if not section_anomalies.empty else "✅ No anomalies!", use_container_width=True)

    st.subheader("🛠️ Healed Timetable")
    st.dataframe(section_healed if not section_healed.empty else "✅ No healing needed!", use_container_width=True)

    st.subheader("🚦 Transit Violations")
    st.dataframe(section_transit if not section_transit.empty else "✅ No transit issues!", use_container_width=True)

elif view_type == "Teacher":
    teacher_list = teachers_df["TeacherID"].unique().tolist()
    selected_teacher = st.sidebar.selectbox("Teacher ID", teacher_list)
    st.title("👩‍🏫 Teacher Timetable")
    teacher_tt = final_tt_df[final_tt_df["TeacherID"] == selected_teacher]
    st.dataframe(teacher_tt if not teacher_tt.empty else "No classes assigned", use_container_width=True)

elif view_type == "Admin":
    st.title("🛠️ Admin Dashboard")
    st.markdown("View all schedules across sections, batches, and teachers")
    st.dataframe(final_tt_df, use_container_width=True)
    st.markdown("---")
    st.subheader("⚠️ Anomalies")
    st.dataframe(anomalies_df, use_container_width=True)
    st.subheader("🔁 Healed Timetable")
    st.dataframe(healed_df, use_container_width=True)
    st.subheader("🚦 Transit Violations")
    st.dataframe(transit_df, use_container_width=True)

st.markdown("---")
st.info("To integrate this with frontend, expose endpoints from these datasets.")
