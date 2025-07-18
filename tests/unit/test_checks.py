import pytest
from cactus_test_definitions.checks import Check, validate_check_parameters
from cactus_test_definitions.errors import TestProcedureDefinitionError


@pytest.mark.parametrize(
    "check, is_valid",
    [
        (Check("foo", {}), False),  # Unknown check
        (Check("readings-site-active-power", {}), False),
        (Check("readings-site-active-power", {"minimum_count": "3"}), False),
        (Check("readings-site-active-power", {"minimum_count": 3}), True),
        (Check("der-settings-contents", {"setGradW": 27}), True),
        (Check("der-settings-contents", {"doeModesEnabled": "0f"}), True),
        (Check("der-settings-contents", {"modesEnabled": "E"}), True),
        (Check("der-settings-contents", {"doeModesEnabled": 12}), False),
    ],
)
def test_validate_check_parameters(check: Check, is_valid: bool):
    if is_valid:
        validate_check_parameters("foo", check)
    else:
        with pytest.raises(TestProcedureDefinitionError):
            validate_check_parameters("foo", check)
