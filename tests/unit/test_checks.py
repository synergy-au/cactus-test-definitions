import pytest
from cactus_test_definitions.actions import (
    Action,
)
from cactus_test_definitions.checks import Check, validate_check_parameters
from cactus_test_definitions.errors import TestProcedureDefinitionError


@pytest.mark.parametrize(
    "action, is_valid",
    [
        (Check("foo", {}), False),  # Unknown check
        (Check("readings-site-active-power", {}), False),
        (Check("readings-site-active-power", {"minimum_count": "3"}), False),
        (Check("readings-site-active-power", {"minimum_count": 3}), True),
    ],
)
def test_validate_check_parameters(action: Action, is_valid: bool):
    if is_valid:
        validate_check_parameters("foo", action)
    else:
        with pytest.raises(TestProcedureDefinitionError):
            validate_check_parameters("foo", action)
