from datetime import datetime

import pytest
from cactus_test_definitions.actions import (
    Action,
    validate_action_parameters,
)
from cactus_test_definitions.errors import TestProcedureDefinitionError


@pytest.mark.parametrize(
    "action, is_valid",
    [
        (Action("foo", {}), False),
        (Action("enable-listeners", {"listeners": []}), True),
        (Action("enable-listeners", {"listeners": ["other-step"]}), True),
        (Action("enable-listeners", {"listeners": ["other-step"], "unused-param": 123}), False),  # extra param
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
