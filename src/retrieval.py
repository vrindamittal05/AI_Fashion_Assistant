import numpy as np


class SemanticRetriever:
    def __init__(self, products, embeddings):
        self.products = products.reset_index(drop=True)
        self.embeddings = np.asarray(embeddings)

    def search(self, query_embedding, top_k=30):
        scores = self.embeddings @ query_embedding
        indices = np.argsort(scores)[::-1][:top_k]

        results = self.products.iloc[indices].copy()
        results["semantic_score"] = scores[indices]

        return results.reset_index(drop=True)
