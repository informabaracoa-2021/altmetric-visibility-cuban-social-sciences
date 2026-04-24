from pathlib import Path
import pandas as pd

def test_required_columns():
    path = Path("data/raw/Produccion_cientifica_Ciencias_Sociales_Cuba_2020_2024.xlsx")
    df = pd.read_excel(path, nrows=5)
    required = [
        "id",
        "publication_year",
        "doi",
        "Score",
        "cited_by_count",
        "open_access.oa_status",
        "primary_topic.display_name",
    ]
    missing = [c for c in required if c not in df.columns]
    assert not missing, f"Missing required columns: {missing}"
