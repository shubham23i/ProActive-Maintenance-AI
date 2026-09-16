import requests
import streamlit as st
import plotly.graph_objects as go


st.set_page_config(
    page_title="ProActive Maintenance AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000/predict"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #061637 0%,
            #071A49 50%,
            #09245C 100%
        );
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* HEADER */

    .header {
        background: linear-gradient(135deg, #0B2257, #09245C);
        border: 1px solid rgba(242, 140, 40, 0.35);
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 30px;
    }

    .header-title {
        color: #FFF4E8;
        font-size: 34px;
        font-weight: 800;
        margin: 0;
    }

    .header-subtitle {
        color: #B9C9E3;
        font-size: 14px;
        margin-top: 6px;
    }

    .status {
        display: inline-block;
        margin-top: 15px;
        padding: 7px 14px;
        border-radius: 30px;
        background: rgba(59, 196, 122, 0.12);
        border: 1px solid rgba(59, 196, 122, 0.35);
        color: #7DE2A5;
        font-size: 11px;
        font-weight: 800;
    }

    /* SECTIONS */

    .section-title {
        color: #FFF4E8;
        font-size: 20px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #B9C9E3;
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* CARDS */

    .card {
        background: #C8754B;
        border-radius: 20px;
        padding: 20px;
        min-height: 110px;
        border: 1px solid rgba(255,255,255,0.12);
    }

    .card-title {
        color: #FFE9D5;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .card-value {
        color: #FFFFFF;
        font-size: 27px;
        font-weight: 800;
        margin-top: 6px;
    }

    .card-description {
        color: #FFE1CC;
        font-size: 11px;
        margin-top: 4px;
    }

    /* RISK */

    .risk-card {
        background: rgba(9, 36, 92, 0.75);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .risk-feature {
        color: #FFF4E8;
        font-size: 13px;
        font-weight: 700;
    }

    .risk-impact {
        color: #FFE2C9;
        font-size: 11px;
        margin-top: 5px;
    }

    .risk-up {
        color: #FFD0B0;
        font-weight: 800;
    }

    .risk-down {
        color: #D8F4E3;
        font-weight: 800;
    }

    /* SENSOR */

    .sensor-card {
        background: rgba(9, 36, 92, 0.70);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 14px;
        margin-bottom: 10px;
    }

    .sensor-name {
        color: #FFE5D2;
        font-size: 11px;
        font-weight: 700;
    }

    .sensor-value {
        color: #FFFFFF;
        font-size: 17px;
        font-weight: 800;
        margin-top: 3px;
    }

    /* MAINTENANCE */

    .maintenance-card {
        background: rgba(9, 36, 92, 0.70);
        border: 1px solid rgba(242, 140, 40, 0.25);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .maintenance-label {
        color: #FFE1C9;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .maintenance-value {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: 800;
        margin-top: 5px;
    }

    .maintenance-text {
        color: #E5ECF7;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 8px;
    }

    /* RECOMMENDATION */

    .recommendation {
        background: linear-gradient(135deg, #0B2257, #09245C);
        border: 1px solid rgba(242, 140, 40, 0.38);
        border-radius: 20px;
        padding: 22px;
        margin-top: 15px;
    }

    .recommendation-title {
        color: #F5A623;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .recommendation-text {
        color: #FFF4E8;
        font-size: 14px;
        line-height: 1.5;
        margin-top: 8px;
    }

    /* BUTTON */

    .stButton > button {
        background: #C8754B;
        color: #FFFFFF;
        border: none;
        border-radius: 12px;
        padding: 10px 25px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        background: #E08A58;
        color: #FFFFFF;
    }

    /* INPUTS */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #0B2257;
        border-color: rgba(242, 140, 40, 0.35);
    }

    label {
        color: #E5ECF7 !important;
    }

    /* FOOTER */

    .footer {
        text-align: center;
        color: #91A5C7;
        font-size: 11px;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="header">

        <div class="header-title">
            ⚙ ProActive Maintenance AI
        </div>

        <div class="header-subtitle">
            Real-time Equipment Failure Risk & Diagnostics Dashboard
        </div>

        <div class="status">
            ● API ENDPOINT ACTIVE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MACHINE PARAMETERS
# =========================================================

st.markdown(
    '<div class="section-title">Machine Parameters</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Enter the current machine sensor readings to evaluate failure risk.</div>',
    unsafe_allow_html=True
)


row1 = st.columns(3)

with row1[0]:
    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"]
    )

with row1[1]:
    air_temperature = st.number_input(
        "Air Temperature [K]",
        min_value=250.0,
        max_value=350.0,
        value=298.0,
        step=0.1
    )

with row1[2]:
    process_temperature = st.number_input(
        "Process Temperature [K]",
        min_value=250.0,
        max_value=400.0,
        value=308.0,
        step=0.1
    )


row2 = st.columns(3)

with row2[0]:
    rotational_speed = st.number_input(
        "Rotational Speed [rpm]",
        min_value=500.0,
        max_value=3000.0,
        value=1500.0,
        step=10.0
    )

with row2[1]:
    torque = st.number_input(
        "Torque [Nm]",
        min_value=0.0,
        max_value=100.0,
        value=40.0,
        step=0.5
    )

with row2[2]:
    tool_wear = st.number_input(
        "Tool Wear [min]",
        min_value=0.0,
        max_value=300.0,
        value=100.0,
        step=1.0
    )


# Center button

left, center, right = st.columns([2, 1, 2])

with center:
    analyze = st.button(
        "ANALYZE MACHINE",
        use_container_width=True
    )


# =========================================================
# PREDICTION
# =========================================================

if analyze:

    input_data = {
        "Type": machine_type,
        "Air_temperature_K": air_temperature,
        "Process_temperature_K": process_temperature,
        "Rotational_speed_rpm": rotational_speed,
        "Torque_Nm": torque,
        "Tool_wear_min": tool_wear
    }

    try:

        with st.spinner("Analyzing machine condition..."):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=120
            )

        if response.status_code != 200:
            st.error(f"Prediction failed: {response.text}")
            st.stop()

        result = response.json()

        probability = float(
            result.get("failure_probability", 0)
        )

        probability_percent = probability * 100

        risk_level = result.get(
            "risk_level",
            "UNKNOWN"
        )

        maintenance_priority = result.get(
            "maintenance_priority",
            "UNKNOWN"
        )

        recommended_action = result.get(
            "recommended_action",
            "No recommendation available."
        )

        inspection_window = result.get(
            "inspection_window",
            "Not specified"
        )

        anomaly_status = result.get(
            "anomaly_status",
            "NORMAL"
        )

        anomaly_score = float(
            result.get("anomaly_score", 0)
        )

        top_risk_factors = result.get(
            "top_risk_factors",
            []
        )


        # =================================================
        # MACHINE INTELLIGENCE
        # =================================================

        st.markdown(
            '<div class="section-title">Machine Intelligence</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # KPI CARDS
        # =================================================

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">Failure Risk</div>
                    <div class="card-value">{probability_percent:.2f}%</div>
                    <div class="card-description">Predicted probability</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k2:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">Risk Level</div>
                    <div class="card-value">{risk_level}</div>
                    <div class="card-description">Machine condition</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k3:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">Maintenance</div>
                    <div class="card-value">{maintenance_priority}</div>
                    <div class="card-description">Recommended priority</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k4:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">Anomaly</div>
                    <div class="card-value">{anomaly_status}</div>
                    <div class="card-description">Sensor detection</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        st.write("")


        # =================================================
        # FAILURE RISK / RISK FACTORS
        # =================================================

        chart_col, risk_col = st.columns(2)


        with chart_col:

            st.markdown(
                '<div class="section-title">Failure Risk</div>',
                unsafe_allow_html=True
            )

            if probability_percent < 30:
                gauge_color = "#3BC47A"
            elif probability_percent < 70:
                gauge_color = "#F5A623"
            else:
                gauge_color = "#E45756"

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=probability_percent,
                    number={
                        "suffix": "%",
                        "font": {
                            "size": 30,
                            "color": "#FFF4E8"
                        }
                    },
                    title={
                        "text": "FAILURE RISK",
                        "font": {
                            "size": 13,
                            "color": "#FFF4E8"
                        }
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100],
                            "tickcolor": "#B9C9E3"
                        },
                        "bar": {
                            "color": gauge_color
                        },
                        "bgcolor": "#09245C",
                        "borderwidth": 0,
                        "steps": [
                            {
                                "range": [0, 30],
                                "color": "#194A48"
                            },
                            {
                                "range": [30, 70],
                                "color": "#69522B"
                            },
                            {
                                "range": [70, 100],
                                "color": "#66383B"
                            }
                        ]
                    }
                )
            )

            fig.update_layout(
                height=290,
                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=15
                ),
                paper_bgcolor="#C8754B"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )


        with risk_col:

            st.markdown(
                '<div class="section-title">Top Risk Factors</div>',
                unsafe_allow_html=True
            )

            if top_risk_factors:

                for item in top_risk_factors:

                    feature = item.get(
                        "feature",
                        "Unknown"
                    )

                    impact = float(
                        item.get("impact", 0)
                    )

                    direction = item.get(
                        "direction",
                        ""
                    )

                    direction_class = (
                        "risk-up"
                        if impact >= 0
                        else "risk-down"
                    )

                    st.markdown(
                        f"""
                        <div class="risk-card">

                            <div class="risk-feature">
                                {feature}
                            </div>

                            <div class="risk-impact">
                                Impact:
                                <span class="{direction_class}">
                                    {impact:+.4f}
                                </span>
                                &nbsp; | &nbsp;
                                {direction}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info("No major risk factors detected.")


        # =================================================
        # MACHINE PROFILE
        # =================================================

        st.markdown(
            '<div class="section-title">Machine Profile</div>',
            unsafe_allow_html=True
        )

        profile_values = [
            ("Machine Type", machine_type),
            ("Air Temperature", f"{air_temperature:.1f} K"),
            ("Process Temperature", f"{process_temperature:.1f} K"),
            ("Rotational Speed", f"{rotational_speed:.0f} rpm"),
            ("Torque", f"{torque:.1f} Nm"),
            ("Tool Wear", f"{tool_wear:.0f} min")
        ]

        profile_cols = st.columns(6)

        for i, (name, value) in enumerate(profile_values):

            with profile_cols[i]:

                st.markdown(
                    f"""
                    <div class="sensor-card">

                        <div class="sensor-name">
                            {name}
                        </div>

                        <div class="sensor-value">
                            {value}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # =================================================
        # MAINTENANCE INTELLIGENCE
        # =================================================

        st.markdown(
            '<div class="section-title">Maintenance Intelligence</div>',
            unsafe_allow_html=True
        )

        maintenance_col, anomaly_col = st.columns(2)


        # =================================================
        # MAINTENANCE PRIORITY
        # =================================================

        with maintenance_col:

            priority_map = {
                "ROUTINE": 25,
                "MEDIUM": 50,
                "HIGH": 75,
                "URGENT": 90,
                "CRITICAL": 100
            }

            priority = maintenance_priority.upper()

            priority_value = priority_map.get(
                priority,
                25
            )

            if priority == "CRITICAL":
                active_color = "#E45756"
            elif priority == "URGENT":
                active_color = "#E87845"
            elif priority == "HIGH":
                active_color = "#F28C28"
            elif priority == "MEDIUM":
                active_color = "#F5A623"
            else:
                active_color = "#3BC47A"

            fig = go.Figure(
                go.Pie(
                    values=[
                        priority_value,
                        100 - priority_value
                    ],
                    hole=0.72,
                    marker=dict(
                        colors=[
                            active_color,
                            "#8E4935"
                        ]
                    ),
                    textinfo="none",
                    hoverinfo="skip"
                )
            )

            fig.add_annotation(
                text=maintenance_priority,
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    size=18,
                    color="#FFF4E8"
                )
            )

            fig.update_layout(
                height=250,
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
                paper_bgcolor="#C8754B",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )


        # =================================================
        # ANOMALY
        # =================================================

        with anomaly_col:

            st.markdown(
                f"""
                <div class="maintenance-card">

                    <div class="maintenance-label">
                        Anomaly Detection
                    </div>

                    <div class="maintenance-value">
                        {anomaly_status}
                    </div>

                    <div class="maintenance-text">
                        Anomaly Score:
                        <strong>{anomaly_score:.4f}</strong>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="maintenance-card">

                    <div class="maintenance-label">
                        Inspection Window
                    </div>

                    <div class="maintenance-value">
                        {inspection_window}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # RECOMMENDATION
        # =================================================

        st.markdown(
            f"""
            <div class="recommendation">

                <div class="recommendation-title">
                    Recommended Action
                </div>

                <div class="recommendation-text">
                    {recommended_action}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # =================================================
        # SENSOR SUMMARY
        # =================================================

        st.markdown(
            '<div class="section-title">Sensor Summary</div>',
            unsafe_allow_html=True
        )

        sensor_data = [
            ("Air Temperature", f"{air_temperature:.1f} K"),
            ("Process Temperature", f"{process_temperature:.1f} K"),
            (
                "Temperature Difference",
                f"{process_temperature - air_temperature:.1f} K"
            ),
            ("Rotational Speed", f"{rotational_speed:.0f} rpm"),
            ("Torque", f"{torque:.1f} Nm"),
            ("Tool Wear", f"{tool_wear:.0f} min")
        ]

        sensor_cols = st.columns(3)

        for i, (name, value) in enumerate(sensor_data):

            with sensor_cols[i % 3]:

                st.markdown(
                    f"""
                    <div class="sensor-card">

                        <div class="sensor-name">
                            {name}
                        </div>

                        <div class="sensor-value">
                            {value}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # =================================================
        # FOOTER
        # =================================================

        st.markdown(
            """
            <div class="footer">
                ProActive Maintenance AI · Predictive Maintenance
                &nbsp;|&nbsp; XGBoost · Isolation Forest · SHAP
            </div>
            """,
            unsafe_allow_html=True
        )


    except requests.exceptions.Timeout:

        st.error(
            "Prediction request timed out. "
            "Make sure the FastAPI server is running."
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to the FastAPI server. "
            "Start FastAPI before using the dashboard."
        )

    except Exception as e:

        st.error(
            f"Prediction failed: {str(e)}"
        )