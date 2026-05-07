# osint-engine/backend/tests/test_config.py
from config import Settings


def test_settings_defaults():
    s = Settings()
    assert s.backend_port == 8000
    assert s.planner_timeout == 60
    assert s.crawler_timeout == 10


def test_settings_override(monkeypatch):
    monkeypatch.setenv("BACKEND_PORT", "9000")
    s = Settings()
    assert s.backend_port == 9000
