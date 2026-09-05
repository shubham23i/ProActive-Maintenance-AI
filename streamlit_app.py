import streamlit as st
import time
import pandas as pd
st.set_page_config(
    page_title="ProActive Maintenance AI",
    layout="wide"
)
# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

    .stApp {
        background-color: #081A33;
        color: #FFFFFF;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #061326;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    /* Main Title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 17px;
        color: #AFC1D6;
        margin-bottom: 30px;
    }

    /* Section Title */
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #FFFFFF;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    /* Caption */
    .stCaption {
        color: #AFC1D6;
    }

    /* Labels */
    label {
        color: #E8EEF6 !important;
    }

    /* Sensor Cards */
    .sensor-card {
        background-color: #0D2442;
        border: 1px solid #1D416B;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        margin-bottom: 10px;
    }

    .sensor-label {
        font-size: 12px;
        color: #8FA7C2;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .sensor-value {
        font-size: 24px;
        font-weight: 600;
        color: #FFFFFF;
        margin-top: 5px;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #0D2442;
        border: 1px solid #1D416B;
        border-radius: 8px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"] {
        color: #AFC1D6 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    /* Button */
    .stButton > button {
        background-color: #1D5FA7;
        color: white;
        border: none;
        border-radius: 6px;
        height: 48px;
        font-size: 16px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #2874C4;
        color: white;
        border: none;
    }

    /* Divider */
    hr {
        border-color: #1D416B !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #7792B0;
        font-size: 13px;
        padding-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown("## ProActive Maintenance AI")

    st.caption("Predictive Maintenance System")

    st.divider()

    st.markdown("### About")

    st.write(
        "Analyze machine sensor readings and estimate "
        "the probability of machine failure using machine learning."
    )

    st.divider()

    st.markdown("### Workflow")

    st.write("01   Enter sensor data")
    st.write("02   Analyze machine")
    st.write("03   Review risk assessment")

    st.divider()

    st.caption("Machine Learning Based System")


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="main-title">ProActive Maintenance AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Machine Failure Prediction and Risk Assessment'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">Machine Sensor Data</div>',
    unsafe_allow_html=True
)

st.caption(
    "Enter the current machine sensor readings. "
    "Use the information icon beside each field for details."
)

col1, col2 = st.columns(2)


with col1:

    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"],
        help="Machine quality category. L = Low, M = Medium, H = High. Unit: None."
    )

    air_temperature = st.number_input(
        "Air Temperature [K]",
        min_value=250.0,
        max_value=400.0,
        value=300.0,
        step=0.1,
        help="Temperature of the air surrounding the machine. Unit: Kelvin (K)."
    )

    process_temperature = st.number_input(
        "Process Temperature [K]",
        min_value=250.0,
        max_value=450.0,
        value=310.0,
        step=0.1,
        help="Temperature during the manufacturing process. Unit: Kelvin (K)."
    )


with col2:

    rotational_speed = st.number_input(
        "Rotational Speed [rpm]",
        min_value=0,
        max_value=10000,
        value=1500,
        step=1,
        help="Speed at which the machine component rotates. Unit: Revolutions per minute (rpm)."
    )

    torque = st.number_input(
        "Torque [Nm]",
        min_value=0.0,
        max_value=200.0,
        value=40.0,
        step=0.1,
        help="Rotational force generated by the machine. Unit: Newton metre (Nm)."
    )

    tool_wear = st.number_input(
        "Tool Wear [min]",
        min_value=0,
        max_value=500,
        value=100,
        step=1,
        help="Accumulated operating time representing tool wear. Unit: Minutes (min)."
    )

# ---------------------------------------------------
# PREDICTION
# ---------------------------------------------------

if st.button(
    "Analyze Machine",
    use_container_width=True,
    type="primary"
):

    input_data = {
        "Type": machine_type,
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }

    try:

        status = st.empty()

        status.info("Initializing prediction engine...")
        time.sleep(0.5)

        status.info("Processing sensor readings...")
        time.sleep(0.5)

        status.info("Evaluating machine failure patterns...")
        time.sleep(0.5)

        status.info("Calculating failure probability...")
        time.sleep(0.5)

        with st.spinner("Generating final assessment..."):

            from proactive_maintenance_ai.pipeline.prediction_pipeline import (
                PredictionPipeline
            )

            pipeline = PredictionPipeline()

            result = pipeline.start_prediction(input_data)

        status.empty()


        # ---------------------------------------------------
        # RESULTS
        # ---------------------------------------------------

        prediction = result["prediction"]
        probability = result["failure_probability"]
        risk_level = result["risk_level"]
        # Save prediction to history
        st.session_state.prediction_history.append({
            "Machine Type": machine_type,
            "Failure Probability": f"{probability * 100:.2f}%",
            "Risk Level": risk_level,
            "Prediction": (
                "Failure Predicted"
                if prediction == 1
                else "Operating Normally"
            )
        })


        st.divider()

        st.markdown(
            '<div class="section-title">Analysis Results</div>',
            unsafe_allow_html=True
        )


        result_col1, result_col2, result_col3 = st.columns(3)


        with result_col1:

            status_text = (
                "Failure Predicted"
                if prediction == 1
                else "Operating Normally"
            )

            st.metric(
                "Machine Status",
                status_text
            )


        with result_col2:

            st.metric(
                "Failure Probability",
                f"{probability * 100:.2f}%"
            )


        with result_col3:

            st.metric(
                "Risk Assessment",
                risk_level
            )


        # ---------------------------------------------------
        # FAILURE RISK LEVEL
        # ---------------------------------------------------

        st.markdown(
            '<div class="section-title">Failure Risk Level</div>',
            unsafe_allow_html=True
        )

        probability_percentage = float(probability) * 100

        # Prevent value from going below 0 or above 100
        probability_percentage = max(0, min(probability_percentage, 100))

        # Traffic light colors
        if probability_percentage < 30:
            risk_color = "#22C55E"
            risk_text = "LOW RISK"

        elif probability_percentage < 60:
            risk_color = "#EAB308"
            risk_text = "MEDIUM RISK"

        else:
            risk_color = "#EF4444"
            risk_text = "HIGH RISK"


        # Display percentage and risk
        st.markdown(
            f"<p style='color:{risk_color}; font-size:18px; font-weight:600;'>"
            f"{probability_percentage:.2f}% | {risk_text}"
            f"</p>",
            unsafe_allow_html=True
        )

        # Traffic-light risk bar
        st.markdown(
            f"""
            <div style="width:100%; height:14px; background:#061326;
                        border-radius:10px; overflow:hidden;">
                <div style="width:{probability_percentage}%; height:100%;
                            background:{risk_color}; border-radius:10px;">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Green: 0–30%     |     Yellow: 30–60%     |     Red: 60–100%")


        # ---------------------------------------------------
        # EXPANDABLE DETAILS
        # ---------------------------------------------------

        with st.expander("View Detailed Analysis"):

            st.write("Input Sensor Readings")

            st.dataframe(
                {
                    "Parameter": [
                        "Machine Type",
                        "Air Temperature",
                        "Process Temperature",
                        "Rotational Speed",
                        "Torque",
                        "Tool Wear"
                    ],
                    "Value": [
                        machine_type,
                        f"{air_temperature} K",
                        f"{process_temperature} K",
                        f"{rotational_speed} rpm",
                        f"{torque} Nm",
                        f"{tool_wear} min"
                    ]
                },
                use_container_width=True,
                hide_index=True
            )

            st.write("Prediction Summary")

            st.dataframe(
                {
                    "Metric": [
                        "Prediction",
                        "Failure Probability",
                        "Risk Level"
                    ],
                    "Result": [
                        status_text,
                        f"{probability_percentage:.2f}%",
                        risk_level
                    ]
                },
                use_container_width=True,
                hide_index=True
            )


    except Exception as e:

        st.error("The prediction could not be completed.")

        st.exception(e)


    # ---------------------------------------------------
    # MACHINE HEALTH SCORE
    # ---------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-title">Machine Health Score</div>',
        unsafe_allow_html=True
    )

    health_score = 100 - probability_percentage

    if health_score >= 80:
        health_status = "EXCELLENT"
    elif health_score >= 60:
        health_status = "GOOD"
    elif health_score >= 40:
        health_status = "MODERATE"
    else:
        health_status = "CRITICAL"


    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            "Health Score",
            f"{health_score:.1f} / 100"
        )

    with col2:
        st.write(f"**Machine Condition: {health_status}**")

        st.progress(
            int(health_score),
            text=f"Overall machine health: {health_score:.1f}%"
        )

# ---------------------------------------------------
# PREDICTION HISTORY
# ---------------------------------------------------

if st.session_state.prediction_history:

    st.divider()

    st.markdown(
        '<div class="section-title">Prediction History</div>',
        unsafe_allow_html=True
    )

    history_df = pd.DataFrame(
        st.session_state.prediction_history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("Clear History"):
        st.session_state.prediction_history = []
        st.rerun()

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.markdown(
    '<div class="footer">'
    'ProActive Maintenance AI | Predictive Maintenance System | 2026'
    '</div>',
    unsafe_allow_html=True
)