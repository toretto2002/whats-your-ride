import re


def extract_float(text: str) -> float | None:
    match = re.search(r"[\d\.,]+", text)
    if match:
        return float(match.group(0).replace(",", "."))
    return None

def extract_int(text: str) -> int | None:
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def parse_mm(val: str) -> float:
    match = re.search(r"([\d,\.]+)", val)
    return float(match.group(1).replace(",", ".")) if match else None

def parse_kg(val: str) -> float:
    return parse_mm(val)

def parse_float(val: str) -> float:
    return parse_mm(val)

def parse_price(val: str) -> float:
    return parse_mm(val.replace("€", ""))

def parse_boolean(val: str) -> bool:
    return val.strip().lower() in ["sì", "si", "yes", "true"]

def parse_power(val: str) -> dict:
    hp_match = re.search(r"([\d,\.]+)\s*CV", val)
    rpm_match = re.search(r"(\d{3,5})\s*rpm", val)
    return {
        "power_hp": float(hp_match.group(1).replace(",", ".")) if hp_match else None,
        "power_rpm": int(rpm_match.group(1)) if rpm_match else None
    }

def parse_torque(val: str) -> dict:
    nm_match = re.search(r"([\d,\.]+)\s*Nm", val)
    rpm_match = re.search(r"(\d{3,5})\s*rpm", val)
    return {
        "torque_nm": float(nm_match.group(1).replace(",", ".")) if nm_match else None,
        "torque_rpm": int(rpm_match.group(1)) if rpm_match else None
    }
