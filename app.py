
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from content import MODULES
from scoring import score_module, keyword_coach

st.set_page_config(page_title="Avril Executive Academy",page_icon="🌱",layout="wide",initial_sidebar_state="expanded")
st.markdown("""<style>
[data-testid="stSidebar"]{background:linear-gradient(180deg,#102f3b,#1d4b55);color:white}.block-container{padding-top:1.4rem;max-width:1250px}.hero{background:linear-gradient(120deg,#153744,#315d67);padding:28px;border-radius:22px;color:white;box-shadow:0 18px 40px #102f3b25}.eyebrow{letter-spacing:2px;font-size:11px;font-weight:800;color:#78923c}.metric-card{background:white;border:1px solid #dfe5df;border-radius:15px;padding:16px}.lesson{background:white;border:1px solid #dfe5df;border-radius:16px;padding:18px;min-height:140px}.formula{background:#143642;color:white;padding:14px;border-radius:11px}.stButton>button{border-radius:10px;font-weight:700}.passed{color:#779531;font-weight:800}
</style>""",unsafe_allow_html=True)

if "progress" not in st.session_state: st.session_state.progress={}
if "module" not in st.session_state: st.session_state.module=1
if "answers" not in st.session_state: st.session_state.answers={}

def export_payload():
    return json.dumps({"progress":st.session_state.progress,"answers":st.session_state.answers},ensure_ascii=False,indent=2)

with st.sidebar:
    st.markdown("## 🌱 Executive Academy")
    st.caption("Corporate Strategy & M&A")
    passed=sum(1 for v in st.session_state.progress.values() if v.get("passed"))
    st.progress(passed/len(MODULES),text=f"Progression {passed}/{len(MODULES)}")
    labels=[f"{m['id']:02d} · {m['title']}" for m in MODULES]
    choice=st.radio("Parcours",labels,index=st.session_state.module-1,label_visibility="collapsed")
    st.session_state.module=labels.index(choice)+1
    st.divider()
    st.download_button("Exporter la progression",export_payload(),"progression.json","application/json",use_container_width=True)
    upload=st.file_uploader("Importer",type="json",label_visibility="collapsed")
    if upload:
        try:
            payload=json.load(upload); st.session_state.progress=payload.get("progress",{}); st.session_state.answers=payload.get("answers",{}); st.success("Progression importée")
        except Exception: st.error("Fichier invalide")

m=MODULES[st.session_state.module-1]
st.markdown('<div class="eyebrow">AVRIL EXECUTIVE LEARNING · CORPORATE STRATEGY & M&A</div>',unsafe_allow_html=True)
st.title(f"Module {m['id']} · {m['title']}")
st.caption(m['objective'])
a,b,c=st.columns(3)
with a: st.markdown(f'<div class="metric-card"><small>PARCOURS</small><br><b>{m["track"]}</b></div>',unsafe_allow_html=True)
with b: st.markdown('<div class="metric-card"><small>MÉTHODE</small><br><b>Cours · cas · quiz</b></div>',unsafe_allow_html=True)
with c:
    saved=st.session_state.progress.get(str(m['id']),{})
    st.markdown(f'<div class="metric-card"><small>SCORE</small><br><b>{saved.get("total",0)}%</b></div>',unsafe_allow_html=True)
st.markdown(f'<div class="hero"><h2>{m["objective"]}</h2><p>Un parcours appliqué à votre transition du M&A IT vers la Stratégie & M&A Groupe.</p></div>',unsafe_allow_html=True)

tabs=st.tabs(["Cours","Cas pratique","Quiz & notation","Laboratoire finance","Coach COMEX"])
with tabs[0]:
    cols=st.columns(3)
    for col,(i,lesson) in zip(cols,enumerate(m['lesson'],1)):
        with col: st.markdown(f'<div class="lesson"><h3>{i:02d}</h3><p>{lesson}</p></div>',unsafe_allow_html=True)
    st.info("Réflexe exécutif : tout calcul doit conduire à une implication puis à une décision.")
with tabs[1]:
    st.subheader("Cas pratique")
    st.write(m['case'])
    key=f"text_{m['id']}"
    text=st.text_area("Votre réponse",value=st.session_state.answers.get(key,""),height=250,key=f"widget_{key}")
    st.session_state.answers[key]=text
    st.markdown("#### Auto-évaluation")
    checks={}
    for i,item in enumerate(m['rubric']): checks[i]=st.checkbox(item,key=f"c_{m['id']}_{i}")
with tabs[2]:
    st.subheader("Quiz et moteur de notation")
    quiz_answers={}
    for i,q in enumerate(m['quiz']):
        quiz_answers[i]=st.radio(q['q'],range(len(q['choices'])),format_func=lambda x,q=q:q['choices'][x],key=f"q_{m['id']}_{i}")
    if st.button("Calculer mon score",type="primary"):
        check_values={i:st.session_state.get(f"c_{m['id']}_{i}",False) for i in range(len(m['rubric']))}
        result=score_module(m,quiz_answers,check_values)
        st.session_state.progress[str(m['id'])]={"quiz":result.quiz,"case":result.case,"total":result.total,"passed":result.passed}
        x,y,z=st.columns(3); x.metric("Quiz",f"{result.quiz}%"); y.metric("Cas",f"{result.case}%"); z.metric("Total",f"{result.total}%")
        (st.success if result.passed else st.warning)(" ".join(result.feedback))
with tabs[3]:
    st.subheader("Simulateur de valorisation")
    c1,c2,c3=st.columns(3)
    ebitda=c1.number_input("EBITDA (M€)",0.0,500.0,15.0,.5)
    multiple=c2.slider("Multiple EV/EBITDA",3.0,15.0,8.0,.5)
    net_debt=c3.number_input("Dette nette (M€)",0.0,500.0,35.0,.5)
    ev=ebitda*multiple; equity=ev-net_debt
    a1,a2=st.columns(2); a1.metric("Enterprise Value",f"{ev:.1f} M€"); a2.metric("Equity Value",f"{equity:.1f} M€")
    mults=np.arange(max(3,multiple-2),multiple+2.1,.5)
    fig=go.Figure(go.Bar(x=mults,y=ebitda*mults-net_debt,marker_color="#86A63D"))
    fig.update_layout(title="Sensibilité de l'Equity Value",xaxis_title="Multiple",yaxis_title="M€",height=350,margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig,use_container_width=True)
with tabs[4]:
    st.subheader("Coach COMEX")
    st.caption("Évaluation indicative par critères explicites, sans IA externe ni envoi de données.")
    recommendation=st.text_area("Collez votre recommandation",height=220,key=f"coach_{m['id']}")
    keywords=["recommandation","risque","valeur","scénario","hypothèse","exécution"]
    if st.button("Challenger ma note"):
        score,found=keyword_coach(recommendation,keywords)
        st.metric("Couverture des dimensions attendues",f"{score}%")
        st.write("Dimensions détectées :",", ".join(found) if found else "aucune")
        st.write("À renforcer :",", ".join(k for k in keywords if k not in found) or "aucune")

st.divider()
st.caption("Cas fictifs à visée pédagogique. Ne pas utiliser comme recommandation d'investissement réelle.")
