def menu(request):
    return {
        "menu": [
            {"name": "home", "link": "index", "active": ["index"]},
            {
                "name": "product",
                "link": "product:index",
                "active": ["product:category", "product:index"],
            },
            {"name": "contacts", "link": "contact", "active": ["contact"]},
        ]
    }
