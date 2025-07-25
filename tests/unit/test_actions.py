from datetime import datetime

import pytest
from cactus_test_definitions.actions import (
    Action,
    validate_action_parameters,
)
from cactus_test_definitions.errors import TestProcedureDefinitionError
from cactus_test_definitions import variable_expressions as varexps


@pytest.mark.parametrize(
    "action, is_valid",
    [
        (Action("foo", {}), False),
        (Action("enable-steps", {"steps": []}), True),
        (Action("enable-steps", {"steps": ["other-step"]}), True),
        (Action("enable-steps", {"steps": ["other-step"], "unused-param": 123}), False),  # extra param
        (Action("set-default-der-control", {}), True),
        (Action("set-default-der-control", {"opModImpLimW": 12.3, "opModExpLimW": 14}), True),
        (Action("set-default-der-control", {"opModImpLimW": 12.3, "opModExpLimW": "Invalid"}), False),  # bad type
        (Action("create-der-control", {"start": datetime(2022, 1, 3)}), False),  # Missing duration_seconds
        (Action("create-der-control", {"start": datetime(2022, 1, 3), "duration_seconds": 123}), True),
    ],
)
def test_validate_action_parameters(action: Action, is_valid: bool):
    if is_valid:
        validate_action_parameters("foo", "bar", action)
    else:
        with pytest.raises(TestProcedureDefinitionError):
            validate_action_parameters("foo", "bar", action)


def test_action_expression() -> None:
    """Tests the creation of an Action that has an expression as one of its parameters"""
    type_str = "some_action"
    params = {"setMaxW": "$(this == rtgMaxW)"}
    action = Action(type_str, params)

    check_set_max_w = action.parameters["setMaxW"]
    assert isinstance(check_set_max_w, varexps.Expression)
    assert check_set_max_w.operation == varexps.OperationType.EQ
    assert check_set_max_w.lhs_operand == varexps.NamedVariable(varexps.NamedVariableType.DERSETTING_SET_MAX_W)
    assert check_set_max_w.rhs_operand == varexps.NamedVariable(varexps.NamedVariableType.DERCAPABILITY_RTG_MAX_W)
