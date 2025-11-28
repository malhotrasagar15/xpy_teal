[![PyPI version](https://img.shields.io/pypi/v/xpy-teal.svg)](https://pypi.org/project/xpy-teal/)
# 🌌 XPy-Teal: XP Tool for Emission and Absorption Lines

XPy-Teal is a Python version of the tool developed by [M. Weiler et al. 2023](https://arxiv.org/abs/2211.06946) for the analysis of Gaia DR3 XP spectra.
This repository provides a modular Python toolkit for downloading, processing, and analyzing **Gaia DR3 XP (BP/RP) spectra**.  
It includes tools for XP data retrieval via the Gaia Archive, data calibration, equivalent width measurement, and mathematical utilities for line analysis.

⚠️ Note: The current version only supports the **Narrow Line Approximation** for equivalent width measurements. See the [original paper](https://arxiv.org/abs/2211.06946) for more details.
---

## Column Description

### Hα line output columns

- `Halpha_W`  
  Equivalent width of the Hα line (nm). Note the sign convention: positive = emission, negative = absorption.

- `Halpha_Werror`  
  Uncertainty on the equivalent width (nm).

- `Halpha_p`  
  Significance of the detected extremum associated with the Hα line.

- `Halpha_D`  
  Line-width parameter (see Eq. 89 in [Weiler et al. 2023](https://arxiv.org/abs/2211.06946)). Values ≫ 1 indicate a broad line.

- `Halpha_order`  
  Derivative order of the detected extremum (0 or 2). If no extremum is detected, this field is set to `uL` and an upper limit on the equivalent width is provided instead.

Notes
- Units are in nanometres (nm) unless otherwise stated.
- The same column naming convention is used for other requested lines.

---

## ⚙️ Installation

⚡ Option 1 — Using uv (recommended for speed)

uv is a fast, modern Python package manager built by Astral — it handles environments, dependencies, and builds efficiently.

🪄 Step 1 — Install uv

If you don’t have it already, install with:
```
pip install uv
```
or (recommended):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

⚙️ Step 2 — Install XPy-Teal
In the root of this repository, run:
```
uv pip install xpy-teal
```
🚀 Step 3 — uv sync
```
uv sync
```
---

## 🚀 Usage

Here is a simple example of how to use XPy-Teal to run the analysis pipeline on a table of source IDs from Gaia DR3.

```python
from xpy_teal import xpy_teal_pipeline as xpy

results = xpy.run_pipeline(sources_table)
```

---


## 📄 License

GNU GENERAL PUBLIC LICENSE

---

