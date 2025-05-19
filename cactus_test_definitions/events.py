from dataclasses import dataclass
from typing import Any

from cactus_test_definitions.errors import TestProcedureDefinitionError
from cactus_test_definitions.parameters import (
    ParameterSchema,
    ParameterType,
    validate_parameters,
)
from cactus_test_definitions.variable_expressions import (
    parse_variable_expression_body,
    try_extract_variable_expression,
)


@dataclass
class Event:
    type: str
    parameters: dict[str, Any]

    def __post_init__(self):
        """Some parameter values might contain variable expressions (eg: a string "$now") that needs to be replaced
        with an parsed Expression object instead."""
        for k, v in self.parameters.items():
            variable_expr = try_extract_variable_expression(v)
            if variable_expr:
                self.parameters[k] = parse_variable_expression_body(variable_expr)


# The parameter schema for each event, keyed by the event name
EVENT_PARAMETER_SCHEMA: dict[str, dict[str, ParameterSchema]] = {
    "GET-request-received": {"endpoint": ParameterSchema(True, ParameterType.String)},
    "POST-request-received": {"endpoint": ParameterSchema(True, ParameterType.String)},
    "wait": {"duration_seconds": ParameterSchema(True, ParameterType.Integer)},
}
VALID_EVENT_NAMES: set[str] = set(EVENT_PARAMETER_SCHEMA.keys())


def validate_event_parameters(procedure_name: str, step: str, event: Event) -> None:
    """Validates the event parameters for the parent TestProcedure based on the  EVENT_PARAMETER_SCHEMA

    raises TestProcedureDefinitionError on failure"""
    location = f"{procedure_name}.{step} Event: {event.type}"  # Descriptive location of this event being validated

    parameter_schema = EVENT_PARAMETER_SCHEMA.get(event.type, None)
    if parameter_schema is None:
        raise TestProcedureDefinitionError(f"{location} not a valid action name. {VALID_EVENT_NAMES}")

    validate_parameters(location, event.parameters, parameter_schema)
