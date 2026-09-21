import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests



# ============================================================
# PAGE CONFIG
# ============================================================
API_URL = "https://proactive-maintenance-ai.onrender.com"
st.set_page_config(
    page_title="ProActive Maintenance AI",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "prediction_result" not in st.session_state:
    st.session_state["prediction_result"] = None

if "machine_payload" not in st.session_state:
    st.session_state["machine_payload"] = None


# ============================================================
# COLORS
# ============================================================

BG = "#061A2D"
CLAY = "#123B4A"

ORANGE = "#18C3B1"
GOLD = "#F5C451"

WHITE = "#F4FAFA"
TEXT_DARK = "#102027"
MUTED = "#CFE2E2"
BORDER = "#F5C451"

RISK_LOW = "#4CAF7D"
RISK_MEDIUM = "#E0B84F"
RISK_HIGH = "#D95757"

ACCENT_BLUE = "#2D6FA3"
ACCENT_TEAL = "#18C3B1"
ACCENT_PURPLE = "#665A9A"

METER_BG = "#285B68"

GRAPH_BLUE = "#061A2D"
GRAPH_GREEN = "#4CAF7D"
GRAPH_RED = "#D95757"


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    f"""
    <style>

    html, body, [data-testid="stAppViewContainer"] {{
        background: {BG};
    }}

    [data-testid="stAppViewContainer"] {{
        background: {BG};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stToolbar"] {{
        display: none;
    }}

    .block-container {{
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}


    /* ============================================================
    HOVER TOOLTIPS
    ============================================================ */

    .hover-info {{
        position: relative;
        cursor: help;
        overflow: visible !important;
    }}

    .hover-info::after {{
        content: attr(data-tooltip);

        position: absolute;
        left: calc(100% + 12px);
        top: 50%;

        width: 250px;
        padding: 12px 14px;

        transform: translateY(-50%) translateX(6px);

        background: #071A2D;
        color: {WHITE};

        border: 1px solid {GOLD};
        border-radius: 10px;

        font-size: 11px;
        font-weight: 600;
        line-height: 1.5;
        letter-spacing: 0;

        text-align: left;

        opacity: 0;
        visibility: hidden;
        pointer-events: none;

        transition:
            opacity 0.18s ease,
            transform 0.18s ease;

        z-index: 99999;

        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    }}

    .hover-info:hover::after {{
        opacity: 1;
        visibility: visible;
        transform: translateY(-50%) translateX(0);
    }}

    /* Keep cards capable of displaying the tooltip */

    .kpi-card,
    .analytics-panel,
    .maintenance-card,
    .sensor-card {{
        overflow: visible !important;
    }}


    /* HEADER */

    .app-header {{
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        padding: 4px 0 18px 0;
        border-bottom: 2px solid {ORANGE};
        margin-bottom: 28px;
    }}

    .header-left {{
        display: flex;
        flex-direction: column;
        gap: 5px;
    }}

    .app-title {{
        color: {WHITE};
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }}

    .app-subtitle {{
        color: {MUTED};
        font-size: 14px;
        font-weight: 500;
    }}

    .api-status {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(23,107,77,0.16);
        border: 1px solid {RISK_LOW};
        color: #B7E4D1;
        border-radius: 999px;
        padding: 8px 14px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.7px;
    }}

    .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {RISK_LOW};
        box-shadow: 0 0 8px rgba(23,107,77,0.8);
    }}


    /* SECTION TITLES */

    .section-title {{
        color: {ORANGE};
        font-size: 18px;
        font-weight: 900;
        letter-spacing: 1.4px;
        margin: 28px 0 14px 0;
        text-transform: uppercase;
        padding-left: 12px;
        border-left: 4px solid {GOLD};
        line-height: 1.1;
    }}


    /* INPUTS */

    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {{
        color: {WHITE} !important;
        font-weight: 800 !important;
        font-size: 12px !important;
    }}

    div[data-testid="stTextInput"],
    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"] {{
        background: {CLAY};
        border: 1px solid {GOLD};
        border-radius: 14px;
        padding: 10px 12px 7px 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.16);
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {{
        color: {WHITE} !important;
        background: transparent !important;
        font-weight: 700 !important;
        border: none !important;
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
        background: transparent !important;
        border: none !important;
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {{
        color: {WHITE} !important;
        font-weight: 700 !important;
    }}


    /* BUTTON */

    div.stButton {{
        display: flex;
        justify-content: center;
        margin-top: 22px;
        margin-bottom: 12px;
    }}

    div.stButton > button {{
        background: {ORANGE} !important;
        color: #FFFFFF !important;
        border: 1px solid #FFB45C !important;
        border-radius: 10px !important;
        padding: 11px 30px !important;
        font-size: 12px !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        min-width: 210px;
        transition: all 0.2s ease !important;
        box-shadow: 0 5px 14px rgba(0,0,0,0.2);
    }}

    div.stButton > button:hover {{
        background: {GOLD} !important;
        transform: translateY(-1px);
    }}


    /* KPI */

    .kpi-card {{
        background: {CLAY};
        border: 1px solid {GOLD};
        border-radius: 16px !important;
        padding: 18px 20px;
        min-height: 105px;
        box-shadow: 0 5px 16px rgba(0,0,0,0.18);
        overflow: hidden;
    }}

    .kpi-label {{
        color: {MUTED};
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 11px;
    }}

    .kpi-value {{
        color: {WHITE};
        font-size: 25px;
        font-weight: 900;
        line-height: 1;
    }}


    /* ANALYTICS */

    .analytics-panel {{
        background: {CLAY};
        border: 1px solid {GOLD};
        border-radius: 16px !important;
        padding: 14px;
        box-shadow: 0 5px 16px rgba(0,0,0,0.18);
        height: 100%;
        overflow: hidden;
    }}

    .analytics-title {{
        color: {WHITE};
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 3px 5px 7px 5px;
    }}


    /* ROUNDED GRAPH BOXES */

    div[data-testid="stPlotlyChart"] {{
        background: {CLAY} !important;
        border: 1px solid {GOLD} !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 5px 16px rgba(0,0,0,0.18) !important;
        padding: 0 !important;
    }}

    div[data-testid="stPlotlyChart"] > div {{
        border-radius: 16px !important;
        overflow: hidden !important;
    }}


    /* MAINTENANCE */

    .maintenance-card {{
        background: {CLAY};
        border: 1px solid {GOLD};
        border-radius: 16px !important;
        padding: 20px;
        min-height: 280px;
        box-shadow: 0 5px 16px rgba(0,0,0,0.18);
        overflow: hidden;
    }}

    .maintenance-label {{
        color: {MUTED};
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .recommendation {{
        color: {WHITE};
        font-size: 14px;
        font-weight: 650;
        line-height: 1.55;
    }}

    .inspection {{
        color: {WHITE};
        font-size: 19px;
        font-weight: 900;
        margin-top: 5px;
    }}


    /* SENSOR */

    .sensor-card {{
        background: {CLAY};
        border: 1px solid {GOLD};
        border-radius: 14px !important;
        padding: 15px 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.16);
        min-height: 88px;
        overflow: hidden;
    }}

    .sensor-name {{
        color: {MUTED};
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }}

    .sensor-value {{
        color: {WHITE};
        font-size: 19px;
        font-weight: 900;
    }}

    div[data-testid="column"] {{
        min-width: 0;
    }}

    @media (max-width: 900px) {{

        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        .app-header {{
            align-items: flex-start;
            flex-direction: column;
            gap: 14px;
        }}

        .app-title {{
            font-size: 25px;
        }}

    }}

    </style>
    """
)


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="app-header">

        <div class="header-left">

            <div class="app-title">
                ⚙ ProActive Maintenance AI
            </div>

            <div class="app-subtitle">
                Real-time Equipment Failure Risk &amp;
                Diagnostics Dashboard
            </div>

        </div>

        <div class="api-status">
            <span class="status-dot"></span>
            API ENDPOINT ACTIVE
        </div>

    </div>
    """
)


# ============================================================
# MACHINE PARAMETERS
# ============================================================

st.html(
    '<div class="section-title">Machine Parameters</div>'
)

input_col1, input_col2, input_col3 = st.columns(
    3,
    gap="medium"
)

with input_col1:

    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"],
        index=1
    )

with input_col2:

    air_temperature = st.number_input(
        "Air Temperature [K]",
        min_value=250.0,
        max_value=350.0,
        value=298.1,
        step=0.1
    )

with input_col3:

    process_temperature = st.number_input(
        "Process Temperature [K]",
        min_value=250.0,
        max_value=400.0,
        value=308.6,
        step=0.1
    )


input_col4, input_col5, input_col6 = st.columns(
    3,
    gap="medium"
)

with input_col4:

    rotational_speed = st.number_input(
        "Rotational Speed [rpm]",
        min_value=500.0,
        max_value=3000.0,
        value=1551.0,
        step=1.0
    )

with input_col5:

    torque = st.number_input(
        "Torque [Nm]",
        min_value=0.0,
        max_value=100.0,
        value=42.8,
        step=0.1
    )

with input_col6:

    tool_wear = st.number_input(
        "Tool Wear [min]",
        min_value=0.0,
        max_value=300.0,
        value=108.0,
        step=1.0
    )


# ============================================================
# ANALYZE MACHINE
# ============================================================

if st.button(
    "ANALYZE MACHINE",
    type="primary"
):

    api_payload = {
        "Type": machine_type,
        "Air_temperature_K": air_temperature,
        "Process_temperature_K": process_temperature,
        "Rotational_speed_rpm": rotational_speed,
        "Torque_Nm": torque,
        "Tool_wear_min": tool_wear
    }

    dashboard_payload = {
        "Type": machine_type,
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }
    

    try:

        with st.spinner(
            "Analyzing machine condition..."
        ):
            st.write("DEBUG API PAYLOAD:", api_payload)
            response = requests.post(
                f"{API_URL}/predict",
                json=api_payload,
                timeout=120
            )

            response.raise_for_status()

            result = response.json()
            if result.get("out_of_distribution", False):

                st.warning(
                    "Input is outside the operating range seen during model training. "
                    "Prediction reliability may be reduced."
                )

                warnings = result.get(
                    "distribution_warnings",
                    []
                )

                for warning in warnings:

                    st.write(
                        f"**{warning['feature']}**: "
                        f"{warning['value']} "
                        f"(training range: "
                        f"{warning['training_min']} - "
                        f"{warning['training_max']})"
                    )

            else:

                st.success(
                    "Input is within the operating range observed during model training."
                )

            st.session_state["prediction_result"] = result
            st.session_state["machine_payload"] = dashboard_payload

    except Exception as e:

        st.error(
            f"Prediction failed: {str(e)}"
                )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state["prediction_result"]
payload = st.session_state["machine_payload"]


if result is not None and payload is not None:

    # ========================================================
    # RESULT VALUES
    # ========================================================

    failure_probability = float(
        result.get(
            "failure_probability",
            0.0
        )
    )

    risk_level = str(
        result.get(
            "risk_level",
            "LOW"
        )
    ).upper()

    maintenance_priority = str(
        result.get(
            "maintenance_priority",
            "ROUTINE"
        )
    ).upper()

    anomaly_status = str(
        result.get(
            "anomaly_status",
            "NORMAL"
        )
    ).upper()

    anomaly_score = float(
        result.get(
            "anomaly_score",
            0.0
        )
    )

    recommended_action = result.get(
        "recommended_action",
        "Continue normal operation and monitor sensor trends."
    )

    inspection_window = result.get(
        "inspection_window",
        "30+ days"
    )

    top_risk_factors = result.get(
        "top_risk_factors",
        []
    )


    # ========================================================
    # RISK COLOR
    # ========================================================

    risk_colors = {
        "LOW": RISK_LOW,
        "MEDIUM": RISK_MEDIUM,
        "HIGH": RISK_HIGH
    }

    risk_color = risk_colors.get(
        risk_level,
        RISK_LOW
    )


    # ========================================================
    # MACHINE HEALTH OVERVIEW
    # ========================================================

    st.html(
        '<div class="section-title">'
        'Machine Health Overview'
        '</div>'
    )

    k1, k2 = st.columns(
        2,
        gap="medium"
    )


    # FAILURE PROBABILITY

    with k1:

        st.html(
            f"""
            <div
                class="kpi-card hover-info"
                data-tooltip="Estimated probability that the machine will experience a failure based on its current sensor measurements and engineered features."
            >

                <div class="kpi-label">
                    Failure Probability
                </div>

                <div class="kpi-value">
                    {failure_probability * 100:.2f}%
                </div>

            </div>
            """
        )


    # RISK LEVEL

    with k2:

        st.html(
            f"""
            <div
                class="kpi-card hover-info"
                data-tooltip="Overall machine failure risk based on the predicted failure probability and current machine condition."
            >

                <div class="kpi-label">
                    Risk Level
                </div>

                <div style="
                    display:flex;
                    align-items:center;
                    gap:18px;
                    margin-top:2px;
                ">

                    <div style="
                        width:52px;
                        height:52px;
                        min-width:52px;
                        border-radius:50%;
                        border:4px solid {GOLD};
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        background:rgba(245,196,81,0.08);
                        box-shadow:
                            0 0 0 2px rgba(245,196,81,0.18),
                            0 0 14px rgba(245,196,81,0.45),
                            inset 0 0 8px rgba(245,196,81,0.15);
                    ">

                        <div style="
                            width:16px;
                            height:16px;
                            border-radius:50%;
                            background:{risk_color};
                            box-shadow:
                                0 0 10px {risk_color};
                        "></div>

                    </div>

                    <div style="
                        color:{risk_color};
                        font-size:27px;
                        font-weight:900;
                        line-height:1;
                    ">
                        {risk_level}
                    </div>

                </div>

            </div>
            """
        )


    # ========================================================
    # RISK & MACHINE ANALYTICS
    # ========================================================

    st.html(
        '<div class="section-title">'
        'Risk & Machine Analytics'
        '</div>'
    )

    chart1, chart2, chart3 = st.columns(
        3,
        gap="medium"
    )


    # ========================================================
    # FAILURE RISK
    # ========================================================

    with chart1:
        st.html(
            f"""
            <div
                class="analytics-title hover-info"
                data-tooltip="Estimated probability of machine failure based on current sensor measurements and engineered features."
            >
                FAILURE RISK
            </div>
            """
        )
        risk_gauge = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=failure_probability * 100,

                number={
                    "suffix": "%",
                    "font": {
                        "size": 34,
                        "color": WHITE
                    }
                },

                title={
                    "text": "",
                    "font": {
                        "size": 12,
                        "color": WHITE
                    }
                },

                gauge={

                    "axis": {
                        "range": [0, 100],
                        "tickcolor": WHITE,
                        "tickfont": {
                            "color": WHITE
                        }
                    },

                    "bar": {
                        "color": risk_color,
                        "thickness": 0.30
                    },

                    "bgcolor": METER_BG,

                    "borderwidth": 0,

                    "steps": [
                        {
                            "range": [0, 30],
                            "color": "#174D3B"
                        },
                        {
                            "range": [30, 70],
                            "color": "#80520C"
                        },
                        {
                            "range": [70, 100],
                            "color": "#702638"
                        }
                    ]

                }

            )
        )

        risk_gauge.update_layout(
            height=320,
            margin=dict(
                l=15,
                r=15,
                t=10,
                b=30
            ),
            paper_bgcolor=CLAY,
            plot_bgcolor=CLAY
        )

        st.plotly_chart(
            risk_gauge,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


    # ========================================================
    # TOP RISK FACTORS
    # ========================================================

    with chart2:
        st.html(
            f"""
            <div
                class="analytics-title hover-info"
                data-tooltip="Shows the machine features contributing most strongly to the predicted failure risk."
            >
                TOP RISK FACTORS
            </div>
            """
        )

        risk_df = pd.DataFrame(
            top_risk_factors
        )

        if not risk_df.empty:

            risk_df = risk_df.sort_values(
                "impact",
                ascending=True
            )

            factor_colors = [
                GRAPH_GREEN
                if x < 0
                else GRAPH_RED
                for x in risk_df["impact"]
            ]
            
            factor_fig = go.Figure()

            factor_fig.add_trace(
                go.Bar(

                    x=risk_df["impact"],

                    y=risk_df["feature"],

                    orientation="h",

                    marker=dict(
                        color=factor_colors,
                        line=dict(
                            color=GRAPH_BLUE,
                            width=0.7
                        )
                    ),

                    text=[
                        f"{x:.2f}"
                        for x in risk_df["impact"]
                    ],

                    textposition="outside",

                    textfont=dict(
                        color=GRAPH_BLUE,
                        size=10
                    )

                )
            )

            factor_fig.update_layout(

                height=320,

                margin=dict(
                    l=10,
                    r=40,
                    t=10,
                    b=30
                ),

                paper_bgcolor=CLAY,
                plot_bgcolor=CLAY,

                font=dict(
                    color=GRAPH_BLUE
                ),

                xaxis=dict(
                    color=GRAPH_BLUE,
                    gridcolor="rgba(7,26,73,0.18)",
                    zerolinecolor=GRAPH_BLUE,
                    zerolinewidth=1
                ),

                yaxis=dict(
                    color=GRAPH_BLUE,
                    gridcolor="rgba(7,26,73,0.08)"
                ),

                showlegend=False

            )

            st.plotly_chart(
                factor_fig,
                width="stretch",
                config={
                    "displayModeBar": False
                }
            )

    # ========================================================
    # MACHINE PROFILE
    # ========================================================

    with chart3:

        machine_profile = {

            "Air Temperature":
                payload["Air temperature [K]"],

            "Process Temperature":
                payload["Process temperature [K]"],

            "Rotational Speed":
                payload["Rotational speed [rpm]"],

            "Torque":
                payload["Torque [Nm]"],

            "Tool Wear":
                payload["Tool wear [min]"]

        }

        profile_df = pd.DataFrame(
            list(machine_profile.items()),
            columns=[
                "Feature",
                "Value"
            ]
        )
        st.html(
            f"""
            <div
                class="analytics-title hover-info"
                data-tooltip="Current machine operating parameters used by the predictive maintenance system."
            >
                MACHINE PROFILE
            </div>
            """
        )
        profile_fig = go.Figure()

        profile_fig.add_trace(
            go.Bar(

                x=profile_df["Value"],

                y=profile_df["Feature"],

                orientation="h",

                marker=dict(
                    color=ACCENT_BLUE,
                    line=dict(
                        color=GRAPH_BLUE,
                        width=1
                    )
                ),

                text=[
                    f"{x:.1f}"
                    for x in profile_df["Value"]
                ],

                textposition="outside",

                textfont=dict(
                    color=GRAPH_BLUE,
                    size=10
                )

            )
        )

        profile_fig.update_layout(

            height=320,

            margin=dict(
                l=10,
                r=40,
                t=10,
                b=30
            ),

            paper_bgcolor=CLAY,
            plot_bgcolor=CLAY,

            font=dict(
                color=GRAPH_BLUE
            ),

            xaxis=dict(
                color=GRAPH_BLUE,
                gridcolor="rgba(7,26,73,0.16)",
                zerolinecolor=GRAPH_BLUE
            ),

            yaxis=dict(
                color=GRAPH_BLUE,
                gridcolor="rgba(7,26,73,0.08)"
            ),

            showlegend=False

        )

        st.plotly_chart(
            profile_fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


    # ========================================================
    # MAINTENANCE INTELLIGENCE
    # ========================================================

    st.html(
        '<div class="section-title">'
        'Maintenance Intelligence'
        '</div>'
    )

    maintenance_col, recommendation_col, anomaly_col = st.columns(
        3,
        gap="medium"
    )


    # ========================================================
    # MAINTENANCE PRIORITY
    # ========================================================

    with maintenance_col:

        priority_values = {
            "ROUTINE": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "URGENT": 4,
            "CRITICAL": 5
        }

        priority_score = priority_values.get(
            maintenance_priority,
            1
        )
        st.html(
            f"""
            <div
                class="analytics-title hover-info"
                data-tooltip="Recommended urgency of maintenance. Higher priority means the machine requires faster inspection or intervention."
                style="margin-bottom:6px;"
            >
                MAINTENANCE PRIORITY
            </div>
            """
        )

        priority_fig = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=priority_score,

                number={
                    "font": {
                        "size": 27,
                        "color": WHITE
                    },
                    "suffix": "/5"
                },

                title={
                    "text": "",
                    "font": {
                        "size": 12,
                        "color": WHITE
                    }
                },

                gauge={

                    "axis": {
                        "range": [0, 5],

                        "tickvals": [
                            1, 2, 3, 4, 5
                        ],

                        "ticktext": [
                            "Routine",
                            "Medium",
                            "High",
                            "Urgent",
                            "Critical"
                        ],

                        "tickfont": {
                            "size": 8,
                            "color": WHITE
                        },

                        "tickcolor": WHITE
                    },

                    "bar": {
                        "color": ACCENT_PURPLE,
                        "thickness": 0.65
                    },

                    "bgcolor": METER_BG,

                    "borderwidth": 0

                }

            )
        )

        priority_fig.update_layout(
            height=280,
            margin=dict(
                l=15,
                r=15,
                t=35,
                b=15
            ),
            paper_bgcolor=CLAY,
            plot_bgcolor=CLAY
        )

        st.plotly_chart(
            priority_fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


    # ========================================================
    # RECOMMENDED ACTION
    # ========================================================

    with recommendation_col:

        st.html(
            f"""
            <div
                class="maintenance-card hover-info"
                data-tooltip="Recommended maintenance action based on machine failure risk, current operating conditions, and detected anomalies."
            >

                <div class="maintenance-label">
                    Recommended Action
                </div>

                <div class="recommendation">
                    {recommended_action}
                </div>

                <div style="
                    margin-top:24px;
                    border-top:1px solid
                    rgba(27,23,32,0.22);
                    padding-top:15px;
                ">

                    <div class="maintenance-label">
                        Inspection Window
                    </div>

                    <div class="inspection">
                        {inspection_window}
                    </div>

                </div>

            </div>
            """
        )


    # ========================================================
    # ANOMALY SCORE
    # ========================================================

    with anomaly_col:

        anomaly_meter_color = (
            ACCENT_TEAL
            if anomaly_status == "NORMAL"
            else RISK_HIGH
        )
        st.html(
            f"""
            <div
                class="analytics-title hover-info"
                data-tooltip="Measures how unusual the current sensor pattern is compared with normal machine behavior."
                style="margin-bottom:6px;"
            >
                ANOMALY SCORE
            </div>
            """
        )
        anomaly_fig = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=anomaly_score,

                number={
                    "font": {
                        "size": 28,
                        "color": WHITE
                    }
                },

                title={
                    "text": "",
                    "font": {
                        "size": 12,
                        "color": WHITE
                    }
                },

                gauge={

                    "axis": {
                        "range": [0, 1],

                        "tickfont": {
                            "color": WHITE
                        },

                        "tickcolor": WHITE
                    },

                    "bar": {
                        "color": anomaly_meter_color,
                        "thickness": 0.65
                    },

                    "bgcolor": METER_BG,

                    "borderwidth": 0

                }

            )
        )

        anomaly_fig.update_layout(
            height=280,
            margin=dict(
                l=20,
                r=20,
                t=35,
                b=15
            ),
            paper_bgcolor=CLAY,
            plot_bgcolor=CLAY
        )

        st.plotly_chart(
            anomaly_fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

        st.html(
            f"""
            <div style="
                text-align:center;
                color:{anomaly_meter_color};
                font-size:11px;
                font-weight:900;
                letter-spacing:0.8px;
                margin-top:-20px;
            ">
                STATUS: {anomaly_status}
            </div>
            """
        )


    # ========================================================
    # SENSOR SUMMARY
    # ========================================================

    st.html(
        '<div class="section-title">'
        'Sensor Summary'
        '</div>'
    )

    s1, s2, s3, s4, s5 = st.columns(
        5,
        gap="medium"
    )

    sensors = [

        (
            "Air Temp",
            f"{air_temperature:.1f} K"
        ),

        (
            "Process Temp",
            f"{process_temperature:.1f} K"
        ),

        (
            "Rotational Speed",
            f"{rotational_speed:.0f} rpm"
        ),

        (
            "Torque",
            f"{torque:.1f} Nm"
        ),

        (
            "Tool Wear",
            f"{tool_wear:.0f} min"
        )

    ]

    sensor_columns = [
        s1,
        s2,
        s3,
        s4,
        s5
    ]

    for column, (name, value) in zip(
        sensor_columns,
        sensors
    ):

        with column:

            st.html(
                f"""
                <div
                    class="sensor-card hover-info"
                    data-tooltip="{{
                        'Ambient air temperature surrounding the machine, measured in Kelvin.'
                        if name == 'Air Temp'
                        else
                        'Temperature of the machine manufacturing process, measured in Kelvin.'
                        if name == 'Process Temp'
                        else
                        'Speed at which the machine shaft rotates, measured in revolutions per minute.'
                        if name == 'Rotational Speed'
                        else
                        'Rotational force applied to the machine shaft, measured in Newton-metres.'
                        if name == 'Torque'
                        else
                        'Accumulated operating time of the machine tool, measured in minutes.'
                    }}"
                >

                    <div class="sensor-name">
                        {name}
                    </div>

                    <div class="sensor-value">
                        {value}
                    </div>

                </div>
                """
            )


else:

    # ========================================================
    # INITIAL STATE
    # ========================================================

    st.html(
        f"""
        <div style="
            margin-top:35px;
            padding:35px;
            background:{CLAY};
            border:1px solid {BORDER};
            border-radius:16px;
            text-align:center;
            box-shadow:0 5px 16px rgba(0,0,0,0.18);
        ">

            <div style="
                color:{GOLD};
                font-size:22px;
                font-weight:900;
                margin-bottom:8px;
            ">
                Machine analysis ready
            </div>

            <div style="
                color:{MUTED};
                font-size:13px;
            ">
                Enter the machine parameters above and click
                <b>ANALYZE MACHINE</b> to generate the diagnostic report.
            </div>

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    f"""
    <div style="
        margin-top:35px;
        padding-top:16px;
        border-top:1px solid rgba(245,196,81,0.35);
        text-align:center;
        color:rgba(207,226,226,0.65);
        font-size:10px;
        letter-spacing:0.5px;
    ">
        ProActive Maintenance AI
        &nbsp;•&nbsp;
        Predictive Maintenance System
        &nbsp;•&nbsp;
        XGBoost + Anomaly Detection + SHAP
    </div>
    """
)