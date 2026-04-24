from __future__ import annotations

from pathlib import Path
import subprocess
import sys

SCRIPTS_DIR = Path("scripts")
SCRIPT_ORDER = [
    "01_load_and_validate_corpus.py",
    "02_build_observability_table_and_figure.py",
    "03_summarize_altmetric_platforms.py",
    "04_plot_platform_ecology.py",
    "05_plot_oa_routes_doi_coverage.py",
    "06_build_oa_routes_visibility_table.py",
    "07_render_oa_routes_visibility_table.py",
    "08_plot_aas_citation_relationship.py",
    "09_plot_thematic_distribution_attention.py",
    "10_build_altmetric_summary_table.py",
]


def main() -> None:
    for script_name in SCRIPT_ORDER:
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Missing script: {script_path}")
        print(f"Running {script_path}...")
        subprocess.run([sys.executable, str(script_path)], check=True)


if __name__ == "__main__":
    main()
