"""Unit tests for Table 3 feasibility rubric scoring."""

import pytest
from src.feasibility_rubric import (
    RubricRating,
    evaluate_speculative_claim
)


def test_feasibility_evaluation_complete():
    scorecard = evaluate_speculative_claim(
        claim_id="SPEC-TEST",
        hypothesis_title="Hypothetical Cryogenic Silane Biochemistry",
        chem_rating=RubricRating.MET,
        chem_notes="All reactions atom and charge balanced.",
        thermo_rating=RubricRating.PARTLY_MET,
        thermo_notes="Kinetically very slow at 94 K.",
        env_rating=RubricRating.MET,
        env_notes="Stable in liquid methane.",
        func_rating=RubricRating.NOT_MET,
        func_notes="No enzyme-like catalyst or genetic replication demonstrated.",
        emp_rating=RubricRating.PARTLY_MET,
        emp_notes="Simulation chambers can test monomer stability.",
        knowledge_gaps=["Catalytic diversity", "Template copying fidelity"],
        proposed_tests=["DFT activation barrier calculations"]
    )

    assert scorecard.claim_id == "SPEC-TEST"
    assert scorecard.chemical_validity.rating == RubricRating.MET
    assert scorecard.functional_completeness.rating == RubricRating.NOT_MET
    assert "Speculative Hypothesis" in scorecard.overall_verdict
    
    summary = scorecard.summary()
    assert "[SPEC-TEST]" in summary
    assert "Chemical Validity: MET" in summary

    md = scorecard.to_markdown()
    assert "### Feasibility Evaluation:" in md
    assert "| Chemical Validity | **MET** |" in md
