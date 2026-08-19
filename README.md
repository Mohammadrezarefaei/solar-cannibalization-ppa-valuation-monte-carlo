# ☀️ Solar & Wind PPA Valuation & Cannibalization Risk Model

[![PPA Engine CI](https://github.com/Mohammadrezarefaei/solar-cannibalization-ppa-valuation-monte-carlo/actions/workflows/ci.yml/badge.svg)](https://github.com/Mohammadrezarefaei/solar-cannibalization-ppa-valuation-monte-carlo/actions)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://solar-cannibalization-ppa-valuation-monte-carlo-grwsbkxraezhef.streamlit.app/)

A quantitative risk-management and valuation framework for structuring **Renewable Power Purchase Agreements (PPAs)** and calculating **Solar/Wind Capture Price Discounts (Cannibalization Effect)** with **Monte Carlo Cashflow-at-Risk (CFaR)** in the German electricity market.

---

## 🚀 Live Interactive Demo
👉 **[Access the Live Streamlit Web App](https://solar-cannibalization-ppa-valuation-monte-carlo-grwsbkxraezhef.streamlit.app/)**

---

## 📌 Financial Structuring & Market Mechanics

As renewable penetration increases, the merit-order effect compresses power prices during peak solar generation hours:
* **Capture Price Formulation:**
  $$\text{Realized Capture Price} = \text{Baseload Price} \times \text{Capture Factor}$$
* **Revenue Stacking (PPA + Merchant Tail):**
  $$\text{Total Revenue} = (V_{\text{PPA}} \times P_{\text{Strike}}) + (V_{\text{Merchant}} \times P_{\text{Capture}})$$
* **Monte Carlo CFaR ($N = 2,500$ simulations):** Evaluates P90 (conservative bankable debt-service case) vs. P50 (expected base-case) annual EBITDA under wholesale price and capture factor volatility.

---

## 🔍 Model Validation & Regime Boundary Analysis

The model was validated against historical German wholesale market spread dynamics:
* **High Cannibalization Scenario (Solar Boom):** Capture rates drop to $50-60\%$, highlighting severe merchant downside risk without hedging.
* **Hedge Optimization:** A $70\%$ PPA volume hedge stabilizes the P90 cashflow floor above minimum debt-service covenants.
* **Limitation:** Assumes unconstrained local grid evacuation; real-world revenue may face additional redispatch/curtailment depending on transmission network congestion.

---

## 🛠️ Software Architecture & Automated Testing
* **CI/CD Pipeline:** Fully automated testing via **GitHub Actions** (`pytest` suite validating capture rates, hybrid PPA revenue logic, and Monte Carlo P90/P50 percentiles).
* **Modular Core Engine:** Located in `src/ppa_engine.py`.
* **Tech Stack:** Python 3.11, NumPy, Pandas, Matplotlib, Streamlit, Pytest.
