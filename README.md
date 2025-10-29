# 🌌 XPy-Teal: XP Tool for Emission and Absorption Lines

This repository provides a modular Python toolkit for downloading, processing, and analyzing **Gaia DR3 XP (BP/RP) spectra**.  
It includes tools for XP data retrieval via the Gaia Archive, data calibration, equivalent width measurement, and mathematical utilities for line analysis.

---

## 📁 Repository Structure

```
/
├── src
│   └── xpy_teal
│       ├── Codes
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── dataIO.py
│       │   ├── download_xp_spectra.py
│       │   ├── line_analysis.py
│       │   ├── main.py
│       │   ├── math_tools.py
│       │   ├── spectrum_tools.py
│       │   └── xpy_teal_pipeline.py
│       ├── Configuration_Data
│       │   ├── BasisTransformationMatrix_BP.csv
│       │   ├── BasisTransformationMatrix_RP.csv
│       │   ├── DerivativeMatrix_D1.csv
│       │   ├── DerivativeMatrix_D2.csv
│       │   ├── DerivativeMatrix_D3.csv
│       │   ├── DerivativeMatrix_D4.csv
│       │   ├── HermiteIntegrals.csv
│       │   ├── LSFModel_BP.csv
│       │   ├── LSFModel_RP.csv
│       │   ├── RootMatrix_H.csv
│       │   ├── bpC03_v375wi_dispersion.csv
│       │   ├── bpC03_v375wi_response.csv
│       │   ├── rpC03_v142r_dispersion.csv
│       │   └── rpC03_v142r_response.csv
│       ├── Data
│       │   ├── Test_EqWidths.csv
│       │   ├── Test_Extrema.pkl
│       │   ├── source_ids.csv
│       │   ├── test.xml
│       │   ├── xp_continuous_downloaded.csv
│       │   └── xp_continuous_test.csv
│       └── __init__.py
├── examples
│   └── tutorial.ipynb
├── LICENSE
├── README.md
├── pyproject.toml
└── uv.lock


```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/malhotrasagar15/xp-teal.git
   cd xp-teal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


---

## 🚀 Usage

### Download XP spectra
```bash
python Codes/download_xp_spectra.py
```

### Run the main analysis pipeline
```bash
python Codes/main.py
```

or use the provided **Jupyter notebook**:
```bash
jupyter notebook examples/tutorial.ipynb
```

---

## 🧠 Features

- **Automated XP Spectra Downloading** via ESA Gaia Archive (`astroquery`)
- **Equivalent Width and Line Analysis**
- **Mathematical Utilities** for spectral modeling
- **Configurable Pipeline** via modular scripts
- **Example Data** for quick testing and reproducibility

---

## 🧩 Dependencies

Core Python packages:
- `numpy`, `scipy`, `pandas`, `joblib`, `xml.etree.ElementTree`
- `astroquery`, 

---

## 📄 License

GNU GENERAL PUBLIC LICENSE

---

