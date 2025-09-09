from fastapi import FastAPI
from mapbox import Geocoder
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


load_dotenv()

app = FastAPI()
geocoder_service = Geocoder(access_token=os.getenv("MAPBOX_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory=".", html=True), name="static")



@app.get("/")
def read_root():
    return{"message": "Welcome to the Fastapi Geocoding Service"}

@app.get("/coordinates/{location_name}")
def get_coordinates(location_name:str):

    response = geocoder_service.forward(location_name)
    first_result = response.json().get("features")[0]
    return {
        "place_name": first_result.get("place_name"),
        "coordinates": first_result.get("geometry").get("coordinates")
    }
