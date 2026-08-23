import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def load_json(filename):
    file_path = KNOWLEDGE_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


business_data = load_json("business.json")
menu_data = load_json("menu.json")


def search_menu(query: str):
    """
    Search the menu using simple keyword matching.
    Returns the most relevant menu items.
    """

    query_words = query.lower().split()
    results = []

    categories = menu_data["menu"]["categories"]

    for category, items in categories.items():

        for item in items:

            searchable_text = (
                item.get("name", "") + " " +
                item.get("description", "") + " " +
                category
            ).lower()

            score = 0

            for word in query_words:
                if len(word) > 2 and word in searchable_text:
                    score += 1

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
