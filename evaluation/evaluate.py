import pandas as pd
from embeddings.search import search


def recall_at_10(true_urls, predicted_results):
    predicted_urls = [p["url"] for p in predicted_results]
    correct = len(set(true_urls) & set(predicted_urls))
    return correct / len(true_urls)


def evaluate():
    df = pd.read_excel("Gen_AI Dataset.xlsx", sheet_name="Train-Set")

    grouped = df.groupby("Query")

    recalls = []

    for query, group in grouped:
        true_urls = list(group["Assessment_url"])
        predicted = search(query, top_k=10)

        r = recall_at_10(true_urls, predicted)
        recalls.append(r)

        print("\nQuery:", query[:80])
        print("Recall@10:", round(r, 3)) 

    mean_recall = sum(recalls) / len(recalls)

    print("\n===========================")
    print("Mean Recall@10:", round(mean_recall, 3))
    print("===========================")


if __name__ == "__main__":
    evaluate()