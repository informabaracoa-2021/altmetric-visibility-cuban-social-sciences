from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/Produccion_cientifica_Ciencias_Sociales_Cuba_2020_2024.xlsx")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = PROCESSED_DIR / "corpus_validated.csv"

REQUIRED_COLUMNS = [
    "id",
    "publication_year",
    "doi",
    "Score",
    "cited_by_count",
    "open_access.oa_status",
    "primary_topic.display_name",
]

def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError("The input file is missing required columns: " + ", ".join(missing))

def derive_core_variables(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out[out["id"].notna()].copy()
    out["publication_year"] = pd.to_numeric(out["publication_year"], errors="coerce").astype("Int64")
    out["has_doi"] = out["doi"].notna() & out["doi"].astype(str).str.strip().ne("")
    out["Score_num"] = pd.to_numeric(out["Score"], errors="coerce").fillna(0)
    out["cited_by_count_num"] = pd.to_numeric(out["cited_by_count"], errors="coerce").fillna(0)
    out["has_altmetric_attention"] = out["Score_num"] > 0
    out["is_cited"] = out["cited_by_count_num"] > 0
    out["oa_status_clean"] = out["open_access.oa_status"].astype(str).str.strip().str.lower()
    out["primary_topic_clean"] = out["primary_topic.display_name"].astype(str).str.strip()
    return out

def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {RAW_FILE}")
    df = pd.read_excel(RAW_FILE)
    df.columns = [str(c).strip() for c in df.columns]
    validate_required_columns(df, REQUIRED_COLUMNS)
    df = derive_core_variables(df)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Validated corpus saved to: {OUTPUT_CSV}")
    print(f"Rows exported: {len(df):,}")

if __name__ == "__main__":
    main()
