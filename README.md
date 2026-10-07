# Strategy & M&A Academy

Application Streamlit de formation : 10 modules (stratégie, finance, valorisation, M&A, décision COMEX), 29 exercices corrigés, 50 questions de quiz, 8 laboratoires interactifs, simulateur d'entretien et coach de recommandation.

## Lancer en local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Déployer sur Streamlit Community Cloud
Repository : ce dépôt · Branch : `main` · Main file path : `app.py`

## Fichiers
| Fichier | Rôle |
|---|---|
| `app.py` | Interface et navigation |
| `content.py`, `content_a.py`, `content_b.py`, `content_c.py` | Cours, exemples, exercices, quiz, glossaire, entretien |
| `finance.py` | Fonctions financières (VAN, TRI, DCF, EV → Equity…) |
| `labs.py` | Laboratoires interactifs |
| `scoring.py` | Moteur de notation |
| `ui.py` | Habillage visuel |
| `.streamlit/config.toml` | Thème (dossier `.streamlit` à la racine du dépôt) |

Cas, chiffres et hypothèses : **fictifs et pédagogiques**. Aucune donnée interne n'est embarquée.
