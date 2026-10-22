"""
Four-Tier Evidence Taxonomy & Audit Schema.

This module implements Section 3.2 (Table 2) and Appendix A of the framework:
It provides a formal schema and validation engine that categorizes scientific claims
into four mutually exclusive tiers (Classes A–D), enforcing source provenance,
uncertainty calibration, and separating empirical observations from computational
inferences and hypothetical speculations.
"""

from __future__ import annotations

import csv
import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator


class EvidenceClass(str, Enum):
    """
    Four-tier evidence classification (Table 2):
      A: Established observation (Directly supported by empirical evidence in verified literature)
      B: Inference (Follows systematically from a model/theory under stated assumptions)
      C: Speculation (A chemically coherent hypothesis lacking direct empirical evidence)
      D: Unsupported or Contradicted (Fabricated citations, atom-imbalanced reactions, or contradictions)
    """
    CLASS_A = "Class A (Established Observation)"
    CLASS_B = "Class B (Inference)"
    CLASS_C = "Class C (Speculation)"
    CLASS_D = "Class D (Unsupported/Contradicted)"


class ReviewerStatus(str, Enum):
    """Human expert audit status."""
    ACCEPTED = "accepted"
    EDITED = "edited"
    REJECTED = "rejected"
    UNCERTAIN = "uncertain"


class EvidenceRecord(BaseModel):
    """
    Structured record according to Appendix A: Evidence-Record Schema.
    Guarantees that every claim is traceable to source passages and audited.
    """
    claim_id: str = Field(..., description="Unique identifier (e.g. CLAIM-001)")
    claim_text: str = Field(..., description="Normalized statement of the claim")
    source_title: str = Field(..., description="Title of the source publication or database")
    authors: str = Field(..., description="Authors of the referenced work")
    year: int = Field(..., description="Publication year")
    doi_or_url: str = Field(..., description="Persistent DOI or verified URL")
    access_date: str = Field(..., description="Date record was accessed or verified (YYYY-MM-DD)")
    supporting_passage: str = Field(..., description="Verbatim excerpt from the source supporting the claim")
    evidence_class: EvidenceClass = Field(..., description="Taxonomy classification A–D")
    counterevidence: Optional[str] = Field(default=None, description="Known contradictory findings or boundary caveats")
    reviewer_status: ReviewerStatus = Field(default=ReviewerStatus.ACCEPTED, description="Audit verdict")
    confidence_rationale: str = Field(..., description="Justification for confidence rating and class assignment")
    validation_checks: List[str] = Field(default_factory=list, description="List of computational and manual checks passed")
    notes: Optional[str] = Field(default=None, description="Additional contextual notes or limitations")

    @field_validator("claim_id")
    @classmethod
    def validate_claim_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("claim_id cannot be empty")
        return v.strip()

    @field_validator("claim_text")
    @classmethod
    def validate_claim_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("claim_text cannot be empty")
        return v.strip()

    @model_validator(mode="after")
    def validate_evidence_rigor(self) -> "EvidenceRecord":
        """Enforce strict evidence integrity rules."""
        # Class A requires a verifiable DOI/URL and verbatim supporting text
        if self.evidence_class == EvidenceClass.CLASS_A:
            if not self.supporting_passage.strip() or self.supporting_passage.lower() == "none":
                raise ValueError("Class A claims must provide a non-empty verbatim supporting passage.")
            if not self.doi_or_url.strip() or self.doi_or_url.lower() == "none":
                raise ValueError("Class A claims must provide a valid DOI or verifiable URL.")

        # Class D claims flagged with invalid balance cannot be marked as accepted without caveats
        if self.evidence_class == EvidenceClass.CLASS_D and self.reviewer_status == ReviewerStatus.ACCEPTED:
            # Only allowed if the notes explicitly acknowledge it as an audited negative control
            if not (self.notes and "negative control" in self.notes.lower()):
                raise ValueError("Class D (unsupported/contradicted) claims cannot have reviewer_status='accepted' unless documented as a negative control.")

        return self


class EvidenceStore:
    """In-memory database and verification manager for evidence records."""

    def __init__(self, records: Optional[List[EvidenceRecord]] = None):
        self.records: Dict[str, EvidenceRecord] = {}
        if records:
            for r in records:
                self.add_record(r)

    def add_record(self, record: EvidenceRecord) -> None:
        self.records[record.claim_id] = record

    def get(self, claim_id: str) -> Optional[EvidenceRecord]:
        return self.records.get(claim_id)

    def count_by_class(self) -> Dict[str, int]:
        counts = {c.value: 0 for c in EvidenceClass}
        for r in self.records.values():
            counts[r.evidence_class.value] += 1
        return counts

    def unsupported_claim_rate(self) -> float:
        """Calculate the proportion of claims judged Class D (Section 4.9)."""
        if not self.records:
            return 0.0
        class_d = sum(1 for r in self.records.values() if r.evidence_class == EvidenceClass.CLASS_D)
        return class_d / len(self.records)

    def to_markdown_table(self) -> str:
        """Format stored claims into an audit markdown table."""
        headers = ["Claim ID", "Claim Statement", "Class", "Source", "Reviewer Status"]
        rows = []
        for r in self.records.values():
            short_class = r.evidence_class.name.replace("CLASS_", "Class ")
            short_claim = r.claim_text if len(r.claim_text) < 70 else r.claim_text[:67] + "..."
            short_source = f"{r.authors} ({r.year})"
            rows.append(f"| {r.claim_id} | {short_claim} | {short_class} | {short_source} | {r.reviewer_status.value} |")

        sep = "| " + " | ".join(["---"] * len(headers)) + " |"
        header_str = "| " + " | ".join(headers) + " |"
        return "\n".join([header_str, sep] + rows)

    @classmethod
    def load_json(cls, json_path: Union[str, Path]) -> "EvidenceStore":
        path = Path(json_path)
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        store = cls()
        for item in raw_data:
            store.add_record(EvidenceRecord(**item))
        return store

    def save_json(self, json_path: Union[str, Path]) -> None:
        path = Path(json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [r.model_dump() for r in self.records.values()]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_csv(self, csv_path: Union[str, Path]) -> None:
        path = Path(csv_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not self.records:
            return
        
        fieldnames = list(next(iter(self.records.values())).model_dump().keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in self.records.values():
                d = r.model_dump()
                d["validation_checks"] = "; ".join(d["validation_checks"])
                writer.writerow(d)
