"""
Feasibility Rubric for Speculative Alternative Biochemistries.

This module implements Section 3.3 (Table 3) of the framework:
It provides a multi-dimensional evaluation rubric for scoring speculative claims (Class C)
across five essential pillars:
  1. Chemical validity (atom & charge balance, valence rules)
  2. Thermodynamic plausibility (favourable free-energy change under stated conditions)
  3. Stability and environment (stability in proposed solvent, temperature, pressure)
  4. Functional completeness (information storage, catalysis, compartmentalisation, energy conservation)
  5. Empirical accessibility (falsifiable observation or testable experiment)
"""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class RubricRating(str, Enum):
    MET = "MET"
    PARTLY_MET = "PARTLY_MET"
    NOT_MET = "NOT_MET"
    UNKNOWN = "UNKNOWN"


class CriterionEvaluation(BaseModel):
    criterion: str
    question: str
    rating: RubricRating
    rationale: str


class FeasibilityScorecard(BaseModel):
    claim_id: str
    hypothesis_title: str
    chemical_validity: CriterionEvaluation
    thermodynamic_plausibility: CriterionEvaluation
    stability_and_environment: CriterionEvaluation
    functional_completeness: CriterionEvaluation
    empirical_accessibility: CriterionEvaluation
    overall_verdict: str
    key_knowledge_gaps: List[str] = Field(default_factory=list)
    proposed_computational_tests: List[str] = Field(default_factory=list)

    def summary(self) -> str:
        ratings = [
            f"Chemical Validity: {self.chemical_validity.rating.value}",
            f"Thermodynamics: {self.thermodynamic_plausibility.rating.value}",
            f"Stability/Env: {self.stability_and_environment.rating.value}",
            f"Functional Completeness: {self.functional_completeness.rating.value}",
            f"Empirical Accessibility: {self.empirical_accessibility.rating.value}",
        ]
        return f"[{self.claim_id}] {self.hypothesis_title} -> {self.overall_verdict}\n  " + "\n  ".join(ratings)

    def to_markdown(self) -> str:
        lines = [
            f"### Feasibility Evaluation: {self.hypothesis_title} (`{self.claim_id}`)",
            f"**Overall Verdict:** {self.overall_verdict}\n",
            "| Criterion | Rating | Rationale |",
            "|---|---|---|",
            f"| Chemical Validity | **{self.chemical_validity.rating.value}** | {self.chemical_validity.rationale} |",
            f"| Thermodynamic Plausibility | **{self.thermodynamic_plausibility.rating.value}** | {self.thermodynamic_plausibility.rationale} |",
            f"| Stability & Environment | **{self.stability_and_environment.rating.value}** | {self.stability_and_environment.rationale} |",
            f"| Functional Completeness | **{self.functional_completeness.rating.value}** | {self.functional_completeness.rationale} |",
            f"| Empirical Accessibility | **{self.empirical_accessibility.rating.value}** | {self.empirical_accessibility.rationale} |",
        ]
        if self.key_knowledge_gaps:
            lines.append("\n**Key Knowledge Gaps:**")
            for gap in self.key_knowledge_gaps:
                lines.append(f"- {gap}")
        if self.proposed_computational_tests:
            lines.append("\n**Proposed Computational / Experimental Tests:**")
            for test in self.proposed_computational_tests:
                lines.append(f"- {test}")
        return "\n".join(lines)


def evaluate_speculative_claim(
    claim_id: str,
    hypothesis_title: str,
    chem_rating: RubricRating,
    chem_notes: str,
    thermo_rating: RubricRating,
    thermo_notes: str,
    env_rating: RubricRating,
    env_notes: str,
    func_rating: RubricRating,
    func_notes: str,
    emp_rating: RubricRating,
    emp_notes: str,
    knowledge_gaps: Optional[List[str]] = None,
    proposed_tests: Optional[List[str]] = None
) -> FeasibilityScorecard:
    """Helper to construct and summarize a feasibility scorecard."""
    chem = CriterionEvaluation(
        criterion="Chemical validity",
        question="Are all proposed reactions atom- and charge-balanced?",
        rating=chem_rating,
        rationale=chem_notes
    )
    thermo = CriterionEvaluation(
        criterion="Thermodynamic plausibility",
        question="Is the overall free-energy change favourable under stated conditions, using reliable data?",
        rating=thermo_rating,
        rationale=thermo_notes
    )
    env = CriterionEvaluation(
        criterion="Stability and environment",
        question="Are the molecules stable in the proposed solvent, temperature and pressure range?",
        rating=env_rating,
        rationale=env_notes
    )
    func = CriterionEvaluation(
        criterion="Functional completeness",
        question="Are information storage, catalysis, compartmentalisation and energy conservation all addressed?",
        rating=func_rating,
        rationale=func_notes
    )
    emp = CriterionEvaluation(
        criterion="Empirical accessibility",
        question="Is there a feasible observation or experiment that could support or refute the claim?",
        rating=emp_rating,
        rationale=emp_notes
    )

    # Determine overall assessment
    ratings = [chem_rating, thermo_rating, env_rating, func_rating, emp_rating]
    if RubricRating.NOT_MET in (chem_rating, thermo_rating):
        verdict = "Chemically/Thermodynamically Infeasible under Current Physics"
    elif ratings.count(RubricRating.MET) >= 4 and RubricRating.NOT_MET not in ratings:
        verdict = "High Theoretical Plausibility (Requires Empirical Validation)"
    elif ratings.count(RubricRating.UNKNOWN) >= 2 or RubricRating.PARTLY_MET in ratings:
        verdict = "Speculative Hypothesis with Substantial Gaps (Class C)"
    else:
        verdict = "Hypothetical Proposal Requiring Model Constraints"

    return FeasibilityScorecard(
        claim_id=claim_id,
        hypothesis_title=hypothesis_title,
        chemical_validity=chem,
        thermodynamic_plausibility=thermo,
        stability_and_environment=env,
        functional_completeness=func,
        empirical_accessibility=emp,
        overall_verdict=verdict,
        key_knowledge_gaps=knowledge_gaps or [],
        proposed_computational_tests=proposed_tests or []
    )
