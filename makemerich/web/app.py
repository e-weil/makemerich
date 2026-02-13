"""FastAPI web dashboard for MakeMeRich."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from makemerich.crystalbox.audit import AuditLog

app = FastAPI(title="MakeMeRich Dashboard", version="0.1.0")

# Static files and templates
static_dir = Path(__file__).parent / "static"
templates_dir = Path(__file__).parent / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(templates_dir))
audit = AuditLog(data_dir=Path("data/crystalbox"))


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page."""
    history = audit.get_history(limit=50)
    chain_valid = audit.verify_chain()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "trades": history,
        "chain_valid": chain_valid,
    })


@app.get("/api/trades")
async def get_trades(pair: str = None, limit: int = 50):
    """API endpoint for trade history."""
    return audit.get_history(pair=pair, limit=limit)


@app.get("/api/audit/verify")
async def verify_audit():
    """Verify the audit chain integrity."""
    return {"valid": audit.verify_chain()}


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
