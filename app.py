import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from embeddings.search import search

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(request: QueryRequest):
    results = search(request.query, top_k=10)
    return {"recommended_assessments": results}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # This will now start in 1 second because the model isn't loading yet!
    uvicorn.run(app, host="0.0.0.0", port=port)