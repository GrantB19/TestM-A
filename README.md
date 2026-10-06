# Avril Executive Academy - Strategy & M&A

Projet Streamlit autonome pour un parcours de formation en stratégie, finance corporate et M&A.

## Lancer localement

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Contenu
- 10 modules
- cas pratiques fictifs
- quiz et moteur de notation
- simulateur de valorisation
- coach COMEX fondé sur des critères explicites
- export/import JSON de la progression

## Structure
- `app.py` : interface et navigation
- `content.py` : contenus pédagogiques
- `scoring.py` : moteur de notation
- `.streamlit/config.toml` : thème

## Confidentialité
L'application ne fait aucun appel réseau applicatif et n'envoie pas les réponses à un service tiers. Les cas sont synthétiques et pédagogiques.
