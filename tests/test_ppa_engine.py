"""Automated Pytest Suite for PPA Valuation Engine."""

import pytest
from src.ppa_engine import PPAEngine


def test_capture_price_discount():
  engine = PPAEngine(capacity_mw=10.0, annual_yield_mwh_per_mw=1000.0)
  # Baseload = €80/MWh, Capture factor = 0.75 -> Realized = €60/MWh
  cap_price = engine.calculate_capture_price(
      baseload_price_eur=80.0, capture_rate_factor=0.75
  )
  assert cap_price == 60.0


def test_ppa_hedging_revenue():
  # 10 MW * 1000 h = 10,000 MWh
  engine = PPAEngine(
      capacity_mw=10.0, annual_yield_mwh_per_mw=1000.0, opex_per_mw_year=10000.0
  )
  # 70% PPA @ €65/MWh (7,000 MWh = €455,000)
  # 30% Merchant @ €50/MWh (3,000 MWh = €150,000)
  # Total Rev = €605,000 | OPEX = €100,000 | Net EBITDA = €505,000
  res = engine.evaluate_ppa_vs_merchant(
      baseload_price_eur=100.0,
      capture_rate_factor=0.50,
      ppa_strike_price_eur=65.0,
      ppa_volume_share=0.70,
  )
  assert res["total_revenue_eur"] == 605000.0
  assert res["net_ebitda_eur"] == 505000.0


def test_monte_carlo_p90_under_p50():
  engine = PPAEngine(capacity_mw=10.0)
  res = engine.run_monte_carlo_cfar(
      base_ppa_strike=60.0, ppa_volume_share=0.70, n_simulations=500
  )
  assert res["ebitda_p90_eur"] <= res["ebitda_p50_eur"]
  assert res["ebitda_min_eur"] <= res["ebitda_p90_eur"]
