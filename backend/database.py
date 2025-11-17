import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection

# Environment configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[MongoClient] = None
_db = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(DATABASE_URL)
    return _client


def get_db():
    global _db
    if _db is None:
        _db = get_client()[DATABASE_NAME]
    return _db


# Public db handle
db = get_db()


def get_collection(name: str) -> Collection:
    return db[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    col = get_collection(collection_name)
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    result = col.insert_one(payload)
    return str(result.inserted_id)


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    col = get_collection(collection_name)
    q = filter_dict or {}
    docs = (
        col.find(q).sort("created_at", -1).limit(limit)
    )
    out: List[Dict[str, Any]] = []
    for d in docs:
        d["_id"] = str(d.get("_id"))
        out.append(d)
    return out
