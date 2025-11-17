from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os

from database import db, create_document, get_documents
from schemas import Subscriber, Lead, Testimonial, HealthResponse

app = FastAPI(title="Blue Whale Marketing API", version="1.0.0")

# CORS setup - allow all origins by default for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Blue Whale Marketing API is running", "time": datetime.utcnow().isoformat()}

@app.get("/test", response_model=HealthResponse)
def test():
    try:
        # simple roundtrip to db
        collections = db.list_collection_names()
        return HealthResponse(
            backend="fastapi",
            database="mongodb",
            database_url=os.getenv("DATABASE_URL", "mongodb://localhost:27017"),
            database_name=os.getenv("DATABASE_NAME", "app_db"),
            connection_status="connected",
            collections=collections,
            timestamp=datetime.utcnow(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Marketing site endpoints

@app.post("/subscribe")
def subscribe(payload: Subscriber):
    try:
        doc_id = create_document("subscriber", payload.model_dump())
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/lead")
def create_lead(payload: Lead):
    try:
        doc_id = create_document("lead", payload.model_dump())
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/testimonials", response_model=List[Testimonial])
def list_testimonials():
    try:
        docs = get_documents("testimonial", limit=12)
        # Coerce to Testimonial list shape ignoring extra fields
        out: List[Testimonial] = []
        for d in docs:
            out.append(Testimonial(author=d.get("author", "Anonymous"), role=d.get("role"), content=d.get("content", ""), rating=d.get("rating", 5)))
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
