from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import IntEnum, auto
from typing import Any

from cactus_test_definitions.errors import TestProcedureDefinitionError
from cactus_test_definitions.variable_expressions import is_resolvable_variable


class ParameterType(IntEnum):
    """The various "basic" types that can be set in YAML for a parameter. Rudimentary type checking
    will try to enforce these but they can't be guaranteed"""

    String = auto()
    Integer = auto()
    Float = auto()
    Boolean = auto()
    DateTime = auto()  # TZ aware datetime
    ListString = auto()  # List of strings


@dataclass(frozen=True)
class ParameterSchema:
    """What parameters can be passed to a given action/check. Describes a single optional/mandatory field"""

    mandatory: bool  # If this parameter required
    expected_type: ParameterType


def is_valid_parameter_type(expected_type: ParameterType, value: Any) -> bool:
    """Returns true if the specified value "passes" as the expected type. Only performs rudimentary checks to try
    and catch obvious misconfigurations"""
    if value is None:
        return True  # We currently allow None to pass to params. Make it a runtime concern

    if is_resolvable_variable(value):
        return True  # Too hard to validate variable expressions. Make it a runtime concern

    match (expected_type):
        case ParameterType.String:
            return isinstance(value, str)
        case ParameterType.Integer:
            if isinstance(value, int):
                return True
            else:
                # Floats/decimals can pass through so long as they have 0 decimal places
                try:
                    return int(value) == value
                except Exception:
                    return False
        case ParameterType.Float:
            return isinstance(value, float) or isinstance(value, Decimal) or isinstance(value, int)
        case ParameterType.Boolean:
            return isinstance(value, bool)
        case ParameterType.DateTime:
            return isinstance(value, datetime)
        case ParameterType.ListString:
            return isinstance(value, list) and all((isinstance(e, str) for e in value))

    raise TestProcedureDefinitionError(f"Unexpected ParameterType: {ParameterType}")


def validate_parameters(location: str, parameters: dict[str, Any], valid_schema: dict[str, ParameterSchema]) -> None:
    """Validates parameters against valid_schema for the specified location label.

    location: Label to decorate error messages (eg TestProcedureName.Step.Action)
    parameters: The parameters dict to validate
    valid_schema: The schema to validate parameters against. Keys will be the parameter names, value will be the schema

    raises TestProcedureDefinitionError if parameters is invalid"""

    # Check the supplied parameters match the schema definition
    for param_name, param_value in parameters.items():
        param_schema = valid_schema.get(param_name, None)
        if param_schema is None:
            raise TestProcedureDefinitionError(
                f"{location} doesn't have a parameter {param_name}. Valid params are {set(valid_schema.keys())}"
            )

        # Check the type
        if not is_valid_parameter_type(param_schema.expected_type, param_value):
            raise TestProcedureDefinitionError(
                f"{location} has parameter {param_name} expecting {param_schema.expected_type} but got {param_value}"
            )

    # Check all mandatory parameters are set
    for param_name, param_schema in valid_schema.items():
        if param_schema.mandatory and param_name not in parameters:
            raise TestProcedureDefinitionError(f"{location} is missing mandatory parameter {param_name}")
