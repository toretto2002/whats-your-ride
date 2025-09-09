from pathlib import Path

def load_prompt(relative_path_from_root: str) -> str:
    full_path = Path("recommender_app/" + relative_path_from_root).resolve()
    print(f"[DEBUG] Prompt path risolto: {full_path}")

    if not full_path.exists():
        raise FileNotFoundError(f"[Prompt Error] Il file '{full_path}' non esiste.")

    with full_path.open("r", encoding="utf-8") as f:
        return f.read()
