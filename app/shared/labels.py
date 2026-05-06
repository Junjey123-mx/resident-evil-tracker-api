CATEGORY_LABELS = {
    "main_series": "JUEGO PRINCIPAL",
    "remake": "REMAKE",
    "prequel": "PRECUELA",
    "spin_off": "SPIN-OFF",
    "expansion": "EXPANSIÓN",
}

CATEGORY_VARIANTS = {
    "main_series": "primary",
    "remake": "danger",
    "prequel": "warning",
    "spin_off": "secondary",
    "expansion": "muted",
}

STATUS_LABELS = {
    "registered": "REGISTERED",
    "pending": "PENDING",
    "archived": "ARCHIVED",
}

STATUS_VARIANTS = {
    "registered": "success",
    "pending": "warning",
    "archived": "muted",
}

THREAT_LEVEL_LABELS = {
    "low": "LOW",
    "medium": "MEDIUM",
    "high": "HIGH",
    "critical": "CRITICAL",
}

THREAT_VARIANTS = {
    "low": "low",
    "medium": "medium",
    "high": "high",
    "critical": "critical",
}


def _fallback_label(value: str | None) -> str:
    if value:
        return value.upper()

    return "UNKNOWN"


def get_category_label(category: str | None) -> str:
    return CATEGORY_LABELS.get(category, _fallback_label(category))


def get_status_label(status: str | None) -> str:
    return STATUS_LABELS.get(status, _fallback_label(status))


def get_threat_level_label(threat_level: str | None) -> str:
    return THREAT_LEVEL_LABELS.get(threat_level, _fallback_label(threat_level))


def get_category_variant(category: str | None) -> str:
    return CATEGORY_VARIANTS.get(category, "muted")


def get_status_variant(status: str | None) -> str:
    return STATUS_VARIANTS.get(status, "muted")


def get_threat_variant(threat_level: str | None) -> str:
    return THREAT_VARIANTS.get(threat_level, "muted")


def has_cover(cover_image_url: str | None) -> bool:
    return bool(cover_image_url and cover_image_url.strip())
