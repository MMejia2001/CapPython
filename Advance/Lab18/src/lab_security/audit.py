from collections.abc import Iterable

from lab_security.settings import Settings, settings


SAFE_MINIMUM_VERSIONS = {
    "fastapi": ">=0.128.0,<0.129.0",
    "uvicorn": ">=0.40.0,<0.41.0",
    "pydantic-settings": ">=2.12.0,<3.0.0",
}


def dependency_recommendations() -> list[dict[str, str]]:
    return [
        {
            "package": package,
            "recommended": version,
        }
        for package, version in SAFE_MINIMUM_VERSIONS.items()
    ]


def security_checks() -> dict[str, object]:
    current_settings = Settings()

    return {
        "environment": current_settings.app_env,
        "debug_enabled": current_settings.debug,
        "token_configured": current_settings.api_token.get_secret_value() != "change-me",
        "dependency_policy": dependency_recommendations(),
    }


def format_lines(lines: Iterable[str]) -> str:
    return "\n".join(lines)
