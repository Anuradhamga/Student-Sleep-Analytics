import streamlit as st
import requests

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Student Sleep & Smartphone Survey",
    page_icon="🌙",
    layout="centered"
)


# ==========================================
# COMPLETE CSS DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #f1f5f9;
}

.main .block-container {
    max-width: 850px;
    padding: 2rem 1.5rem 3rem 1.5rem;
}

/* HEADER */

.header-box {
    background: linear-gradient(135deg, #172554 0%, #1d4ed8 55%, #3b82f6 100%);
    padding: 45px 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(30, 64, 175, 0.20);
}

.header-title {
    color: #ffffff;
    font-size: 32px;
    font-weight: 800;
    line-height: 1.4;
    margin-bottom: 15px;
}

.header-subtitle {
    color: #dbeafe;
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 12px;
}

.header-description {
    color: #ffffff;
    font-size: 15px;
    line-height: 1.6;
}

/* QUESTIONNAIRE CARD */

[data-testid="stForm"] {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

/* SECTION HEADINGS */

.section-heading {
    color: #1e40af;
    font-size: 21px;
    font-weight: 700;
    padding: 12px 0;
}

/* BUTTON */

div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 16px;
    font-weight: 700;
    width: 100%;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background: #1e40af;
    color: white;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SUPABASE CONNECTION
# ==========================================

try:

    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

    HEADERS = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

except Exception:

    st.error("Unable to connect to the survey system.")
    st.stop()


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header-box">

    <div class="header-title">
        🌙 Student Sleep &amp; Smartphone Survey
    </div>

    <div class="header-subtitle">
        Student Sleep &amp; Smartphone Analytics Research
    </div>

    <div class="header-description">
        Your participation helps us understand student sleep patterns.
    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# INTRODUCTION
# ==========================================

st.info("""
This questionnaire is designed for school students in Sri Lanka.

Please answer honestly.

Do not enter your name, phone number, school name
or other personally identifying information.
""")

st.warning("""
TEST MODE

Please use dummy information while testing.

Real research data collection must only begin after
obtaining the required research ethics approval,
school permission, parental consent and student assent.
""")


# ==========================================
# QUESTIONNAIRE
# ==========================================

st.header("📝 Student Questionnaire")

with st.form("student_survey_form"):

    # SECTION 01

    st.markdown(
        '<div class="section-heading">👤 Section 01 – Student Information</div>',
        unsafe_allow_html=True
    )

    age = st.number_input(
        "1. What is your age?",
        min_value=5,
        max_value=25,
        value=15
    )

    grade = st.selectbox(
        "2. What is your current grade?",
        ["Select Grade"] +
        [f"Grade {i}" for i in range(6, 14)]
    )

    school_type = st.selectbox(
        "3. What type of school do you attend?",
        [
            "Select School Type",
            "Government",
            "Private",
            "International",
            "Other"
        ]
    )

    st.divider()

    # SECTION 02

    st.markdown(
        '<div class="section-heading">📱 Section 02 – Smartphone Usage</div>',
        unsafe_allow_html=True
    )

    smartphone_use_daily = st.radio(
        "4. Do you use a smartphone daily?",
        ["Yes", "No"]
    )

    smartphone_hours_daily = st.selectbox(
        "5. Approximately how many hours do you use a smartphone daily?",
        [
            "Less than 1 hour",
            "1–2 hours",
            "3–4 hours",
            "5–6 hours",
            "More than 6 hours",
            "Not applicable"
        ]
    )

    smartphone_main_purpose = st.selectbox(
        "6. What is your main purpose for using a smartphone?",
        [
            "Select Purpose",
            "Education",
            "Social media",
            "Entertainment / Gaming",
            "Communication",
            "Other",
            "Not applicable"
        ]
    )

    smartphone_before_sleep = st.selectbox(
        "7. How often do you use your smartphone within one hour before sleeping?",
        [
            "Always",
            "Often",
            "Sometimes",
            "Rarely",
            "Never",
            "Not applicable"
        ]
    )

    st.divider()

    # SECTION 03

    st.markdown(
        '<div class="section-heading">😴 Section 03 – Sleep Patterns</div>',
        unsafe_allow_html=True
    )

    sleep_duration_school_night = st.selectbox(
        "8. How many hours do you usually sleep on school nights?",
        [
            "Less than 5 hours",
            "5–6 hours",
            "7–8 hours",
            "9–10 hours",
            "More than 10 hours"
        ]
    )

    sleep_quality = st.selectbox(
        "9. How would you describe your sleep quality?",
        [
            "Very good",
            "Good",
            "Average",
            "Poor",
            "Very poor"
        ]
    )

    st.divider()

    # SECTION 04

    st.markdown(
        '<div class="section-heading">☀️ Section 04 – Daytime Functioning</div>',
        unsafe_allow_html=True
    )

    daytime_sleepiness = st.selectbox(
        "10. How often do you feel sleepy during school hours?",
        [
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
            "Always"
        ]
    )

    concentration_difficulty = st.selectbox(
        "11. How often do you have difficulty concentrating during school hours?",
        [
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
            "Always"
        ]
    )

    daytime_tiredness = st.selectbox(
        "12. How often do you feel tired during the daytime?",
        [
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
            "Always"
        ]
    )

    st.divider()

    st.caption("Research Questionnaire | TEST Mode")

    submitted = st.form_submit_button(
        "🚀 Submit Questionnaire"
    )


# ==========================================
# SUPABASE DATA SUBMISSION
# ==========================================

if submitted:

    if grade == "Select Grade":

        st.warning("Please select your grade.")

    elif school_type == "Select School Type":

        st.warning("Please select your school type.")

    elif smartphone_use_daily == "Yes" and smartphone_main_purpose == "Select Purpose":

        st.warning("Please select your main smartphone usage purpose.")

    else:

        if smartphone_use_daily == "No":

            smartphone_hours_daily = "Not applicable"
            smartphone_main_purpose = "Not applicable"
            smartphone_before_sleep = "Not applicable"

        response_data = {
            "record_type": "TEST",
            "age": int(age),
            "grade": grade,
            "school_type": school_type,
            "smartphone_use_daily": smartphone_use_daily,
            "smartphone_hours_daily": smartphone_hours_daily,
            "smartphone_main_purpose": smartphone_main_purpose,
            "smartphone_before_sleep": smartphone_before_sleep,
            "sleep_duration_school_night": sleep_duration_school_night,
            "sleep_quality": sleep_quality,
            "daytime_sleepiness": daytime_sleepiness,
            "concentration_difficulty": concentration_difficulty,
            "daytime_tiredness": daytime_tiredness
        }

        try:

            with st.spinner("Submitting your response..."):

                response = requests.post(
                    f"{SUPABASE_URL}/rest/v1/student_responses",
                    headers=HEADERS,
                    json=response_data,
                    timeout=20
                )

            if response.status_code in (200, 201, 204):

                st.success(
                    "✅ Your response has been submitted successfully!"
                )

                st.balloons()

                st.info(
                    "Thank you for participating in the questionnaire!"
                )

            else:

                st.error("Unable to submit your response.")

                with st.expander("Technical Error Details"):

                    st.code(
                        f"Status: {response.status_code}\n"
                        f"{response.text[:500]}"
                    )

        except requests.exceptions.RequestException:

            st.error(
                "Connection problem. Please check your internet connection."
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div class="footer">

    🌙 Student Sleep &amp; Smartphone Analytics

    <br><br>

    Research Questionnaire | TEST Mode

</div>
""", unsafe_allow_html=True)