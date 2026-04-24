from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

INPUT_FILE = Path("data/processed/corpus_validated.csv")
PROCESSED_DIR = Path("data/processed")
RESULTS_DIR = Path("results")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

PLATFORM_SUMMARY_OUTPUT = PROCESSED_DIR / "platform_summary.csv"
FIGURE_DATA_OUTPUT = RESULTS_DIR / "figure_2_data.csv"
TABLE_OUTPUT = RESULTS_DIR / "altmetric_summary_table.csv"

PLATFORM_ALIASES = {
    "Altmetric Attention Score": ["Score_num", "Score"],
    "X users": [" X users", "X users", "X posts_count"],
    "Mendeley readers": ["Mendeley readers ", "Mendeley ", "readers_count"],
    "Facebook pages": ["Facebook page", "facebook posts_count"],
    "News outlets": ["News outlets", "news posts_count"],
    "Blogs": ["Blogs", "blogs posts_count"],
    "Wikipedia pages": ["Wikipedia pages", "wikipedia posts_count"],
    "Policy sources": ["Policy sources", "policy posts_count"],
    "Redditors": ["Redditors", "reddit posts_count"],
    "Peer review sites": ["Peer review site", "peer_review posts_count"],
    "YouTube creators": ["YouTube creator", "video posts_count"],
    "Patents": ["Patent", "patent posts_count"],
    "Bluesky users": ["Bluesky user", "bluesky posts_count"],
    "Clinical guideline sources": ["Clinical guideline source", "clinical_guidelines posts_count"],
}

ECOLOGY_PLATFORMS = [
    "X users",
    "Mendeley readers",
    "Facebook pages",
    "News outlets",
    "Blogs",
    "Wikipedia pages",
    "Policy sources",
    "Redditors",
    "Peer review sites",
    "YouTube creators",
    "Patents",
    "Bluesky users",
    "Clinical guideline sources",
]

def resolve_columns(df: pd.DataFrame) -> dict[str, str]:
    mapping = {}
    for label, aliases in PLATFORM_ALIASES.items():
        for alias in aliases:
            if alias in df.columns:
                mapping[label] = alias
                break
    if "Altmetric Attention Score" not in mapping:
        raise ValueError("Could not resolve a column for Altmetric Attention Score.")
    return mapping

def safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0)

def build_platform_summary(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    total_publications = len(df)
    rows = []
    for label, col in mapping.items():
        values = safe_numeric(df[col])
        positive = values[values > 0]
        rows.append({
            "metric": label,
            "coverage_publications": int((values > 0).sum()),
            "coverage_pct": float((values > 0).mean() * 100),
            "total_mentions_or_readers": float(values.sum()),
            "mean_all": float(values.mean()) if len(values) else 0,
            "mean_positive": float(positive.mean()) if len(positive) else 0,
            "median_positive": float(positive.median()) if len(positive) else 0,
            "std_positive": float(positive.std(ddof=1)) if len(positive) > 1 else 0,
            "maximum": float(values.max()) if len(values) else 0,
            "p90_positive": float(np.percentile(positive, 90)) if len(positive) else 0,
        })
    return pd.DataFrame(rows)

def build_platform_ecology_inputs(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    altmetric_subset = df[df["Score_num"] > 0].copy()
    rows = []
    for label in ECOLOGY_PLATFORMS:
        if label not in mapping:
            continue
        col = mapping[label]
        values = safe_numeric(altmetric_subset[col])
        covered = values > 0
        positive_values = values[covered]
        other_platforms = []
        for other_label in ECOLOGY_PLATFORMS:
            if other_label == label or other_label not in mapping:
                continue
            other_platforms.append(safe_numeric(altmetric_subset[mapping[other_label]]) > 0)
        if other_platforms:
            any_other = pd.concat(other_platforms, axis=1).any(axis=1)
            exclusive_count = int((covered & ~any_other).sum())
            exclusivity = exclusive_count / int(covered.sum()) * 100 if int(covered.sum()) else np.nan
        else:
            exclusivity = np.nan
        rows.append({
            "platform": label,
            "coverage_pct_altmetric_subset": float(covered.mean() * 100),
            "total_volume": float(values.sum()),
            "conditional_mean": float(positive_values.mean()) if len(positive_values) else 0,
            "exclusivity_pct": float(exclusivity) if pd.notna(exclusivity) else np.nan,
        })
    return pd.DataFrame(rows)

def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    mapping = resolve_columns(df)
    summary = build_platform_summary(df, mapping)
    ecology = build_platform_ecology_inputs(df, mapping)
    summary.to_csv(TABLE_OUTPUT, index=False)
    ecology.to_csv(FIGURE_DATA_OUTPUT, index=False)
    ecology.to_csv(PLATFORM_SUMMARY_OUTPUT, index=False)
    print(f"Altmetric summary table exported to: {TABLE_OUTPUT}")

if __name__ == "__main__":
    main()
