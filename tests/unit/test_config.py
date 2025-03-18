from pathlib import Path

import pytest

from cactus_test_definitions import TestProcedureConfig, TestProcedureDefinitionError


def test_from_yamlfile():
    """This test confirms the standard test procedure yaml file (intended for production use)
    can be read and converted to the appropriate dataclasses.
    """
    test_procedures = TestProcedureConfig.from_resource()
    test_procedures.validate()


@pytest.mark.parametrize(
    "filename",
    [
        "tests/data/config_with_errors1.yaml",  # No 'listeners' parameters defined for enable-listeners action (NOT-A-VALID-PARAMETER-NAME supplied instead)
        "tests/data/config_with_errors2.yaml",  # Action refers to step "NOT-A-VALID-STEP"
    ],
)
def test_TestProcedures_validate_raises_exception(filename: str):

    with pytest.raises(TestProcedureDefinitionError):
        _ = TestProcedureConfig.from_yamlfile(path=Path(filename))
