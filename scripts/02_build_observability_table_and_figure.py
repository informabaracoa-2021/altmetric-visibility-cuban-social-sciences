from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path("data/processed/corpus_validated.csv")
RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

TABLE_OUTPUT = RESULTS_DIR / "table_1_analytic_base_by_year.csv"
FIGURE_DATA_OUTPUT = RESULTS_DIR / "figure_1_data.csv"
FIGURE_ES = FIGURES_DIR / "figure_1_observability_layers_es.png"
FIGURE_EN = FIGURES_DIR / "figure_1_observability_layers_en.png"

def build_observability_table(df: pd.DataFrame) -> pd.DataFrame:
    yearly = (
        df.groupby("publication_year", dropna=True)
        .agg(
            publications=("id", "size"),
            with_doi=("has_doi", "sum"),
            open_access=("oa_status_clean", lambda s: s.ne("closed").sum()),
            with_altmetric_attention=("has_altmetric_attention", "sum"),
        )
        .reset_index()
        .rename(columns={"publication_year": "year"})
        .sort_values("year")
    )
    yearly["pct_with_doi"] = yearly["with_doi"] / yearly["publications"] * 100
    yearly["pct_open_access"] = yearly["open_access"] / yearly["publications"] * 100
    yearly["pct_altmetric_over_total"] = yearly["with_altmetric_attention"] / yearly["publications"] * 100
    yearly["pct_altmetric_over_doi"] = (yearly["with_altmetric_attention"] / yearly["with_doi"] * 100).fillna(0)
    total_row = pd.DataFrame({
        "year": ["Total"],
        "publications": [yearly["publications"].sum()],
        "with_doi": [yearly["with_doi"].sum()],
        "pct_with_doi": [yearly["with_doi"].sum() / yearly["publications"].sum() * 100],
        "open_access": [yearly["open_access"].sum()],
        "pct_open_access": [yearly["open_access"].sum() / yearly["publications"].sum() * 100],
        "with_altmetric_attention": [yearly["with_altmetric_attention"].sum()],
        "pct_altmetric_over_total": [yearly["with_altmetric_attention"].sum() / yearly["publications"].sum() * 100],
        "pct_altmetric_over_doi": [yearly["with_altmetric_attention"].sum() / yearly["with_doi"].sum() * 100],
    })
    return pd.concat([yearly, total_row], ignore_index=True)

def plot_observability_figure(df_plot: pd.DataFrame, output_file: Path, language: str) -> None:
    years = df_plot["year"].astype(int)
    fig, ax1 = plt.subplots(figsize=(10.5, 6.2))
    ax1.bar(years, df_plot["publications"], width=0.6)
    ax1.set_xlabel("Año" if language == "es" else "Year")
    ax1.set_ylabel("Número de publicaciones" if language == "es" else "Number of publications")
    ax2 = ax1.twinx()
    ax2.plot(years, df_plot["pct_with_doi"], marker="o", linewidth=2, label="% con DOI" if language == "es" else "% with DOI")
    ax2.plot(years, df_plot["pct_altmetric_over_total"], marker="o", linewidth=2, linestyle="--", label="% con atención altmétrica" if language == "es" else "% with altmetric attention")
    ax2.set_ylabel("Porcentaje (%)" if language == "es" else "Percentage (%)")
    ax1.set_title("Evolución de las capas de observabilidad del corpus" if language == "es" else "Evolution of corpus observability layers")
    lines, labels = ax2.get_legend_handles_labels()
    ax2.legend(lines, labels, loc="upper left", frameon=False)
    for spine in ["top"]:
        ax1.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)
    ax1.grid(axis="y", linewidth=0.4, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    table = build_observability_table(df)
    table.to_csv(TABLE_OUTPUT, index=False)
    plot_data = table[table["year"] != "Total"].copy()
    plot_data.to_csv(FIGURE_DATA_OUTPUT, index=False)
    plot_observability_figure(plot_data, FIGURE_ES, language="es")
    plot_observability_figure(plot_data, FIGURE_EN, language="en")
    print(f"Table exported to: {TABLE_OUTPUT}")

if __name__ == "__main__":
    main()
