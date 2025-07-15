import re


def extract_float(text: str) -> float | None:
    match = re.search(r"[\d\.,]+", text)
    if match:
        return float(match.group(0).replace(",", "."))
    return None

def extract_int(text: str) -> int | None:
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None