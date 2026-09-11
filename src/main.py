import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.context_extractor import extract_context
from src.embeddings import EmbeddingModel
from src.retrieval import SemanticRetriever
from src.reranking import rerank
from src.personalization import Personalization


PRODUCT_FILE = ROOT / "data" / "products.csv"
EMBEDDING_FILE = ROOT / "data" / "product_embeddings.npy"


def load_system():
    products = pd.read_csv(PRODUCT_FILE)

    model = EmbeddingModel()

    if EMBEDDING_FILE.exists():
        import numpy as np
        embeddings = np.load(EMBEDDING_FILE)
        print("Loaded cached product embeddings.")
    else:
        print("Creating product embeddings...")
        embeddings = model.encode_products(products["description"].tolist())

        import numpy as np
        np.save(EMBEDDING_FILE, embeddings)
        print("Saved product embeddings.")

    retriever = SemanticRetriever(products, embeddings)
    personalization = Personalization(ROOT / "data" / "user_profile.json")

    return model, retriever, personalization


def recommend(query, model, retriever, personalization, top_k=10):
    context = extract_context(query)

    query_embedding = model.encode_query(query)

    candidates = retriever.search(
        query_embedding,
        top_k=50,
    )

    ranked = rerank(
        candidates,
        context,
        top_k=30,
    )

    ranked = personalization.personalize(ranked)

    return context, ranked.head(top_k)


def main():
    if not PRODUCT_FILE.exists():
        print("products.csv not found.")
        print("Run this first:")
        print("python data/generate_products.py")
        return

    model, retriever, personalization = load_system()

    print("\nContext-Aware AI Shopping Agent")
    print("Type 'exit' to stop.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        context, recommendations = recommend(
            query,
            model,
            retriever,
            personalization,
        )

        print("\nExtracted context:")
        print(context)

        print("\nRecommendations:\n")

        for i, (_, row) in enumerate(
            recommendations.iterrows(), start=1
        ):
            print(
                f"{i}. {row['name']} | "
                f"{row['category']} | "
                f"{row['style']} | "
                f"{row['color']} | "
                f"₹{row['price']} | "
                f"score={row['final_score']:.3f}"
            )

        print()


if __name__ == "__main__":
    main()
