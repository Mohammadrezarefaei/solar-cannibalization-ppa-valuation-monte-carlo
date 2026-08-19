"""PPA Valuation, Capture Rate Discount, and Monte Carlo Cashflow-at-Risk Engine."""

from typing import Dict
import numpy as np


class PPAEngine:

  def __init__(
      self,
      capacity_mw: float = 20.0,
      annual_yield_mwh_per_mw: float = 1050.0,
      opex_per_mw_year: float = 12000.0,
  ):
    self.capacity_mw = capacity_mw
    self.annual_yield = annual_yield_mwh_per_mw
    self.opex_annual = opex_per_mw_year * capacity_mw
    self.annual_generation_mwh = self.capacity_mw * self.annual_yield

  def calculate_capture_price(
      self, baseload_price_eur: float, capture_rate_factor: float
  ) -> float:
    """Calculates realized asset revenue price after solar/wind cannibalization discount."""
    return round(baseload_price_eur * capture_rate_factor, 2)

  def evaluate_ppa_vs_merchant(
      self,
      baseload_price_eur: float,
      capture_rate_factor: float,
      ppa_strike_price_eur: float,
      ppa_volume_share: float = 0.70,
  ) -> Dict[str, float]:
    """Computes revenue split between fixed PPA structure and merchant wholesale exposure."""
    capture_price = self.calculate_capture_price(
        baseload_price_eur, capture_rate_factor
    )

    ppa_mwh = self.annual_generation_mwh * ppa_volume_share
    merchant_mwh = self.annual_generation_mwh * (1.0 - ppa_volume_share)

    ppa_rev = ppa_mwh * ppa_strike_price_eur
    merchant_rev = merchant_mwh * capture_price
    total_rev = ppa_rev + merchant_rev
    net_ebitda = total_rev - self.opex_annual

    return {
        "annual_generation_mwh": round(self.annual_generation_mwh, 2),
        "realized_capture_price": capture_price,
        "ppa_revenue_eur": round(ppa_rev, 2),
        "merchant_revenue_eur": round(merchant_rev, 2),
        "total_revenue_eur": round(total_rev, 2),
        "net_ebitda_eur": round(net_ebitda, 2),
    }

  def run_monte_carlo_cfar(
      self,
      base_ppa_strike: float,
      baseload_mean: float = 75.0,
      baseload_std: float = 18.0,
      capture_factor_mean: float = 0.78,
      capture_factor_std: float = 0.08,
      ppa_volume_share: float = 0.70,
      n_simulations: int = 2000,
  ) -> Dict[str, float]:
    """Performs Monte Carlo simulation to calculate P90 / P50 Cashflow-at-Risk (CFaR)."""
    np.random.seed(42)
    sim_baseload = np.random.normal(baseload_mean, baseload_std, n_simulations)
    sim_capture = np.random.normal(
        capture_factor_mean, capture_factor_std, n_simulations
    )
    sim_capture = np.clip(sim_capture, 0.40, 1.05)

    sim_realized_price = sim_baseload * sim_capture

    ppa_mwh = self.annual_generation_mwh * ppa_volume_share
    merchant_mwh = self.annual_generation_mwh * (1.0 - ppa_volume_share)

    sim_ebitda = (
        (ppa_mwh * base_ppa_strike)
        + (merchant_mwh * sim_realized_price)
        - self.opex_annual
    )

    p90_ebitda = np.percentile(sim_ebitda, 10)  # Conservative bankable case
    p50_ebitda = np.percentile(sim_ebitda, 50)  # Expected base case

    return {
        "ebitda_p90_eur": round(float(p90_ebitda), 2),
        "ebitda_p50_eur": round(float(p50_ebitda), 2),
        "ebitda_min_eur": round(float(np.min(sim_ebitda)), 2),
        "ebitda_max_eur": round(float(np.max(sim_ebitda)), 2),
    }
