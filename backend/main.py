import os
import sys
import uuid
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from data_loader import DataLoader
from investigation_engine import CasualCourtEngine
from models import InvestigationResult

app = FastAPI(
    title="CasualCourt Investigation Engine API",
    description="Autonomous business process investigator API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "CasualCourt_demo_dataset")
sample_engine = CasualCourtEngine(DATA_DIR)

# In-memory store for upload sessions
UPLOAD_SESSIONS: Dict[str, Dict[str, Any]] = {}

@app.get("/")
def read_root():
    return {
        "service": "CasualCourt Investigation Engine API",
        "status": "online",
        "endpoints": {
            "health": "/api/health",
            "sample_investigation": "/api/sample-investigation",
            "upload_and_validate": "/api/upload-and-validate",
            "run_uploaded_investigation": "/api/run-uploaded-investigation"
        }
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "engine_ready": True, "data_dir_exists": os.path.exists(DATA_DIR)}

@app.get("/api/investigation", response_model=InvestigationResult)
@app.get("/api/sample-investigation", response_model=InvestigationResult)
@app.post("/api/investigate", response_model=InvestigationResult)
def run_sample_investigation():
    try:
        result = sample_engine.run_investigation()
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"We couldn't complete the investigation: {str(e)}"}
        )

@app.post("/api/upload-and-validate")
async def upload_and_validate_files(files: List[UploadFile] = File(...)):
    try:
        raw_files = {}
        for file in files:
            content = await file.read()
            raw_files[file.filename] = content

        loader = DataLoader()
        data_dict, summary = loader.process_uploaded_files(raw_files)

        session_id = str(uuid.uuid4())
        UPLOAD_SESSIONS[session_id] = {
            "data_dict": data_dict,
            "summary": summary
        }

        # Format response
        return {
            "session_id": session_id,
            "can_run": summary["can_run"],
            "sources_recognized": summary["sources_recognized"],
            "validation_details": summary["validation_details"],
            "warnings": summary["warnings"]
        }
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"detail": f"Failed to parse uploaded files: {str(e)}"}
        )

@app.post("/api/run-uploaded-investigation")
def run_uploaded_investigation(payload: Dict[str, Any] = Body(...)):
    session_id = payload.get("session_id")
    if not session_id or session_id not in UPLOAD_SESSIONS:
        # Fallback to sample data if session not found
        return sample_engine.run_investigation()

    session_data = UPLOAD_SESSIONS[session_id]
    data_dict = session_data["data_dict"]

    from orchestrator import InvestigationOrchestrator

    try:
        orchestrator = InvestigationOrchestrator(data_dict=data_dict)
        return orchestrator.run_orchestrated_investigation()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"We couldn't complete the investigation. Check the data sources and try again."}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
