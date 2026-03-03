import pandas as pd
import numpy as np
import faiss
import pickle
import json
from sentence_transformers import SentenceTransformer

print("Loading detailed catalog...")
df = pd.read_csv("scraper/shl_catalog_detailed.csv")

# Convert the JSON string of test types back into a native Python list for the API
df["test_type"] = df["test_type"].apply(lambda x: json.loads(x) if isinstance(x, str) else ["Knowledge & Skills"])

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings using rich descriptions...")
# This is where the magic happens: combining name and the new deep descriptions!
texts = (df["name"] + " " + df["description"]).tolist()
embeddings = model.encode(texts, show_progress_bar=True)

print("Creating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

print("Saving index...")
faiss.write_index(index, "shl_index.faiss")

print("Saving rich metadata...")
with open("shl_metadata.pkl", "wb") as f:
    pickle.dump(df.to_dict(orient="records"), f)

print("✅ Index built successfully with deep metadata!")