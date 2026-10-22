# AI-Assisted Research into Alternative Life

An evidence-grounded computational framework and evaluation protocol for investigating oxygen-independent metabolism and hypothetical biochemistries using artificial intelligence and constraint-based metabolic modeling[cite: 1].

---

## Overview

Research into alternative life asks which aspects of terrestrial biology are universal and which are accidents of planetary history[cite: 1]. While AI systems can accelerate literature synthesis and hypothesis generation, they present major risks of hallucinated citations, missing chemical caveats, and stoichiometrically impossible reaction proposals[cite: 1].

Furthermore, scientific discussions frequently conflate:

1. **Organisms that do not require molecular oxygen ($O_2$)**: Well-established across anaerobic organisms[cite: 1].
2. **Organisms containing no oxygen atoms whatsoever**: Highly speculative and undemonstrated in nature[cite: 1].

This repository hosts the conceptual framework, formal evidence taxonomy, and computational validation protocol designed to enforce scientific rigor, source traceability, and stoichiometric validity in AI-generated alternative biochemistry claims[cite: 1].

---

## Core Framework & Methodological Layers

The framework introduces an auditable, multi-stage pipeline[cite: 1]:

```
Define Research Question 
   └── Literature Retrieval & Screening 
         └── AI-Assisted Claim Extraction 
               └── Evidence Taxonomy Classification (Classes A–D)
                     └── Constraint-Based Modeling (COBRApy) & Balance Checks
                           └── Feasibility Rubric Scoring 
                                 └── Human Expert Review & Reporting
```[cite: 1]

### 1. Three Levels of "Life Without Oxygen"
* **Level 1 (Established):** Organisms and processes not requiring molecular oxygen ($O_2$) gas (e.g., anaerobic fermentation, anaerobic respiration)[cite: 1].
* **Level 2 (Established):** Respiration using alternative terminal electron acceptors (nitrate, sulfate, $CO_2$) that still contain oxygen atoms[cite: 1].
* **Level 3 (Speculative):** Hypothetical chemistries containing zero oxygen atoms in their molecular composition[cite: 1].

### 2. Four-Tier Evidence Taxonomy
Every claim is assigned exactly one class:
* **Class A (Established Observation):** Directly supported by empirical evidence in verified literature[cite: 1].
* **Class B (Inference):** Derived systematically from a computational model or theory under explicit assumptions[cite: 1].
* **Class C (Speculation):** Chemically coherent hypotheses lacking empirical validation[cite: 1].
* **Class D (Unsupported/Contradicted):** Unverified citations, physically inconsistent assertions, or atom-imbalanced reactions[cite: 1].

### 3. Automated Validation & Feasibility Rubric
* **Stoichiometric & Charge Balance:** Automated chemical formula parsing to guarantee elemental conservation ($C, H, O, N, P, S$, charge)[cite: 1].
* **Metabolic Modeling:** Constraint-based simulation using **COBRApy** on curated models (e.g., *E. coli* `iJO1366`) to rigorously evaluate zero-$O_2$ uptake bounds[cite: 1].
* **Feasibility Rubric:** Evaluates speculative claims across chemical validity, thermodynamic plausibility, environmental stability, functional completeness, and empirical testability[cite: 1].

---

## Repository Structure

```text
├── Alternative Life Manuscript.docx   # Full manuscript & study protocol
├── README.md                          # Project documentation and summary
└── (Planned implementation files)
    ├── data/                          # Evidence databases and screening tables
    ├── models/                        # Genome-scale metabolic models (SBML/JSON)
    ├── src/                           # COBRApy simulation and atom-balance scripts
    └── benchmark/                     # Ground-truth tasks and evaluation sets
```[cite: 1]

---

## Implementation Stack (Planned)

* **Language:** Python 3.10+
* **Core Libraries:**
  * [COBRApy](https://github.com/opencobra/cobrapy) (Constraint-Based Reconstruction and Analysis)[cite: 1]
  * `pandas` (Structured evidence table processing)[cite: 1]
  * `rdkit` / custom parsers (Elemental and charge balance verification)
  * Jupyter Notebooks[cite: 1]

---

## Citation

If you use this conceptual framework, evaluation protocol, or evidence schema in your research, please cite:

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
```[cite: 1]

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

```
