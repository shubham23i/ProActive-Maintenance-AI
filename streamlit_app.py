import streamlit as st

st.set_page_config(
    page_title="ProActive Maintenance AI",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 ProActive Maintenance AI")
st.subheader("Machine Failure Prediction System")

st.write(
    "Enter the machine sensor values below to predict the probability "
    "of machine failure."
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"]
    )

    air_temperature = st.number_input(
        "Air Temperature [K]",
        value=300.0
    )

    process_temperature = st.number_input(
        "Process Temperature [K]",
        value=310.0
    )

with col2:

    rotational_speed = st.number_input(
        "Rotational Speed [rpm]",
        value=1500
    )

    torque = st.number_input(
        "Torque [Nm]",
        value=40.0
    )

    tool_wear = st.number_input(
        "Tool Wear [min]",
        value=100
    )

st.divider()

if st.button("Predict Machine Failure", use_container_width=True):

    input_data = {
        "Type": machine_type,
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }

    try:
        with st.spinner("Analyzing machine data..."):

            from proactive_maintenance_ai.pipeline.prediction_pipeline import PredictionPipeline

            pipeline = PredictionPipeline()

            result = pipeline.start_prediction(input_data)

        prediction = result["prediction"]
        probability = result["failure_probability"]
        risk_level = result["risk_level"]

        st.divider()
        st.subheader("Prediction Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            if prediction == 1:
                st.error("⚠️ Machine Failure Predicted")
            else:
                st.success("✅ No Machine Failure Predicted")

        with col2:
            st.metric(
                "Failure Probability",
                f"{probability * 100:.2f}%"
            )

        with col3:
            st.metric(
                "Risk Level",
                risk_level
            )

        st.divider()
        st.subheader("Maintenance Recommendation")

        if risk_level == "HIGH":
            st.error(
                "⚠️ Immediate inspection is recommended. "
                "Schedule preventive maintenance as soon as possible."
            )

        elif risk_level == "MEDIUM":
            st.warning(
                "⚠️ Monitor the machine closely and schedule "
                "maintenance soon."
            )

        else:
            st.success(
                "✅ Machine condition appears normal. "
                "Continue regular monitoring and preventive maintenance."
            )

    except Exception as e:
        st.error("Prediction failed.")
        st.exception(e)