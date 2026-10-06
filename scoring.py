
from dataclasses import dataclass

@dataclass
class ScoreResult:
    quiz: int
    case: int
    total: int
    passed: bool
    feedback: list[str]

def score_quiz(module, answers):
    qs=module.get("quiz",[])
    if not qs: return 0
    good=sum(1 for i,q in enumerate(qs) if answers.get(i)==q["answer"])
    return round(good/len(qs)*100)

def score_case(module, checks):
    rubric=module.get("rubric",[])
    if not rubric: return 0
    return round(sum(bool(checks.get(i)) for i in range(len(rubric)))/len(rubric)*100)

def score_module(module, answers, checks):
    q=score_quiz(module, answers); c=score_case(module, checks)
    total=round(q*.4+c*.6)
    feedback=[]
    if q<75: feedback.append("Revoir les concepts et refaire le quiz.")
    if c<75: feedback.append("Renforcer le livrable avec la grille d'évaluation.")
    if total>=75: feedback.append("Module validé. Passez au suivant.")
    return ScoreResult(q,c,total,total>=75,feedback)

def keyword_coach(text, keywords):
    clean=text.lower(); found=[k for k in keywords if k.lower() in clean]
    score=round(len(found)/max(1,len(keywords))*100)
    return score, found
