from lab_security.audit import dependency_recommendations, security_checks


def test_security_checks_detect_custom_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "secure-token")

    report = security_checks()

    assert report["token_configured"] is True


def test_security_checks_hide_default_risk_state(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)
    report = security_checks()

    assert report["environment"] == "dev"
    assert report["debug_enabled"] is False
    assert report["token_configured"] is False


def test_dependency_recommendations_include_expected_packages():
    packages = {item["package"] for item in dependency_recommendations()}

    assert {"fastapi", "uvicorn", "pydantic-settings"}.issubset(packages)
