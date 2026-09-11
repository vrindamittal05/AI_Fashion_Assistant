import json
from pathlib import Path


class Personalization:
    def __init__(self, profile_path="data/user_profile.json"):
        self.path = Path(profile_path)
        self.profile = {
            "liked_styles": {},
            "liked_categories": {},
            "saved_products": [],
            "skipped_products": [],
        }

        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                self.profile = json.load(f)

    def update(self, product, action):
        if action == "like":
            style = product["style"]
            category = product["category"]

            self.profile["liked_styles"][style] = (
                self.profile["liked_styles"].get(style, 0) + 1
            )
            self.profile["liked_categories"][category] = (
                self.profile["liked_categories"].get(category, 0) + 1
            )

        elif action == "save":
            if product["product_id"] not in self.profile["saved_products"]:
                self.profile["saved_products"].append(product["product_id"])

        elif action == "skip":
            if product["product_id"] not in self.profile["skipped_products"]:
                self.profile["skipped_products"].append(product["product_id"])

        self.save()

    def personalize(self, products):
        results = products.copy()

        def adjustment(row):
            adjustment = 0.0

            adjustment += 0.03 * self.profile["liked_styles"].get(
                row["style"], 0
            )

            adjustment += 0.03 * self.profile["liked_categories"].get(
                row["category"], 0
            )

            if row["product_id"] in self.profile["skipped_products"]:
                adjustment -= 0.30

            if row["product_id"] in self.profile["saved_products"]:
                adjustment += 0.20

            return adjustment

        results["personalization_score"] = results.apply(adjustment, axis=1)
        results["final_score"] += results["personalization_score"]

        return results.sort_values(
            "final_score", ascending=False
        ).reset_index(drop=True)

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=2)
