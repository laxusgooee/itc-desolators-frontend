def format_currency(value: float, symbol: str = "$") -> str:
    """Format a float as a currency string, e.g. 9.99 → '$9.99'."""
    return f"{symbol}{value:,.2f}"


def truncate(text: str, max_length: int = 60) -> str:
    """Truncate a string and append '…' if it exceeds max_length."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "…"

