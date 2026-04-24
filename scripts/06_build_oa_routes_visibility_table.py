from __future__ import annotations

from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/corpus_validated.csv")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RESULTS_DIR / "table_2_oa_routes_visibility_citation.csv"

ROUTE_ORDER = ["diamond", "green", "hybrid", "gold", "closed", "bronze"]
ROUTE_LABELS_ES = {"diamond":"Diamante","green":"Verde","hybrid":"Híbrido","gold":"Dorado","closed":"Cerrado","bronze":"Bronce"}
ROUTE_LABELS_EN = {"diamond":"Diamond","green":"Green","hybrid":"Hybrid","gold":"Gold","closed":"Closed","bronze":"Bronze"}

def build_oa_visibility_table(df: pd.DataFrame) -> pd.DataFrame:
    subset = df[df["has_doi"]].copy()
    rows=[]
    for route in ROUTE_ORDER:
        g=subset[subset["oa_status_clean"]==route].copy()
        if g.empty:
            continue
        g_attention=g[g["Score_num"]>0].copy()
        rows.append({
            "oa_route": route,
            "oa_route_es": ROUTE_LABELS_ES[route],
            "oa_route_en": ROUTE_LABELS_EN[route],
            "publications_with_doi": int(len(g)),
            "publications_with_aas_gt_0": int(len(g_attention)),
            "altmetric_coverage_pct": float(len(g_attention)/len(g)*100),
            "median_aas_positive": float(g_attention["Score_num"].median()) if len(g_attention) else 0.0,
            "mean_citations": float(g["cited_by_count_num"].mean()),
            "median_citations": float(g["cited_by_count_num"].median()),
            "pct_cited_publications": float((g["cited_by_count_num"]>0).mean()*100),
        })
    return pd.DataFrame(rows)

def main():
    df=pd.read_csv(INPUT_FILE, low_memory=False)
    table=build_oa_visibility_table(df)
    table.to_csv(OUTPUT_FILE,index=False)

if __name__ == "__main__":
    main()
