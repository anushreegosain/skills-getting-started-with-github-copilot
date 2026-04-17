"""
Shared pytest fixtures for the FastAPI test suite.

Provides:
- test_client: FastAPI TestClient for making HTTP requests
- reset_activities: Fixture to reset the activities database to a known state
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_client():
    """
    ARRANGE: Create an isolated TestClient for the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    ARRANGE: Reset activities to initial state before each test.
    
    This fixture deep-copies the original activities dict to prevent
    test pollution and ensures each test starts with a clean slate.
    """
    # Store the original state
    original_state = copy.deepcopy(activities)
    
    yield  # Run the test
    
    # Restore original state after test
    activities.clear()
    activities.update(original_state)
