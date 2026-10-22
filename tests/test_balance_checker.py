"""Unit tests for chemical and charge balance checker."""

import pytest
from src.balance_checker import check_balance, parse_formula


def test_parse_simple_formulas():
    counts, charge = parse_formula("C6H12O6")
    assert counts == {"C": 6, "H": 12, "O": 6}
    assert charge == 0

    counts, charge = parse_formula("H2O")
    assert counts == {"H": 2, "O": 1}
    assert charge == 0


def test_parse_charged_formulas():
    counts, charge = parse_formula("SO4[2-]")
    assert counts == {"S": 1, "O": 4}
    assert charge == -2

    counts, charge = parse_formula("Fe[3+]")
    assert counts == {"Fe": 1}
    assert charge == 3

    counts, charge = parse_formula("NO3-")
    assert counts == {"N": 1, "O": 3}
    assert charge == -1

    counts, charge = parse_formula("NH4+")
    assert counts == {"N": 1, "H": 4}
    assert charge == 1

    counts, charge = parse_formula("e-")
    assert counts == {}
    assert charge == -1


def test_parse_parenthesized_formulas():
    counts, charge = parse_formula("Ca(OH)2")
    assert counts == {"Ca": 1, "O": 2, "H": 2}
    assert charge == 0

    counts, charge = parse_formula("(NH4)2SO4")
    assert counts == {"N": 2, "H": 8, "S": 1, "O": 4}
    assert charge == 0


def test_table_4_balanced_reaction():
    """Table 4: C6H12O6 -> 2 C2H5OH + 2 CO2 (Balanced)."""
    rxn = "C6H12O6 -> 2 C2H5OH + 2 CO2"
    result = check_balance(rxn)
    assert result.is_balanced is True
    assert result.atom_deltas == {"C": 0, "H": 0, "O": 0}
    assert result.charge_delta == 0
    assert result.verdict == "Balanced"


def test_table_4_imbalanced_reaction():
    """Table 4: C6H12O6 -> 2 C2H5OH + CO2 (Deficit of 1 C and 2 O)."""
    rxn = "C6H12O6 -> 2 C2H5OH + CO2"
    result = check_balance(rxn)
    assert result.is_balanced is False
    assert result.atom_deltas["C"] == -1
    assert result.atom_deltas["O"] == -2
    assert result.atom_deltas["H"] == 0
    assert "C deficit of 1" in result.verdict
    assert "O deficit of 2" in result.verdict


def test_redox_charge_balance():
    # Balanced ferric reduction
    res = check_balance("Fe[3+] + e- -> Fe[2+]")
    assert res.is_balanced is True
    assert res.charge_delta == 0

    # Imbalanced charge
    res_bad = check_balance("Fe[3+] -> Fe[2+]")
    assert res_bad.is_balanced is False
    assert res_bad.charge_delta == -1
    assert "Charge imbalance" in res_bad.verdict


def test_invalid_syntax():
    res = check_balance("No arrow reaction here")
    assert res.is_balanced is False
    assert "Invalid Syntax" in res.verdict
