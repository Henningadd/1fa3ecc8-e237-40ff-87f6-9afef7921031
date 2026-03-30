from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
import os
from main import app

client = TestClient(app)

def test_get_weather_success():
    # Setting the environment variable required for the test
    os.environ["WEATHER_API_KEY"] = "test_api_key"

    # Mocking the response to simulate successful data retrieval from API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "location": {"name": "Berlin"},
        "current": {
            "temp_c": 20,
            "condition": {"text": "Sunny"}
        }
    }
    mock_response.raise_for_status = MagicMock()
    mock_response.status_code = 200

    # Patching the httpx.AsyncClient to control its behavior in the test
    with patch("httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_response)

        response = client.get("/", params={"city": "Berlin"})
        assert response.status_code == 200
        assert "Weather in Berlin" in response.text
        assert "Temperature: 20°C" in response.text
        assert "Condition: Sunny" in response.text
