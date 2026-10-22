# AI-Assisted Research into Alternative Life

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23574418.svg)](https://doi.org/10.5281/zenodo.23574418)
[![CI](https://github.com/Zainul9142/AI-Assisted-Research-into-Alternative-Life/actions/workflows/ci.yml/badge.svg)](https://github.com/Zainul9142/AI-Assisted-Research-into-Alternative-Life/actions)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An evidence-grounded computational framework and evaluation protocol for investigating oxygen-independent metabolism and hypothetical biochemistries using artificial intelligence and constraint-based metabolic modeling.

---

## Overview

Research into alternative life asks which aspects of terrestrial biology are universal and which are accidents of planetary history. While generative AI systems can accelerate literature synthesis and hypothesis generation, they present major scientific risks: hallucinated citations, missing thermodynamic caveats, and stoichiometrically impossible reaction proposals.

Crucially, scientific and public discussions frequently conflate:

1. **Organisms that do not require molecular oxygen ($O_2$ gas)**: Well-established across diverse anaerobic taxa (e.g., fermentation, anaerobic respiration).
2. **Organisms containing no oxygen atoms whatsoever**: Highly speculative and undemonstrated in nature (since nucleic acids, amino acids, lipids, and water universally contain oxygen atoms).

This repository provides the reference computational implementation, evidence-record schemas, stoichiometric validation parsers, and constraint-based metabolic simulation protocols corresponding to the thesis:

> **Ekbal, Md.** (2026). *AI-Assisted Research into Alternative Life: An Evidence-Grounded Computational Framework for Oxygen-Independent Metabolism and Hypothetical Biochemistries*. Zenodo. DOI: [10.5281/zenodo.23574418](https://doi.org/10.5281/zenodo.23574418).

---

## Conceptual Framework & Methodological Layers

```text
Define Research Question 
   └── Literature Retrieval & Screening 
         └── AI-Assisted Claim Extraction 
               └── Evidence Taxonomy Classification (Classes A–D)
                     └── Constraint-Based Modeling (COBRApy) & Mass Balance Checks
                           └── Feasibility Rubric Scoring (5 Pillars)
                                 └── Human Expert Review & Audit Reporting
```

### 1. Three Levels of "Life Without Oxygen" (Table 1)

| Level | Claim | Status & Scientific Reality |
|---|---|---|
| **Level 1** | A process or organism does not require molecular oxygen ($O_2$) | **Established**. Anaerobic fermentation and respiration are documented across thousands of terrestrial species. |
| **Level 2** | An organism does not use $O_2$ as electron acceptor, but uses oxygen-bearing molecules ($NO_3^-$, $SO_4^{2-}$, $CO_2$, $H_2O$) | **Established**. Most anaerobes fall here. Their existence proves that oxygen atoms are deeply embedded in biochemistry even where $O_2$ gas is absent. |
| **Level 3** | An organism's molecules contain no oxygen atoms at all | **Speculative**. Undemonstrated in nature. Water, genetic polymers, and metabolic backbones universally contain oxygen atoms. |

### 2. Four-Tier Evidence Taxonomy (Table 2)

Every claim in the framework is strictly assigned to exactly one class:

* **Class A (Established Observation):** Directly supported by empirical evidence in verified, peer-reviewed literature.
* **Class B (Inference):** Derived systematically from a computational model or theory under explicit assumptions.
* **Class C (Speculation):** Chemically coherent hypotheses lacking empirical validation.
* **Class D (Unsupported/Contradicted):** Unverified citations, physically inconsistent assertions, or atom-imbalanced reactions.

### 3. Automated Validation & Feasibility Rubric (Table 3)

* **Stoichiometric & Charge Balance:** Automated chemical formula parser guaranteeing conservation of mass ($C, H, O, N, P, S$, etc.) and net formal charge.
* **Metabolic Modeling:** Constraint-based simulation using **COBRApy** on curated models (e.g., *E. coli* `e_coli_core` / `iJO1366`) enforcing zero-$O_2$ uptake bounds to distinguish Level 1 from Level 3.
* **Five-Pillar Feasibility Rubric:** Evaluates speculative claims across:
  1. *Chemical validity* (atom & charge balance)
  2. *Thermodynamic plausibility* ($\Delta G^\circ < 0$)
  3. *Stability and environment* (solvent, temperature, pressure compatibility)
  4. *Functional completeness* (catalysis, heredity, compartmentalisation, bioenergetics)
  5. *Empirical accessibility* (falsifiable experimental/observational tests)

---

## Repository Structure

```text
├── Alternative Life Manuscript.docx    # Full manuscript & study protocol (updated v1.1)
├── Alternative Life Manuscript.pdf     # Publication-ready PDF formatted version
├── README.md                           # Documentation and usage guide
├── requirements.txt                    # Pinned Python dependencies
├── pyproject.toml                      # Package configuration & build metadata
├── LICENSE                             # Creative Commons Attribution 4.0 International (CC BY 4.0)
│
├── src/                                # Core computational framework
│   ├── __init__.py                     # Package exports
│   ├── balance_checker.py              # Stoichiometric & charge balance verification engine
│   ├── evidence_taxonomy.py            # 4-tier taxonomy schema & validation database
│   ├── feasibility_rubric.py           # Table 3 speculative claim evaluation rubric
│   ├── metabolic_model.py              # COBRApy FBA simulation & oxygen dependency audit
│   └── cli.py                          # Unified command-line interface
│
├── data/                               # Curated evidence databases & schemas
│   ├── evidence_records.json           # Audited evidence records (Classes A–D)
│   ├── evidence_records.csv            # Tabular export for review tables
│   └── speculative_claims.json         # Evaluated speculative hypotheses
│
├── benchmark/                          # Ground-truth evaluation test sets
│   └── reaction_test_set.json          # 20 benchmark reactions with balanced/imbalanced labels
│
├── models/                             # Curated metabolic models
│   └── e_coli_core.json                # Standard textbook genome-scale metabolic network
│
├── tests/                              # Automated test suite (Pytest)
│   ├── test_balance_checker.py         # Chemical parser & balance tests
│   ├── test_evidence_taxonomy.py       # Taxonomy and schema validation tests
│   ├── test_feasibility_rubric.py      # Rubric scoring & markdown export tests
│   ├── test_metabolic_model.py         # COBRApy simulation & oxygen audit tests
│   └── test_cli.py                     # CLI subcommand integration tests
│
└── manuscript_drafts/                  # Archived previous drafts
    ├── AI-Assisted Research into Alternative Life...docx
    └── Alternative_Life_Thesis_Word.docx
```

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Zainul9142/AI-Assisted-Research-into-Alternative-Life.git
cd AI-Assisted-Research-into-Alternative-Life

# Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage Guide

### 1. Command-Line Interface (CLI)

The framework includes a unified CLI for running audits, balance checks, simulations, and benchmarks:

#### Chemical and Charge Balance Validation
Check whether a chemical reaction equation conserves elemental mass and net charge:

```bash
# Test a balanced reaction (ethanol fermentation)
python -m src.cli check-balance "C6H12O6 -> 2 C2H5OH + 2 CO2"

# Test an imbalanced reaction (missing CO2)
python -m src.cli check-balance "C6H12O6 -> 2 C2H5OH + CO2"

# Test redox charge balance
python -m src.cli check-balance "Fe[3+] + e- -> Fe[2+]"
```

#### Evidence Schema Validation
Audit an evidence database to guarantee all entries comply with the Appendix A schema and calculate the unsupported-claim rate (Class D):

```bash
python -m src.cli validate-evidence data/evidence_records.json
```

#### Metabolic Modeling Simulation (COBRApy)
Simulate anaerobic growth under zero-$O_2$ uptake bounds and audit cellular oxygen dependency:

```bash
python -m src.cli simulate-metabolism
```

*Sample Output:*
```text
=================================================================
 CONSTRAINT-BASED METABOLIC MODELING (COBRApy)
=================================================================
Model ID: e_coli_core

1. Baseline Aerobic Conditions (O2 available):
   Growth Rate: 0.8739 hr-1
   O2 Uptake:   -21.7995 mmol/gDW/hr

2. Anaerobic Conditions (EX_o2_e bounded to 0.0):
   Growth Rate: 0.2117 hr-1
   O2 Uptake:   0.0000 mmol/gDW/hr
   Active Fermentation Excretion Fluxes:
     * EX_etoh_e     : 8.2795 mmol/gDW/hr
     * EX_ac_e       : 8.5036 mmol/gDW/hr
     * EX_for_e      : 17.8047 mmol/gDW/hr

3. Oxygen Dependency Audit (Table 1 Validation):
   * Total Metabolites in Model: 72
   * Metabolites Containing Oxygen: 68 (94.44%)
   * Conclusion: Level 1 Anaerobic = True (Viable growth without O2 gas)
                 Level 3 Oxygen-Free = False (Cells strictly require oxygen atoms)
=================================================================
```

#### Run the Benchmark Test Suite
Execute the 20-reaction ground-truth benchmark to evaluate sensitivity and specificity:

```bash
python -m src.cli run-benchmark
```

---

### 2. Python API Usage

You can also import and use the framework modules directly in your scripts:

```python
from src.balance_checker import check_balance
from src.evidence_taxonomy import EvidenceStore
from src.metabolic_model import simulate_metabolic_phenotype

# 1. Validate a reaction
res = check_balance("CH4 + SO4[2-] -> HCO3- + HS- + H2O")
print(res.summary())
# Output: Balanced (Net atoms conserved: C: 1, H: 4, O: 4, S: 1; Charge: -2)

# 2. Query evidence database
store = EvidenceStore.load_json("data/evidence_records.json")
print("Unsupported claim rate:", store.unsupported_claim_rate())

# 3. Run FBA simulation
report = simulate_metabolic_phenotype(anaerobic=True)
print(f"Anaerobic growth rate: {report.objective_value} hr⁻¹")
```

---

## Running the Automated Test Suite

Run the full pytest suite:

```bash
pytest -v
```

All 17 automated tests cover stoichiometric parsing, taxonomy validation, rubric scoring, COBRApy metabolic simulations, and CLI commands.

---

## Citation

If you use this conceptual framework, computational validation protocol, or evidence schema in your research, please cite:

```bibtex
@article{ekbal2026alternative_life,
  author    = {Ekbal, Md},
  title     = {AI-Assisted Research into Alternative Life: An Evidence-Grounded Computational Framework for Oxygen-Independent Metabolism and Hypothetical Biochemistries},
  year      = {2026},
  month     = {October},
  doi       = {10.5281/zenodo.23574418},
  publisher = {Zenodo},
  url       = {https://doi.org/10.5281/zenodo.23574418}
}
```

---

## License

This project and manuscript are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
