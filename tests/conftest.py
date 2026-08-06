from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


INITIAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(app_module, "activities", deepcopy(INITIAL_ACTIVITIES))
