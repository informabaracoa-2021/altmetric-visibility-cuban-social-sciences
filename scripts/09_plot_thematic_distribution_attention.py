from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path("data/processed/corpus_validated.csv")
RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DATA_OUTPUT = RESULTS_DIR / "figure_5_data.csv"
FIGURE_ES = FIGURES_DIR / "figure_5_thematic_attention_es.png"
FIGURE_EN = FIGURES_DIR / "figure_5_thematic_attention_en.png"

MIN_TOTAL_PUBLICATIONS = 20
MIN_ALT_PUBLICATIONS = 4

def shorten_label(text: str, max_len: int = 42) -> str:
    if not isinstance(text, str):
        return ""
    text = text.strip()
    return text if len(text) <= max_len else text[: max_len - 1] + "…"

def build_thematic_comparison(df: pd.DataFrame) -> pd.DataFrame:
    total = df["primary_topic_clean"].dropna().value_counts()
    alt = df[df["has_altmetric_attention"]]["primary_topic_clean"].dropna().value_counts()
    n_total = len(df)
    n_alt = int(df["has_altmetric_attention"].sum())

    comp = pd.concat(
        [
            total.rename("n_total"),
            (total / n_total * 100).rename("share_total"),
            alt.rename("n_alt"),
            (alt / n_alt * 100).rename("share_alt"),
        ],
        axis=1,
    ).fillna(0)

    comp["repr_ratio"] = comp["share_alt"] / comp["share_total"].replace(0, np.nan)
    comp.index.name = "theme"
    comp = comp.reset_index().sort_values("repr_ratio", ascending=True).reset_index(drop=True)
    comp = comp[
        (comp["n_total"] >= MIN_TOTAL_PUBLICATIONS)
        & (comp["n_alt"] >= MIN_ALT_PUBLICATIONS)
    ].copy()
    comp["theme_short"] = comp["theme"].map(shorten_label)
    return comp

def plot_thematic_distribution(df_plot: pd.DataFrame, output_file: Path, language: str) -> None:
    y = np.arange(len(df_plot))
    fig, ax = plt.subplots(figsize=(10.8, 7.3))

    for i, row in df_plot.iterrows():
        ax.plot([row["share_total"], row["share_alt"]], [i, i], linewidth=1.2, color="#B0B0B0", zorder=1)

    ax.scatter(df_plot["share_total"], y, s=58, color="#7F7F7F", zorder=3, label="Corpus total" if language == "es" else "Full corpus")
    ax.scatter(df_plot["share_alt"], y, s=58, color="green", zorder=3, label="Subconjunto con atención altmétrica" if language == "es" else "Subset with altmetric attention")

    for i, row in df_plot.iterrows():
        xmax = max(row["share_total"], row["share_alt"])
        ax.text(xmax + 0.35, i, f"×{row['repr_ratio']:.1f}", va="center", fontsize=8.8, color="#4D4D4D")

    ax.set_yticks(y)
    ax.set_yticklabels(df_plot["theme_short"])
    ax.set_xlabel("Participación dentro del conjunto correspondiente (%)" if language == "es" else "Share within the corresponding set (%)")
    ax.set_ylabel("Tema principal" if language == "es" else "Primary topic")
    ax.set_title("Cambio en el peso temático entre el corpus total y el subconjunto con atención altmétrica" if language == "es" else "Shift in thematic weight between the full corpus and the subset with altmetric attention")
    ax.grid(axis="x", linewidth=0.5, alpha=0.35)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False, borderaxespad=0.0)
    note = (
        "Nota: Se muestran temas con al menos 20 publicaciones en el corpus total y al menos 4 publicaciones con AAS > 0. La razón al extremo derecho indica cuántas veces aumenta la participación relativa del tema en el subconjunto con atención altmétrica."
        if language == "es"
        else "Note: Topics with at least 20 publications in the full corpus and at least 4 publications with AAS > 0 are shown. The ratio at the far right indicates how many times the theme's relative share increases in the subset with altmetric attention."
    )
    fig.text(0.5, 0.01, note, ha="center", va="bottom", fontsize=8.8)
    fig.subplots_adjust(left=0.25, right=0.78, top=0.92, bottom=0.12)
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main():
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    comp = build_thematic_comparison(df)
    comp.to_csv(DATA_OUTPUT, index=False)
    plot_thematic_distribution(comp, FIGURE_ES, language="es")
    plot_thematic_distribution(comp, FIGURE_EN, language="en")

if __name__ == "__main__":
    main()
