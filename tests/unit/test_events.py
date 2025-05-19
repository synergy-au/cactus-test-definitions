import pytest
from cactus_test_definitions.actions import (
    Action,
)
from cactus_test_definitions.errors import TestProcedureDefinitionError
from cactus_test_definitions.events import Event, validate_event_parameters


@pytest.mark.parametrize(
    "action, is_valid",
    [
        (Event("foo", {}), False),  # Unknown check
        (Event("wait", {}), False),
        (Event("wait", {"duration_seconds": "3"}), False),
        (Event("wait", {"duration_seconds": 3}), True),
        (Event("wait", {"duration_seconds": 3, "other": 4}), False),
        (Event("GET-request-received", {"endpoint": "/dcap"}), True),
    ],
)
def test_validate_event_parameters(action: Action, is_valid: bool):
    if is_valid:
        validate_event_parameters("foo", "bar", action)
    else:
        with pytest.raises(TestProcedureDefinitionError):
            validate_event_parameters("foo", "bar", action)
