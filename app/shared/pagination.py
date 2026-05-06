from math import ceil


def calculate_offset(page: int, limit: int) -> int:
    safe_page = max(page, 1)
    safe_limit = max(limit, 1)
    return (safe_page - 1) * safe_limit


def calculate_total_pages(total: int, limit: int) -> int:
    if total <= 0:
        return 0

    safe_limit = max(limit, 1)
    return ceil(total / safe_limit)


def has_next_page(page: int, total_pages: int) -> bool:
    return page < total_pages


def has_previous_page(page: int) -> bool:
    return page > 1
