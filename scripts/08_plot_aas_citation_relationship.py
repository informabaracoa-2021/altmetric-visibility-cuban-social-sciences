from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

INPUT_FILE = Path("data/processed/corpus_validated.csv")
RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DATA_OUTPUT = RESULTS_DIR / "figure_4_data.csv"
FIGURE_ES = FIGURES_DIR / "figure_4_aas_citations_es.png"
FIGURE_EN = FIGURES_DIR / "figure_4_aas_citations_en.png"

def build_subset(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["has_doi"]) & (df["Score_num"] > 0)].copy()

def compute_quadrants(df: pd.DataFrame) -> dict[str, float]:
    rho, pval = spearmanr(df["Score_num"], df["cited_by_count_num"])
    aas_p90 = df["Score_num"].quantile(0.9)
    cite_p90 = df["cited_by_count_num"].quantile(0.9)
    return {
        "rho": float(rho),
        "pval": float(pval),
        "aas_p90": float(aas_p90),
        "cite_p90": float(cite_p90),
        "high_high": int(((df["Score_num"] >= aas_p90) & (df["cited_by_count_num"] >= cite_p90)).sum()),
        "high_aas_low_cite": int(((df["Score_num"] >= aas_p90) & (df["cited_by_count_num"] < cite_p90)).sum()),
        "low_aas_high_cite": int(((df["Score_num"] < aas_p90) & (df["cited_by_count_num"] >= cite_p90)).sum()),
        "low_low": int(((df["Score_num"] < aas_p90) & (df["cited_by_count_num"] < cite_p90)).sum()),
        "zero_cited_with_attention": int((df["cited_by_count_num"] == 0).sum()),
        "zero_cited_with_attention_pct": float((df["cited_by_count_num"] == 0).mean() * 100),
    }

def plot_relationship(df: pd.DataFrame, stats: dict[str, float], output_file: Path, language: str) -> None:
    x=np.log1p(df["Score_num"]); y=np.log1p(df["cited_by_count_num"])
    fig,ax=plt.subplots(figsize=(9.5,7.2))
    ax.scatter(x, y, alpha=0.7, color="green")
    xthr=float(np.log1p(stats["aas_p90"])); ythr=float(np.log1p(stats["cite_p90"]))
    ax.axvline(xthr, linestyle="--", linewidth=1); ax.axhline(ythr, linestyle="--", linewidth=1)
    ax.set_xlabel("log(1 + Altmetric Attention Score)")
    ax.set_ylabel("log(1 + citas)" if language=="es" else "log(1 + citations)")
    ax.set_title("Relación entre atención altmétrica y citación" if language=="es" else "Relationship between altmetric attention and citations")
    xmax=float(x.max()); ymax=float(y.max())
    label_bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="0.75", alpha=0.9)
    if language=="es":
        quad_labels={"hh":f"Alta AAS\nAlta citación\nn = {stats['high_high']}",
                     "hl":f"Alta AAS\nBaja citación\nn = {stats['high_aas_low_cite']}",
                     "lh":f"Baja AAS\nAlta citación\nn = {stats['low_aas_high_cite']}",
                     "ll":f"Baja AAS\nBaja citación\nn = {stats['low_low']}"}
        summary=(f"n = {len(df)} publicaciones con DOI y AAS > 0\n"
                 f"Spearman ρ = {stats['rho']:.2f} (p < 0.001)\n"
                 f"Publicaciones con AAS > 0 y 0 citas: {stats['zero_cited_with_attention']} ({stats['zero_cited_with_attention_pct']:.1f}%)\n"
                 f"Percentil 90 AAS = {stats['aas_p90']:.1f}; Percentil 90 citas = {stats['cite_p90']:.1f}")
    else:
        quad_labels={"hh":f"High AAS\nHigh citations\nn = {stats['high_high']}",
                     "hl":f"High AAS\nLow citations\nn = {stats['high_aas_low_cite']}",
                     "lh":f"Low AAS\nHigh citations\nn = {stats['low_aas_high_cite']}",
                     "ll":f"Low AAS\nLow citations\nn = {stats['low_low']}"}
        summary=(f"n = {len(df)} publications with DOI and AAS > 0\n"
                 f"Spearman ρ = {stats['rho']:.2f} (p < 0.001)\n"
                 f"Publications with AAS > 0 and 0 citations: {stats['zero_cited_with_attention']} ({stats['zero_cited_with_attention_pct']:.1f}%)\n"
                 f"90th percentile AAS = {stats['aas_p90']:.1f}; 90th percentile citations = {stats['cite_p90']:.1f}")
    ax.text(xthr+(xmax-xthr)*0.55, ythr+(ymax-ythr)*0.55, quad_labels["hh"], ha="center", va="center", fontsize=9, fontweight="bold", bbox=label_bbox)
    ax.text(xthr+(xmax-xthr)*0.55, ythr*0.45, quad_labels["hl"], ha="center", va="center", fontsize=9, fontweight="bold", bbox=label_bbox)
    ax.text(xthr*0.45, ythr+(ymax-ythr)*0.55, quad_labels["lh"], ha="center", va="center", fontsize=9, fontweight="bold", bbox=label_bbox)
    ax.text(xthr*0.45, ythr*0.45, quad_labels["ll"], ha="center", va="center", fontsize=9, fontweight="bold", bbox=label_bbox)
    ax.text(0.02, 0.98, summary, transform=ax.transAxes, ha="left", va="top", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="0.8"))
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main():
    df=pd.read_csv(INPUT_FILE, low_memory=False)
    subset=build_subset(df)
    subset.to_csv(DATA_OUTPUT, index=False)
    stats=compute_quadrants(subset)
    plot_relationship(subset, stats, FIGURE_ES, language="es")
    plot_relationship(subset, stats, FIGURE_EN, language="en")

if __name__ == "__main__":
    main()
