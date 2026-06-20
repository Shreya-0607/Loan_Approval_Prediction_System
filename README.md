# 🏦 Loan Approval Prediction System — "Lumina Predict"
### AIML Summer Internship 2026 · IIHMF, MNNIT Allahabad, Prayagraj

---

## 📁 Folder Structure (Submit as ZIP)

```
LoanApprovalPrediction_YourName/
│
├── Dataset/
│   └── train_u6lujuX_CVtuZ9i.csv
│
├── Notebook/
│   └── LoanApprovalPrediction.ipynb
│
├── Model/
│   ├── loan_model.pkl
│   ├── scaler.pkl
│   ├── selector.pkl
│   └── feature_names.json
│
├── Streamlit_App/
│   ├── app.py
│   ├── requirements.txt
│   └── .streamlit/
│       └── config.toml          ⚠️ REQUIRED — sets the dark theme
│
├── Documentation/
│   └── ProjectReport.pdf
│
└── README.md          ← this file
```

> ⚠️ **Don't forget the `.streamlit/config.toml` file!** It's what makes Streamlit's
> native widgets (slider thumbs, focus rings, etc.) use the blue Lumina Predict
> theme instead of Streamlit's default red. It's a hidden folder — make sure your
> zip/GitHub upload includes it.

---

## 🎨 Design — "Lumina Predict"

This app is a faithful Streamlit recreation of the **Lumina Predict** design system —
a dark, glassmorphism fintech aesthetic with:
- Sidebar navigation (Personal Info / Financials / Property / Result anchors)
- Sticky-style top header bar with brand + nav links
- Glass-card hero banner and slider containers
- Custom-styled sliders, pill-toggle radio buttons, and gradient buttons
- Green/red themed result cards for Approved/Rejected outcomes

---

## 🚀 Step-by-Step Workflow

### STEP 1 — Run the Colab Notebook
1. Open `LoanApprovalPrediction.ipynb` in Google Colab
2. `Runtime → Run All`
3. Upload `archive__1_.zip` (the Kaggle Loan Prediction dataset) when prompted
4. After completion, **download** these 4 files:
   - `loan_model.pkl`
   - `scaler.pkl`
   - `selector.pkl`
   - `feature_names.json`

### STEP 2 — Test Streamlit Locally (Optional)
```bash
pip install -r requirements.txt
# Place loan_model.pkl, scaler.pkl, selector.pkl, feature_names.json
# in the same folder as app.py
streamlit run app.py
```

### STEP 3 — Deploy on Streamlit Cloud
1. Create a GitHub repository (e.g. `loan-approval-predictor`)
2. Upload to the repo root, **including the hidden `.streamlit` folder**:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `loan_model.pkl`
   - `scaler.pkl`
   - `selector.pkl`
   - `feature_names.json`
3. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
4. Connect your repo → set **Main file path:** `app.py`
5. Click **Deploy**

---

## 🤖 Models Trained (6 Total)

| Model               | Type              |
|---------------------|-------------------|
| Logistic Regression | Linear Classifier |
| Decision Tree       | Tree-based        |
| Random Forest       | Ensemble (Bagging)|
| SVM                 | Kernel-based      |
| KNN                 | Instance-based    |
| **XGBoost**          | Ensemble (Boosting) — *new* |

---

## 📊 Evaluation Metrics Used

| Metric     | Why Used                              |
|------------|----------------------------------------|
| Accuracy   | Overall correctness                    |
| Precision  | Of predicted approved, how many were   |
| Recall     | Of actual approved, how many found     |
| F1 Score   | Balance of Precision & Recall          |
| ROC-AUC    | Model's ability to distinguish classes |

---

## 🔧 Pipeline (Important for Debugging)

The notebook's actual processing order is **SELECT → SCALE**, not the other way:

```
encode 11 engineered features
        ↓
SelectKBest.transform()   → 11 → 8   (picks the 8 best by chi2)
        ↓
StandardScaler.transform() → 8 → 8   (scaler was fit AFTER selection)
        ↓
model.predict()
```

`app.py` already mirrors this exact order — if you ever rebuild the notebook
yourself, keep this order or the deployed app will throw a feature-mismatch error.

---

## 📋 Submission Checklist

- [ ] Source Code ZIP named: `LoanApprovalPrediction_YourName.zip`
- [ ] Project Report (15–25 pages, PDF)
- [ ] Presentation (10–15 slides, PPT/PDF)
- [ ] Dataset included
- [ ] Streamlit deployment link
- [ ] `.streamlit/config.toml` included in the repo (don't forget the hidden folder!)

---

## 👥 Team

- Member 1: [Your Name]
- Member 2: [Partner Name]

**Submission Format:** `LoanApprovalPrediction_[TeamLeaderName].zip`
