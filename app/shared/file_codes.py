def build_file_code(entry_id: int) -> str:
    """Build the visual archive file code used by the UI."""

    if entry_id is None or entry_id < 1:
        return "#000"

    return f"#{entry_id:03d}"
