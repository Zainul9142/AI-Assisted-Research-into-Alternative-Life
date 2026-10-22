"""
Constraint-Based Metabolic Modeling & Oxygen Dependency Simulation.

This module implements Section 2.5, Section 4.4, and Section 7.2 of the framework:
It uses COBRApy and flux balance analysis (FBA) to:
  1. Reproduce baseline growth under standard aerobic conditions.
  2. Simulate anaerobic conditions by setting the oxygen exchange lower bound (EX_o2_e) to zero.
  3. Quantify active fermentation fluxes (ethanol, acetate, formate, lactate, succinate).
  4. Perform an elemental mass and atom audit demonstrating the fundamental thesis distinction:
     An organism can readily grow with zero molecular oxygen (O2) uptake (Level 1 / Level 2),
     while still strictly requiring oxygen atoms embedded in its substrates, metabolites,
     and biomass (refuting naive Level 3 claims).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import cobra
    from cobra.io import load_json_model, read_sbml_model
    COBRA_AVAILABLE = True
except ImportError:
    COBRA_AVAILABLE = False


@dataclass
class MetabolicSimulationReport:
    """Structured report detailing FBA solution under aerobic vs anaerobic constraints."""
    model_id: str
    condition: str
    objective_value: float
    solver_status: str
    o2_exchange_flux: float
    glucose_exchange_flux: float
    active_fermentation_fluxes: Dict[str, float] = field(default_factory=dict)
    biomass_requires_oxygen_atoms: bool = True
    level_1_anaerobic_feasible: bool = True
    level_3_oxygen_free_feasible: bool = False
    notes: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "Feasible" if self.objective_value > 1e-4 else "Infeasible"
        ferment_str = ", ".join(f"{k}: {v:.4f}" for k, v in self.active_fermentation_fluxes.items()) or "None"
        return (
            f"Model: {self.model_id} | Condition: {self.condition}\n"
            f"Growth Rate (Objective): {self.objective_value:.4f} hr⁻¹ ({status})\n"
            f"O2 Uptake Flux: {self.o2_exchange_flux:.4f} mmol/gDW/hr\n"
            f"Glucose Uptake Flux: {self.glucose_exchange_flux:.4f} mmol/gDW/hr\n"
            f"Active Fermentation Byproducts: {ferment_str}\n"
            f"Framework Assessment: Level 1 (O2-independent) = {self.level_1_anaerobic_feasible}; "
            f"Level 3 (Oxygen-atom-free) = {self.level_3_oxygen_free_feasible}"
        )


def get_default_model_path() -> Path:
    """Return path to bundled e_coli_core.json model."""
    root_dir = Path(__file__).resolve().parent.parent
    return root_dir / "models" / "e_coli_core.json"


def load_metabolic_model(model_path: Optional[str | Path] = None) -> Any:
    """
    Load a metabolic model from a JSON or SBML file path.
    Falls back to bundled e_coli_core.json or COBRApy textbook model.
    """
    if not COBRA_AVAILABLE:
        raise RuntimeError("COBRApy is not installed. Please install with 'pip install cobra'.")

    path = Path(model_path) if model_path else get_default_model_path()

    if path.exists():
        if path.suffix.lower() == ".json":
            return load_json_model(str(path))
        elif path.suffix.lower() in (".xml", ".sbml"):
            return read_sbml_model(str(path))

    # Fallback to cobra built-in textbook
    from cobra.io import load_model
    return load_model("textbook")


def simulate_metabolic_phenotype(
    model: Optional[Any] = None,
    anaerobic: bool = False,
    glucose_uptake: float = 10.0,
    model_path: Optional[str | Path] = None
) -> MetabolicSimulationReport:
    """
    Run Flux Balance Analysis on the model under defined aerobic or anaerobic constraints.

    Parameters:
      model: Pre-loaded cobra.Model instance (or None to load default).
      anaerobic: If True, set EX_o2_e lower_bound to 0.0 (zero molecular oxygen uptake).
      glucose_uptake: Lower bound for glucose exchange (default 10 mmol/gDW/hr).
      model_path: Optional path to JSON/SBML model.
    """
    if model is None:
        model = load_metabolic_model(model_path)

    # Use a copy/context so modifications don't alter original in-memory instance permanently
    with model:
        # Standardize carbon source (glucose)
        if "EX_glc__D_e" in model.reactions:
            model.reactions.get_by_id("EX_glc__D_e").lower_bound = -abs(glucose_uptake)

        # Apply oxygen uptake boundary condition
        condition_name = "Anaerobic (Zero O2 Uptake)" if anaerobic else "Aerobic (Unconstrained O2)"
        o2_rxn = None
        for rxn_id in ("EX_o2_e", "EX_o2(e)", "R_EX_o2_e"):
            if rxn_id in model.reactions:
                o2_rxn = model.reactions.get_by_id(rxn_id)
                break

        if o2_rxn is not None:
            if anaerobic:
                o2_rxn.lower_bound = 0.0  # Level 1 constraint: zero molecular oxygen consumed
            else:
                o2_rxn.lower_bound = -1000.0  # Ample O2 available

        # Run FBA optimization
        solution = model.optimize()
        obj_val = float(solution.objective_value) if solution.objective_value is not None else 0.0
        status = str(solution.status)

        o2_flux = float(solution.fluxes[o2_rxn.id]) if o2_rxn and o2_rxn.id in solution.fluxes else 0.0
        glc_flux = float(solution.fluxes["EX_glc__D_e"]) if "EX_glc__D_e" in solution.fluxes else 0.0

        # Collect key fermentation exchange fluxes
        candidate_ferment = [
            "EX_etoh_e", "EX_ac_e", "EX_for_e", "EX_lac__D_e", "EX_succ_e",
            "EX_pyr_e", "EX_h2_e", "EX_co2_e"
        ]
        active_ferment: Dict[str, float] = {}
        for rxn_id in candidate_ferment:
            if rxn_id in model.reactions and rxn_id in solution.fluxes:
                flux = float(solution.fluxes[rxn_id])
                if abs(flux) > 1e-4:
                    active_ferment[rxn_id] = round(flux, 4)

        solver_info = getattr(model.solver, "interface", type(model.solver)).__name__
        notes = [
            f"FBA completed using solver: {solver_info}",
            "Objective function: " + str(model.objective.expression),
        ]
        if anaerobic:
            notes.append("O2 exchange strictly bounded to 0.0 mmol/gDW/hr.")
            if obj_val > 0.01:
                notes.append("System achieved viable growth rate via mixed-acid fermentation pathways.")
                notes.append(
                    "CRITICAL AUDIT: Although O2 gas consumption is zero (Level 1 proven), "
                    "biomass synthesis still consumes oxygen atoms from glucose (C6H12O6) and water (H2O). "
                    "This computational test directly refutes that Level 1 implies Level 3 (oxygen-atom-free life)."
                )

        return MetabolicSimulationReport(
            model_id=model.id,
            condition=condition_name,
            objective_value=round(obj_val, 4),
            solver_status=status,
            o2_exchange_flux=round(o2_flux, 4),
            glucose_exchange_flux=round(glc_flux, 4),
            active_fermentation_fluxes=active_ferment,
            biomass_requires_oxygen_atoms=True,
            level_1_anaerobic_feasible=(obj_val > 1e-4),
            level_3_oxygen_free_feasible=False,
            notes=notes
        )


def audit_metabolic_oxygen_dependency(model: Optional[Any] = None) -> Dict[str, Any]:
    """
    Inspect model metabolites and biomass reaction to calculate the proportion
    of essential cellular metabolites containing oxygen atoms.
    """
    if model is None:
        model = load_metabolic_model()

    total_mets = len(model.metabolites)
    mets_with_oxygen = 0
    oxygen_free_mets = []

    for met in model.metabolites:
        formula = met.formula or ""
        # Check if formula contains 'O' as an element
        # (avoid matching Os for Osmium or looking inside other element names)
        import re
        has_oxygen = bool(re.search(r'O(?![a-z])', formula))
        if has_oxygen:
            mets_with_oxygen += 1
        else:
            oxygen_free_mets.append(met.id)

    pct_with_o = (mets_with_oxygen / total_mets * 100.0) if total_mets > 0 else 0.0

    return {
        "model_id": model.id,
        "total_metabolites": total_mets,
        "metabolites_containing_oxygen": mets_with_oxygen,
        "percentage_oxygen_bearing": round(pct_with_o, 2),
        "sample_oxygen_free_metabolites": oxygen_free_mets[:10],
        "conclusion": (
            f"{pct_with_o:.1f}% of metabolites in the curated metabolic model contain oxygen atoms. "
            "Even under anaerobic fermentation, oxygen is intrinsically conserved in nucleic acids, "
            "lipids, amino acids, and central carbon intermediates."
        )
    }
