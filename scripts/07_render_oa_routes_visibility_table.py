from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

INPUT_FILE = Path("results/table_2_oa_routes_visibility_citation.csv")
FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_ES = FIGURES_DIR / "table_2_oa_routes_visibility_es.png"
OUTPUT_EN = FIGURES_DIR / "table_2_oa_routes_visibility_en.png"

GROUP1 = ["publications_with_doi", "publications_with_aas_gt_0"]
GROUP2 = ["altmetric_coverage_pct", "median_aas_positive"]
GROUP3 = ["mean_citations", "median_citations", "pct_cited_publications"]
METRIC_COLS = GROUP1 + GROUP2 + GROUP3
BAR_COLORS = {**{c:"#6C5CE7" for c in GROUP1}, **{c:"#00B894" for c in GROUP2}, **{c:"#E17055" for c in GROUP3}}
HEADER_FILLS = {**{c:"#EEEAFE" for c in GROUP1}, **{c:"#E7FBF6" for c in GROUP2}, **{c:"#FFF0EB" for c in GROUP3}}
GROUP_FILLS = {"g1":"#DDD6FE","g2":"#CCFBF1","g3":"#FED7CC"}

def normalize_table(df: pd.DataFrame, metric_cols: list[str]) -> pd.DataFrame:
    out=df.copy()
    for col in metric_cols:
        vmax=out[col].max(skipna=True)
        out[f"{col}_norm"]=out[col]/vmax if pd.notna(vmax) and vmax>0 else 0.0
    return out

def fmt_value(col: str, val: float) -> str:
    if pd.isna(val): return ""
    if col in ["publications_with_doi","publications_with_aas_gt_0"]:
        return f"{int(round(val)):,}"
    return f"{val:.2f}".rstrip("0").rstrip(".")

def render_table(df: pd.DataFrame, output_file: Path, language: str) -> None:
    label_col="oa_route_es" if language=="es" else "oa_route_en"
    column_labels = {
        "publications_with_doi":"Publicaciones\ncon DOI" if language=="es" else "Publications\nwith DOI",
        "publications_with_aas_gt_0":"Publicaciones\ncon AAS > 0" if language=="es" else "Publications\nwith AAS > 0",
        "altmetric_coverage_pct":"Cobertura\naltmétrica (%)" if language=="es" else "Altmetric\ncoverage (%)",
        "median_aas_positive":"Mediana\ndel AAS" if language=="es" else "Median\nAAS",
        "mean_citations":"Media de\ncitas" if language=="es" else "Mean\ncitations",
        "median_citations":"Mediana de\ncitas" if language=="es" else "Median\ncitations",
        "pct_cited_publications":"% de public.\ncitadas" if language=="es" else "% of cited\npublications",
    }
    g1_title="Base observable" if language=="es" else "Observable base"
    g2_title="Visibilidad altmétrica" if language=="es" else "Altmetric visibility"
    g3_title="Desempeño por citación" if language=="es" else "Citation performance"
    title="Tabla 4. Rutas de acceso abierto y patrones diferenciados de visibilidad y citación en el subconjunto con DOI" if language=="es" else "Table 4. Open access routes and differentiated visibility and citation patterns in the DOI subset"
    note="Nota: El ancho de cada barra se reescaló por columna; una celda completamente llena representa el valor máximo observado en esa métrica." if language=="es" else "Note: Bar width was rescaled by column; a fully filled cell represents the maximum observed value within that metric."
    n_rows=len(df); w_metric=2.35; w=1.75; fig_w=w_metric+len(METRIC_COLS)*w; fig_h=n_rows*0.70+2.9
    fig,ax=plt.subplots(figsize=(fig_w*0.90, fig_h))
    ax.set_xlim(0, w_metric+len(METRIC_COLS)*w); ax.set_ylim(-1.40, n_rows+1.25); ax.invert_yaxis(); ax.axis("off")
    y_group=-1.08; y_header=-0.28; header_h=0.72; group_h=0.54
    g1_x=w_metric; g2_x=w_metric+len(GROUP1)*w; g3_x=w_metric+(len(GROUP1)+len(GROUP2))*w
    ax.add_patch(Rectangle((g1_x,y_group), len(GROUP1)*w, group_h, facecolor=GROUP_FILLS["g1"], edgecolor="none"))
    ax.add_patch(Rectangle((g2_x,y_group), len(GROUP2)*w, group_h, facecolor=GROUP_FILLS["g2"], edgecolor="none"))
    ax.add_patch(Rectangle((g3_x,y_group), len(GROUP3)*w, group_h, facecolor=GROUP_FILLS["g3"], edgecolor="none"))
    ax.text(g1_x+len(GROUP1)*w/2, y_group+group_h/2, g1_title, ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.text(g2_x+len(GROUP2)*w/2, y_group+group_h/2, g2_title, ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.text(g3_x+len(GROUP3)*w/2, y_group+group_h/2, g3_title, ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.add_patch(Rectangle((0,y_header), w_metric, header_h, facecolor="#ECECEC", edgecolor="#C8C8C8", linewidth=0.8))
    ax.text(w_metric/2, y_header+header_h/2, "Ruta OA" if language=="es" else "OA route", ha="center", va="center", fontsize=10, fontweight="bold")
    for j,col in enumerate(METRIC_COLS):
        x=w_metric+j*w
        ax.add_patch(Rectangle((x,y_header), w, header_h, facecolor=HEADER_FILLS[col], edgecolor="#C8C8C8", linewidth=0.8))
        ax.text(x+w/2, y_header+header_h/2, column_labels[col], ha="center", va="center", fontsize=8.8, fontweight="bold")
    for i in range(n_rows):
        y=i+0.42
        ax.add_patch(Rectangle((0,y), w_metric,1.0, facecolor="#F7F7F7", edgecolor="#D7D7D7", linewidth=0.6))
        ax.text(0.10, y+0.5, str(df.loc[i,label_col]), ha="left", va="center", fontsize=10)
        for j,col in enumerate(METRIC_COLS):
            x=w_metric+j*w
            ax.add_patch(Rectangle((x,y), w,1.0, facecolor="white", edgecolor="#D7D7D7", linewidth=0.6))
            p=float(df.loc[i,f"{col}_norm"]) if pd.notna(df.loc[i,f"{col}_norm"]) else 0.0
            if p>0:
                pad_x=0.06; pad_y=0.17; bar_w=(w-2*pad_x)*p; bar_h=1.0-2*pad_y
                ax.add_patch(Rectangle((x+pad_x,y+pad_y), bar_w, bar_h, facecolor=BAR_COLORS[col], edgecolor="none", alpha=0.92))
            ax.text(x+w/2, y+0.5, fmt_value(col, df.loc[i,col]), ha="center", va="center", fontsize=9.2, color="#1f1f1f")
    for sep_x in [g2_x, g3_x]:
        ax.plot([sep_x,sep_x],[y_header, n_rows+0.42], color="#9A9A9A", linewidth=1.05)
    ax.add_patch(Rectangle((0,y_header), w_metric+len(METRIC_COLS)*w, n_rows+1.0-y_header, fill=False, edgecolor="#7F7F7F", linewidth=1.0))
    ax.text(0,-1.40,title,ha="left",va="bottom",fontsize=12.2,fontweight="bold")
    ax.text(0,n_rows+1.08,note,ha="left",va="top",fontsize=8.8)
    fig.savefig(output_file,dpi=300,bbox_inches="tight")
    plt.close(fig)

def main():
    df=pd.read_csv(INPUT_FILE)
    df=normalize_table(df, METRIC_COLS)
    render_table(df, OUTPUT_ES, language="es")
    render_table(df, OUTPUT_EN, language="en")

if __name__ == "__main__":
    main()
