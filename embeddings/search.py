import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load index
index = faiss.read_index("shl_index.faiss")

# Load metadata
with open("shl_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

def search(query, top_k=10):
    query_embedding = model.encode([query])
    
    # Grab extra results initially so we have enough left over after filtering
    fetch_k = top_k * 5 
    distances, indices = index.search(np.array(query_embedding), fetch_k)

    results = []

    for idx in indices[0]:
        # Safety check for valid indices
        if idx == -1 or idx >= len(metadata):
            continue
            
        meta = metadata[idx]
        
        # 🛑 STRICT RULE: Ignore "Pre-packaged Job Solutions" [cite: 46]
        name_lower = str(meta.get("name", "")).lower()
        url_lower = str(meta.get("url", "")).lower()
        
        if "solution" in name_lower or "solution" in url_lower:
            continue
            
        results.append({
            "url": meta["url"],
            "name": meta["name"],
            "adaptive_support": meta.get("adaptive_support", "No"),
            "description": meta.get("description", meta["name"]),
            "duration": meta.get("duration", 15),
            "remote_support": meta.get("remote_support", "Yes"),
            "test_type": meta.get("test_type", ["Knowledge & Skills"])
        })
        
        # Stop once we hit the requested number of valid recommendations
        if len(results) == top_k:
            break

    return results