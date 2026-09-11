def rerank(products, context, top_k=10):
    results = products.copy()

    def score(row):
        score = float(row["semantic_score"])

        if context.get("occasion") and row["occasion"] == context["occasion"]:
            score += 0.20

        if context.get("style") and row["style"] == context["style"]:
            score += 0.20

        if context.get("color") and row["color"] == context["color"]:
            score += 0.10

        budget = context.get("budget")
        if budget is not None:
            if row["price"] <= budget:
                score += 0.15
            else:
                score -= 0.25

        return score

    results["final_score"] = results.apply(score, axis=1)

    return (
        results
        .sort_values("final_score", ascending=False)
        .head(top_k)
        .reset_index(drop=True)
    )
