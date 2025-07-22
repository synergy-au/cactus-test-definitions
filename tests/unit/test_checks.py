import pytest
from cactus_test_definitions.checks import Check, validate_check_parameters
from cactus_test_definitions.errors import TestProcedureDefinitionError
from cactus_test_definitions import variable_expressions as varexps


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


def test_check_expression() -> None:
    """Tests the creation of a Check that has an expression as one of its parameters"""
    type_str = "some_check"
    params = {"setMaxW": "$(this < rtgMaxW)"}
    check = Check(type_str, params)

    check_set_max_w = check.parameters["setMaxW"]
    assert isinstance(check_set_max_w, varexps.Expression)
    assert check_set_max_w.operation == varexps.OperationType.LT
    assert check_set_max_w.lhs_operand == varexps.NamedVariable(varexps.NamedVariableType.DERSETTING_SET_MAX_W)
    assert check_set_max_w.rhs_operand == varexps.NamedVariable(varexps.NamedVariableType.DERCAPABILITY_RTG_MAX_W)
