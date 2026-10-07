"""Moteur de notation : modules, axes de compétence, coach de recommandation, entretien."""
from __future__ import annotations

import re

PASS_THRESHOLD = 70

AXES = ["Diagnostic stratégique", "Finance & valorisation", "M&A", "Corporate strategy", "Communication COMEX"]


def module_scores(entry: dict | None, module: dict) -> dict:
    entry = entry or {}
    quiz = entry.get("quiz")
    n_ex = len(module["exercises"])
    done = sum(1 for v in (entry.get("ex_done") or {}).values() if v)
    ex_pct = round(100 * done / n_ex) if n_ex else 0
    quiz_pct = quiz if quiz is not None else 0
    total = round(0.5 * quiz_pct + 0.5 * ex_pct)
    passed = quiz is not None and quiz >= PASS_THRESHOLD and ex_pct >= 50
    return {"quiz": quiz, "exercises": ex_pct, "total": total, "passed": passed, "ex_done": done, "ex_total": n_ex}


def axis_scores(progress: dict, modules: list[dict]) -> dict:
    buckets: dict[str, list[int]] = {a: [] for a in AXES}
    for m in modules:
        s = module_scores(progress.get(str(m["id"])), m)
        buckets[m["axis"]].append(s["total"])
    return {a: (round(sum(v) / len(v)) if v else 0) for a, v in buckets.items()}


def global_score(progress: dict, modules: list[dict]) -> int:
    vals = [module_scores(progress.get(str(m["id"])), m)["total"] for m in modules]
    return round(sum(vals) / len(vals)) if vals else 0


def passed_count(progress: dict, modules: list[dict]) -> int:
    return sum(1 for m in modules if module_scores(progress.get(str(m["id"])), m)["passed"])


def quiz_grade(module: dict, answers: dict) -> tuple[int, list[dict]]:
    detail = []
    good = 0
    for i, q in enumerate(module["quiz"]):
        given = answers.get(i)
        ok = given == q["answer"]
        good += ok
        detail.append({"i": i, "given": given, "ok": ok})
    pct = round(100 * good / len(module["quiz"])) if module["quiz"] else 0
    return pct, detail


def numeric_check(value: float, answer: float, tol: float) -> bool:
    return abs(value - answer) <= tol


COACH_CRITERIA = {
    "Décision claire": [r"je recommande", r"nous recommandons", r"recommandation", r"il faut", r"nous proposons", r"décision"],
    "Création de valeur chiffrée": [r"van\b", r"vna\b", r"roce", r"tri\b", r"ev\b", r"valeur", r"m€", r"multiple", r"synerg"],
    "Alternatives comparées": [r"alternative", r"option", r"organique", r"acquisition", r"joint", r"\bjv\b", r"partenariat"],
    "Risques & mitigations": [r"risque", r"mitigation", r"limite", r"vigilance", r"downside"],
    "Scénarios / sensibilités": [r"scénario", r"sensibilit", r"hypoth", r"upside", r"base case"],
    "Gouvernance & exécution": [r"gouvernance", r"plan d.action", r"100 jours", r"jalon", r"milestone", r"kpi", r"calendrier"],
    "Conditions & prochaines étapes": [r"condition", r"prochaines étapes", r"due diligence", r"suspensive", r"go/no", r"décision du comité"],
}


def coach_text(text: str) -> dict:
    t = (text or "").lower()
    words = len(re.findall(r"\w+", t))
    detail = {crit: any(re.search(p, t) for p in patterns) for crit, patterns in COACH_CRITERIA.items()}
    score = round(100 * sum(detail.values()) / len(COACH_CRITERIA))
    if words < 60:
        score = min(score, 40)
    return {"score": score, "detail": detail, "words": words}


def interview_score(text: str, expected: list[list[str]]) -> dict:
    """expected = liste de groupes de mots-clés ; un groupe est couvert si l'un de ses termes apparaît."""
    t = (text or "").lower()
    covered = [any(k.lower() in t for k in group) for group in expected]
    words = len(re.findall(r"\w+", t))
    pct = round(100 * sum(covered) / len(expected)) if expected else 0
    structure = bool(re.search(r"(premièrement|d.abord|1\)|1\.|tout d.abord)", t)) and bool(re.search(r"(en conclusion|je recommande|donc|en synthèse)", t))
    return {"pct": pct, "covered": covered, "words": words, "structure": structure}
