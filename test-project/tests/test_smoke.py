from test_project.main import run


def test_run_returns_zero() -> None:
    assert run("Pi") == 0
