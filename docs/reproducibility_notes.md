# Reproducibility notes

## Scope
This repository reconstructs the analytical workflow used to prepare figures, derived tables, and descriptive metrics associated with the manuscript.

## Important notes
- Relative paths are used throughout.
- Raw data are expected in `data/raw/`.
- Processed outputs are written to `data/processed/`, `results/`, and `figures/`.
- Some scripts were consolidated from multiple stable iterations carried out during manuscript preparation.
- The repository preserves the final analytical logic rather than every intermediate draft.

## Known limitations
- Exact package versions were not fully traceable in the original analytical process.
- Some visual outputs were iteratively refined; the repository preserves the stable final form.
- The deduplication routine applied before the final dataset was not fully recoverable as a standalone script; the workflow therefore starts from the validated corpus file supplied in `data/raw/`.


## Validation status
- The full script sequence was executed in a clean directory using the repository structure and relative paths.
- Core outputs were regenerated successfully from raw inputs.
- Basic validation tests are included under `tests/`.
