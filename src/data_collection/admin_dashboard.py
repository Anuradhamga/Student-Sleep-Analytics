import streamlit as st
import pandas as pd
import plotly.express as px

from supabase import create_client
from io import BytesIO


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Student Sleep Analytics | Admin",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM CSS
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
    color: white;
}

.main-title {
    color: #172554;
    font-size: 32px;
    font-weight: 800;
}

.metric-card {
    background-color: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SUPABASE CONNECTION
# =====================================================

try:

    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

except Exception:

    st.error("Unable to connect to Supabase.")

    st.stop()


# =====================================================
# 4. SESSION STATE
# =====================================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "admin_access_token" not in st.session_state:
    st.session_state.admin_access_token = None

if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""


# =====================================================
# 5. ADMIN LOGIN
# =====================================================

def admin_login():

    st.markdown(
        "<h1 style='text-align:center;color:#172554;'>"
        "🌙 Student Sleep Analytics"
        "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#64748B;'>"
        "Private Administrator Dashboard"
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    left, center, right = st.columns([1, 1.4, 1])

    with center:

        st.subheader("🔐 Admin Login")

        with st.form("admin_login_form"):

            email = st.text_input(
                "Admin Email"
            )

            password = st.text_input(
                "Admin Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if submitted:

            if not email.strip() or not password:

                st.warning("Please enter email and password.")

            else:

                try:

                    response = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password
                    })

                    if response.user is None or response.session is None:
                        st.error("Login failed.")
                        return

                    st.session_state.admin_logged_in = True

                    st.session_state.admin_access_token = (
                        response.session.access_token
                    )

                    st.session_state.admin_email = email.strip()

                    supabase.postgrest.auth(
                        response.session.access_token
                    )

                    st.success("Login successful!")

                    st.rerun()

                except Exception:

                    st.error(
                        "Login failed. Please check your credentials "
                        "or try again."
                    )


# =====================================================
# 6. AUTHENTICATED DATABASE ACCESS
# =====================================================

def authenticate_database():

    token = st.session_state.admin_access_token

    if not token:
        return False

    try:

        supabase.postgrest.auth(token)

        return True

    except Exception:

        return False


# =====================================================
# 7. GET RESPONSES
# =====================================================

def get_all_responses():

    try:

        response = (
            supabase
            .table("student_responses")
            .select("*")
            .order("id", desc=True)
            .execute()
        )

        df = pd.DataFrame(response.data)

        return df

    except Exception:

        st.error(
            "Unable to retrieve survey responses. "
            "Please log in again."
        )

        return pd.DataFrame()


# =====================================================
# 8. RECORD FILTER
# =====================================================

def filter_records(df, record_filter):

    if df.empty:
        return df

    if record_filter == "TEST Only":

        return df[df["record_type"] == "TEST"]

    elif record_filter == "RESEARCH Only":

        return df[df["record_type"] == "RESEARCH"]

    return df


# =====================================================
# 9. DATA LOADING
# =====================================================

def load_data():

    df = get_all_responses()

    if not df.empty and "collection_date" in df.columns:

        df["collection_date"] = pd.to_datetime(
            df["collection_date"],
            errors="coerce",
            utc=True
        )

    return df


# =====================================================
# 10. SIDEBAR
# =====================================================

def show_sidebar():

    st.sidebar.markdown("# 🌙 Sleep Analytics")

    st.sidebar.markdown("---")

    st.sidebar.success("Admin Authenticated")

    st.sidebar.caption(
        st.session_state.admin_email
    )

    menu = st.sidebar.radio(
        "MAIN MENU",
        [
            "📊 Dashboard",
            "📋 Survey Responses",
            "📈 Analytics",
            "📥 Export Data"
        ]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.admin_logged_in = False
        st.session_state.admin_access_token = None
        st.session_state.admin_email = ""

        st.rerun()

    st.sidebar.caption(
        "Student Sleep & Smartphone Analytics"
    )

    return menu


# =====================================================
# 11. DASHBOARD
# =====================================================

def show_dashboard(df):

    st.header("📊 Research Dashboard")

    st.write(
        "Overview of Student Sleep & Smartphone Survey Responses"
    )

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

    col1.metric(
        "Total Responses",
        total
    )

    col2.metric(
        "TEST Responses",
        test_count
    )

    col3.metric(
        "RESEARCH Responses",
        research_count
    )

    st.divider()

    if df.empty:

        st.info("No survey responses available.")

        return

    st.subheader("Recent Survey Responses")

    display_columns = [
        "participant_code",
        "record_type",
        "age",
        "grade",
        "sleep_quality",
        "smartphone_hours_daily"
    ]

    available_columns = [
        c for c in display_columns if c in df.columns
    ]

    st.dataframe(
        df[available_columns].head(10),
        use_container_width=True,
        hide_index=True
    )

    if "record_type" in df.columns:

        st.subheader("Response Distribution")

        counts = (
            df["record_type"]
            .value_counts()
            .reset_index()
        )

        counts.columns = ["Record Type", "Count"]

        fig = px.pie(
            counts,
            names="Record Type",
            values="Count",
            hole=0.45,
            title="TEST vs RESEARCH Responses"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =====================================================
# 12. SURVEY RESPONSES
# =====================================================

def show_responses(df):

    st.header("📋 Survey Responses")

    if df.empty:

        st.info("No responses available.")

        return

    record_filter = st.selectbox(
        "Filter Records",
        [
            "All Records",
            "TEST Only",
            "RESEARCH Only"
        ]
    )

    filtered_df = filter_records(
        df,
        record_filter
    )

    st.write(
        f"Total Records: {len(filtered_df)}"
    )

    search = st.text_input(
        "Search by Participant Code"
    )

    if search and "participant_code" in filtered_df.columns:

        filtered_df = filtered_df[
            filtered_df["participant_code"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 13. ANALYTICS
# =====================================================

def show_analytics(df):

    st.header("📈 Research Analytics")

    if df.empty:

        st.info("No data available for analysis.")

        return

    record_filter = st.radio(
        "Select records for analysis",
        [
            "All Records",
            "TEST Only",
            "RESEARCH Only"
        ],
        horizontal=True
    )

    data = filter_records(
        df,
        record_filter
    )

    if data.empty:

        st.warning("No records available for this filter.")

        return

    if "age" in data.columns:

        st.subheader("Age Distribution")

        fig = px.histogram(
            data,
            x="age",
            color="record_type",
            title="Student Age Distribution",
            labels={
                "age": "Age",
                "count": "Number of Students"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if "smartphone_hours_daily" in data.columns:

        st.subheader("Daily Smartphone Usage")

        counts = (
            data["smartphone_hours_daily"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Smartphone Hours",
            "Students"
        ]

        fig = px.bar(
            counts,
            x="Smartphone Hours",
            y="Students",
            title="Daily Smartphone Usage Distribution",
            text="Students"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if "sleep_quality" in data.columns:

        st.subheader("Sleep Quality")

        counts = (
            data["sleep_quality"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Sleep Quality",
            "Students"
        ]

        fig = px.bar(
            counts,
            x="Sleep Quality",
            y="Students",
            title="Student Sleep Quality"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if "daytime_sleepiness" in data.columns:

        st.subheader("Daytime Sleepiness")

        counts = (
            data["daytime_sleepiness"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Daytime Sleepiness",
            "Students"
        ]

        fig = px.bar(
            counts,
            x="Daytime Sleepiness",
            y="Students",
            title="Daytime Sleepiness Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if "concentration_difficulty" in data.columns:

        st.subheader("Concentration Difficulty")

        counts = (
            data["concentration_difficulty"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Concentration Difficulty",
            "Students"
        ]

        fig = px.bar(
            counts,
            x="Concentration Difficulty",
            y="Students",
            title="Concentration Difficulty Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =====================================================
# 14. EXPORT DATA
# =====================================================

def show_export(df):

    st.header("📥 Export Research Data")

    if df.empty:

        st.info("No data available for export.")

        return

    record_filter = st.selectbox(
        "Select Records to Export",
        [
            "All Records",
            "TEST Only",
            "RESEARCH Only"
        ]
    )

    export_df = filter_records(
        df,
        record_filter
    ).drop(
        columns=["id"],
        errors="ignore"
    ).copy()

    # FIX: Remove timezone information before Excel export
    for column in export_df.columns:

        if isinstance(export_df[column].dtype, pd.DatetimeTZDtype):

            export_df[column] = (
                export_df[column].dt.tz_localize(None)
            )

    st.write(
        f"Records Available: {len(export_df)}"
    )

    # CSV EXPORT

    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📄 Download CSV",
        data=csv_data,
        file_name="student_sleep_data.csv",
        mime="text/csv",
        use_container_width=True
    )

    # EXCEL EXPORT

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
        label="📊 Download Excel",
        data=excel_buffer.getvalue(),
        file_name="student_sleep_data.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )


# =====================================================
# 15. MAIN APPLICATION
# =====================================================

if not st.session_state.admin_logged_in:

    admin_login()

else:

    if not authenticate_database():

        st.session_state.admin_logged_in = False
        st.session_state.admin_access_token = None

        st.warning(
            "Your login session is unavailable. Please log in again."
        )

        st.rerun()

    else:

        menu = show_sidebar()

        df = load_data()

        if menu == "📊 Dashboard":

            show_dashboard(df)

        elif menu == "📋 Survey Responses":

            show_responses(df)

        elif menu == "📈 Analytics":

            show_analytics(df)

        elif menu == "📥 Export Data":

            show_export(df)