import csv
import random
from pathlib import Path

random.seed(42)

CATEGORIES = {
    "dresses": ["Midi Dress", "Maxi Dress", "Wrap Dress", "Bodycon Dress", "Shirt Dress"],
    "tops": ["Satin Top", "Crop Top", "Blouse", "Knit Top", "Oversized Shirt"],
    "ethnic": ["Anarkali", "Kurta Set", "Saree", "Sharara Set", "Lehenga"],
    "bottoms": ["Wide Leg Trousers", "Straight Jeans", "Palazzo Pants", "Pleated Skirt"],
    "shoes": ["Block Heels", "Sneakers", "Loafers", "Flats", "Sandals"],
    "accessories": ["Shoulder Bag", "Tote Bag", "Clutch", "Statement Earrings", "Watch"],
}

STYLES = ["elegant", "casual", "minimal", "trendy", "traditional", "formal", "streetwear"]
COLORS = ["black", "white", "beige", "blue", "pink", "green", "red", "brown", "navy", "lavender"]
OCCASIONS = ["college", "office", "party", "wedding", "date", "travel", "festive", "everyday"]
MATERIALS = ["cotton", "linen", "denim", "silk", "satin", "polyester", "knit"]

rows = []
product_id = 1

for _ in range(2000):
    category = random.choice(list(CATEGORIES))
    name = random.choice(CATEGORIES[category])
    style = random.choice(STYLES)
    color = random.choice(COLORS)
    occasion = random.choice(OCCASIONS)
    material = random.choice(MATERIALS)
    price = random.randrange(700, 10000, 100)

    description = (
        f"{color} {style} {name} for {occasion}. "
        f"Made from {material}. Suitable for {style} looks and {occasion} occasions."
    )

    rows.append({
        "product_id": f"P{product_id:04d}",
        "name": name,
        "category": category,
        "style": style,
        "color": color,
        "occasion": occasion,
        "material": material,
        "price": price,
        "description": description,
    })
    product_id += 1

output = Path(__file__).parent / "products.csv"

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} products -> {output}")
