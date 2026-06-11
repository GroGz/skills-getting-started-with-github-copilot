import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store original activities state
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Fixture providing TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Autouse fixture to reset activities to original state before each test"""
    # Reset before each test
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Clean up after test (optional but good practice)
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
