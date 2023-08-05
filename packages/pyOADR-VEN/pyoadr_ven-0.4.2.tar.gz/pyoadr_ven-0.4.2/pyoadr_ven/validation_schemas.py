from voluptuous import Schema


REPORT_PARAMETER_SCHEMA = Schema(
    {
        str: {
            "report_name_metadata": str,
            "report_interval_secs_default": int,
            "telemetry_parameters": dict,
        }
    },
    required=True,
)
