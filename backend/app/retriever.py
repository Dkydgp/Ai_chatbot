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


# Words that help us understand common customer questions
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
    "seafood": [
        "seafood",
        "fish",
        "prawn",
        "prawns",
        "salmon"
    ]
}


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text


def expand_query(query):
    query = normalize(query)

    words = set(query.split())

    expanded_words = set(words)

    for group, synonyms in KEYWORD_GROUPS.items():

        if any(word in words for word in synonyms):
            expanded_words.add(group)
            expanded_words.update(synonyms)

    return expanded_words


def search_menu(query: str):

    query_words = expand_query(query)

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

            # Match query words
            for word in query_words:

                if len(word) > 2 and word in searchable_text:
                    score += 1

            # Extra relevance for category matches
            category_text = normalize(category)

            for word in query_words:

                if word in category_text:
                    score += 2

            # Vegetarian preference
            if "vegetarian" in query_words:

                vegetarian_words = [
                    "vegetarian",
                    "veggie",
                    "vegetables",
                    "mushroom",
                    "burrata",
                    "margherita",
                    "truffle",
                    "funghi"
                ]

                if any(
                    word in searchable_text
                    for word in vegetarian_words
                ):
                    score += 2

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
