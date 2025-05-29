from cactus_test_definitions.test_procedures import TestProcedureConfig, TestProcedureId


def test_TestProcedureId_synchronised():
    """Ensures that TestProcedureId is in sync with all available TestProcedures"""
    available_tests = set(TestProcedureConfig.available_tests())
    for t in available_tests:
        assert t in TestProcedureId, "TestProcedureConfig has a procedure not encoded in TestProcedureId"

    # By convention - test ALL-01 will be an enum ALL_01
    # for t in (t.replace("_", "-") for t in TestProcedureId):
    for t in TestProcedureId:
        assert t.value in available_tests, "TestProcedureId has extra procedures not found in TestProcedureConfig"


def test_available_tests_populated():
    """Force test procedures to load and ensure they all validate (and we at least have a few)"""
    assert len(TestProcedureConfig.available_tests()) > 0
