"""
AI-Assisted Research into Alternative Life: Computational Framework.

An evidence-grounded computational framework and evaluation protocol for investigating
oxygen-independent metabolism and hypothetical biochemistries using artificial intelligence
and constraint-based metabolic modeling.
"""

__version__ = "1.1.0"
__author__ = "Md Ekbal"

from src.balance_checker import check_balance, BalanceResult, parse_formula
from src.evidence_taxonomy import EvidenceClass, EvidenceRecord, EvidenceStore, ReviewerStatus
from src.feasibility_rubric import FeasibilityScorecard, RubricRating, evaluate_speculative_claim
from src.metabolic_model import simulate_metabolic_phenotype, audit_metabolic_oxygen_dependency, load_metabolic_model

__all__ = [
    "check_balance",
    "BalanceResult",
    "parse_formula",
    "EvidenceClass",
    "EvidenceRecord",
    "EvidenceStore",
    "ReviewerStatus",
    "FeasibilityScorecard",
    "RubricRating",
    "evaluate_speculative_claim",
    "simulate_metabolic_phenotype",
    "audit_metabolic_oxygen_dependency",
    "load_metabolic_model",
]
