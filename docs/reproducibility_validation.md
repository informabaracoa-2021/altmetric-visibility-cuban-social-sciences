# Reproducibility validation

## Validation objective
This document records the minimum validation carried out before public release of the repository.

## Validation steps
1. The repository was unpacked into a clean directory.
2. Existing processed outputs were removed.
3. The workflow was re-executed from raw inputs using the scripted pipeline.
4. Core tests were run to verify required inputs, output directories, and selected result files.

## Outcome
The full analytical workflow was successfully re-executed from raw inputs, and the core validation tests passed.

## Caveat
Some scripts were reconstructed from a stable analytical workflow rather than preserved as original standalone source files. The repository therefore documents the final reproducible workflow rather than every historical intermediate draft.
