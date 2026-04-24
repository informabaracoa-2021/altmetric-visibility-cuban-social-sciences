from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

INPUT_FILE = Path("results/altmetric_summary_table.csv")
RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

CURATED_OUTPUT = RESULTS_DIR / "altmetric_summary_table_curated.csv"
FIGURE_ES = FIGURES_DIR / "table_altmetric_summary_es.png"
FIGURE_EN = FIGURES_DIR / "table_altmetric_summary_en.png"

DISPLAY_ORDER = [
    "Altmetric Attention Score", "X users", "Mendeley readers", "Facebook pages",
    "News outlets", "Blogs", "Wikipedia pages", "Policy sources", "Redditors",
    "Peer review sites", "YouTube creators", "Patents", "Bluesky users",
    "Clinical guideline sources",
]
GROUP1 = ["coverage_publications", "coverage_pct"]
GROUP2 = ["total_mentions_or_readers", "mean_all", "mean_positive"]
GROUP3 = ["median_positive", "std_positive", "maximum", "p90_positive"]
METRIC_COLS = GROUP1 + GROUP2 + GROUP3
BAR_COLORS = {**{c:"#6C5CE7" for c in GROUP1}, **{c:"#00B894" for c in GROUP2}, **{c:"#E17055" for c in GROUP3}}
HEADER_FILLS = {**{c:"#EEEAFE" for c in GROUP1}, **{c:"#E7FBF6" for c in GROUP2}, **{c:"#FFF0EB" for c in GROUP3}}
GROUP_FILLS = {"g1":"#DDD6FE","g2":"#CCFBF1","g3":"#FED7CC"}

def prepare_table(df: pd.DataFrame) -> pd.DataFrame:
    out=df.copy()
    out=out[out["metric"].isin(DISPLAY_ORDER)].copy()
    out["metric"]=pd.Categorical(out["metric"], categories=DISPLAY_ORDER, ordered=True)
    out=out.sort_values("metric").reset_index(drop=True)
    for col in METRIC_COLS:
        vmax=out[col].max(skipna=True)
        out[f"{col}_norm"]=out[col]/vmax if pd.notna(vmax) and vmax>0 else 0.0
    return out

def fmt_value(col: str, val: float) -> str:
    if pd.isna(val): return ""
    if col=="coverage_publications":
        return f"{int(round(val)):,}"
    if col=="total_mentions_or_readers":
        return f"{int(round(val)):,}" if float(val).is_integer() else f"{val:.2f}".rstrip("0").rstrip(".")
    return f"{val:.2f}".rstrip("0").rstrip(".")

def render_table(df: pd.DataFrame, output_file: Path, language: str) -> None:
    col_labels = {
        "coverage_publications":"Cobertura\n(publicaciones)" if language=="es" else "Coverage\n(publications)",
        "coverage_pct":"Cobertura\n(%)" if language=="es" else "Coverage\n(%)",
        "total_mentions_or_readers":"Volumen\ntotal" if language=="es" else "Total\nvolume",
        "mean_all":"Media\n(corpus total)" if language=="es" else "Mean\n(full corpus)",
        "mean_positive":"Media\n(condicional)" if language=="es" else "Mean\n(conditional)",
        "median_positive":"Mediana\n(condicional)" if language=="es" else "Median\n(conditional)",
        "std_positive":"Desv. estándar\n(condicional)" if language=="es" else "Std. dev.\n(conditional)",
        "maximum":"Máximo" if language=="es" else "Maximum",
        "p90_positive":"P90\n(condicional)" if language=="es" else "P90\n(conditional)",
    }
    g1_title="Cobertura" if language=="es" else "Coverage"
    g2_title="Magnitud" if language=="es" else "Magnitude"
    g3_title="Dispersión y extremos" if language=="es" else "Dispersion and extremes"
    title="Tabla 3. Resumen estadístico comparado de los indicadores altmétricos en el corpus total de OpenAlex" if language=="es" else "Table 3. Comparative statistical summary of altmetric indicators in the full OpenAlex corpus"
    note="Nota: El tamaño de cada barra se reescaló por columna. Así, 0 aparece en blanco y el valor máximo de cada columna ocupa el ancho completo de la celda." if language=="es" else "Note: The size of each bar was rescaled by column. Thus, 0 appears blank and the maximum value in each column occupies the full width of the cell."
    n_rows=len(df); w_metric=2.90; w=1.65; fig_w=w_metric+len(METRIC_COLS)*w; fig_h=n_rows*0.58+3.0
    fig,ax=plt.subplots(figsize=(fig_w*0.88, fig_h))
    ax.set_xlim(0, w_metric+len(METRIC_COLS)*w); ax.set_ylim(-1.40, n_rows+1.30); ax.invert_yaxis(); ax.axis("off")
    y_group=-1.08; y_header=-0.28; header_h=0.72; group_h=0.54
    g1_x=w_metric; g2_x=w_metric+len(GROUP1)*w; g3_x=w_metric+(len(GROUP1)+len(GROUP2))*w
    ax.add_patch(Rectangle((g1_x,y_group), len(GROUP1)*w, group_h, facecolor=GROUP_FILLS["g1"], edgecolor="none"))
    ax.add_patch(Rectangle((g2_x,y_group), len(GROUP2)*w, group_h, facecolor=GROUP_FILLS["g2"], edgecolor="none"))
    ax.add_patch(Rectangle((g3_x,y_group), len(GROUP3)*w, group_h, facecolor=GROUP_FILLS["g3"], edgecolor="none"))
    ax.text(g1_x+len(GROUP1)*w/2, y_group+group_h/2, g1_title, ha="center", va="center", fontsize=10.3, fontweight="bold")
    ax.text(g2_x+len(GROUP2)*w/2, y_group+group_h/2, g2_title, ha="center", va="center", fontsize=10.3, fontweight="bold")
    ax.text(g3_x+len(GROUP3)*w/2, y_group+group_h/2, g3_title, ha="center", va="center", fontsize=10.3, fontweight="bold")
    ax.add_patch(Rectangle((0,y_header), w_metric, header_h, facecolor="#ECECEC", edgecolor="#C8C8C8", linewidth=0.8))
    ax.text(w_metric/2, y_header+header_h/2, "Métrica" if language=="es" else "Metric", ha="center", va="center", fontsize=10, fontweight="bold")
    for j,col in enumerate(METRIC_COLS):
        x=w_metric+j*w
        ax.add_patch(Rectangle((x,y_header), w, header_h, facecolor=HEADER_FILLS[col], edgecolor="#C8C8C8", linewidth=0.8))
        ax.text(x+w/2, y_header+header_h/2, col_labels[col], ha="center", va="center", fontsize=8.5, fontweight="bold")
    for i in range(n_rows):
        y=i+0.42
        ax.add_patch(Rectangle((0,y), w_metric, 1.0, facecolor="#F7F7F7", edgecolor="#D7D7D7", linewidth=0.6))
        ax.text(0.10, y+0.5, str(df.loc[i,"metric"]), ha="left", va="center", fontsize=9.6)
        for j,col in enumerate(METRIC_COLS):
            x=w_metric+j*w
            ax.add_patch(Rectangle((x,y), w,1.0, facecolor="white", edgecolor="#D7D7D7", linewidth=0.6))
            p=float(df.loc[i,f"{col}_norm"]) if pd.notna(df.loc[i,f"{col}_norm"]) else 0.0
            if p>0:
                pad_x=0.06; pad_y=0.17; bar_w=(w-2*pad_x)*p; bar_h=1.0-2*pad_y
                ax.add_patch(Rectangle((x+pad_x,y+pad_y), bar_w, bar_h, facecolor=BAR_COLORS[col], edgecolor="none", alpha=0.92))
            ax.text(x+w/2, y+0.5, fmt_value(col, df.loc[i,col]), ha="center", va="center", fontsize=8.9, color="#1F1F1F")
    for sep_x in [g2_x,g3_x]:
        ax.plot([sep_x,sep_x], [y_header, n_rows+0.42], color="#9A9A9A", linewidth=1.05)
    ax.add_patch(Rectangle((0,y_header), w_metric+len(METRIC_COLS)*w, n_rows+1.0-y_header, fill=False, edgecolor="#7F7F7F", linewidth=1.0))
    ax.text(0,-1.40,title,ha="left",va="bottom",fontsize=12.0,fontweight="bold")
    ax.text(0,n_rows+1.10,note,ha="left",va="top",fontsize=8.8)
    fig.savefig(output_file,dpi=300,bbox_inches="tight")
    plt.close(fig)

def main():
    df=pd.read_csv(INPUT_FILE, low_memory=False)
    df=prepare_table(df)
    df.to_csv(CURATED_OUTPUT, index=False)
    render_table(df, FIGURE_ES, language="es")
    render_table(df, FIGURE_EN, language="en")

if __name__ == "__main__":
    main()
