from pathlib import Path
import pandas as pd


def test_core_result_files_exist():
    expected = [
        "results/table_1_analytic_base_by_year.csv",
        "results/altmetric_summary_table.csv",
        "results/table_2_oa_routes_visibility_citation.csv",
        "results/figure_4_data.csv",
        "results/figure_5_data.csv",
    ]
    for rel in expected:
        assert Path(rel).exists(), f"Missing expected output: {rel}"


def test_table_2_required_columns():
    df = pd.read_csv("results/table_2_oa_routes_visibility_citation.csv")
    required = [
        "oa_route",
        "publications_with_doi",
        "publications_with_aas_gt_0",
        "altmetric_coverage_pct",
        "median_aas_positive",
        "mean_citations",
        "median_citations",
        "pct_cited_publications",
    ]
    missing = [c for c in required if c not in df.columns]
    assert not missing, f"Missing columns in table_2_oa_routes_visibility_citation.csv: {missing}"


def test_figure_4_subset_nonempty():
    df = pd.read_csv("results/figure_4_data.csv")
    assert len(df) > 0, "AAS-citation subset is empty."
