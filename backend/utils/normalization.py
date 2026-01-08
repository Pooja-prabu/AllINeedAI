def normalize_tool(tool: dict) -> dict:
    return {
        "id": tool.get("id"),
        "name": tool.get("name", ""),
        "description": tool.get("description", ""),
        "category": tool.get("category", ""),
        "tags": tool.get("tags") or [],
        "url": tool.get("url") or tool.get("website"),
        "rating": tool.get("rating", 0.0),
        "pricing": tool.get("pricing", "unknown"),
        "trending": tool.get("trending", False),
        "popularity": tool.get("popularity", 0),
        "reviews": tool.get("reviews") or []
    }
