"""
MakeMeRich API — by FORGE
Simple FastAPI server to serve the web app and provide optional API features.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="MakeMeRich", version="0.2.0")

# Serve the static app
APP_DIR = Path(__file__).parent.parent

app.mount("/css", StaticFiles(directory=str(APP_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(APP_DIR / "js")), name="js")
app.mount("/data", StaticFiles(directory=str(APP_DIR / "data")), name="data")
app.mount("/assets", StaticFiles(directory=str(APP_DIR / "assets")), name="assets")


@app.get("/")
async def index():
    return FileResponse(str(APP_DIR / "index.html"))


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.2.0", "app": "MakeMeRich"}
