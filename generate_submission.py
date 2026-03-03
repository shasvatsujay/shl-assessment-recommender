import pandas as pd
from embeddings.search import search

def generate_submission():
    print("Loading Test-Set...")
    # Load the unlabeled test set
    test_df = pd.read_excel("Gen_AI Dataset.xlsx", sheet_name="Test-Set")

    rows = []
    
    print("Generating predictions...")
    # Iterate through each query and get top 10 recommendations
    for query in test_df["Query"]:
        predictions = search(query, top_k=10)

        for p in predictions:
            rows.append({
                "Query": query,
                "Assessment_url": p["url"]
            })

    # Save to CSV
    submission_df = pd.DataFrame(rows)
    submission_df.to_csv("submission.csv", index=False)

    print("✅ submission.csv generated successfully!")

if __name__ == "__main__":
    generate_submission()
