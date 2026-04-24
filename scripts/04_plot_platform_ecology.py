from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

INPUT_FILE = Path("data/processed/platform_summary.csv")
FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_ES = FIGURES_DIR / "figure_2_platform_ecology_es.png"
OUTPUT_EN = FIGURES_DIR / "figure_2_platform_ecology_en.png"

PLATFORM_ORDER = [
    "X users", "Mendeley readers", "Facebook pages", "News outlets", "Blogs",
    "Wikipedia pages", "Policy sources", "Redditors", "Peer review sites",
    "YouTube creators", "Patents", "Bluesky users", "Clinical guideline sources",
]
PLATFORM_COLORS = {
    "X users": "#000000",
    "Mendeley readers": "#b71c1c",
    "Facebook pages": "#1877F2",
    "News outlets": "#F39C12",
    "Blogs": "#8E44AD",
    "Wikipedia pages": "#7F8C8D",
    "Policy sources": "#16A085",
    "Redditors": "#FF4500",
    "Peer review sites": "#2E86C1",
    "YouTube creators": "#FF0000",
    "Patents": "#6E2C00",
    "Bluesky users": "#3498DB",
    "Clinical guideline sources": "#27AE60",
}

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out[out["platform"].isin(PLATFORM_ORDER)].copy()
    out["platform"] = pd.Categorical(out["platform"], categories=PLATFORM_ORDER, ordered=True)
    out = out.sort_values("platform").reset_index(drop=True)
    out["total_volume_log10"] = 0.0
    positive_mask = out["total_volume"] > 0
    out.loc[positive_mask, "total_volume_log10"] = np.log10(out.loc[positive_mask, "total_volume"])
    return out

def normalize_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        vmax = out[col].max(skipna=True)
        out[f"{col}_norm"] = out[col] / vmax if pd.notna(vmax) and vmax > 0 else 0
    return out

def blend_with_white(hex_color: str, intensity: float) -> tuple[float, float, float]:
    base = np.array(mcolors.to_rgb(hex_color))
    white = np.array([1.0, 1.0, 1.0])
    return tuple(white - (white - base) * intensity)

def plot_ecology(df: pd.DataFrame, output_file: Path, language: str) -> None:
    metrics = [
        ("coverage_pct_altmetric_subset", "Cobertura" if language == "es" else "Coverage"),
        ("total_volume_log10", "Volumen total (log10)" if language == "es" else "Total volume (log10)"),
        ("conditional_mean", "Intensidad media condicional" if language == "es" else "Conditional mean intensity"),
        ("exclusivity_pct", "Exclusividad" if language == "es" else "Exclusivity"),
    ]
    fig = plt.figure(figsize=(13.2, 7.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.65], wspace=0.18)
    ax_left = fig.add_subplot(gs[0, 0])
    ax_right = fig.add_subplot(gs[0, 1])

    y = np.arange(len(df))
    colors = [PLATFORM_COLORS[p] for p in df["platform"].astype(str)]
    ax_left.barh(y, df["coverage_pct_altmetric_subset"], color=colors, height=0.72)
    ax_left.set_yticks(y)
    ax_left.set_yticklabels(df["platform"])
    ax_left.invert_yaxis()
    ax_left.set_xlabel("Cobertura entre publicaciones con atención (%)" if language == "es" else "Coverage among publications with attention (%)")
    ax_left.set_title("Panel A. Cobertura por plataforma" if language == "es" else "Panel A. Platform coverage")
    ax_left.grid(axis="x", linewidth=0.4, alpha=0.3)
    for spine in ["top", "right"]:
        ax_left.spines[spine].set_visible(False)

    ax_right.set_xlim(0, len(metrics))
    ax_right.set_ylim(0, len(df))
    ax_right.invert_yaxis()
    ax_right.set_xticks(np.arange(len(metrics)) + 0.5)
    ax_right.set_xticklabels([m[1] for m in metrics], rotation=20, ha="right")
    ax_right.set_yticks(np.arange(len(df)) + 0.5)
    ax_right.set_yticklabels(df["platform"])
    ax_right.set_title("Panel B. Matriz analítica de plataformas" if language == "es" else "Panel B. Analytical platform matrix")

    for i, row in df.iterrows():
        platform = str(row["platform"])
        base_color = PLATFORM_COLORS[platform]
        for j, (metric_col, _) in enumerate(metrics):
            val = row[metric_col]
            norm_val = row[f"{metric_col}_norm"]
            if pd.isna(val):
                facecolor = (1, 1, 1)
                label = ""
            else:
                facecolor = blend_with_white(base_color, max(float(norm_val), 0.08))
                if metric_col == "total_volume_log10":
                    label = f"{val:.2f}"
                elif metric_col in ["coverage_pct_altmetric_subset", "exclusivity_pct"]:
                    label = f"{val:.1f}"
                else:
                    label = f"{val:.2f}".rstrip("0").rstrip(".")
            rect = plt.Rectangle((j, i), 1, 1, facecolor=facecolor, edgecolor="#D9D9D9")
            ax_right.add_patch(rect)
            ax_right.text(j + 0.5, i + 0.5, label, ha="center", va="center", fontsize=8.4)
    for spine in ["top", "right", "left", "bottom"]:
        ax_right.spines[spine].set_visible(False)

    fig.text(0.5, 0.01,
             "Nota: En el caso del volumen total, los valores se expresan en escala logarítmica base 10 con fines de visualización. Los colores del panel B se normalizaron por columna; por tanto, la intensidad cromática expresa magnitud relativa dentro de cada métrica y no comparabilidad absoluta entre métricas."
             if language == "es" else
             "Note: Total volume values are displayed on a base-10 logarithmic scale for visualization. Panel B colors were normalized by column; color intensity therefore expresses relative magnitude within each metric rather than absolute comparability across metrics.",
             ha="center", va="bottom", fontsize=8.8)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.12, wspace=0.18)
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    df = prepare_data(df)
    metric_cols = ["coverage_pct_altmetric_subset", "total_volume_log10", "conditional_mean", "exclusivity_pct"]
    df = normalize_columns(df, metric_cols)
    plot_ecology(df, OUTPUT_ES, language="es")
    plot_ecology(df, OUTPUT_EN, language="en")

if __name__ == "__main__":
    main()
