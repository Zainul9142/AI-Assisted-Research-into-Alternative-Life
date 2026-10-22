"""Unit tests for evidence taxonomy and Appendix A schema."""

import pytest
from pathlib import Path
from pydantic import ValidationError
from src.evidence_taxonomy import (
    EvidenceClass,
    EvidenceRecord,
    EvidenceStore,
    ReviewerStatus
)


def test_valid_class_a_record():
    record = EvidenceRecord(
        claim_id="CLAIM-TEST-01",
        claim_text="Anaerobic microorganisms exist and thrive without molecular oxygen.",
        source_title="Principles of Microbiology",
        authors="Test Author",
        year=2024,
        doi_or_url="https://doi.org/10.1000/182",
        access_date="2026-10-22",
        supporting_passage="Anaerobic microbes grow under anoxic regimes without O2 gas.",
        evidence_class=EvidenceClass.CLASS_A,
        reviewer_status=ReviewerStatus.ACCEPTED,
        confidence_rationale="Empirically confirmed in laboratory isolation.",
        validation_checks=["Literature peer review"]
    )
    assert record.evidence_class == EvidenceClass.CLASS_A
    assert record.reviewer_status == ReviewerStatus.ACCEPTED


def test_class_a_requires_source_passage():
    with pytest.raises(ValidationError):
        EvidenceRecord(
            claim_id="CLAIM-TEST-BAD",
            claim_text="Hypothesis without proof.",
            source_title="Some source",
            authors="Test Author",
            year=2024,
            doi_or_url="https://doi.org/10.1000/182",
            access_date="2026-10-22",
            supporting_passage="",  # Empty supporting passage must fail for Class A
            evidence_class=EvidenceClass.CLASS_A,
            confidence_rationale="No rationale"
        )


def test_evidence_store_operations(tmp_path: Path):
    json_file = Path(__file__).resolve().parent.parent / "data" / "evidence_records.json"
    store = EvidenceStore.load_json(json_file)
    
    assert len(store.records) >= 5
    counts = store.count_by_class()
    assert counts[EvidenceClass.CLASS_A.value] >= 2
    assert counts[EvidenceClass.CLASS_D.value] >= 1
    
    rate = store.unsupported_claim_rate()
    assert 0.0 < rate < 1.0

    # Markdown export
    md = store.to_markdown_table()
    assert "| Claim ID |" in md
    assert "CLAIM-001" in md

    # CSV save and reload check
    csv_out = tmp_path / "test_export.csv"
    store.save_csv(csv_out)
    assert csv_out.exists()
    assert csv_out.stat().st_size > 100
