from proactive_maintenance_ai.components.stage_10_maintenance_decision import (
    MaintenanceDecisionEngine
)


engine = MaintenanceDecisionEngine()

test_cases = [
    ("LOW", "NORMAL"),
    ("LOW", "ANOMALY"),
    ("MEDIUM", "NORMAL"),
    ("MEDIUM", "ANOMALY"),
    ("HIGH", "NORMAL"),
    ("HIGH", "ANOMALY")
]

for risk_level, anomaly_status in test_cases:

    result = engine.generate_decision(
        risk_level=risk_level,
        anomaly_status=anomaly_status
    )

    print(
        f"\nRisk: {risk_level}"
        f"\nAnomaly: {anomaly_status}"
        f"\nPriority: {result['maintenance_priority']}"
        f"\nAction: {result['recommended_action']}"
        f"\nWindow: {result['inspection_window']}"
    )