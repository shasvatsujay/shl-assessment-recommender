import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# We set these to None initially
_model = None
_index = None
_metadata = None

def load_resources():
    global _model, _index, _metadata
    if _model is None:
        print("Loading SentenceTransformer...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    if _index is None:
        print("Loading FAISS Index...")
        _index = faiss.read_index("shl_index.faiss")
    if _metadata is None:
        print("Loading Metadata...")
        with open("shl_metadata.pkl", "rb") as f:
            _metadata = pickle.load(f)

def search(query, top_k=10):
    # Only load the heavy stuff when a request actually comes in
    load_resources()
    
    query_embedding = _model.encode([query])
    fetch_k = top_k * 5 
    distances, indices = _index.search(np.array(query_embedding), fetch_k)

    results = []
    for idx in indices[0]:
        if idx == -1 or idx >= len(_metadata): continue
        meta = _metadata[idx]
        
        name_lower = str(meta.get("name", "")).lower()
        url_lower = str(meta.get("url", "")).lower()
        if "solution" in name_lower or "solution" in url_lower: continue
            
        results.append({
            "url": meta["url"],
            "name": meta["name"],
            "adaptive_support": meta.get("adaptive_support", "No"),
            "description": meta.get("description", meta["name"]),
            "duration": meta.get("duration", 15),
            "remote_support": meta.get("remote_support", "Yes"),
            "test_type": meta.get("test_type", ["Knowledge & Skills"])
        })
        if len(results) == top_k: break
    return results