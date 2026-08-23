import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def load_json(filename):
    file_path = KNOWLEDGE_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


business_data = load_json("business.json")
menu_data = load_json("menu.json")


KEYWORD_GROUPS = {
    "pizza": ["pizza", "pizzas"],
    "pasta": ["pasta", "pastas"],
    "burger": ["burger", "burgers"],
    "sandwich": ["sandwich", "sandwiches"],
    "drink": ["drink", "drinks", "beverage", "beverages"],
    "coffee": ["coffee", "latte", "cappuccino", "espresso"],
    "dessert": ["dessert", "desserts", "sweet"],
    "breakfast": ["breakfast", "morning"],
    "chicken": ["chicken"],
    "vegetarian": [
        "vegetarian",
        "veg",
        "veggie",
        "vegetables",
        "vegetable"
    ],
    "non_vegetarian": [
        "non veg",
        "non-veg",
        "non vegetarian",
        "chicken",
        "fish",
        "prawn",
        "prawns",
        "salmon",
        "lamb",
        "pepperoni"
    ]
}


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s₹]", " ", text)
    return text


def extract_price_limit(query):
    """
    Detect simple budget questions such as:
    - under 500
    - below ₹600
    - less than 700
    - within 500
    """

    query = normalize(query)

    patterns = [
        r"under\s*[₹rs\.]*\s*(\d+)",
        r"below\s*[₹rs\.]*\s*(\d+)",
        r"less\s+than\s*[₹rs\.]*\s*(\d+)",
        r"within\s*[₹rs\.]*\s*(\d+)",
        r"upto\s*[₹rs\.]*\s*(\d+)",
        r"up\s+to\s*[₹rs\.]*\s*(\d+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, query)

        if match:
            return int(match.group(1))

    return None


def expand_query(query):

    query = normalize(query)

    words = set(query.split())

    expanded_words = set(words)

    for group, synonyms in KEYWORD_GROUPS.items():

        if any(
            synonym in query
            for synonym in synonyms
        ):
            expanded_words.add(group)
            expanded_words.update(synonyms)

    return expanded_words


def is_vegetarian(item):

    name = item.get("name", "").lower()
    description = item.get("description", "").lower()

    text = f"{name} {description}"

    non_veg_words = [
        "chicken",
        "lamb",
        "fish",
        "prawn",
        "prawns",
        "salmon",
        "pepperoni",
        "bacon",
        "sausage",
        "pork"
    ]

    return not any(
        word in text
        for word in non_veg_words
    )


def search_menu(query: str):

    query_words = expand_query(query)

    price_limit = extract_price_limit(query)

    wants_vegetarian = (
        "vegetarian" in query_words
        or "veg" in query_words
        or "veggie" in query_words
    )

    wants_non_vegetarian = (
        "non_vegetarian" in query_words
    )

    results = []

    categories = menu_data["menu"]["categories"]

    for category, items in categories.items():

        for item in items:

            name = item.get("name", "")
            description = item.get("description", "")

            searchable_text = normalize(
                f"{category} {name} {description}"
            )

            score = 0

            # -------------------------
            # Keyword matching
            # -------------------------

            for word in query_words:

                if len(word) > 2 and word in searchable_text:
                    score += 1

            # Category matching gets extra weight

            category_text = normalize(category)

            for word in query_words:

                if word in category_text:
                    score += 2

            # -------------------------
            # Dietary filtering
            # -------------------------

            vegetarian = is_vegetarian(item)

            if wants_vegetarian:

                if vegetarian:
                    score += 5
                else:
                    continue

            if wants_non_vegetarian:

                if not vegetarian:
                    score += 5
                else:
                    continue

            # -------------------------
            # Price filtering
            # -------------------------

            if price_limit is not None:

                price = item.get("price")

                if price is None:
                    continue

                if price <= price_limit:
                    score += 5
                else:
                    continue

            # -------------------------
            # Save result
            # -------------------------

            if score > 0:

                results.append({
                    "score": score,
                    "category": category,
                    "item": item
                })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:10]


def get_business_information():
    return business_data
