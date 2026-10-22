"""Unit tests for the CLI interface."""

import subprocess
import sys


def test_cli_check_balance():
    cmd = [sys.executable, "-m", "src.cli", "check-balance", "C6H12O6 -> 2 C2H5OH + 2 CO2"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "PASSED (Balanced)" in res.stdout


def test_cli_validate_evidence():
    cmd = [sys.executable, "-m", "src.cli", "validate-evidence", "data/evidence_records.json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "EVIDENCE DATABASE VALIDATION AUDIT" in res.stdout


def test_cli_benchmark():
    cmd = [sys.executable, "-m", "src.cli", "run-benchmark"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "Benchmark Accuracy: 20/20 (100.0%)" in res.stdout
