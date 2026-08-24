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


# ============================================================
# KEYWORD GROUPS
# ============================================================

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
        "non-vegetarian",
        "chicken",
        "fish",
        "prawn",
        "prawns",
        "salmon",
        "lamb",
        "pepperoni",
        "bacon",
        "sausage",
        "pork",
        "egg",
        "eggs",
        "meat",
        "seafood"
    ]
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s₹]",
        " ",
        text
    )

    return text


# ============================================================
# GET ALL MENU ITEMS
# ============================================================

def get_all_menu_items():
    """Return every menu item in one list."""

    items = []

    categories = menu_data["menu"]["categories"]

    for category, category_items in categories.items():

        for item in category_items:

            item_copy = item.copy()

            item_copy["category"] = category

            items.append(item_copy)

    return items


# ============================================================
# GET FOOD TYPE
# ============================================================

def get_food_type(item):
    """
    Read the diet field directly from menu.json.

    Expected values:
        veg
        non-veg
    """

    value = item.get("diet")

    if value is None:
        return ""

    return str(value).lower().strip()


# ============================================================
# VEGETARIAN CHECK
# ============================================================

def is_vegetarian(item):

    diet = get_food_type(item)

    return diet == "veg"


# ============================================================
# NON-VEGETARIAN CHECK
# ============================================================

def is_non_vegetarian(item):

    diet = get_food_type(item)

    return diet == "non-veg"


# ============================================================
# CHEAPEST ITEM
# ============================================================

def get_cheapest_item(items=None):
    """Find the cheapest item."""

    if items is None:
        items = get_all_menu_items()

    priced_items = [
        item
        for item in items
        if isinstance(
            item.get("price"),
            (int, float)
        )
    ]

    if not priced_items:
        return None

    return min(
        priced_items,
        key=lambda item: item["price"]
    )


# ============================================================
# MOST EXPENSIVE ITEM
# ============================================================

def get_most_expensive_item(items=None):
    """Find the most expensive item."""

    if items is None:
        items = get_all_menu_items()

    priced_items = [
        item
        for item in items
        if isinstance(
            item.get("price"),
            (int, float)
        )
    ]

    if not priced_items:
        return None

    return max(
        priced_items,
        key=lambda item: item["price"]
    )


# ============================================================
# ITEMS UNDER PRICE
# ============================================================

def get_items_under_price(
    max_price,
    items=None
):
    """Return all items at or below a given price."""

    if items is None:
        items = get_all_menu_items()

    return [
        item
        for item in items
        if isinstance(
            item.get("price"),
            (int, float)
        )
        and item["price"] <= max_price
    ]


# ============================================================
# CATEGORY SEARCH
# ============================================================

def get_items_in_category(category_keyword):
    """Return menu items belonging to a category."""

    category_keyword = normalize(
        category_keyword
    )

    results = []

    categories = menu_data["menu"]["categories"]

    for category, items in categories.items():

        category_text = normalize(
            category
        )

        if category_keyword in category_text:

            for item in items:

                item_copy = item.copy()

                item_copy["category"] = category

                results.append(item_copy)

    return results


# ============================================================
# PRICE EXTRACTION
# ============================================================

def extract_price_limit(query):
    """
    Extract price limits such as:
    under 500
    below ₹700
    less than 600
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

        match = re.search(
            pattern,
            query
        )

        if match:
            return int(
                match.group(1)
            )

    return None


# ============================================================
# EXPAND QUERY
# ============================================================

def expand_query(query):

    query = normalize(query)

    words = set(
        query.split()
    )

    expanded_words = set(words)

    for group, synonyms in KEYWORD_GROUPS.items():

        if any(
            synonym in query
            for synonym in synonyms
        ):

            expanded_words.add(
                group
            )

            expanded_words.update(
                synonyms
            )

    return expanded_words


# ============================================================
# SEARCH MENU
# ============================================================

def search_menu(query: str):

    query_words = expand_query(
        query
    )

    price_limit = extract_price_limit(
        query
    )

    wants_vegetarian = (
        "vegetarian" in query_words
        or "veg" in query_words
        or "veggie" in query_words
    )

    wants_non_vegetarian = (
    "non_vegetarian" in query_words
    or "non veg" in query_words
    or "non-veg" in query_words
    or "non vegetarian" in query_words
    or "non-vegetarian" in query_words
    )

    results = []

    categories = menu_data["menu"]["categories"]

    for category, items in categories.items():

        for item in items:

            name = item.get(
                "name",
                ""
            )

            description = item.get(
                "description",
                ""
            )

            searchable_text = normalize(
                f"{category} {name} {description}"
            )

            score = 0

            # ------------------------------------------------
            # Keyword matching
            # ------------------------------------------------

            for word in query_words:

                if (
                    len(word) > 2
                    and word in searchable_text
                ):

                    score += 1

            # ------------------------------------------------
            # Category matching
            # ------------------------------------------------

            category_text = normalize(
                category
            )

            for word in query_words:

                if word in category_text:
                    score += 2

            # ------------------------------------------------
            # Dietary filtering
            # ------------------------------------------------

            if wants_vegetarian:

                if is_vegetarian(item):
                    score += 5

                else:
                    continue

            if wants_non_vegetarian:

                if is_non_vegetarian(item):
                    score += 5

                else:
                    continue

            # ------------------------------------------------
            # Price filtering
            # ------------------------------------------------

            if price_limit is not None:

                price = item.get(
                    "price"
                )

                if not isinstance(
                    price,
                    (int, float)
                ):
                    continue

                if price <= price_limit:
                    score += 5

                else:
                    continue

            # ------------------------------------------------
            # Add result
            # ------------------------------------------------

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


# ============================================================
# BUSINESS INFORMATION
# ============================================================

def get_business_information():

    return business_data