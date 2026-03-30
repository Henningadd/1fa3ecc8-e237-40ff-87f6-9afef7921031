from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import httpx

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

API_URL = "https://api.example.com/weather"  # Beispiel-API-URL

async def fetch_weather_data(location: str) -> dict:
    """Fetch weather data from external API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL, params={'location': location})
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=str(e))
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.get("/", response_class=HTMLResponse)
async def read_weather(request: Request, location: str = "Berlin"):
    """Fetch and display weather data."""
    data = await fetch_weather_data(location)
    return templates.TemplateResponse("index.html", {"request": request, "data": data})
