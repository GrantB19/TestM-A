"""Fonctions financières pures (sans dépendance Streamlit) utilisées par les cours et les laboratoires."""
from __future__ import annotations


def annuity_factor(rate: float, n: int) -> float:
    return n if rate == 0 else (1 - (1 + rate) ** -n) / rate


def npv(rate: float, cashflows: list[float]) -> float:
    """cashflows[0] est le flux à t=0 (investissement négatif)."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows: list[float], lo: float = -0.95, hi: float = 5.0, tol: float = 1e-7) -> float | None:
    f_lo, f_hi = npv(lo, cashflows), npv(hi, cashflows)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = npv(mid, cashflows)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def payback(cashflows: list[float]) -> float | None:
    cum = 0.0
    for t, cf in enumerate(cashflows):
        prev = cum
        cum += cf
        if cum >= 0 and t > 0:
            return (t - 1) + (-prev / cf if cf else 0)
    return None


def cagr(start: float, end: float, years: float) -> float:
    return (end / start) ** (1 / years) - 1


def ev_to_equity(ev: float, net_debt: float, debt_like: float = 0.0, non_operating: float = 0.0) -> float:
    return ev - net_debt - debt_like + non_operating


def dcf(fcf1: float, growth: float, wacc: float, terminal_growth: float, years: int = 5) -> dict:
    flows = [fcf1 * (1 + growth) ** t for t in range(years)]
    pv_flows = [f / (1 + wacc) ** (t + 1) for t, f in enumerate(flows)]
    tv = flows[-1] * (1 + terminal_growth) / (wacc - terminal_growth) if wacc > terminal_growth else float("nan")
    pv_tv = tv / (1 + wacc) ** years
    ev = sum(pv_flows) + pv_tv
    return {"flows": flows, "pv_flows": pv_flows, "tv": tv, "pv_tv": pv_tv, "ev": ev,
            "tv_share": pv_tv / ev if ev else float("nan")}


def synergy_net_value(run_rate: float, multiple: float, execution_risk: float, one_off_costs: float) -> float:
    """Valeur nette simplifiée des synergies = run-rate capitalisé x (1 - risque) - coûts one-off."""
    return run_rate * multiple * (1 - execution_risk) - one_off_costs


def weighted_score(weights: list[float], scores: list[float]) -> float:
    total_w = sum(weights) or 1
    return sum(w * s for w, s in zip(weights, scores)) / total_w


def fcf(ebitda: float, cash_tax: float, delta_wc: float, capex: float) -> float:
    return ebitda - cash_tax - delta_wc - capex


def fmt(x: float, digits: int = 1, unit: str = "") -> str:
    if x is None or x != x:
        return "n.d."
    s = f"{x:,.{digits}f}".replace(",", " ").replace(".", ",")
    return f"{s} {unit}".strip()
