import re


OCCASION_KEYWORDS = {
    "wedding": ["wedding", "engagement", "shaadi", "marriage", "bride", "wedding guest"],
    "party": ["party", "club", "night out", "celebration"],
    "office": ["office", "work", "meeting", "corporate"],
    "college": ["college", "campus", "class"],
    "date": ["date", "dinner date"],
    "travel": ["travel", "vacation", "holiday", "trip"],
    "festive": ["festive", "festival", "diwali", "puja"],
    "everyday": ["everyday", "daily", "casual"],
}

STYLE_KEYWORDS = {
    "elegant": ["elegant", "classy", "sophisticated"],
    "casual": ["casual", "comfortable", "relaxed"],
    "minimal": ["minimal", "simple", "clean"],
    "trendy": ["trendy", "fashionable", "modern"],
    "traditional": ["traditional", "ethnic", "desi"],
    "formal": ["formal", "professional"],
    "streetwear": ["streetwear", "street", "oversized"],
}

COLOR_KEYWORDS = [
    "black", "white", "beige", "blue", "pink", "green",
    "red", "brown", "navy", "lavender"
]


def extract_budget(text: str):
    text = text.lower().replace(",", "")

    patterns = [
        r"(?:under|below|less than|upto|up to)\s*[₹rs.]?\s*(\d+)",
        r"[₹rs.]\s*(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return float(match.group(1))

    return None


def extract_first_match(text: str, mapping: dict):
    text = text.lower()

    for value, keywords in mapping.items():
        for keyword in keywords:
            if keyword in text:
                return value

    return None


def extract_context(query: str):
    context = {
        "query": query,
        "occasion": extract_first_match(query, OCCASION_KEYWORDS),
        "style": extract_first_match(query, STYLE_KEYWORDS),
        "color": next((c for c in COLOR_KEYWORDS if c in query.lower()), None),
        "budget": extract_budget(query),
    }

    return context
