import streamlit as st

st.set_page_config(
    page_title="ProActive Maintenance AI",
    layout="wide"
)


# Custom CSS
st.markdown("""
<style>

    /* Main Background */
    .stApp {
        background-color: #081A33;
        color: #FFFFFF;
    }

    /* Main Container */
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
        color: #B8C7D9;
        margin-bottom: 30px;
    }

    /* Section Title */
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 5px;
    }

    /* Caption */
    .stCaption {
        color: #B8C7D9;
    }

    /* Labels */
    label {
        color: #EAF0F8 !important;
        font-weight: 500 !important;
    }

    /* Input Fields */
    .stSelectbox > div > div,
    .stNumberInput input {
        border-radius: 6px !important;
    }

    /* Button */
    .stButton > button {
        background-color: #1E5AA8;
        color: white;
        border: 1px solid #2E6FC2;
        border-radius: 6px;
        height: 48px;
        font-size: 16px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #2E6FC2;
        border: 1px solid #4A8FE7;
        color: white;
    }

    /* Divider */
    hr {
        border-color: #25466D !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #0D2442;
        border: 1px solid #25466D;
        border-radius: 8px;
        padding: 15px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8FA7C2;
        font-size: 13px;
        padding-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:

    st.markdown("## ProActive Maintenance AI")

    st.caption("Predictive Maintenance System")

    st.divider()

    st.markdown("### About")

    st.write(
        "Analyze machine sensor data and estimate "
        "the probability of machine failure."
    )

    st.divider()

    st.markdown("### Workflow")

    st.write("01  Enter sensor data")
    st.write("02  Analyze machine")
    st.write("03  Review results")

    st.divider()

    st.caption("Machine Learning Based System")


# Header
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


# Input Section
st.markdown(
    '<div class="section-title">Machine Sensor Data</div>',
    unsafe_allow_html=True
)



col1, col2 = st.columns(2)


with col1:

    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"],
        help="""
        Machine quality category.

        L = Low quality
        M = Medium quality
        H = High quality

        Unit: No unit (categorical value)
        """
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
        help="Temperature measured during the machine process or operation. Unit: Kelvin (K)."
    )


with col2:

    rotational_speed = st.number_input(
        "Rotational Speed [rpm]",
        min_value=0,
        max_value=10000,
        value=1500,
        step=1,
        help="Speed at which the machine component rotates. Unit: Revolutions Per Minute (rpm)."
    )

    torque = st.number_input(
        "Torque [Nm]",
        min_value=0.0,
        max_value=200.0,
        value=40.0,
        step=0.1,
        help="Rotational force produced by the machine. Unit: Newton-metre (Nm)."
    )

    tool_wear = st.number_input(
        "Tool Wear [min]",
        min_value=0,
        max_value=500,
        value=100,
        step=1,
        help="Total operating time representing the wear accumulated by the tool. Unit: Minutes (min)."
    )


st.divider()


# Prediction
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

        with st.spinner("Analyzing machine condition..."):

            from proactive_maintenance_ai.pipeline.prediction_pipeline import (
                PredictionPipeline
            )

            pipeline = PredictionPipeline()

            result = pipeline.start_prediction(input_data)


        prediction = result["prediction"]
        probability = result["failure_probability"]
        risk_level = result["risk_level"]


        st.divider()

        st.markdown(
            '<div class="section-title">Analysis Results</div>',
            unsafe_allow_html=True
        )

        result_col1, result_col2, result_col3 = st.columns(3)


        with result_col1:

            status = (
                "Failure Predicted"
                if prediction == 1
                else "Operating Normally"
            )

            st.metric(
                "Machine Status",
                status
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


        st.divider()

        st.markdown(
            '<div class="section-title">Maintenance Recommendation</div>',
            unsafe_allow_html=True
        )


        if risk_level == "HIGH":

            st.error(
                "Immediate inspection is recommended. "
                "Schedule preventive maintenance as soon as possible."
            )

        elif risk_level == "MEDIUM":

            st.warning(
                "Monitor the machine closely and schedule "
                "maintenance soon."
            )

        else:

            st.success(
                "Machine condition appears normal. "
                "Continue regular monitoring and preventive maintenance."
            )


    except Exception as e:

        st.error("The prediction could not be completed.")
        st.exception(e)


# Footer
st.divider()

st.markdown(
    '<div class="footer">'
    'ProActive Maintenance AI | Predictive Maintenance System | 2026'
    '</div>',
    unsafe_allow_html=True
)