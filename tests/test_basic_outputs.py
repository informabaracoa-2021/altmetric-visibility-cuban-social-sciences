from pathlib import Path

def test_expected_output_dirs():
    for rel in ["data/processed", "results", "figures", "scripts"]:
        assert Path(rel).exists(), f"Missing path: {rel}"
