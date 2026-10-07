"""Strategy & M&A Academy – application Streamlit (point d'entrée : app.py)."""
from __future__ import annotations

import json

import plotly.graph_objects as go
import streamlit as st

import ai
import labs
import ui
from content import GLOSSARY, INTERVIEW, MODULES, PLAN
from scoring import (AXES, COACH_CRITERIA, PASS_THRESHOLD, axis_scores, coach_text, global_score, interview_score,
                     module_scores, numeric_check, passed_count, quiz_grade)

st.set_page_config(page_title="Strategy & M&A Academy", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
ui.inject_css()

BY_ID = {m["id"]: m for m in MODULES}
NAV_KEYS = ["home"] + [f"m{m['id']}" for m in MODULES] + ["lab", "interview", "glossary", "bilan"]
NAV_STATIC = {"home": "Accueil", "lab": "Laboratoire", "interview": "Entretien & coach",
              "glossary": "Glossaire", "bilan": "Bilan & attestation"}
KEEP_ON_RESET = ("nav", "ai_calls", "ai_consent_ok")


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("prog", {})
    ss.setdefault("nav", "home")
    ss.setdefault("name", "")
    ss.setdefault("iv", {})
    ss.setdefault("iv_idx", 0)
    ss.setdefault("coach_saved", "")
    ss.setdefault("ai_scores", {})


def entry(mid: int) -> dict:
    return st.session_state["prog"].setdefault(str(mid), {})


def goto(key: str) -> None:
    st.session_state["nav"] = key


def nav_label(key: str, done_ids: frozenset = frozenset()) -> str:
    if key in NAV_STATIC:
        return NAV_STATIC[key]
    m = BY_ID[int(key[1:])]
    return f"{'✓' if m['id'] in done_ids else '○'}  {m['id']:02d} · {m['title']}"


def next_module_key() -> str:
    for m in MODULES:
        if not module_scores(st.session_state["prog"].get(str(m["id"])), m)["passed"]:
            return f"m{m['id']}"
    return "bilan"


def sidebar() -> None:
    prog = st.session_state["prog"]
    n_ok = passed_count(prog, MODULES)
    done_ids = frozenset(m["id"] for m in MODULES if module_scores(prog.get(str(m["id"])), m)["passed"])
    with st.sidebar:
        ui.sidebar_brand(round(100 * n_ok / len(MODULES)), f"{n_ok}/{len(MODULES)} modules validés")
        st.radio("Navigation", NAV_KEYS, format_func=lambda k: nav_label(k, done_ids), key="nav", label_visibility="collapsed")
        st.divider()
        st.caption(ai.status_caption())
        st.caption("La progression est conservée pendant votre session. Exportez-la pour la retrouver plus tard.")
        payload = json.dumps({"version": 5, "prog": prog, "name": st.session_state["name"], "iv": st.session_state["iv"],
                              "ai_scores": st.session_state.get("ai_scores", {})}, ensure_ascii=False, indent=2)
        st.download_button("Exporter ma progression", payload, "progression_academy.json", "application/json")
        up = st.file_uploader("Importer une progression", type="json", key="uploader")
        if up is not None and st.button("Appliquer l'import"):
            try:
                data = json.load(up)
                st.session_state["prog"] = data.get("prog", {})
                st.session_state["name"] = data.get("name", "")
                st.session_state["iv"] = data.get("iv", {})
                st.session_state["ai_scores"] = data.get("ai_scores", {})
                st.success("Progression importée.")
                st.rerun()
            except Exception:
                st.error("Fichier invalide.")
        if st.button("Réinitialiser la progression"):
            for k in list(st.session_state.keys()):
                if k not in KEEP_ON_RESET:
                    del st.session_state[k]
            st.rerun()


def radar(values: dict, height: int = 380) -> go.Figure:
    short = {"Diagnostic stratégique": "Diagnostic", "Finance & valorisation": "Finance", "M&A": "M&A",
             "Corporate strategy": "Strategy", "Communication COMEX": "COMEX"}
    cats = [short.get(k, k) for k in values.keys()]
    vals = list(values.values())
    fig = go.Figure(go.Scatterpolar(r=vals + vals[:1], theta=cats + cats[:1], fill="toself",
                                    fillcolor="rgba(255,230,0,0.45)", line=dict(color="#1A1A24", width=3)))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100], tickvals=[25, 50, 75, 100], gridcolor="#E3E3DC"),
                                 angularaxis=dict(gridcolor="#E3E3DC")),
                      showlegend=False, height=height, margin=dict(l=70, r=70, t=30, b=30),
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#1A1A24", size=13))
    return fig


def page_home() -> None:
    prog = st.session_state["prog"]
    n_ok = passed_count(prog, MODULES)
    g = global_score(prog, MODULES)
    quizzes = [module_scores(prog.get(str(m["id"])), m)["quiz"] for m in MODULES]
    quizzes = [q for q in quizzes if q is not None]
    avg_quiz = round(sum(quizzes) / len(quizzes)) if quizzes else 0
    done_ex = sum(module_scores(prog.get(str(m["id"])), m)["ex_done"] for m in MODULES)
    tot_ex = sum(len(m["exercises"]) for m in MODULES)
    ui.hero("CORPORATE STRATEGY & M&A", "De l'expertise M&A à la stratégie groupe",
            "Un parcours pratique en 10 modules : diagnostic stratégique, finance d'entreprise, valorisation, M&A et décision COMEX – avec cours, exemples chiffrés, exercices corrigés, quiz, simulateurs et correction interactive par IA.",
            ["10 modules", "8 laboratoires", "50 questions de quiz", "10 questions d'entretien"], f"{g}%", "SCORE GLOBAL", f"{n_ok}/10 modules validés")
    ui.stats([("Modules validés", f"{n_ok}/10", f"seuil : quiz ≥ {PASS_THRESHOLD} % et 50 % des exercices"),
              ("Score moyen aux quiz", f"{avg_quiz}%", f"{len(quizzes)} quiz passés"),
              ("Exercices traités", f"{done_ex}/{tot_ex}", "corrections détaillées incluses"),
              ("Temps restant estimé", f"{max(0, 8 - round(8 * n_ok / 10))} sem.", "à 3-4 h par semaine")])
    nxt = next_module_key()
    c1, c2 = st.columns([1.1, 1])
    with c1:
        st.subheader("Votre prochaine étape")
        if nxt == "bilan":
            st.success("Tous les modules sont validés. Consultez votre bilan et passez au simulateur d'entretien.")
            st.button("Voir mon bilan", on_click=goto, args=("bilan",), type="primary")
        else:
            m = BY_ID[int(nxt[1:])]
            st.markdown(f"**Module {m['id']} · {m['title']}**  \n{m['objective']}")
            st.caption(f"{m['duration']} · niveau {m['level']}")
            st.button(f"Commencer le module {m['id']} →", on_click=goto, args=(nxt,), type="primary")
        st.subheader("Comment utiliser cette académie")
        st.markdown("1. **Lisez** le cours (onglet *Cours*) puis l'**exemple chiffré**.\n"
                    "2. **Traitez** les exercices – vérifiez vos calculs, puis demandez une **correction interactive** (IA ou prompt Copilot).\n"
                    "3. **Passez le quiz** : au moins 70 % pour valider.\n"
                    "4. **Expérimentez** dans les laboratoires, puis **entraînez-vous** à l'entretien.")
    with c2:
        st.subheader("Profil de compétences")
        st.plotly_chart(radar(axis_scores(prog, MODULES)))
    st.subheader("Progression par module")
    for m in MODULES:
        s = module_scores(prog.get(str(m["id"])), m)
        a, b, c, d = st.columns([0.5, 3, 2.2, 1.2])
        a.markdown(f"**{m['id']:02d}**")
        b.markdown(f"{m['title']}  \n<small>{m['axis']}</small>", unsafe_allow_html=True)
        c.progress(s["total"] / 100, text=f"{s['total']} %")
        d.button("Ouvrir", key=f"open_{m['id']}", on_click=goto, args=(f"m{m['id']}",))
    st.subheader("Plan de travail conseillé (8 semaines)")
    ui.md_table([{"Semaine": p[0], "Modules": p[1], "Contenu": p[2], "Temps": p[3]} for p in PLAN])


def tab_course(m: dict) -> None:
    ui.box("obj", "Objectifs d'apprentissage", m["outcomes"])
    for i, sec in enumerate(m["sections"], 1):
        with st.container(border=True):
            ui.section_title(i, sec["title"].split(". ", 1)[-1])
            st.markdown(sec["body"])
    c1, c2 = st.columns(2)
    with c1:
        ui.box("key", "À retenir", m["key_points"])
    with c2:
        ui.box("warn", "Pièges classiques", m["pitfalls"])
    e = entry(m["id"])
    e["read"] = st.checkbox("J'ai lu et compris ce cours", value=e.get("read", False), key=f"read_{m['id']}")


def tab_example(m: dict) -> None:
    ex = m["example"]
    st.subheader(ex["title"])
    st.markdown(ex["body"])
    ui.md_table(ex["table"])
    st.caption("Utilisez l'onglet *Outil* pour rejouer ce cas avec vos propres hypothèses.")


def tab_exercises(m: dict) -> None:
    e = entry(m["id"])
    e.setdefault("ex_done", {})
    e.setdefault("ex_val", {})
    e.setdefault("ex_text", {})
    st.markdown("Traitez chaque exercice **avant** d'ouvrir la correction. Les exercices chiffrés se valident automatiquement ; "
                "les exercices rédactionnels se valident par auto-évaluation. La **correction interactive par IA** est un complément : "
                "la validation reste fondée sur le calcul ou sur votre auto-évaluation.")
    first_todo = next((j for j in range(len(m["exercises"])) if not e["ex_done"].get(str(j))), -1)
    for i, ex in enumerate(m["exercises"]):
        k = str(i)
        done = e["ex_done"].get(k, False)
        with st.expander(f"{'✓' if done else '○'}  Exercice {i + 1} · {ex['title']}", expanded=(i == first_todo)):
            st.markdown(ex["statement"])
            chk = ex.get("check")
            if chk:
                c1, c2 = st.columns([2, 1])
                val = c1.number_input(f"Votre réponse – {chk['label']}", value=float(e["ex_val"].get(k, 0.0)), step=0.01, format="%.2f", key=f"exv_{m['id']}_{i}")
                if c2.button("Vérifier", key=f"exb_{m['id']}_{i}", type="primary"):
                    e["ex_val"][k] = val
                    if numeric_check(val, chk["answer"], chk["tol"]):
                        e["ex_done"][k] = True
                        e["flash"] = f"Correct – {chk['label']} ≈ {chk['answer']:.2f} {chk['unit']}"
                        st.rerun()
                    else:
                        st.error("Pas tout à fait. Relisez l'indice ou la correction, puis réessayez.")
                if done:
                    st.success(e.pop("flash", "Exercice validé."))
                ai_answer = f"{val:.2f} {chk['unit']}".strip()
                ai_kind = "numeric"
                ai_extra = f"VALEUR ATTENDUE : {chk['answer']:.2f} {chk['unit']} (tolérance ±{chk['tol']})"
                ai_label = "Expliquer mon calcul"
            else:
                txt = st.text_area("Votre réponse (brouillon)", value=e["ex_text"].get(k, ""), height=150, key=f"ext_{m['id']}_{i}")
                e["ex_text"][k] = txt
                ok = st.checkbox("J'ai traité cet exercice et comparé à la correction", value=done, key=f"exc_{m['id']}_{i}")
                if ok != done:
                    e["ex_done"][k] = ok
                    st.rerun()
                ai_answer, ai_kind, ai_extra, ai_label = txt, "open", "", "Corriger avec l'IA"
            ai.panel(scope=f"ex_{m['id']}_{i}", kind=ai_kind, task=ex["statement"], reference=ex["solution"],
                     user_answer=ai_answer, extra=ai_extra, button_label=ai_label)
            with st.expander("Indice"):
                st.markdown(ex["hint"])
            with st.expander("Correction détaillée"):
                st.markdown(ex["solution"])


def tab_quiz(m: dict) -> None:
    e = entry(m["id"])
    retake = st.session_state.get(f"retake_{m['id']}", False)
    if e.get("quiz") is not None and not retake:
        pct = e["quiz"]
        msg = "seuil atteint ✓" if pct >= PASS_THRESHOLD else f"seuil de {PASS_THRESHOLD} % non atteint, relisez puis réessayez"
        (st.success if pct >= PASS_THRESHOLD else st.warning)(f"Score : **{pct} %** — {msg}")
        for i, q in enumerate(m["quiz"]):
            d = e["quiz_detail"][i]
            given = q["choices"][d["given"]] if d["given"] is not None else "—"
            with st.container(border=True):
                st.markdown(f"{'✓' if d['ok'] else '✗'} **{i + 1}. {q['q']}**")
                st.markdown(f"Votre réponse : *{given}*" + ("" if d["ok"] else f"  \nBonne réponse : **{q['choices'][q['answer']]}**"))
                st.caption(q["why"])
        if st.button("Refaire le quiz", key=f"rq_{m['id']}"):
            st.session_state[f"retake_{m['id']}"] = True
            st.rerun()
        return
    with st.form(f"quiz_{m['id']}"):
        st.markdown(f"Répondez aux {len(m['quiz'])} questions. Seuil de validation : **{PASS_THRESHOLD} %**.")
        for i, q in enumerate(m["quiz"]):
            st.radio(f"{i + 1}. {q['q']}", q["choices"], index=None, key=f"q_{m['id']}_{i}")
        sub = st.form_submit_button("Corriger mon quiz", type="primary")
    if sub:
        answers = {}
        for i, q in enumerate(m["quiz"]):
            sel = st.session_state.get(f"q_{m['id']}_{i}")
            answers[i] = q["choices"].index(sel) if sel in q["choices"] else None
        if any(v is None for v in answers.values()):
            st.warning("Répondez à toutes les questions avant de corriger.")
            return
        pct, detail = quiz_grade(m, answers)
        e["quiz"] = pct
        e["quiz_detail"] = detail
        st.session_state[f"retake_{m['id']}"] = False
        st.rerun()


def page_module(mid: int) -> None:
    m = BY_ID[mid]
    prog = st.session_state["prog"]
    s = module_scores(prog.get(str(mid)), m)
    e = entry(mid)
    ui.hero(f"MODULE {mid:02d} · {m['axis'].upper()}", m["title"], m["objective"],
            [m["level"], m["duration"], "Validé" if s["passed"] else "En cours"], f"{s['total']}%", "SCORE DU MODULE",
            f"quiz {s['quiz'] if s['quiz'] is not None else '—'}{'%' if s['quiz'] is not None else ''} · exercices {s['ex_done']}/{s['ex_total']}")
    ui.stepper([("Cours", "lu" if e.get("read") else "à lire", bool(e.get("read"))),
                ("Exercices", f"{s['ex_done']}/{s['ex_total']} traités", s["ex_done"] == s["ex_total"]),
                ("Quiz", f"{s['quiz']} %" if s["quiz"] is not None else "à passer", s["quiz"] is not None and s["quiz"] >= PASS_THRESHOLD),
                ("Validation", "module validé" if s["passed"] else f"quiz ≥ {PASS_THRESHOLD} %", s["passed"])])
    t1, t2, t3, t4, t5 = st.tabs(["Cours", "Exemple chiffré", "Exercices", "Quiz", "Outil"])
    with t1:
        tab_course(m)
    with t2:
        tab_example(m)
    with t3:
        tab_exercises(m)
    with t4:
        tab_quiz(m)
    with t5:
        st.subheader(f"Laboratoire : {labs.LABS[m['lab']][0]}")
        labs.render_lab(m["lab"])
    st.divider()
    a, b, _ = st.columns([1, 1, 3])
    if mid > 1:
        a.button(f"← Module {mid - 1}", on_click=goto, args=(f"m{mid - 1}",))
    if mid < len(MODULES):
        b.button(f"Module {mid + 1} →", on_click=goto, args=(f"m{mid + 1}",), type="primary")


def page_lab() -> None:
    ui.hero("LABORATOIRE", "Simulateurs financiers & stratégiques",
            "Huit outils interactifs pour manipuler les concepts : modifiez les hypothèses, observez l'impact sur la valeur, les risques et la décision.",
            ["Valorisation", "DCF", "VAN / TRI", "Business plan", "Synergies", "Décision", "Marché", "Cash"])
    keys = list(labs.LABS)
    choice = st.radio("Outil", keys, format_func=lambda k: labs.LABS[k][0], horizontal=True, key="lab_choice", label_visibility="collapsed")
    st.divider()
    labs.render_lab(choice)


def page_interview() -> None:
    ui.hero("ENTRETIEN & COACHING", "Entraînez-vous à convaincre",
            "Répondez comme devant un Directeur Stratégie : recommandation d'abord, trois arguments, risque principal, conclusion. L'évaluation par mots-clés est indicative ; la correction interactive par IA va plus loin sur la qualité du raisonnement.",
            ["10 questions", "Coach COMEX", "Correction IA"])
    t1, t2 = st.tabs(["Simulateur d'entretien", "Coach COMEX"])
    with t1:
        idx = st.session_state["iv_idx"] % len(INTERVIEW)
        q = INTERVIEW[idx]
        st.markdown(f"##### Question {idx + 1} / {len(INTERVIEW)}")
        st.markdown(f"> **{q['q']}**")
        saved = st.session_state["iv"].get(str(idx), {})
        txt = st.text_area("Votre réponse (visez 90 secondes à l'oral, soit 150 à 200 mots)", value=saved.get("text", ""), height=220, key=f"iv_text_{idx}")
        c1, c2, c3 = st.columns([1, 1, 3])
        if c1.button("Évaluer (mots-clés)", type="primary", key=f"iv_eval_{idx}"):
            r = interview_score(txt, q["expected"])
            st.session_state["iv"][str(idx)] = {"text": txt, "pct": r["pct"]}
            st.session_state[f"iv_res_{idx}"] = r
        if c2.button("Question suivante →", key=f"iv_next_{idx}"):
            st.session_state["iv"].setdefault(str(idx), {})["text"] = txt
            st.session_state["iv_idx"] = idx + 1
            st.rerun()
        r = st.session_state.get(f"iv_res_{idx}")
        if r:
            st.progress(r["pct"] / 100, text=f"Couverture des idées attendues : {r['pct']} %")
            st.markdown(f"{r['words']} mots · structure (annonce + conclusion) : {'✓' if r['structure'] else '△ à renforcer'}")
            st.markdown("  ".join(f"{'✓' if c else '○'} Idée {n}" for n, c in enumerate(r["covered"], 1)))
            missing = [", ".join(g[:3]) for g, c in zip(q["expected"], r["covered"]) if not c]
            if missing:
                st.info("Pistes à intégrer (mots-clés manquants) : " + " · ".join(missing))
        with st.expander("Voir une réponse modèle"):
            st.markdown(q["model"])
        expected_txt = "\n".join(f"- Idée {n} : {', '.join(g)}" for n, g in enumerate(q["expected"], 1))
        ai.panel(scope=f"iv_{idx}", kind="interview", task=q["q"], reference=q["model"], user_answer=txt,
                 extra=expected_txt, button_label="Évaluer avec l'IA")
        scored = [v.get("pct") for v in st.session_state["iv"].values() if v.get("pct") is not None]
        if scored:
            st.caption(f"Questions travaillées : {len(scored)}/{len(INTERVIEW)} · couverture moyenne : {round(sum(scored) / len(scored))} %")
    with t2:
        st.markdown("Collez une **recommandation** (executive summary, memo) : le coach vérifie la présence de sept dimensions attendues par un comité de décision, puis l'IA peut jouer un membre sceptique du comité.")
        txt = st.text_area("Votre recommandation", value=st.session_state["coach_saved"], height=260, key="coach_text_area")
        if st.button("Challenger ma note (mots-clés)", type="primary", key="coach_btn"):
            st.session_state["coach_saved"] = txt
            r = coach_text(txt)
            st.progress(r["score"] / 100, text=f"Score de couverture : {r['score']} / 100 · {r['words']} mots")
            for crit, ok in r["detail"].items():
                st.markdown(f"{'✓' if ok else '○'} **{crit}**")
            if r["words"] < 60:
                st.warning("Texte trop court pour une note de décision (moins de 60 mots).")
            missing = [c for c, ok in r["detail"].items() if not ok]
            if missing:
                st.info("À renforcer : " + ", ".join(missing) + ".")
        criteria_txt = "\n".join(f"- {c}" for c in COACH_CRITERIA)
        ai.panel(scope="coach", kind="coach", task="Recommandation sur un cas fictif traité en formation (par exemple : JV internationale dans les protéines végétales).",
                 reference=criteria_txt, user_answer=txt, button_label="Challenger avec l'IA")


def page_glossary() -> None:
    ui.hero("GLOSSAIRE", "Le vocabulaire de la stratégie et du M&A", "Définitions courtes des termes utilisés dans les modules.", [f"{len(GLOSSARY)} termes"])
    q = st.text_input("Rechercher un terme", placeholder="ex. WACC, TSA, goodwill…")
    items = [(k, v) for k, v in sorted(GLOSSARY.items(), key=lambda kv: kv[0].lower()) if q.lower() in k.lower() or q.lower() in v.lower()]
    if not items:
        st.info("Aucun terme trouvé.")
    for k, v in items:
        with st.container(border=True):
            st.markdown(f"**{k}**  \n{v}")


def certificate_html(name: str, g: int, axes: dict, n_ok: int) -> str:
    rows = "".join(f"<tr><td style='padding:6px 12px;text-align:left'>{ui.esc(a)}</td><td style='padding:6px 12px;text-align:right'><b>{v}%</b></td></tr>" for a, v in axes.items())
    safe = ui.esc(name or "Participant")
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Attestation</title></head>
<body style="font-family:Arial,sans-serif;background:#f4f4f0;padding:30px"><div style="max-width:760px;margin:auto;background:#fff;border:10px solid #1a1a24;outline:3px solid #ffe600;outline-offset:-16px;padding:46px;text-align:center">
<div style="letter-spacing:3px;font-size:12px;font-weight:700;color:#555">STRATEGY &amp; M&amp;A ACADEMY</div>
<h1 style="margin:14px 0">Attestation de progression</h1><p>Décernée à</p>
<div style="font-size:28px;font-weight:800;border-bottom:2px solid #1a1a24;display:inline-block;padding:4px 26px">{safe}</div>
<p style="margin-top:22px">pour la réalisation du parcours Corporate Strategy &amp; M&amp;A</p>
<div style="font-size:54px;font-weight:900">{g}%</div><p>{n_ok} / {len(MODULES)} modules validés</p>
<table style="margin:auto;border-collapse:collapse">{rows}</table>
<p style="font-size:11px;color:#777;margin-top:26px">Auto-évaluation générée localement. Outil d'apprentissage interne, non diplômant.</p></div></body></html>"""


def page_bilan() -> None:
    prog = st.session_state["prog"]
    g = global_score(prog, MODULES)
    n_ok = passed_count(prog, MODULES)
    axes = axis_scores(prog, MODULES)
    ui.hero("BILAN", "Votre niveau de préparation", "Synthèse par axe de compétence et plan de renforcement.", [f"{n_ok}/10 modules validés"], f"{g}%", "SCORE GLOBAL",
            "prêt pour des cas avancés" if g >= 75 else "parcours en cours")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.plotly_chart(radar(axes))
    with c2:
        st.subheader("Scores par axe")
        for a in AXES:
            st.progress(axes[a] / 100, text=f"{a} — {axes[a]} %")
        weakest = min(axes, key=axes.get)
        st.info(f"Axe prioritaire à renforcer : **{weakest}** ({axes[weakest]} %).")
    st.subheader("Détail par module")
    rows = []
    for m in MODULES:
        s = module_scores(prog.get(str(m["id"])), m)
        rows.append({"Module": f"{m['id']:02d} · {m['title']}", "Axe": m["axis"], "Quiz": f"{s['quiz']} %" if s["quiz"] is not None else "—",
                     "Exercices": f"{s['ex_done']}/{s['ex_total']}", "Score": f"{s['total']} %", "Statut": "Validé" if s["passed"] else "En cours"})
    ui.md_table(rows)
    ai_scores = st.session_state.get("ai_scores", {})
    if ai_scores:
        st.subheader("Notes indicatives de la correction IA")
        st.caption("Ces notes sont données à titre indicatif et ne comptent pas dans le score global.")
        ui.md_table([{"Exercice / séance": k.replace("ex_", "Exercice ").replace("iv_", "Entretien Q").replace("coach", "Coach COMEX"), "Note IA": f"{v} / 100"}
                     for k, v in sorted(ai_scores.items())])
    st.subheader("Attestation")
    name = st.text_input("Nom à faire figurer", value=st.session_state["name"], key="name_input")
    st.session_state["name"] = name
    st.download_button("Télécharger l'attestation (HTML, imprimable en PDF)", certificate_html(name, g, axes, n_ok), "attestation_academy.html", "text/html", type="primary")


init_state()
sidebar()
nav = st.session_state["nav"]
if nav == "home":
    page_home()
elif nav.startswith("m"):
    page_module(int(nav[1:]))
elif nav == "lab":
    page_lab()
elif nav == "interview":
    page_interview()
elif nav == "glossary":
    page_glossary()
else:
    page_bilan()
