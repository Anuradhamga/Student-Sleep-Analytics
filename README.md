# 📱 Student Sleep & Smartphone Analytics

### Investigating the Association Between Smartphone Usage Patterns, Sleep Quality and Daytime Functioning Among School Students in Sri Lanka Using Machine Learning

---

## 📌 Project Overview

Student Sleep & Smartphone Analytics is a research-oriented data science project that investigates the relationship between smartphone usage patterns, sleep quality, and daytime functioning among school students in Sri Lanka.

The system combines web-based data collection, cloud database technology, data analytics, statistical analysis, and machine learning to identify meaningful patterns associated with students' sleep health and smartphone usage habits.

The project includes a public data collection form and a secure administrator dashboard for monitoring and managing submitted responses.

## 🎯 Research Objectives

- Analyze smartphone usage patterns among school students in Sri Lanka.
- Investigate the association between smartphone usage and sleep quality.
- Examine the relationship between sleep quality and daytime functioning.
- Identify factors associated with poor sleep quality.
- Apply machine learning techniques to explore predictive patterns.
- Generate data-driven insights to support student sleep health awareness.

## 🛠️ Technologies & Tools

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application development |
| Supabase | Cloud database and authentication |
| Pandas | Data manipulation |
| NumPy | Numerical computing |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive charts |
| SciPy | Statistical analysis |
| Statsmodels | Statistical modeling |
| Scikit-learn | Machine learning |
| Jupyter Notebook | Research and experimentation |
| OpenPyXL | Excel data export |
| Git & GitHub | Version control |
| Streamlit Community Cloud | Application deployment |

## 🏗️ System Architecture

The project consists of three main components.

### 1. Public Data Collection Form

- Web-based student data collection interface.
- Accessible through mobile phones and computers.
- Collects responses through an online form.
- Submits responses to the Supabase database.

### 2. Supabase Cloud Database

- Stores submitted responses.
- Provides cloud database connectivity.
- Uses Row Level Security (RLS) policies to control data access.
- Supports separate handling of test and research records.

### 3. Admin Dashboard

- Secure administrator login.
- Displays submitted responses.
- Provides response summaries and analytics.
- Generates interactive visualizations.
- Supports CSV and Excel data exports.

## 🔬 Research Methodology

The research will follow these main stages:

1. Research Design
2. Data Collection
3. Data Cleaning and Preprocessing
4. Exploratory Data Analysis (EDA)
5. Statistical Analysis
6. Feature Engineering
7. Machine Learning Model Development
8. Model Evaluation
9. Research Findings and Interpretation

## 🤖 Machine Learning Approaches

Potential machine learning techniques include:

- Linear Regression
- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- XGBoost

Final model selection will depend on the research questions, dataset characteristics, and evaluation results.

## 📊 Expected Outcomes

- Identification of smartphone usage patterns.
- Understanding of sleep quality-related factors.
- Analysis of daytime functioning patterns.
- Machine learning-based predictive insights.
- Research findings relevant to student sleep health in Sri Lanka.

## 📁 Project Structure

```text
Student-Sleep-Analytics/
│
├── src/
│   └── data_collection/
│       ├── public_form.py
│       └── admin_dashboard.py
│
├── dataset/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── 01_initial_data_exploration.ipynb
│
├── results/
│
├── .streamlit/
│   └── secrets.toml
│
├── requirements.txt
├── .gitignore
└── README.md
```

Note: The local `secrets.toml` file is excluded from GitHub and must never be committed.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Anuradhamga/Student-Sleep-Analytics.git
```

### 2. Navigate to the Project Folder

```bash
cd Student-Sleep-Analytics
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Supabase Configuration

The applications use Supabase credentials for database connectivity.

For local development, create a file named:

`.streamlit/secrets.toml`

Add the following configuration:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_PUBLIC_KEY"
```

For cloud deployment, configure the required credentials through the Streamlit Community Cloud application Secrets settings.

**Security Notice:**

- Never upload `secrets.toml` to GitHub.
- Never expose database passwords or service-role keys.
- Keep administrator credentials confidential.
- Maintain appropriate database access policies.

## 🚀 Running the Applications

### Public Data Collection Form

```bash
python -m streamlit run src/data_collection/public_form.py
```

### Admin Dashboard

```bash
python -m streamlit run src/data_collection/admin_dashboard.py
```

## 🌐 Cloud Deployment

The applications are deployed using Streamlit Community Cloud.

### Public Data Collection Form

## 🌐 Cloud Deployment

The applications are deployed using Streamlit Community Cloud.

### Public Data Collection Form

[Open Public Data Collection Form](https://student-sleep-analytics-mnyk3gxjsyaipnhny5v8fp.streamlit.app/)

### Admin Dashboard

[Open Admin Dashboard](https://student-sleep-analytics-5ofor3c6b9rvgy542g8jnw.streamlit.app/)
## 🧪 System Testing

The following components have been tested:

- Public form accessibility using a mobile device.
- Form submission functionality.
- Supabase database insertion.
- Administrator authentication.
- Admin dashboard response display.
- Analytics and visualizations.
- CSV export functionality.
- Excel export functionality.
- Cloud application deployment.

## 🔐 Ethical Considerations

- Student privacy and confidentiality will be protected.
- Appropriate ethical approvals and institutional permissions must be maintained.
- Parental consent and student assent will be obtained where applicable.
- Personal identifying information will not be published.
- Research data will be handled responsibly.
- Machine learning predictions will not be presented as medical diagnoses.
- Test records will be kept separate from actual research records.

## 📌 Project Status

**Status: System Development and Testing Completed – Research Data Collection Preparation Pending**

The initial web-based data collection system, Supabase database integration, and administrator dashboard have been implemented and tested.

The next stages include final research preparation, authorized data collection, data preprocessing, statistical analysis, and machine learning model development.

## 👨‍💻 Researcher

**M.G. Akitha Anuradha**

BHSc (Hons) in Health Information and Communication Technology (HICT)

Gampaha Wickramarachchi University of Indigenous Medicine

Sri Lanka

GitHub: [Anuradhamga](https://github.com/Anuradhamga)

## 📜 License

This project is intended for academic and research purposes.

---

⭐ If you find this project interesting, feel free to explore and follow its development.