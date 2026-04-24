from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

INPUT_FILE = Path("data/processed/corpus_validated.csv")
RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DATA_OUTPUT = RESULTS_DIR / "figure_3_data.csv"
FIGURE_ES = FIGURES_DIR / "figure_3_oa_routes_doi_coverage_es.png"
FIGURE_EN = FIGURES_DIR / "figure_3_oa_routes_doi_coverage_en.png"

ROUTE_ORDER = ["closed", "diamond", "green", "hybrid", "gold", "bronze"]
ROUTE_LABELS_ES = {"closed":"Cerrado","diamond":"Diamante","green":"Verde","hybrid":"Híbrido","gold":"Dorado","bronze":"Bronce"}
ROUTE_LABELS_EN = {"closed":"Closed","diamond":"Diamond","green":"Green","hybrid":"Hybrid","gold":"Gold","bronze":"Bronze"}
ROUTE_COLORS = {"closed":"#2C3E50","diamond":"#3498DB","green":"#2ECC71","hybrid":"#E74C3C","gold":"#F1C40F","bronze":"#D35400"}

def lighten_color(hex_color: str, amount: float = 0.68):
    base = np.array(mcolors.to_rgb(hex_color))
    white = np.array([1.0,1.0,1.0])
    return tuple(base + (white-base)*amount)

def build_oa_route_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped=(df.groupby("oa_status_clean", dropna=False)
               .agg(publications=("id","size"), with_doi=("has_doi","sum"))
               .reset_index()
               .rename(columns={"oa_status_clean":"oa_route"}))
    grouped=grouped[grouped["oa_route"].isin(ROUTE_ORDER)].copy()
    grouped["oa_route"]=pd.Categorical(grouped["oa_route"], categories=ROUTE_ORDER, ordered=True)
    grouped=grouped.sort_values("oa_route").reset_index(drop=True)
    grouped["pct_with_doi"]=grouped["with_doi"]/grouped["publications"]*100
    return grouped

def plot_oa_routes(df_plot: pd.DataFrame, output_file: Path, language: str) -> None:
    labels=[ROUTE_LABELS_ES[r] if language=="es" else ROUTE_LABELS_EN[r] for r in df_plot["oa_route"].astype(str)]
    colors_dark=[ROUTE_COLORS[r] for r in df_plot["oa_route"].astype(str)]
    colors_light=[lighten_color(ROUTE_COLORS[r]) for r in df_plot["oa_route"].astype(str)]
    x=np.arange(len(df_plot))
    width=0.72
    fig,ax=plt.subplots(figsize=(10.8,6.4))
    bars_total=ax.bar(x, df_plot["publications"], width=width, color=colors_light, edgecolor="none", zorder=1)
    bars_doi=ax.bar(x, df_plot["with_doi"], width=width*0.72, color=colors_dark, edgecolor="none", zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Número de publicaciones" if language=="es" else "Number of publications")
    ax.set_title("Distribución de rutas de acceso y cobertura de DOI por ruta" if language=="es" else "Access route distribution and DOI coverage by route")
    ax.grid(axis="y", linewidth=0.4, alpha=0.3)
    for spine in ["top","right"]:
        ax.spines[spine].set_visible(False)
    maxpub=max(df_plot["publications"])
    for rect_total, rect_doi, pct, route in zip(bars_total, bars_doi, df_plot["pct_with_doi"], df_plot["oa_route"].astype(str)):
        ax.text(rect_total.get_x()+rect_total.get_width()/2, rect_total.get_height()+maxpub*0.015, f"{int(rect_total.get_height()):,}", ha="center", va="bottom", fontsize=9)
        ax.text(rect_doi.get_x()+rect_doi.get_width()/2, rect_doi.get_height()-maxpub*0.02, f"{pct:.1f}% DOI", ha="center", va="top", fontsize=8.8, color="white" if route=="closed" else "black", fontweight="bold")
    note = "Nota: Color claro = publicaciones totales en la ruta; color fuerte = publicaciones con DOI dentro de la ruta." if language=="es" else "Note: Light color = total publications in the route; strong color = publications with DOI within the route."
    fig.text(0.5,0.01,note,ha="center",va="bottom",fontsize=8.8)
    fig.tight_layout(rect=[0,0.04,1,1])
    fig.savefig(output_file,dpi=300,bbox_inches="tight")
    plt.close(fig)

def main():
    df=pd.read_csv(INPUT_FILE, low_memory=False)
    summary=build_oa_route_summary(df)
    summary.to_csv(DATA_OUTPUT,index=False)
    plot_oa_routes(summary, FIGURE_ES, language="es")
    plot_oa_routes(summary, FIGURE_EN, language="en")

if __name__ == "__main__":
    main()
