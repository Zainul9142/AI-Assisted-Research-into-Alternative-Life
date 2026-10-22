"""
Interactive Web Application for AI-Assisted Research into Alternative Life.

Runs on localhost to provide a graphical interface for:
  - Chemical and charge balance checking
  - Evidence database exploration (Classes A-D)
  - Live COBRApy metabolic modeling simulations
  - Benchmark evaluation execution
  - Manuscript viewing and download
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from src.balance_checker import check_balance
from src.evidence_taxonomy import EvidenceStore
from src.feasibility_rubric import FeasibilityScorecard
from src.metabolic_model import (
    simulate_metabolic_phenotype,
    audit_metabolic_oxygen_dependency,
    load_metabolic_model,
    COBRA_AVAILABLE
)

app = FastAPI(
    title="AI-Assisted Research into Alternative Life",
    description="Interactive Web Interface & Computational Framework",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

# Pre-load metabolic model if COBRApy is available
_cached_model = None
if COBRA_AVAILABLE:
    try:
        _cached_model = load_metabolic_model()
    except Exception:
        pass


class ReactionCheckRequest(BaseModel):
    reaction: str


class MetabolicSimRequest(BaseModel):
    anaerobic: bool = True
    glucose_uptake: float = 10.0


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "version": "1.1.0",
        "cobra_available": COBRA_AVAILABLE,
        "model_loaded": _cached_model is not None
    }


@app.post("/api/check-balance")
def api_check_balance(req: ReactionCheckRequest):
    if not req.reaction.strip():
        raise HTTPException(status_code=400, detail="Reaction string cannot be empty")
    res = check_balance(req.reaction)
    return {
        "reaction": res.reaction_str,
        "is_balanced": res.is_balanced,
        "verdict": res.verdict,
        "lhs_atoms": res.lhs_atoms,
        "rhs_atoms": res.rhs_atoms,
        "atom_deltas": res.atom_deltas,
        "lhs_charge": res.lhs_charge,
        "rhs_charge": res.rhs_charge,
        "charge_delta": res.charge_delta,
        "imbalances": res.imbalances,
        "summary": res.summary()
    }


@app.get("/api/evidence")
def api_get_evidence():
    json_path = BASE_DIR / "data" / "evidence_records.json"
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Evidence database not found")
    store = EvidenceStore.load_json(json_path)
    return {
        "records": [r.model_dump() for r in store.records.values()],
        "counts": store.count_by_class(),
        "unsupported_rate": round(store.unsupported_claim_rate() * 100, 1)
    }


@app.get("/api/speculative")
def api_get_speculative():
    json_path = BASE_DIR / "data" / "speculative_claims.json"
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Speculative claims file not found")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.post("/api/simulate-metabolism")
def api_simulate_metabolism(req: MetabolicSimRequest):
    if not COBRA_AVAILABLE:
        raise HTTPException(status_code=503, detail="COBRApy is not available")
    
    global _cached_model
    if _cached_model is None:
        _cached_model = load_metabolic_model()

    rep = simulate_metabolic_phenotype(
        _cached_model,
        anaerobic=req.anaerobic,
        glucose_uptake=req.glucose_uptake
    )
    audit = audit_metabolic_oxygen_dependency(_cached_model)

    return {
        "model_id": rep.model_id,
        "condition": rep.condition,
        "objective_value": rep.objective_value,
        "solver_status": rep.solver_status,
        "o2_exchange_flux": rep.o2_exchange_flux,
        "glucose_exchange_flux": rep.glucose_exchange_flux,
        "active_fermentation_fluxes": rep.active_fermentation_fluxes,
        "level_1_anaerobic_feasible": rep.level_1_anaerobic_feasible,
        "level_3_oxygen_free_feasible": rep.level_3_oxygen_free_feasible,
        "notes": rep.notes,
        "oxygen_audit": audit
    }


@app.post("/api/run-benchmark")
def api_run_benchmark():
    benchmark_path = BASE_DIR / "benchmark" / "reaction_test_set.json"
    if not benchmark_path.exists():
        raise HTTPException(status_code=404, detail="Benchmark test set not found")
    with open(benchmark_path, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    results = []
    correct = 0
    for t in tasks:
        rxn = t["reaction"]
        expected = t["expected_balanced"]
        res = check_balance(rxn)
        is_correct = (res.is_balanced == expected)
        if is_correct:
            correct += 1
        results.append({
            "task_id": t["task_id"],
            "category": t["category"],
            "reaction": rxn,
            "expected_balanced": expected,
            "actual_balanced": res.is_balanced,
            "is_correct": is_correct,
            "verdict": res.verdict,
            "notes": t.get("notes", "")
        })

    accuracy = (correct / len(tasks) * 100) if tasks else 0
    return {
        "total_tasks": len(tasks),
        "correct_predictions": correct,
        "accuracy": round(accuracy, 1),
        "tasks": results
    }


@app.get("/api/manuscript/pdf")
def get_pdf():
    pdf_path = BASE_DIR / "Alternative Life Manuscript.pdf"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(pdf_path, media_type="application/pdf", filename="Alternative_Life_Manuscript.pdf")


@app.get("/api/manuscript/docx")
def get_docx():
    docx_path = BASE_DIR / "Alternative Life Manuscript.docx"
    if not docx_path.exists():
        raise HTTPException(status_code=404, detail="DOCX not found")
    return FileResponse(docx_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="Alternative_Life_Manuscript.docx")


@app.get("/", response_class=HTMLResponse)
def index():
    html_file = BASE_DIR / "src" / "web" / "index.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    return "<h1>Alternative Life Framework</h1><p>Index template loading...</p>"
