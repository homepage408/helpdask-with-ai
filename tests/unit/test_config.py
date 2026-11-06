from app.core.config import Settings, get_settings


def test_settings_load_from_env() -> None:
    """Ensure settings are correctly loaded from environment."""
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.PROJECT_NAME == "HelpDesk Mini"
    assert settings.API_V1_PREFIX == "/api/v1"


def test_default_credentials_are_empty() -> None:
    """Ensure sensitive credentials have no default values in codebase."""
    assert Settings.model_fields["DATABASE_URL"].default == ""
    assert Settings.model_fields["TEST_DATABASE_URL"].default == ""
    assert Settings.model_fields["JWT_SECRET_KEY"].default == ""
