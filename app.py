"""Streamlit App: Renewable PPA Valuation & Cannibalization Risk Model."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="PPA Valuation & Cannibalization Analyzer",
    page_icon="☀️",
    layout="wide",
)

st.title("☀️ Solar & Wind PPA Pricing & Cannibalization Risk Model")
st.markdown(
    "Quantitative structuring tool for **Power Purchase Agreements (PPA), Solar"
    " Capture Price Discounting, and Monte Carlo Cashflow-at-Risk (CFaR)** in"
    " Germany."
)

st.sidebar.header("⚙️ Asset Technical Parameters")
plant_capacity_mw = st.sidebar.slider("Installed Capacity (MWp)", 5.0, 100.0, 20.0, 5.0)
yield_spec = st.sidebar.slider(
    "Specific Yield (Full Load Hours / MWh/MW)", 850.0, 1400.0, 1050.0, 25.0
)
opex_mw_year = st.sidebar.slider(
    "OPEX + Land Lease (€/MW/year)", 6000.0, 20000.0, 12000.0, 500.0
)

st.sidebar.header("💶 Market & Contract Structuring")
baseload_price = st.sidebar.slider(
    "Expected Market Baseload (€/MWh)", 40.0, 140.0, 75.0, 2.5
)
capture_rate_pct = st.sidebar.slider(
    "Solar/Wind Capture Rate Factor (%)", 40, 100, 78, 2
)
ppa_strike = st.sidebar.slider(
    "Fixed PPA Strike Price (€/MWh)", 40.0, 110.0, 62.0, 1.0
)
ppa_hedge_share = (
    st.sidebar.slider("Hedged PPA Volume Share (%)", 0, 100, 70, 5) / 100.0
)

# Engine calculations
annual_mwh = plant_capacity_mw * yield_spec
annual_opex = plant_capacity_mw * opex_mw_year

capture_price = baseload_price * (capture_rate_pct / 100.0)
ppa_mwh = annual_mwh * ppa_hedge_share
merchant_mwh = annual_mwh * (1.0 - ppa_hedge_share)

ppa_rev = ppa_mwh * ppa_strike
merchant_rev = merchant_mwh * capture_price
total_rev = ppa_rev + merchant_rev
net_ebitda = total_rev - annual_opex

col1, col2 = st.columns([2, 1])

with col1:
  st.subheader("📈 Monte Carlo Cashflow-at-Risk (CFaR) Distribution")

  np.random.seed(42)
  sim_baseload = np.random.normal(baseload_price, 15.0, 2500)
  sim_capture = np.random.normal(capture_rate_pct / 100.0, 0.07, 2500)
  sim_capture = np.clip(sim_capture, 0.40, 1.05)

  sim_realized = sim_baseload * sim_capture
  sim_ebitda_arr = (
      (ppa_mwh * ppa_strike) + (merchant_mwh * sim_realized) - annual_opex
  ) / 1000.0  # kEUR

  p90_k = np.percentile(sim_ebitda_arr, 10)
  p50_k = np.percentile(sim_ebitda_arr, 50)

  fig, ax = plt.subplots(figsize=(9, 4.5))
  ax.hist(
      sim_ebitda_arr,
      bins=40,
      color="#3B82F6",
      edgecolor="black",
      alpha=0.75,
      density=True,
  )
  ax.axvline(
      p90_k,
      color="#EF4444",
      linestyle="--",
      linewidth=2.2,
      label=f"P90 Bankable Case: €{p90_k:,.0f}k",
  )
  ax.axvline(
      p50_k,
      color="#10B981",
      linestyle="-",
      linewidth=2.2,
      label=f"P50 Base Case: €{p50_k:,.0f}k",
  )
  ax.set_xlabel("Annual Net EBITDA [k€ / year]", fontweight="bold")
  ax.set_ylabel("Probability Density", fontweight="bold")
  ax.grid(axis="x", linestyle=":", alpha=0.6)
  ax.legend(frameon=True, loc="upper right")

  st.pyplot(fig)

with col2:
  st.subheader("📊 Financial Structuring Metrics")
  st.metric(
      label="Realized Capture Price",
      value=f"€{capture_price:.2f} / MWh",
      delta=f"{(capture_rate_pct - 100):.1f}% Cannibalization Discount",
  )
  st.metric(
      label="Expected Net Annual EBITDA",
      value=f"€{net_ebitda/1000:,.1f} k / yr",
      delta="Post-OPEX Cashflow",
  )
  st.metric(
      label="P90 Debt-Service Cashflow (10th percentile)",
      value=f"€{p90_k:,.1f} k / yr",
      delta="Bankable Threshold",
  )

st.markdown("---")
st.caption(
    "Modelled for German utility-scale solar PV & onshore wind assets with"
    " merchant-tail PPA contracts."
)
