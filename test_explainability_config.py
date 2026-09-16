from proactive_maintenance_ai.config.configuration import ConfigurationManager


config = ConfigurationManager()

explainability_config = (
    config.get_explainability_config()
)

print(explainability_config)