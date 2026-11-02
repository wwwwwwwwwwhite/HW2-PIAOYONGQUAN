from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import Request
from .recommender import recommend

app = FastAPI(title="BuildMyPC")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def index(): return FileResponse("app/static/index.html")

@app.get("/health")
def health(): return {"status": "ok", "service": "BuildMyPC"}

@app.post("/api/recommend")
def create_recommendation(request: Request): return recommend(request)

