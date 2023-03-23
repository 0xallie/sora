from __future__ import annotations


def pluralize(n: int, singular: str, plural: str | None = None) -> str:
    plural = plural or f"{singular}s"
    return singular if n == 1 else plural
