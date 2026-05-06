def normalize_sort_order(order: str) -> str:
    return "desc" if order.lower() == "desc" else "asc"


def is_desc_order(order: str) -> bool:
    return normalize_sort_order(order) == "desc"
