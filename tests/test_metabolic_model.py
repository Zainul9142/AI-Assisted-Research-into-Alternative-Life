"""Unit tests for constraint-based metabolic modeling."""

import pytest
from src.metabolic_model import (
    load_metabolic_model,
    simulate_metabolic_phenotype,
    audit_metabolic_oxygen_dependency,
    COBRA_AVAILABLE
)

pytestmark = pytest.mark.skipif(not COBRA_AVAILABLE, reason="COBRApy not installed")


def test_load_default_model():
    model = load_metabolic_model()
    assert model is not None
    assert len(model.reactions) > 50
    assert len(model.metabolites) > 50


def test_aerobic_vs_anaerobic_simulation():
    model = load_metabolic_model()
    
    # Aerobic
    rep_aero = simulate_metabolic_phenotype(model, anaerobic=False)
    assert rep_aero.objective_value > 0.5
    assert rep_aero.o2_exchange_flux < -10.0  # Consuming O2
    
    # Anaerobic (Zero O2 uptake)
    rep_anaero = simulate_metabolic_phenotype(model, anaerobic=True)
    assert rep_anaero.objective_value > 0.1  # Can still grow via fermentation
    assert rep_anaero.o2_exchange_flux == 0.0  # Zero molecular oxygen
    assert rep_anaero.level_1_anaerobic_feasible is True
    assert rep_anaero.level_3_oxygen_free_feasible is False
    
    # Must produce fermentation byproducts
    ferment = rep_anaero.active_fermentation_fluxes
    assert any(k in ferment for k in ("EX_etoh_e", "EX_ac_e", "EX_for_e"))


def test_oxygen_dependency_audit():
    model = load_metabolic_model()
    audit = audit_metabolic_oxygen_dependency(model)
    assert audit["total_metabolites"] > 50
    assert audit["metabolites_containing_oxygen"] > 40
    assert audit["percentage_oxygen_bearing"] > 80.0
