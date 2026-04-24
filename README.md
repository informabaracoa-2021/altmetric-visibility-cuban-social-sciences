 Altmetric visibility across access pathways and citation relationships in Cuban social sciences

 Description

This repository contains the code, processed outputs, and technical documentation used to examine the relationship between open access pathways, altmetric attention, and citation patterns in Cuban social sciences during the period 2020–2024.

The repository was prepared to support reproducibility, code review, public archiving, and formal citation in connection with the research article:

Altmetric visibility across access pathways and citation relationships in Cuban social sciences: methodological insights from an underrepresented research system

 Repository objective

The repository provides a structured and reproducible workflow for:

- validating and preparing the study corpus;
- deriving observability indicators;
- summarizing altmetric platform patterns;
- comparing open access routes by visibility and citation indicators;
- examining the relationship between Altmetric Attention Score and citations;
- identifying thematic selectivity in observable altmetric attention;
- generating the figures and tabular outputs used in the manuscript.

 Repository structure

```text
altmetric-visibility-cuban-social-sciences/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── requirements.txt
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│
├── figures/
│
├── results/
│
├── docs/
│
├── notebooks/
│
└── tests/
```

 Main folders

- `data/raw/`: original input files used by the workflow.
- `data/processed/`: cleaned and derived intermediate datasets.
- `scripts/`: sequential Python scripts used to generate all major analytical outputs.
- `figures/`: exported figures and rendered visual tables.
- `results/`: CSV outputs used in the manuscript and in figure/table construction.
- `docs/`: complementary technical documentation.
- `notebooks/`: optional exploratory or validation notebooks.
- `tests/`: minimal validation scripts.

 Software requirements

The workflow was reconstructed in Python 3.11.

Main packages:

- pandas
- numpy
- matplotlib
- scipy
- openpyxl

See `requirements.txt` for the software environment used in the reproducible workflow.

 Installation

 1. Clone the repository

```bash
git clone (https://github.com/informabaracoa-2021/altmetric-visibility-cuban-social-sciences.git)
cd (https://github.com/informabaracoa-2021/altmetric-visibility-cuban-social-sciences)
```

 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

 Linux / macOS

```bash
source .venv/bin/activate
```

 Windows

```bash
.venv\Scripts\activate
```

 3. Install dependencies

```bash
pip install -r requirements.txt
```

 Input data

The workflow assumes the following input files are available in `data/raw/`:

- `Produccion_cientifica_Ciencias_Sociales_Cuba_2020_2024.xlsx`
- `estadisticas_altmetricas_cuba_2020_2024.xlsx`

 Data availability note

This repository can include:
- code,
- processed outputs,
- and derived tables used for manuscript preparation.

Inclusion of raw data depends on permissions, licensing conditions, and journal or repository policies. If raw source files cannot be redistributed, they should be replaced by metadata records or instructions for controlled access.

 Recommended execution order

The full workflow can be executed with:

```bash
python run_pipeline.py
```

Equivalent manual execution order:

1. `scripts/01_load_and_validate_corpus.py`
2. `scripts/02_build_observability_table_and_figure.py`
3. `scripts/03_summarize_altmetric_platforms.py`
4. `scripts/04_plot_platform_ecology.py`
5. `scripts/05_plot_oa_routes_doi_coverage.py`
6. `scripts/06_build_oa_routes_visibility_table.py`
7. `scripts/07_render_oa_routes_visibility_table.py`
8. `scripts/08_plot_aas_citation_relationship.py`
9. `scripts/09_plot_thematic_distribution_attention.py`
10. `scripts/10_build_altmetric_summary_table.py`

 Script overview

 `01_load_and_validate_corpus.py`
Loads the main corpus, validates required fields, derives technical variables used throughout the workflow, and exports a cleaned analytical version.

 `02_build_observability_table_and_figure.py`
Builds the annual analytical-base table and the observability figure showing total publications, DOI availability, and altmetric attention.

 `03_summarize_altmetric_platforms.py`
Computes platform-level coverage, total volume, conditional intensity, exclusivity, and descriptive summary statistics.

 `04_plot_platform_ecology.py`
Generates the main platform ecology figure in Spanish and English.

 `05_plot_oa_routes_doi_coverage.py`
Builds the figure showing open access route distribution and DOI coverage by route.

 `06_build_oa_routes_visibility_table.py`
Computes route-level visibility and citation indicators for the DOI subset.

 `07_render_oa_routes_visibility_table.py`
Renders the open access route comparison table as a publication-ready visual table in Spanish and English.

 `08_plot_aas_citation_relationship.py`
Computes Spearman correlation, percentile-90 quadrants, and the figure comparing AAS and citations.

 `09_plot_thematic_distribution_attention.py`
Builds the thematic comparison dataset and the dumbbell plot comparing the full corpus and the subset with altmetric attention.

 `10_build_altmetric_summary_table.py`
Renders the comparative summary table of altmetric indicators in Spanish and English.

 Link between scripts and manuscript outputs

| Script | Main output | Manuscript section |
|---|---|---|
| 01 | Clean analytical corpus | Methods 2.2–2.5 |
| 02 | Observability table and figure | Results 3.1 |
| 03 | Platform summary data | Results 3.2 |
| 04 | Platform ecology figure | Results 3.2 |
| 05 | OA route DOI coverage figure | Results 3.3 |
| 06 | OA route comparison table | Results 3.3 |
| 07 | Rendered OA route table | Results 3.3 |
| 08 | AAS–citation figure | Results 3.4 |
| 09 | Thematic attention figure | Results 3.5 |
| 10 | Altmetric summary table | Results 3.2 |
| run_pipeline.py | Sequential execution wrapper | Full workflow |

 Reproducibility notes

- The workflow uses relative paths only.
- Derived variables are generated explicitly from the validated corpus.
- Publication-ready figures are exported in Spanish and English when relevant.
- Some scripts were reconstructed from the analytical workflow and visual outputs consolidated during manuscript preparation.
- Intermediate products are exported as CSV whenever possible to support auditability and downstream reuse.

 Included and non-included materials

Included:
- curated scripts;
- processed outputs;
- rendered figures and visual tables;
- repository-level documentation.

Potentially not included:
- restricted raw data files;
- provider-side API credentials;
- manually inspected exploratory drafts not retained in the final analytical workflow.

 Citation

If you use this repository, please cite the archived release indicated in `CITATION.cff`.

Example placeholder:

> Ortiz Núñez, R., & Santa Álvarez, J. S. (2026). Altmetric visibility across access pathways and citation relationships in Cuban social sciences (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.19719267

 License

This repository is released under the license specified in `LICENSE`.

## Contact

For correspondence related to the repository, please update the metadata in `CITATION.cff` and the repository settings before public release.
