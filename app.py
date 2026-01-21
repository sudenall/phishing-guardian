import streamlit as st
import pandas as pd
import os
from src.predict_xai import explain_email

st.set_page_config(layout="wide")

# ===== CUSTOM STYLE =====
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #2E86C1;
        color: white;
        border-radius: 10px;
        font-size: 16px;
    }
    h1, h2, h3 {
        color: #1F618D;
    }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR DESIGN =====

st.sidebar.title("🛡️ Phishing Guardian")

st.sidebar.markdown("""
**Research Dashboard**

- Email Analysis  
- Model Comparison  
- Explainable AI  
- Real World Testing  
""")

st.sidebar.info("Computer Engineering Project")

menu = st.sidebar.selectbox(
    "Navigation Menu",
    [
        "Home",
        "Email Test",
        "Model Comparison (V1 vs V2)",
        "Enron Analysis",
        "Datasets & CSV Outputs"
    ]
)

base = os.path.dirname(__file__)

# ===== EXPLAIN FUNCTION FOR STREAMLIT =====

def streamlit_explain(email_text):
    result, prob, explanation = explain_email(email_text)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Result")
        st.metric("Decision", result)
        st.metric("Risk Score", f"{prob * 100:.2f}%")

    with col2:
        st.subheader("Interpretation")
        if result == "PHISHING":
            st.error("This email is likely to be PHISHING.")
        else:
            st.success("This email appears to be SAFE.")

    st.subheader("XAI Explanation (Text)")

    safe = [e for e in explanation if e[2] < 0]
    phishing = [e for e in explanation if e[2] > 0]

    if safe:
        st.write("### Factors supporting SAFE:")
        for feat, val, imp in safe:
            st.write(f"- {feat} = {val}  (impact: {imp:.4f})")

    if phishing:
        st.write("### Factors pushing to PHISHING:")
        for feat, val, imp in phishing:
            st.write(f"- {feat} = {val}  (impact: +{imp:.4f})")

    # ====== NEW VISUALIZATION PART ======

    st.subheader("XAI Impact Visualization")

    # explanation list: (feature, value, impact)
    df = pd.DataFrame(explanation, columns=["Feature", "Value", "Impact"])

    # Sort by impact size
    df = df.sort_values(by="Impact", ascending=False)

    st.write("### Feature Impact Chart")

    st.bar_chart(data=df.set_index("Feature")["Impact"])

    st.markdown("""
    **How to read this chart:**

    - Values ABOVE zero push the decision toward **PHISHING**
    - Values BELOW zero push the decision toward **SAFE**
    - The longer the bar, the stronger the influence
    """)

# ================== HOME PAGE ==================

if menu == "Home":

    st.title("Phishing Guardian – Research Dashboard")

    st.markdown("""
    ### Welcome

    This platform demonstrates a complete phishing detection research project.

    **Capabilities:**
    - Test emails  
    - Compare models  
    - Analyze Enron dataset  
    - Review training data  
    - Download research outputs  
    """)

    st.success("Navigate using the menu on the left.")


# ================== EMAIL TEST ==================

elif menu == "Email Test":
    st.header("📧 Email Analysis Module")

    st.markdown("### Try Example Emails")

    examples = {
        "Select...": "",

        # -------- PHISHING EXAMPLES --------

        "Bank Account Phishing": """
        Dear Customer,

        We detected unusual activity in your bank account.
        Please verify your identity immediately using the link below:

        http://secure-bank-login.verify-now.com

        Failure to do so will result in account suspension.

        Regards,
        Bank Security Team
        """,

        "Urgent Invoice Scam": """
        Hello,

        Please find attached your unpaid invoice.
        Immediate payment is required to avoid legal action.

        Pay now at:
        http://payment-portal.fake/pay

        Thank you
        Accounting Department
        """,

        "Payroll Update Required": """
        ATTENTION!

        Your payroll information is outdated.
        You must update your banking details TODAY.

        Click here to update:
        http://hr-payroll-update.fake

        Failure to update will delay your salary.
        """,

        "Lottery Winner Scam": """
        Congratulations!!!

        You have been selected as a WINNER of $1,000,000 USD!!!

        Claim your prize immediately:
        http://lottery-winner-claim.fake

        Act fast before offer expires!!!
        """,

        "Microsoft Account Alert": """
        Security Alert!!!

        We detected suspicious login attempts on your Microsoft account.

        Verify now or your account will be LOCKED:

        http://microsoft-security.fake

        Microsoft Security Team
        """,

        # -------- SAFE EXAMPLES --------

        "Normal Business Email": """
        Hi Team,

        Please be informed that the weekly project meeting will be held tomorrow at 10 AM.

        The agenda and documents are attached to this email.

        Best regards,
        Project Coordinator
        """,

        "Academic Notification": """
        Dear Students,

        This is a reminder that the assignment submission deadline is next Friday.

        Please upload your work to the university portal before 17:00.

        Kind regards,
        Course Instructor
        """,

        "HR Announcement": """
        Hello Everyone,

        The company picnic will be held next Saturday at Central Park.
        Families are welcome to attend.

        Please RSVP by Friday.

        Regards,
        Human Resources
        """,

        "Meeting Invitation": """
        Dear Colleagues,

        You are invited to the quarterly planning meeting on Monday.

        Location: Conference Room A
        Time: 14:00

        Best,
        Management
        """,

        "Customer Support Reply": """
        Hello,

        Thank you for contacting support.
        Your issue has been resolved successfully.

        Please let us know if you need further assistance.

        Kind regards,
        Support Team
        """,

        # -------- BORDERLINE / MIXED --------

        "Suspicious but Legit": """
        Dear User,

        We noticed a new login to your account from a new device.

        If this was you, you can safely ignore this message.

        Regards,
        Security Notifications
        """,

        "Generic Promotion": """
        Big Discounts Available Now!

        Visit our official website for seasonal offers.

        Thank you for being our valued customer.
        """
    }

    selected = st.selectbox("Choose Example Email", list(examples.keys()))

    default_email = examples[selected]

    email = st.text_area("Enter email text", value=default_email, height=320)

    if st.button("Analyze Email"):
        if email.strip():
            streamlit_explain(email)
        else:
            st.warning("Please enter an email text.")


# =============== MODEL COMPARISON ===============

elif menu == "Model Comparison (V1 vs V2)":
    st.header("📊 Model Performance Comparison")

    st.subheader("Key Performance Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("V1 Accuracy", "74%")
    col2.metric("V2 Accuracy", "88%")
    col3.metric("Improvement", "+14%")

    st.subheader("Confusion Matrices")

    col1, col2 = st.columns(2)

    with col1:
        st.image(os.path.join(base, "outputs", "confusion_matrix.png"))
        st.caption("Confusion Matrix – V1")

    with col2:
        st.image(os.path.join(base, "outputs", "confusion_matrix_v2.png"))
        st.caption("Confusion Matrix – V2")

    st.subheader("ROC Curve Comparison")

    col3, col4 = st.columns(2)

    with col3:
        st.image(os.path.join(base, "outputs", "roc_curve_v1.png"))
        st.caption("ROC Curve – V1")

    with col4:
        st.image(os.path.join(base, "outputs", "roc_curve_v2.png"))
        st.caption("ROC Curve – V2")

    st.subheader("Feature Importance Comparison")

    col5, col6 = st.columns(2)

    with col5:
        st.image(os.path.join(base, "outputs", "feature_importance.png"))
        st.caption("Base Features (V1)")

    with col6:
        st.image(os.path.join(base, "outputs", "feature_importance_v2.png"))
        st.caption("Extended Features (V2)")

    st.expander("What do these graphs mean?").markdown("""
    - **Confusion Matrix:** shows correct and incorrect classifications  
    - **ROC Curve:** indicates model discrimination ability  
    - **Feature Importance:** shows which features most affect predictions  
    """)


# ================== ENRON ANALYSIS ==================

elif menu == "Enron Analysis":
    st.header("📂 Enron Dataset Analysis")

    st.subheader("Prediction Overview")

    st.image(os.path.join(base, "outputs", "enron_pie_chart.png"))

    st.subheader("Risk Score Distribution")
    st.image(os.path.join(base, "outputs", "enron_risk_distribution.png"))

    st.subheader("High Risk Mail Ratio")
    st.image(os.path.join(base, "outputs", "high_risk_ratio.png"))

    st.subheader("Interactive Exploration")

    pred_path = os.path.join(base, "outputs", "enron_predictions.csv")

    if os.path.exists(pred_path):
        df = pd.read_csv(pred_path)

        st.write("### Filter by Risk Score")

        threshold = st.slider("Risk Score Threshold", 0.0, 1.0, 0.8)

        filtered = df[df["risk_score"] > threshold]

        st.write(f"Mails above threshold: {len(filtered)}")

        st.dataframe(filtered.head(200))

        st.subheader("📋 Preview: First 500000 Enron Predictions")

        st.dataframe(df.head(500000))

    else:
        st.warning("Run Enron prediction script first.")



# ================== DATASETS & CSV ==================

elif menu == "Datasets & CSV Outputs":
    st.header("📁 Datasets and Research Outputs")

    options = {
        "Training Dataset – Raw Cleaned Data": "data/labeled/clean_phishing.csv",
        "Training Dataset – Extracted Features": "data/labeled/features_v2.csv",
        "Enron Predictions": "outputs/enron_predictions.csv",
        "Most Risky Mails": "outputs/most_risky_mails.csv",
        "High Risk Mails": "outputs/high_risk_mails.csv",
        "Enron XAI Reports": "outputs/enron_xai_reports.csv"
    }

    descriptions = {
        "Training Dataset – Raw Cleaned Data":
            "Original labeled dataset used for training. Contains email text and labels (SAFE / PHISHING).",

        "Training Dataset – Extracted Features":
            "Dataset after feature engineering. Contains numerical features used by the machine learning model.",

        "Enron Predictions":
            "Results of running the trained model on the entire Enron email corpus. Includes risk scores.",

        "Most Risky Mails":
            "Top 100 emails with the highest phishing probability scores from Enron dataset.",

        "High Risk Mails":
            "All Enron emails with risk score above 0.8 threshold.",

        "Enron XAI Reports":
            "Explainable AI outputs showing which features influenced each prediction."
    }

    choice = st.selectbox("Select Dataset", list(options.keys()))

    st.info(descriptions[choice])

    path = os.path.join(base, options[choice])

    if os.path.exists(path):
        df = pd.read_csv(path)

        st.subheader("Dataset Preview")
        st.dataframe(df.head(200))

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download CSV File",
            data=csv,
            file_name=os.path.basename(path),
            mime="text/csv"
        )

    else:
        st.warning("Selected file not found.")
