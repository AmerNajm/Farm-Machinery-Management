# 🧰 Farm Calibration Toolkit (Streamlit)

A simple, non-technical Streamlit app (metric units) with **tabs** for:
1) **Sprayer calibration** (application rate in L/ha + tank planning)
2) **Seeder calibration** (weight-based kg/ha + population-based seeds/ha)
3) **Quick fuel & field capacity** (optional planning)

---

## Files
- `tractor_app.py` (the Streamlit app)
- `requirements.txt`

---

## Deploy online (no local installation) — Streamlit Cloud

### 1) Create a GitHub repository
1. Go to https://github.com → **New repository**
2. Upload these files:
   - `tractor_app.py`
   - `requirements.txt`
   - (optional) `logo.png`
3. Commit changes

### 2) Deploy on Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click **New App**
4. Select your repository and branch
5. **Main file path**: `tractor_app.py`
6. Click **Deploy**

### 3) Add logo (optional)
- Put `logo.png` in the repo root.
- In the app, users can also upload a logo using the sidebar uploader.

---

## Troubleshooting
- **ModuleNotFoundError**: confirm all packages are listed in `requirements.txt`.
- **App stuck installing**: check spelling/case in `requirements.txt`.
- **Excel download not working**: ensure `xlsxwriter` is included.

---

## Notes (Formulas used)
- **Sprayer rate (L/ha)**: `600 × Q(L/min) ÷ [Speed(km/h) × spacing(m)]` (or swath width)
- **Seeder (kg/ha)**: `kg collected ÷ area tested (ha)`; area tested = `circumference × width × rev ÷ 10,000`
- **Population**: `seeds per meter = seeds/ha × row spacing ÷ 10,000`
