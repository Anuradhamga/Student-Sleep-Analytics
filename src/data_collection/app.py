import streamlit as st
import pandas as pd
import sqlite3

from pathlib import Path
from datetime import datetime
from io import BytesIO


# =====================================================
# 1. PROJECT CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "dataset" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "student_sleep_data.db"


st.set_page_config(
    page_title="Student Sleep Analytics",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM CSS - PROFESSIONAL UI
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

[data-testid="stSidebar"] {
    background-color: #172554;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #172554;
}

.subtitle {
    color: #64748B;
    font-size: 15px;
}

.metric-card {
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    padding: 22px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
}

.metric-card h3 {
    font-size: 15px;
    color: #E0E7FF;
}

.metric-card h1 {
    font-size: 32px;
    color: white;
}

.section-title {
    color: #172554;
    font-size: 23px;
    font-weight: 700;
}

div.stButton > button {
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 20px;
    font-weight: bold;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #1D4ED8, #6D28D9);
    color: white;
}

.stDownloadButton button {
    background-color: #059669;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATABASE
# =====================================================

def get_connection():

    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            participant_code TEXT UNIQUE,

            record_type TEXT DEFAULT 'TEST',

            collection_date TEXT,

            age INTEGER,
            grade TEXT,
            school_type TEXT,
            gender TEXT,

            smartphone_use TEXT,
            smartphone_hours TEXT,
            smartphone_purpose TEXT,
            before_sleep_use TEXT,
            nighttime_use TEXT,

            bedtime TEXT,
            wakeup_time TEXT,
            sleep_duration TEXT,
            falling_asleep TEXT,
            sleep_quality TEXT,
            night_awakenings TEXT,

            daytime_sleepiness TEXT,
            concentration_difficulty TEXT,
            daytime_tiredness TEXT,
            daily_activity_effect TEXT

        )
    """)

    # Migration for databases created using an older version

    columns = [
        row[1] for row in
        conn.execute("PRAGMA table_info(responses)").fetchall()
    ]

    if "record_type" not in columns:

        conn.execute("""
            ALTER TABLE responses
            ADD COLUMN record_type TEXT DEFAULT 'TEST'
        """)

    conn.commit()
    conn.close()


initialize_database()


# =====================================================
# 4. DATABASE FUNCTIONS
# =====================================================

def get_all_responses():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM responses ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


def save_response(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (

            record_type,
            collection_date,

            age,
            grade,
            school_type,
            gender,

            smartphone_use,
            smartphone_hours,
            smartphone_purpose,
            before_sleep_use,
            nighttime_use,

            bedtime,
            wakeup_time,
            sleep_duration,
            falling_asleep,
            sleep_quality,
            night_awakenings,

            daytime_sleepiness,
            concentration_difficulty,
            daytime_tiredness,
            daily_activity_effect

        )

        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )

    """, data)

    response_id = cursor.lastrowid

    participant_code = f"P{response_id:04d}"

    cursor.execute("""
        UPDATE responses
        SET participant_code = ?
        WHERE id = ?
    """, (participant_code, response_id))

    conn.commit()
    conn.close()

    return participant_code


def delete_responses(codes):

    conn = get_connection()

    cursor = conn.cursor()

    deleted = 0

    for code in codes:

        cursor.execute(
            "DELETE FROM responses WHERE participant_code = ?",
            (code,)
        )

        deleted += cursor.rowcount

    conn.commit()
    conn.close()

    return deleted


# =====================================================
# 5. HEADER
# =====================================================

st.markdown(
    '<div class="main-title">🌙 Student Sleep & Smartphone Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Research Data Collection and Analytics Platform | Sri Lanka</div>',
    unsafe_allow_html=True
)

st.write("")


# =====================================================
# 6. SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown("# 🌙 Sleep Analytics")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "MAIN MENU",
    [
        "🏠 Dashboard",
        "📝 Add New Response",
        "📋 View Responses",
        "📊 Analytics",
        "📥 Export Data",
        "ℹ️ About Research"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Student Sleep Analytics"
)

st.sidebar.caption(
    "Version 2.0 | Local Database"
)


# =====================================================
# 7. DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

    st.header("Research Dashboard")

    df = get_all_responses()

    total = len(df)

    test_count = 0
    research_count = 0

    if not df.empty:

        test_count = len(
            df[df["record_type"] == "TEST"]
        )

        research_count = len(
            df[df["record_type"] == "RESEARCH"]
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Responses</h3>
            <h1>{total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="metric-card">
            <h3>Test Records</h3>
            <h1>{test_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="metric-card">
            <h3>Research Records</h3>
            <h1>{research_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.subheader("Recent Responses")

    if not df.empty:

        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No responses available yet.")

    st.caption(
        "All records are stored locally on this computer."
    )


# =====================================================
# 8. ADD NEW RESPONSE
# =====================================================

elif menu == "📝 Add New Response":

    st.header("📝 Student Questionnaire")

    st.info(
        "Complete the questionnaire by asking the participant "
        "each question consistently."
    )

    with st.form("student_form"):

        st.subheader("Research Record Type")

        record_type = st.selectbox(
            "Select record type",
            ["TEST", "RESEARCH"]
        )

        if record_type == "TEST":

            st.warning(
                "TEST records are for fictional sample data only."
            )

        else:

            st.warning(
                "Only use RESEARCH mode after obtaining the required "
                "ethical approval, school permission and participant "
                "consent/assent."
            )

        approval_confirmed = False

        if record_type == "RESEARCH":

            approval_confirmed = st.checkbox(
                "I confirm that all required ethical approvals, "
                "school permissions and participant consent/assent "
                "have been obtained."
            )

        st.divider()

        st.subheader("01. General Information")

        age = st.number_input(
            "1. Age",
            min_value=5,
            max_value=25,
            value=15
        )

        grade = st.selectbox(
            "2. Grade",
            [
                "Grade 6",
                "Grade 7",
                "Grade 8",
                "Grade 9",
                "Grade 10",
                "Grade 11",
                "Grade 12",
                "Grade 13",
                "Other"
            ]
        )

        school_type = st.selectbox(
            "3. School Type",
            [
                "Government",
                "Private",
                "International",
                "Other"
            ]
        )

        gender = st.selectbox(
            "4. Gender (Optional)",
            [
                "Prefer not to say",
                "Male",
                "Female",
                "Other"
            ]
        )

        st.divider()

        st.subheader("02. Smartphone Usage")

        smartphone_use = st.radio(
            "5. Do you use a smartphone?",
            ["Yes", "No"]
        )

        smartphone_hours = st.selectbox(
            "6. Daily smartphone usage",
            [
                "Do not use",
                "Less than 1 hour",
                "1–2 hours",
                "2–4 hours",
                "4–6 hours",
                "More than 6 hours"
            ]
        )

        smartphone_purpose = st.selectbox(
            "7. Main purpose of smartphone use",
            [
                "Do not use",
                "Education",
                "Social Media",
                "Entertainment",
                "Communication",
                "Gaming",
                "Other"
            ]
        )

        before_sleep_use = st.selectbox(
            "8. Smartphone use before sleeping",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always",
                "Not Applicable"
            ]
        )

        nighttime_use = st.selectbox(
            "9. Smartphone use after going to bed",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always",
                "Not Applicable"
            ]
        )

        st.divider()

        st.subheader("03. Sleep Patterns")

        bedtime = st.selectbox(
            "10. Usual bedtime",
            [
                "Before 8:00 PM",
                "8:00–9:00 PM",
                "9:00–10:00 PM",
                "10:00–11:00 PM",
                "11:00 PM–12:00 AM",
                "After 12:00 AM"
            ]
        )

        wakeup_time = st.selectbox(
            "11. Usual wake-up time",
            [
                "Before 5:00 AM",
                "5:00–6:00 AM",
                "6:00–7:00 AM",
                "7:00–8:00 AM",
                "After 8:00 AM"
            ]
        )

        sleep_duration = st.selectbox(
            "12. Sleep duration on school nights",
            [
                "Less than 5 hours",
                "5–6 hours",
                "6–7 hours",
                "7–8 hours",
                "8–9 hours",
                "More than 9 hours"
            ]
        )

        falling_asleep = st.selectbox(
            "13. Difficulty falling asleep",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always"
            ]
        )

        sleep_quality = st.selectbox(
            "14. Overall sleep quality",
            [
                "Very Good",
                "Good",
                "Average",
                "Poor",
                "Very Poor"
            ]
        )

        night_awakenings = st.selectbox(
            "15. Waking up during the night",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always"
            ]
        )

        st.divider()

        st.subheader("04. Daytime Functioning")

        daytime_sleepiness = st.selectbox(
            "16. Sleepiness during school hours",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always"
            ]
        )

        concentration_difficulty = st.selectbox(
            "17. Difficulty concentrating in class",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always"
            ]
        )

        daytime_tiredness = st.selectbox(
            "18. Feeling tired during the day",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always"
            ]
        )

        daily_activity_effect = st.selectbox(
            "19. Effect of tiredness on school activities",
            [
                "Never",
                "Rarely",
                "Sometimes",
                "Often",
                "Always"
            ]
        )

        st.divider()

        submit = st.form_submit_button(
            "💾 SAVE RESPONSE",
            use_container_width=True
        )

        if submit:

            if smartphone_use == "No":

                smartphone_hours = "Do not use"
                smartphone_purpose = "Do not use"
                before_sleep_use = "Not Applicable"
                nighttime_use = "Not Applicable"

            if record_type == "RESEARCH" and not approval_confirmed:

                st.error(
                    "Required research approvals and consent/assent "
                    "must be confirmed before saving."
                )

            else:

                data = (
                    record_type,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                    age,
                    grade,
                    school_type,
                    gender,

                    smartphone_use,
                    smartphone_hours,
                    smartphone_purpose,
                    before_sleep_use,
                    nighttime_use,

                    bedtime,
                    wakeup_time,
                    sleep_duration,
                    falling_asleep,
                    sleep_quality,
                    night_awakenings,

                    daytime_sleepiness,
                    concentration_difficulty,
                    daytime_tiredness,
                    daily_activity_effect
                )

                participant_code = save_response(data)

                st.success(
                    f"Response saved successfully! ID: {participant_code}"
                )


# =====================================================
# 9. VIEW AND DELETE RESPONSES
# =====================================================

elif menu == "📋 View Responses":

    st.header("📋 Response Management")

    df = get_all_responses()

    if not df.empty:

        st.metric(
            "Total Records",
            len(df)
        )

        st.subheader("Search Records")

        search_code = st.text_input(
            "Search by Participant ID"
        )

        filtered_df = df.copy()

        if search_code:

            filtered_df = filtered_df[
                filtered_df["participant_code"].str.contains(
                    search_code,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            filtered_df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("🗑️ Delete Selected Records")

        st.warning(
            "Deleted records cannot be recovered through this application. "
            "Check your selection carefully."
        )

        selected_codes = st.multiselect(
            "Select Participant IDs to Delete",
            options=df["participant_code"].tolist()
        )

        if selected_codes:

            st.write("Selected Records:")

            st.dataframe(
                df[
                    df["participant_code"].isin(selected_codes)
                ][["participant_code", "record_type", "age", "grade"]],
                use_container_width=True,
                hide_index=True
            )

        confirm_delete = st.checkbox(
            "I understand that the selected records will be permanently deleted."
        )

        if st.button(
            "🗑️ DELETE SELECTED RECORDS",
            disabled=not (selected_codes and confirm_delete)
        ):

            deleted = delete_responses(selected_codes)

            st.success(
                f"{deleted} record(s) deleted successfully!"
            )

            st.rerun()

    else:

        st.info("No responses available yet.")


# =====================================================
# 10. ANALYTICS
# =====================================================

elif menu == "📊 Analytics":

    st.header("📊 Research Analytics")

    df = get_all_responses()

    if not df.empty:

        st.info(
            "Charts below are based on the records currently stored "
            "in the database. Test records are included."
        )

        record_filter = st.radio(
            "Select records for analysis",
            ["All Records", "TEST Only", "RESEARCH Only"],
            horizontal=True
        )

        if record_filter == "TEST Only":

            df = df[df["record_type"] == "TEST"]

        elif record_filter == "RESEARCH Only":

            df = df[df["record_type"] == "RESEARCH"]

        if not df.empty:

            st.subheader("Smartphone Usage Distribution")

            st.bar_chart(
                df["smartphone_hours"].value_counts()
            )

            st.subheader("Sleep Duration Distribution")

            st.bar_chart(
                df["sleep_duration"].value_counts()
            )

            st.subheader("Sleep Quality Distribution")

            st.bar_chart(
                df["sleep_quality"].value_counts()
            )

            st.subheader("Daytime Sleepiness")

            st.bar_chart(
                df["daytime_sleepiness"].value_counts()
            )

            st.subheader("Smartphone Usage vs Sleep Quality")

            comparison = pd.crosstab(
                df["smartphone_hours"],
                df["sleep_quality"]
            )

            st.dataframe(
                comparison,
                use_container_width=True
            )

            st.caption(
                "These are descriptive summaries, not evidence of causation."
            )

        else:

            st.info("No records available for this selection.")

    else:

        st.info(
            "Add sample or approved research records to view analytics."
        )


# =====================================================
# 11. EXPORT DATA
# =====================================================

elif menu == "📥 Export Data":

    st.header("📥 Export Research Data")

    df = get_all_responses()

    if not df.empty:

        record_filter = st.selectbox(
            "Select records to export",
            ["All Records", "TEST Only", "RESEARCH Only"]
        )

        if record_filter == "TEST Only":

            export_df = df[df["record_type"] == "TEST"]

        elif record_filter == "RESEARCH Only":

            export_df = df[df["record_type"] == "RESEARCH"]

        else:

            export_df = df

        export_df = export_df.drop(columns=["id"])

        st.write(
            f"Records available: {len(export_df)}"
        )

        csv_data = export_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📄 Download CSV",
            csv_data,
            "student_sleep_data.csv",
            "text/csv",
            use_container_width=True
        )

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            export_df.to_excel(
                writer,
                index=False,
                sheet_name="Student Responses"
            )

        st.download_button(
            "📊 Download Excel",
            excel_buffer.getvalue(),
            "student_sleep_data.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    else:

        st.info("No data available for export.")


# =====================================================
# 12. ABOUT RESEARCH
# =====================================================

elif menu == "ℹ️ About Research":

    st.header("ℹ️ About This Research")

    st.markdown("""
    ### Research Title

    Investigating the Association Between Smartphone Usage
    Patterns, Sleep Quality and Daytime Functioning Among
    School Students in Sri Lanka Using Machine Learning.

    ### Research Objectives

    1. Investigate smartphone usage patterns.
    2. Examine sleep duration and sleep quality.
    3. Explore daytime functioning among school students.
    4. Investigate associations between smartphone usage and sleep.
    5. Explore machine learning approaches where appropriate.

    ### Technology Stack

    - Python
    - Streamlit
    - SQLite
    - Pandas
    - NumPy
    - Scikit-learn

    ### Data Protection

    - No names are required.
    - Participant IDs are automatically generated.
    - Data are stored locally.
    - Test and research records are identified separately.
    """)

    st.info(
        "The questionnaire is a draft and requires supervisor review, "
        "appropriate validation and ethical approval before actual "
        "participant data collection."
    )

    st.caption(
        "Student Sleep & Smartphone Analytics | Research Project"
    )


# =====================================================
# END OF APPLICATION
# =====================================================