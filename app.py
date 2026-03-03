from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from embeddings.search import search

app = FastAPI()

# Define the expected request body format
class QueryRequest(BaseModel):
    query: str

# 1. Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 2. Assessment Recommendation Endpoint
@app.post("/recommend")
def recommend(request: QueryRequest):
    # Retrieve top 10 recommendations based on the query
    results = search(request.query, top_k=10)
    
    return {
        "recommended_assessments": results
    }

if __name__ == "__main__":
    print("Starting SHL Recommendation API on http://0.0.0.0:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)