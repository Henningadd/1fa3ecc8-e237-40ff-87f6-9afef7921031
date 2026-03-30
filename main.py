import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

API_BASE_URL = "https://api.weatherapi.com/v1/current.json"

@app.get("/", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = "Berlin"):
    API_KEY = os.getenv("WEATHER_API_KEY")  # Fetching API key from environment variable.
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured")

    params = {
        "key": API_KEY,
        "q": city
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error fetching data from Weather API")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service unavailable")
        except ValueError:
            raise HTTPException(status_code=500, detail="Error parsing data from Weather API")

    return templates.TemplateResponse("index.html", {"request": request, "data": data})

# Ensure the template directory and index.html exists for demonstration purposes
os.makedirs(Path(__file__).parent / "templates", exist_ok=True)
with open(Path(__file__).parent / "templates/index.html", "w") as file:
    file.write("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather App</title>
    </head>
    <body>
        <h1>Weather in {{ data['location']['name'] }}</h1>
        <p>Temperature: {{ data['current']['temp_c'] }}°C</p>
        <p>Condition: {{ data['current']['condition']['text'] }}</p>
    </body>
    </html>
    """)

# Create or update requirements.txt
with open("requirements.txt", "w") as file:
    file.write("\n".join([
        "fastapi",
        "httpx",
        "jinja2",
        "pytest"
    ]))
