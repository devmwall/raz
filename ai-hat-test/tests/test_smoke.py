from ai_hat_test.main import check_module


def test_check_module_reports_missing() -> None:
    result = check_module("module_that_does_not_exist_123")
    assert result.ok is False
