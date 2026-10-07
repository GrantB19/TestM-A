"""Laboratoires interactifs : simulateurs financiers et stratégiques."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from finance import dcf, ev_to_equity, irr, npv, payback, synergy_net_value, fmt

C_INK, C_YEL, C_GREY, C_OK, C_KO = "#1A1A24", "#F2C500", "#9A9AA3", "#2E7D5B", "#B3392F"


def _layout(fig: go.Figure, height: int = 340, title: str | None = None) -> go.Figure:
    fig.update_layout(height=height, title=title, margin=dict(l=10, r=10, t=50 if title else 20, b=10),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color=C_INK, size=13),
                      legend=dict(orientation="h", y=-0.2))
    fig.update_xaxes(gridcolor="#EDEDE6")
    fig.update_yaxes(gridcolor="#EDEDE6")
    return fig


def _num(label, key, value, min_value=0.0, max_value=100000.0, step=1.0, fmt_str="%.2f", help=None):
    return st.number_input(label, min_value=float(min_value), max_value=float(max_value), value=float(value),
                           step=float(step), key=key, format=fmt_str, help=help)


def lab_valuation():
    st.markdown("**Du multiple à l'Equity Value** – modifiez les hypothèses, le pont et la sensibilité se recalculent.")
    c = st.columns(5)
    with c[0]: ebitda = _num("EBITDA normalisé (M€)", "v_ebitda", 15.0, 0.0, 5000.0, 0.5, "%.1f")
    with c[1]: mult = _num("Multiple EV/EBITDA (x)", "v_mult", 8.0, 1.0, 40.0, 0.5, "%.1f")
    with c[2]: debt = _num("Dette nette (M€)", "v_debt", 35.0, 0.0, 5000.0, 1.0, "%.1f")
    with c[3]: dlike = _num("Passifs assimilés dette (M€)", "v_dlike", 4.0, 0.0, 5000.0, 1.0, "%.1f")
    with c[4]: nonop = _num("Actifs non opérationnels (M€)", "v_nonop", 2.0, 0.0, 5000.0, 1.0, "%.1f")
    ev = ebitda * mult
    eq = ev_to_equity(ev, debt, dlike, nonop)
    m = st.columns(3)
    m[0].metric("Enterprise Value", fmt(ev, 1, "M€"))
    m[1].metric("Equity Value", fmt(eq, 1, "M€"))
    m[2].metric("Dette & assimilés / EV", fmt((debt + dlike) / ev * 100 if ev else 0, 0, "%"))

    wf = go.Figure(go.Waterfall(
        x=["EV", "Dette nette", "Passifs assimilés", "Actifs non op.", "Equity Value"],
        measure=["absolute", "relative", "relative", "relative", "total"],
        y=[ev, -debt, -dlike, nonop, 0],
        text=[fmt(v, 1) for v in [ev, -debt, -dlike, nonop, eq]], textposition="outside",
        increasing=dict(marker=dict(color=C_OK)), decreasing=dict(marker=dict(color=C_KO)),
        totals=dict(marker=dict(color=C_INK)), connector=dict(line=dict(color=C_GREY))))
    st.plotly_chart(_layout(wf, 330, "Pont EV → Equity Value (M€)"))

    mults = np.arange(max(2.0, mult - 3), mult + 3.01, 1.0)
    df = pd.DataFrame({"Multiple": [f"{x:.1f}x" for x in mults], "EV (M€)": ebitda * mults,
                       "Equity (M€)": [ev_to_equity(ebitda * x, debt, dlike, nonop) for x in mults]})
    bar = go.Figure(go.Bar(x=df["Multiple"], y=df["Equity (M€)"], marker_color=[C_YEL if abs(x - mult) < 1e-9 else "#D8D8CF" for x in mults],
                           text=[fmt(v, 0) for v in df["Equity (M€)"]], textposition="outside"))
    st.plotly_chart(_layout(bar, 300, "Sensibilité de l'Equity Value au multiple"))
    st.dataframe(df.style.format({"EV (M€)": "{:.1f}", "Equity (M€)": "{:.1f}"}), hide_index=True)


def lab_dcf():
    st.markdown("**DCF sur 5 ans** avec valeur terminale (Gordon-Shapiro) et matrice de sensibilité WACC × croissance terminale.")
    c = st.columns(4)
    with c[0]: f1 = _num("FCF année 1 (M€)", "d_f1", 10.0, 0.0, 5000.0, 0.5, "%.1f")
    with c[1]: g = _num("Croissance du FCF (%/an)", "d_g", 5.0, -20.0, 40.0, 0.5, "%.1f") / 100
    with c[2]: w = _num("WACC (%)", "d_w", 9.0, 3.0, 25.0, 0.5, "%.1f") / 100
    with c[3]: tg = _num("Croissance terminale (%)", "d_tg", 2.0, 0.0, 6.0, 0.25, "%.2f") / 100
    if w <= tg:
        st.error("Le WACC doit être supérieur à la croissance terminale.")
        return
    r = dcf(f1, g, w, tg, 5)
    m = st.columns(4)
    m[0].metric("EV (DCF)", fmt(r["ev"], 1, "M€"))
    m[1].metric("PV des flux explicites", fmt(sum(r["pv_flows"]), 1, "M€"))
    m[2].metric("PV valeur terminale", fmt(r["pv_tv"], 1, "M€"))
    m[3].metric("Poids de la VT dans l'EV", fmt(r["tv_share"] * 100, 0, "%"))
    if r["tv_share"] > 0.8:
        st.warning("La valeur terminale pèse plus de 80 % de l'EV : challengez le FCF normatif et la croissance terminale.")

    fig = go.Figure()
    fig.add_bar(x=[f"A{i}" for i in range(1, 6)], y=r["pv_flows"], name="PV des flux", marker_color=C_INK)
    fig.add_bar(x=["Valeur terminale"], y=[r["pv_tv"]], name="PV valeur terminale", marker_color=C_YEL)
    st.plotly_chart(_layout(fig, 320, "Décomposition de la valeur actualisée (M€)"))

    ws = [w + d for d in (-0.02, -0.01, 0, 0.01, 0.02)]
    gs = [max(0.0, tg + d) for d in (-0.01, -0.005, 0, 0.005, 0.01)]
    z = [[dcf(f1, g, ww, gg, 5)["ev"] if ww > gg else np.nan for gg in gs] for ww in ws]
    hm = go.Figure(go.Heatmap(z=z, x=[f"{x*100:.2f} %" for x in gs], y=[f"{x*100:.1f} %" for x in ws],
                              text=[[fmt(v, 0) for v in row] for row in z], texttemplate="%{text}",
                              colorscale=[[0, "#FFF7B0"], [1, C_YEL]], showscale=False))
    hm.update_xaxes(title="Croissance terminale")
    hm.update_yaxes(title="WACC")
    st.plotly_chart(_layout(hm, 330, "Sensibilité de l'EV (M€)"))
    tbl = pd.DataFrame({"Année": [f"A{i}" for i in range(1, 6)], "FCF": r["flows"], "FCF actualisé": r["pv_flows"]})
    st.dataframe(tbl.style.format({"FCF": "{:.2f}", "FCF actualisé": "{:.2f}"}), hide_index=True)


def lab_npv():
    st.markdown("**Comparer deux projets** : VAN, TRI, payback et indice de profitabilité.")
    with st.columns(4)[0]:
        w = _num("WACC (%)", "n_w", 9.0, 0.0, 25.0, 0.5, "%.1f") / 100
    ca, cb = st.columns(2)
    with ca:
        st.markdown("##### Projet A")
        ia = _num("Investissement (M€)", "n_ia", 3.0, 0.1, 10000.0, 0.1, "%.2f")
        fa = _num("FCF annuel (M€)", "n_fa", 0.9, 0.0, 10000.0, 0.05, "%.2f")
        na = int(_num("Durée (années)", "n_na", 5, 1, 20, 1, "%.0f"))
    with cb:
        st.markdown("##### Projet B")
        ib = _num("Investissement (M€)", "n_ib", 5.0, 0.1, 10000.0, 0.1, "%.2f")
        fb = _num("FCF annuel (M€)", "n_fb", 1.35, 0.0, 10000.0, 0.05, "%.2f")
        nb = int(_num("Durée (années)", "n_nb", 5, 1, 20, 1, "%.0f"))
    cfa, cfb = [-ia] + [fa] * na, [-ib] + [fb] * nb
    rows = []
    for name, cf, inv in (("Projet A", cfa, ia), ("Projet B", cfb, ib)):
        van = npv(w, cf)
        tri = irr(cf)
        pb = payback(cf)
        rows.append({"Projet": name, "VAN (M€)": van, "TRI (%)": tri * 100 if tri is not None else np.nan,
                     "Payback (ans)": pb if pb is not None else np.nan, "Indice de profitabilité": van / inv})
    df = pd.DataFrame(rows)
    st.dataframe(df.style.format({"VAN (M€)": "{:.2f}", "TRI (%)": "{:.1f}", "Payback (ans)": "{:.1f}", "Indice de profitabilité": "{:.2f}"}),
                 hide_index=True)
    best = df.sort_values("VAN (M€)", ascending=False).iloc[0]
    st.success(f"**{best['Projet']}** crée le plus de valeur (VAN = {best['VAN (M€)']:.2f} M€). Vérifiez ensuite l'indice de profitabilité si le capital est rationné et les risques non financiers.")
    fig = go.Figure()
    for name, cf, colr in (("Projet A", cfa, C_INK), ("Projet B", cfb, C_YEL)):
        fig.add_scatter(x=list(range(len(cf))), y=np.cumsum(cf), mode="lines+markers", name=name, line=dict(color=colr, width=3))
    fig.add_hline(y=0, line_dash="dot", line_color=C_GREY)
    fig.update_xaxes(title="Année")
    fig.update_yaxes(title="Cash-flow cumulé (M€, non actualisé)")
    st.plotly_chart(_layout(fig, 320, "Cash-flows cumulés"))


BP_PRESETS = {
    "Base": dict(clients=10.0, growth=50.0, arpu=120.0, gm=70.0, fixed=1.2, capex=0.3, wc=15.0),
    "Upside": dict(clients=12.0, growth=65.0, arpu=130.0, gm=72.0, fixed=1.3, capex=0.35, wc=15.0),
    "Downside": dict(clients=8.0, growth=30.0, arpu=105.0, gm=66.0, fixed=1.2, capex=0.3, wc=18.0),
}


def bp_model(p: dict, wacc: float, years: int = 5) -> dict:
    clients = [p["clients"] * (1 + p["growth"] / 100) ** t for t in range(years)]
    rev = [c * p["arpu"] / 1000 for c in clients]
    gross = [r * p["gm"] / 100 for r in rev]
    ebitda = [g - p["fixed"] * (1.03 ** t) for t, g in enumerate(gross)]
    tax = [max(e, 0) * 0.25 for e in ebitda]
    d_wc = [(rev[t] - (rev[t - 1] if t else 0)) * p["wc"] / 100 for t in range(years)]
    capex = [p["capex"]] * years
    fcf = [e - tx - dw - cx for e, tx, dw, cx in zip(ebitda, tax, d_wc, capex)]
    van = sum(f / (1 + wacc) ** (t + 1) for t, f in enumerate(fcf))
    return dict(clients=clients, rev=rev, ebitda=ebitda, fcf=fcf, npv=van)


def lab_bp():
    st.markdown("**Business plan piloté par des drivers** – 3 scénarios et diagramme tornado des sensibilités (impôt cash simplifié = 25 % de l'EBITDA positif ; coûts fixes +3 %/an).")
    top = st.columns([1, 1])
    scen = top[0].radio("Scénario", list(BP_PRESETS), horizontal=True, key="bp_scen")
    wacc = top[1].number_input("WACC (%)", 3.0, 25.0, 10.0, 0.5, key="bp_wacc") / 100
    pr = BP_PRESETS[scen]
    c = st.columns(4)
    p = {}
    with c[0]:
        p["clients"] = _num("Clients année 1", f"bp_cl_{scen}", pr["clients"], 1, 10000, 1, "%.0f")
        p["growth"] = _num("Croissance clients (%/an)", f"bp_g_{scen}", pr["growth"], -50, 300, 5, "%.0f")
    with c[1]:
        p["arpu"] = _num("Revenu moyen / client (k€)", f"bp_a_{scen}", pr["arpu"], 1, 5000, 5, "%.0f")
        p["gm"] = _num("Marge brute (%)", f"bp_gm_{scen}", pr["gm"], 10, 100, 1, "%.0f")
    with c[2]:
        p["fixed"] = _num("Coûts fixes année 1 (M€)", f"bp_f_{scen}", pr["fixed"], 0, 1000, 0.1, "%.2f")
        p["capex"] = _num("Capex annuel (M€)", f"bp_c_{scen}", pr["capex"], 0, 1000, 0.05, "%.2f")
    with c[3]:
        p["wc"] = _num("BFR (% de la variation de CA)", f"bp_w_{scen}", pr["wc"], 0, 100, 1, "%.0f")
    r = bp_model(p, wacc)
    m = st.columns(4)
    m[0].metric("CA année 5", fmt(r["rev"][-1], 2, "M€"))
    m[1].metric("EBITDA année 5", fmt(r["ebitda"][-1], 2, "M€"))
    m[2].metric("FCF cumulé 5 ans", fmt(sum(r["fcf"]), 2, "M€"))
    m[3].metric("VAN des FCF (5 ans)", fmt(r["npv"], 2, "M€"))
    yrs = [f"A{i}" for i in range(1, 6)]
    fig = go.Figure()
    fig.add_bar(x=yrs, y=r["rev"], name="CA", marker_color="#D8D8CF")
    fig.add_bar(x=yrs, y=r["ebitda"], name="EBITDA", marker_color=C_INK)
    fig.add_scatter(x=yrs, y=r["fcf"], name="FCF", mode="lines+markers", line=dict(color=C_YEL, width=4))
    fig.update_layout(barmode="group")
    st.plotly_chart(_layout(fig, 320, f"Trajectoire – scénario {scen} (M€)"))

    base = r["npv"]
    labels = {"clients": "Clients année 1", "growth": "Croissance clients", "arpu": "Revenu moyen", "gm": "Marge brute", "fixed": "Coûts fixes", "capex": "Capex", "wc": "BFR"}
    rows = []
    for k, lab in labels.items():
        lo = bp_model({**p, k: p[k] * 0.8}, wacc)["npv"] - base
        hi = bp_model({**p, k: p[k] * 1.2}, wacc)["npv"] - base
        rows.append((lab, lo, hi, max(abs(lo), abs(hi))))
    rows.sort(key=lambda x: x[3])
    t = go.Figure()
    t.add_bar(y=[x[0] for x in rows], x=[x[1] for x in rows], orientation="h", name="−20 %", marker_color=C_KO)
    t.add_bar(y=[x[0] for x in rows], x=[x[2] for x in rows], orientation="h", name="+20 %", marker_color=C_OK)
    t.update_layout(barmode="overlay")
    t.update_xaxes(title="Écart de VAN vs base (M€)")
    st.plotly_chart(_layout(t, 340, "Tornado : impact d'une variation de ±20 % de chaque hypothèse"))
    st.info(f"Hypothèse la plus sensible : **{rows[-1][0]}**. C'est sur elle que doit se concentrer le débat avec la BU.")


def lab_synergies():
    st.markdown("**Prix plafond d'une acquisition** : valeur autonome + quote-part des synergies nettes (approche simplifiée).")
    c = st.columns(3)
    with c[0]:
        ev0 = _num("EV autonome de la cible (M€)", "s_ev", 120.0, 1.0, 100000.0, 5.0, "%.1f")
        run = _num("Synergies run-rate (M€/an)", "s_run", 8.0, 0.0, 10000.0, 0.5, "%.1f")
    with c[1]:
        mult = _num("Multiple de capitalisation (x)", "s_mult", 7.0, 1.0, 30.0, 0.5, "%.1f")
        risk = _num("Risque d'exécution (%)", "s_risk", 30.0, 0.0, 100.0, 5.0, "%.0f") / 100
    with c[2]:
        cost = _num("Coûts one-off d'intégration (M€)", "s_cost", 18.0, 0.0, 10000.0, 1.0, "%.1f")
        share = _num("Part des synergies cédée au vendeur (%)", "s_share", 50.0, 0.0, 100.0, 5.0, "%.0f") / 100
    net = synergy_net_value(run, mult, risk, cost)
    ceil = ev0 + share * max(net, 0)
    m = st.columns(4)
    m[0].metric("Synergies brutes capitalisées", fmt(run * mult, 1, "M€"))
    m[1].metric("Valeur nette des synergies", fmt(net, 1, "M€"))
    m[2].metric("Prix plafond", fmt(ceil, 1, "M€"))
    m[3].metric("Valeur conservée par l'acheteur", fmt((1 - share) * max(net, 0), 1, "M€"))
    if net <= 0:
        st.warning("Les synergies nettes sont négatives : aucune prime ne se justifie par les synergies.")
    wf = go.Figure(go.Waterfall(x=["Synergies capitalisées", "Risque d'exécution", "Coûts one-off", "Valeur nette"],
                                measure=["absolute", "relative", "relative", "total"],
                                y=[run * mult, -run * mult * risk, -cost, 0],
                                text=[fmt(v, 1) for v in [run * mult, -run * mult * risk, -cost, net]], textposition="outside",
                                increasing=dict(marker=dict(color=C_OK)), decreasing=dict(marker=dict(color=C_KO)), totals=dict(marker=dict(color=C_INK))))
    st.plotly_chart(_layout(wf, 320, "De la synergie brute à la valeur nette (M€)"))
    risks = [0.1, 0.2, 0.3, 0.4, 0.5]
    shares = [0.0, 0.25, 0.5, 0.75, 1.0]
    z = [[ev0 + s * max(synergy_net_value(run, mult, r, cost), 0) for s in shares] for r in risks]
    hm = go.Figure(go.Heatmap(z=z, x=[f"{int(s*100)} %" for s in shares], y=[f"{int(r*100)} %" for r in risks],
                              text=[[fmt(v, 0) for v in row] for row in z], texttemplate="%{text}",
                              colorscale=[[0, "#FFF7B0"], [1, C_YEL]], showscale=False))
    hm.update_xaxes(title="Part des synergies cédée")
    hm.update_yaxes(title="Risque d'exécution")
    st.plotly_chart(_layout(hm, 320, "Prix plafond (M€) selon risque et partage"))


def lab_decision():
    st.markdown("**Matrice de décision pondérée** – éditez les poids et les notes (1 à 5), puis testez la robustesse du classement.")
    if "dec_df" not in st.session_state:
        st.session_state["dec_df"] = pd.DataFrame({
            "Critère": ["Vitesse d'accès au marché", "Contrôle", "Capital requis (5 = faible)", "Risque d'exécution (5 = faible)", "Accès aux capacités"],
            "Poids (%)": [25.0, 20.0, 20.0, 20.0, 15.0],
            "Acquisition": [4, 5, 1, 2, 4],
            "JV": [3, 3, 3, 3, 5],
            "Organique": [1, 5, 4, 4, 2],
        })
    edited = st.data_editor(st.session_state["dec_df"], num_rows="fixed", hide_index=True, key="dec_editor",
                            column_config={"Poids (%)": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
                                           "Acquisition": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
                                           "JV": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
                                           "Organique": st.column_config.NumberColumn(min_value=1, max_value=5, step=1)})
    w = edited["Poids (%)"].astype(float).to_numpy()
    opts = ["Acquisition", "JV", "Organique"]
    if w.sum() <= 0:
        st.warning("La somme des poids doit être strictement positive.")
        return
    if abs(w.sum() - 100) > 0.01:
        st.info(f"La somme des poids est de {w.sum():.0f} % : les poids sont normalisés automatiquement.")
    wn = w / w.sum()
    scores = {o: float((wn * edited[o].astype(float).to_numpy()).sum()) for o in opts}
    ranking = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    m = st.columns(3)
    for col, (o, s) in zip(m, ranking):
        col.metric(o, f"{s:.2f}")
    fig = go.Figure(go.Bar(x=[o for o, _ in ranking], y=[s for _, s in ranking], marker_color=[C_YEL] + [C_INK] * 2,
                           text=[f"{s:.2f}" for _, s in ranking], textposition="outside"))
    fig.update_yaxes(range=[0, 5])
    st.plotly_chart(_layout(fig, 300, "Score pondéré (sur 5)"))
    gap = ranking[0][1] - ranking[1][1]
    if gap < 0.2:
        st.warning(f"Écart de {gap:.2f} point entre **{ranking[0][0]}** et **{ranking[1][0]}** : le score ne tranche pas. Formulez les **conditions de bascule**.")
    else:
        st.success(f"**{ranking[0][0]}** arrive en tête avec {gap:.2f} point d'avance.")
    rng = np.random.default_rng(42)
    wins = {o: 0 for o in opts}
    mat = np.array([edited[o].astype(float).to_numpy() for o in opts])
    for _ in range(2000):
        wp = wn * rng.uniform(0.7, 1.3, size=wn.size)
        wp = wp / wp.sum()
        wins[opts[int(np.argmax(mat @ wp))]] += 1
    st.markdown("**Test de robustesse** – 2 000 tirages avec des poids variant de ±30 % :")
    rb = pd.DataFrame({"Option": opts, "Fréquence en tête (%)": [wins[o] / 20 for o in opts]}).sort_values("Fréquence en tête (%)", ascending=False)
    st.dataframe(rb.style.format({"Fréquence en tête (%)": "{:.0f}"}), hide_index=True)


def lab_market():
    st.markdown("**Market sizing bottom-up** : TAM, SAM, SOM et CAGR.")
    c = st.columns(3)
    with c[0]:
        sites = _num("Nombre de sites / clients cibles", "m_sites", 2000, 1, 10_000_000, 100, "%.0f")
        pct_rel = _num("% pertinents (périmètre)", "m_rel", 40.0, 0.0, 100.0, 5.0, "%.0f") / 100
    with c[1]:
        units = _num("Unités / lignes par site", "m_units", 2.0, 0.1, 1000.0, 0.5, "%.1f")
        price = _num("Prix annuel par unité (k€)", "m_price", 50.0, 0.1, 100000.0, 5.0, "%.1f")
    with c[2]:
        sam_pct = _num("SAM : % adressable", "m_sam", 30.0, 0.0, 100.0, 5.0, "%.0f") / 100
        som_pct = _num("SOM : part du SAM à N ans (%)", "m_som", 10.0, 0.0, 100.0, 1.0, "%.0f") / 100
    tam = sites * pct_rel * units * price / 1000
    sam = tam * sam_pct
    som = sam * som_pct
    m = st.columns(3)
    m[0].metric("TAM", fmt(tam, 1, "M€"))
    m[1].metric("SAM", fmt(sam, 1, "M€"))
    m[2].metric("SOM", fmt(som, 2, "M€"))
    fig = go.Figure(go.Funnel(y=["TAM", "SAM", "SOM"], x=[tam, sam, som], textinfo="value+percent initial",
                              marker=dict(color=["#D8D8CF", C_INK, C_YEL])))
    st.plotly_chart(_layout(fig, 300, "Entonnoir de marché (M€)"))
    st.markdown("**Calculateur de CAGR**")
    d = st.columns(3)
    v0 = d[0].number_input("Valeur initiale (M€)", 0.1, 1e6, 120.0, 5.0, key="m_v0")
    v1 = d[1].number_input("Valeur finale (M€)", 0.1, 1e6, 190.0, 5.0, key="m_v1")
    n = d[2].number_input("Années", 1.0, 50.0, 4.0, 1.0, key="m_n")
    d[0].metric("CAGR", fmt(((v1 / v0) ** (1 / n) - 1) * 100, 1, "%"))


def lab_ratios():
    st.markdown("**De l'EBITDA au free cash-flow** et ratios de lecture financière.")
    c = st.columns(4)
    with c[0]:
        ca = _num("Chiffre d'affaires (M€)", "r_ca", 120.0, 1.0, 1e6, 5.0, "%.1f")
        ebitda = _num("EBITDA (M€)", "r_ebitda", 15.0, -1e5, 1e6, 0.5, "%.1f")
    with c[1]:
        tax = _num("Impôts cash (M€)", "r_tax", 3.0, 0.0, 1e5, 0.5, "%.1f")
        dwc = _num("Variation du BFR (M€)", "r_dwc", 4.0, -1e5, 1e5, 0.5, "%.1f")
    with c[2]:
        capex = _num("CAPEX (M€)", "r_capex", 7.0, 0.0, 1e5, 0.5, "%.1f")
        nd = _num("Dette nette (M€)", "r_nd", 35.0, -1e5, 1e6, 1.0, "%.1f")
    with c[3]:
        rec = _num("Créances clients (M€)", "r_rec", 24.0, 0.0, 1e6, 1.0, "%.1f")
        ce = _num("Capitaux employés (M€)", "r_ce", 100.0, 1.0, 1e6, 5.0, "%.1f")
    free = ebitda - tax - dwc - capex
    m = st.columns(5)
    m[0].metric("Free cash-flow", fmt(free, 1, "M€"))
    m[1].metric("Marge d'EBITDA", fmt(ebitda / ca * 100, 1, "%"))
    m[2].metric("Conversion cash", fmt(free / ebitda * 100 if ebitda else 0, 1, "%"))
    m[3].metric("Levier (DN/EBITDA)", fmt(nd / ebitda if ebitda else 0, 2, "x"))
    m[4].metric("DSO", fmt(rec / ca * 365, 0, "jours"))
    wf = go.Figure(go.Waterfall(x=["EBITDA", "Impôts", "ΔBFR", "CAPEX", "FCF"], measure=["absolute", "relative", "relative", "relative", "total"],
                                y=[ebitda, -tax, -dwc, -capex, 0], text=[fmt(v, 1) for v in [ebitda, -tax, -dwc, -capex, free]], textposition="outside",
                                increasing=dict(marker=dict(color=C_OK)), decreasing=dict(marker=dict(color=C_KO)), totals=dict(marker=dict(color=C_INK))))
    st.plotly_chart(_layout(wf, 320, "Pont EBITDA → free cash-flow (M€)"))
    nopat = st.slider("NOPAT (M€) pour calculer ROCE et EVA", 0.0, max(60.0, ce), 12.0, 0.5, key="r_nopat")
    wacc = st.slider("WACC (%)", 3.0, 15.0, 8.5, 0.5, key="r_wacc")
    k = st.columns(3)
    k[0].metric("ROCE", fmt(nopat / ce * 100, 1, "%"))
    k[1].metric("EVA", fmt(nopat - wacc / 100 * ce, 2, "M€"))
    k[2].metric("Spread ROCE − WACC", fmt(nopat / ce * 100 - wacc, 1, "pts"))


LABS = {
    "valuation": ("Valorisation (multiples)", lab_valuation),
    "dcf": ("DCF", lab_dcf),
    "npv": ("VAN / TRI", lab_npv),
    "bp": ("Business plan", lab_bp),
    "synergies": ("Synergies & prix plafond", lab_synergies),
    "decision": ("Matrice de décision", lab_decision),
    "market": ("Market sizing", lab_market),
    "ratios": ("Ratios & cash", lab_ratios),
}


def render_lab(key: str) -> None:
    LABS[key][1]()
