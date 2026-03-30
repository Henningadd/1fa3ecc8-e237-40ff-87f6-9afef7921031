from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fetch_weather_data():
    mock_response = MagicMock()
    mock_response.json.return_value = {"location": "Berlin", "temperature": 23, "condition": "Sunny"}
    mock_response.raise_for_status = MagicMock()
    mock_response.status_code = 200

    with patch("httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_response)
        
        response = client.get("/?location=Berlin")
        assert response.status_code == 200
        assert "Weather in Berlin" in response.text
        assert "Temperature: 23 °C" in response.text
        assert "Condition: Sunny" in response.text
