import pytest
from unittest.mock import patch
import requests

# Import the function from your app
# Adjust the import path if needed
from app.solar_dashboard import get_allocation_from_ollama

def fake_post(*args, **kwargs):
    """
    Fake response object to simulate Ollama API
    """
    class FakeResponse:
        status_code = 200
        def iter_lines(self):
            # Simulate streaming JSON lines containing a response
            sample = '{"response":"Solar: 75 kWh Grid: 25 kWh"}'
            # yield bytes line as Ollama would
            yield sample.encode("utf-8")
    return FakeResponse()

@patch.object(requests, "post", side_effect=fake_post)
def test_get_allocation_from_ollama(mock_post):
    """
    Ensure that the function correctly parses numbers from a mocked API response.
    """
    solar_used, grid_used = get_allocation_from_ollama(80, 100)
    assert isinstance(solar_used, int)
    assert isinstance(grid_used, int)
    assert solar_used == 75
    assert grid_used == 25

