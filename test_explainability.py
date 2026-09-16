from proactive_maintenance_ai.config.configuration import ConfigurationManager
from proactive_maintenance_ai.components.stage_11_explainability import (
    ModelExplainability
)


config = ConfigurationManager()

explainability_config = (
    config.get_explainability_config()
)

explainer = ModelExplainability(
    explainability_config
)

input_data = {
    "Type": "M",
    "Air temperature [K]": 298.5,
    "Process temperature [K]": 308.7,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 40.0,
    "Tool wear [min]": 100
}

result = explainer.explain(
    input_data
)

print("\nTop Risk Factors:\n")

for feature in result["top_features"]:

    print(
        f"{feature['feature']}: "
        f"{feature['impact']} "
        f"({feature['direction']})"
    )