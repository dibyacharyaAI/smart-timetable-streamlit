# smart-timetable-streamlit/app.py
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="Smart Timetable Dashboard", layout="wide")

# --- Load Files ---
data_dir = "data"
def load_data(filename, filetype="csv"):
    if filetype == "csv":
        return pd.read_csv(os.path.join(data_dir, filename))
    elif filetype == "excel":
        return pd.read_excel(os.path.join(data_dir, filename))
    elif filetype == "json":
        with open(os.path.join(data_dir, filename)) as f:
            return json.load(f)

students_df = load_data("synthetic_students.xlsx", "excel")
teachers_df = load_data("synthetic_teachers.xlsx", "excel")
curriculum_df = load_data("normalized_curriculum.xlsx", "excel")
activities_df = load_data("activities_table.xlsx", "excel")
final_tt_df = load_data("final_clean_timetable.csv")
anomalies_df = load_data("anomalies_detected.csv")
healed_df = load_data("healed_timetable.csv")
transit_df = load_data("flagged_transit_violations.csv")
transit_map = load_data("transit_time.json", "json")

# --- Sidebar ---
st.sidebar.title("📊 Filters")
view_type = st.sidebar.radio("View As", ["Student", "Teacher", "Admin"])
campus_filter = st.sidebar.multiselect("Campus", ["Campus A", "Campus B", "Campus C"], default=["Campus A"])
scheme_filter = st.sidebar.multiselect("Scheme", ["A", "B"], default=["A"])

# --- Upload Updated Timetable ---
latest_uploaded = None
if view_type == "Admin":
    st.sidebar.markdown("---")
    uploaded_file = st.sidebar.file_uploader("Upload Updated Timetable CSV", type=["csv"])
    if uploaded_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_path = os.path.join("data", f"uploaded_timetable_{timestamp}.csv")
        with open(upload_path, "wb") as f:
            f.write(uploaded_file.read())
        st.sidebar.success(f"✅ Uploaded: {upload_path}")
        latest_uploaded = upload_path

        if st.sidebar.button("🔁 Run Timetable Pipeline"):
            with st.spinner("Running AI pipeline..."):
                exit_code = os.system(f"python pipeline_runner.py {upload_path}")
                if exit_code == 0:
                    st.sidebar.success("✅ Pipeline complete. Dashboard updated!")
                else:
                    st.sidebar.error("❌ Pipeline failed. Check console logs.")

# --- Main Views ---
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
    st.markdown("View all schedules across schemes, sections, and teachers")
    st.dataframe(final_tt_df, use_container_width=True)
    st.markdown("---")
    st.subheader("⚠️ Anomalies")
    st.dataframe(anomalies_df, use_container_width=True)
    st.subheader("🔁 Healed Timetable")
    st.dataframe(healed_df, use_container_width=True)
    st.subheader("🚦 Transit Violations")
    st.dataframe(transit_df, use_container_width=True)

st.markdown("---")
st.info("Upload → Run AI Pipeline → View final result below")
