"""Modules 5 à 7 : valorisation, business plan, M&A & synergies."""
from finance import dcf, ev_to_equity, synergy_net_value

DCF_EX = dcf(10.0, 0.05, 0.09, 0.02, 5)
EQ_8X = ev_to_equity(15 * 8, 35, 4, 2)
EQ_7X = ev_to_equity(15 * 7, 35, 4, 2)
EQ_9X = ev_to_equity(15 * 9, 35, 4, 2)
SYN_NET = synergy_net_value(8, 7, 0.30, 18)
CEIL_50 = 120 + 0.5 * SYN_NET


def _c(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


_clients = [10 * 1.5 ** t for t in range(5)]
_rev = [c * 0.120 for c in _clients]
_gm = [r * 0.70 for r in _rev]
_ebitda = [g - 1.2 for g in _gm]


MODULES_B = [
    {
        "id": 5, "title": "Valorisation d'entreprise", "axis": "Finance & valorisation", "level": "Finance",
        "duration": "90 min", "lab": "valuation",
        "objective": "Passer de la performance opérationnelle à une fourchette de valeur défendable : EV, Equity Value, multiples et DCF.",
        "outcomes": [
            "Construire le pont Enterprise Value → Equity Value",
            "Choisir et normaliser des multiples (comparables, transactions)",
            "Construire un DCF et challenger la valeur terminale",
            "Présenter une fourchette de valeur (football field) et ses sensibilités",
        ],
        "sections": [
            {"title": "1. Enterprise Value vs Equity Value", "body": """
- **Enterprise Value (EV)** : valeur des opérations, indépendamment de la façon dont elles sont financées.
- **Equity Value** : part revenant aux actionnaires, après dette nette et autres ajustements.

```
Equity Value = EV − dette financière nette − éléments assimilés à de la dette + actifs non opérationnels
```

**Éléments assimilés à de la dette** : provisions retraites, passifs de restructuration, dettes fiscales anormales, earn-outs, leasing selon les normes comptables. **Actifs non opérationnels** : immobilier non utilisé, participations minoritaires, excès de trésorerie. Le pont EV → Equity est souvent le sujet le plus négocié en fin de transaction.
"""},
            {"title": "2. La méthode des multiples", "body": """
On applique à l'agrégat financier de la cible un multiple observé sur des **comparables** :

| Multiple | Usage | Précaution |
|---|---|---|
| **EV / EBITDA** | Le plus courant en industrie | Normaliser l'EBITDA (éléments non récurrents, IFRS 16) |
| **EV / EBIT** | Activités à forte intensité capitalistique | Sensible aux politiques d'amortissement |
| **EV / CA** | Activités peu ou pas rentables, early stage | Ignore la structure de marges |
| **P/E** | Cotées stables, financières | Sensible à la structure financière |

Bonnes pratiques : choisir des comparables sur **activité, géographie, taille, croissance, marge** ; utiliser des multiples **cohérents** (même agrégat, même période, même périmètre) ; justifier chaque exclusion.
"""},
            {"title": "3. Comparables boursiers et transactions précédentes", "body": """
- **Comparables boursiers** : valeur de marché de pairs cotés ; reflète des positions minoritaires et liquides.
- **Transactions précédentes** : prix payés dans des opérations similaires ; incorporent une **prime de contrôle** et des synergies anticipées, mais datent et dépendent du contexte de marché.

Les deux se complètent : les transactions donnent une borne haute de ce que le marché a payé pour un contrôle ; les comparables, une vue de valorisation « de marché ». Un écart systématique doit être expliqué.
"""},
            {"title": "4. Le DCF (Discounted Cash-Flow)", "body": """
Étapes : (1) projeter les **free cash-flows** sur 5 à 10 ans ; (2) fixer le **WACC** ; (3) calculer la **valeur terminale** ; (4) actualiser ; (5) en déduire l'EV, puis l'Equity Value.

```
Valeur terminale (Gordon-Shapiro) = FCF_n × (1 + g) / (WACC − g)
EV = Σ FCF_t / (1 + WACC)^t  +  VT / (1 + WACC)^n
```

Points d'attention : la valeur terminale représente souvent **60 à 80 %** de l'EV ; le taux de croissance à l'infini *g* doit rester cohérent avec la croissance de long terme de l'économie ; le **FCF terminal** doit être normalisé (capex ≈ amortissements en régime de croisière).
"""},
            {"title": "5. Football field et sensibilités", "body": """
Une valorisation ne se résume pas à un chiffre : on présente une **fourchette** par méthode (comparables, transactions, DCF) sous forme de *football field*, puis on **triangule**. Les sensibilités clés du DCF sont **WACC × g** ; pour les multiples, la fourchette du multiple retenu.

Une bonne note de valorisation répond à quatre questions : sur quoi repose la valeur ? Quelle est la fourchette ? Quelles hypothèses la font bouger ? Où se situe le prix demandé par rapport à cette fourchette ?
"""},
        ],
        "key_points": [
            "EV = valeur des opérations ; Equity = EV − dette nette ± ajustements.",
            "Un multiple n'a de sens que sur un agrégat normalisé et un échantillon comparable.",
            "La valeur terminale domine le DCF : toujours la challenger.",
            "Présenter des fourchettes triangulées, jamais un chiffre unique.",
        ],
        "pitfalls": [
            "Oublier les éléments assimilés à de la dette dans le pont EV → Equity.",
            "Appliquer un multiple à un EBITDA non normalisé.",
            "Prendre g supérieur à la croissance de long terme raisonnable.",
            "Comparer des multiples calculés sur des périmètres différents.",
        ],
        "example": {
            "title": "Pont EV → Equity Value (cas pédagogique)",
            "body": "Cible : EBITDA normalisé **15 M€**, multiple **8x**, dette nette **35 M€**, passif assimilé à dette **4 M€**, actif non opérationnel **2 M€**.",
            "table": [
                {"Étape": "EV = 15 × 8", "M€": "120,0"},
                {"Étape": "− Dette financière nette", "M€": "−35,0"},
                {"Étape": "− Passif assimilé à dette", "M€": "−4,0"},
                {"Étape": "+ Actif non opérationnel", "M€": "+2,0"},
                {"Étape": "= Equity Value", "M€": _c(EQ_8X)},
                {"Étape": "Sensibilité 7x → 9x (Equity)", "M€": f"{_c(EQ_7X)} → {_c(EQ_9X)}"},
            ],
        },
        "exercises": [
            {"title": "Du multiple à l'Equity Value",
             "statement": "EBITDA normalisé **15 M€**, multiple **8x**, dette nette **35 M€**, passif assimilé à dette **4 M€**, actif non opérationnel **2 M€**. Quelle est l'**Equity Value (M€)** ?",
             "hint": "Equity = EV − dette nette − passif assimilé + actif non opérationnel.",
             "solution": f"EV = 120 M€ ; Equity = 120 − 35 − 4 + 2 = **{_c(EQ_8X)} M€**. À 7x : {_c(EQ_7X)} M€ ; à 9x : {_c(EQ_9X)} M€. Chaque tour de multiple vaut 15 M€ d'EV, soit environ 18 % de l'Equity Value : la négociation du multiple est donc déterminante.",
             "check": {"label": "Equity Value (M€)", "answer": EQ_8X, "tol": 0.2, "unit": "M€"}},
            {"title": "Sensibilité du multiple",
             "statement": "Avec les mêmes données, quelle serait l'**Equity Value à 9x** ?",
             "hint": "EV = 15 × 9 = 135 M€.",
             "solution": f"EV = 135 M€ ; Equity = 135 − 35 − 4 + 2 = **{_c(EQ_9X)} M€**.",
             "check": {"label": "Equity Value à 9x (M€)", "answer": EQ_9X, "tol": 0.2, "unit": "M€"}},
            {"title": "Mini DCF",
             "statement": "FCF année 1 : **10 M€**, croissance **5 %/an** pendant 5 ans, **WACC 9 %**, croissance terminale **2 %**. Quelle est l'**EV par DCF (M€)** ?",
             "hint": "Actualisez les 5 flux, puis la valeur terminale = FCF5 × 1,02 / (9 % − 2 %), actualisée sur 5 ans.",
             "solution": f"Somme des flux actualisés = {_c(sum(DCF_EX['pv_flows']))} M€ ; valeur terminale = {_c(DCF_EX['tv'])} M€, soit {_c(DCF_EX['pv_tv'])} M€ actualisés. **EV ≈ {_c(DCF_EX['ev'])} M€**. La valeur terminale pèse {DCF_EX['tv_share']*100:.0f} % de l'EV : c'est là qu'il faut challenger les hypothèses (g, FCF normatif).",
             "check": {"label": "EV DCF (M€)", "answer": round(DCF_EX["ev"], 2), "tol": 1.0, "unit": "M€"}},
        ],
        "quiz": [
            {"q": "À 8x un EBITDA de 15 M€, l'EV vaut…", "choices": ["120 M€", "23 M€", "8 M€"], "answer": 0, "why": "15 × 8 = 120 M€."},
            {"q": "Pour passer de l'EV à l'Equity Value, on…", "choices": ["Ajoute la dette nette", "Retranche la dette nette et les éléments assimilés", "Divise par le nombre d'actions"], "answer": 1, "why": "L'Equity Value revient aux actionnaires après les créanciers."},
            {"q": "Quel élément pèse souvent le plus dans un DCF ?", "choices": ["Les flux de l'année 1", "La valeur terminale", "Les impôts différés"], "answer": 1, "why": "Elle représente fréquemment 60 à 80 % de l'EV."},
            {"q": "Les multiples de transactions précédentes incluent généralement…", "choices": ["Une prime de contrôle", "Aucune synergie", "Uniquement des sociétés cotées"], "answer": 0, "why": "Le prix payé pour un contrôle reflète une prime et des synergies anticipées."},
            {"q": "Que faire avant d'appliquer un multiple d'EBITDA ?", "choices": ["Normaliser l'EBITDA", "Le diviser par deux", "Utiliser le résultat net"], "answer": 0, "why": "Éliminer les éléments non récurrents pour comparer ce qui est comparable."},
        ],
    },
    {
        "id": 6, "title": "Business plan & scénarios", "axis": "Finance & valorisation", "level": "Finance",
        "duration": "75 min", "lab": "bp",
        "objective": "Construire un business plan piloté par des drivers, trois scénarios et des sensibilités hiérarchisées.",
        "outcomes": [
            "Identifier les drivers de revenus, de coûts et de cash",
            "Relier P&L, bilan et cash-flow de façon cohérente",
            "Construire trois scénarios et hiérarchiser les sensibilités",
            "Challenger un business plan présenté par une BU",
        ],
        "sections": [
            {"title": "1. Partir des drivers, pas des formules", "body": """
Un business plan crédible se construit sur des **drivers explicites** :

- **Revenus** : volumes × prix (mix, nombre de clients × revenu moyen, capacité × taux d'utilisation).
- **Coûts** : variables (matières, énergie, logistique) vs fixes (effectifs, structure) ; inflation et productivité.
- **Cash** : capex (maintenance / croissance), BFR (jours de CA, de stocks), impôts.

Avant de modéliser, listez les drivers et pour chacun : **valeur de départ, trajectoire, source, justification**. Un modèle sans hypothèses documentées ne se challenge pas.
"""},
            {"title": "2. Cohérence des trois états", "body": """
Le **P&L**, le **bilan** et le **tableau de flux** doivent se réconcilier :

- la trésorerie de clôture du tableau de flux = trésorerie du bilan ;
- les capex alimentent les immobilisations ; les amortissements les réduisent ;
- la variation de BFR du tableau de flux = variation des postes du bilan.

Ajoutez des **contrôles automatiques** (bilan équilibré, trésorerie ≥ 0, ratios dans des bornes plausibles). Un modèle qui ne s'équilibre pas ne doit jamais circuler.
"""},
            {"title": "3. Scénarios et sensibilités", "body": """
Trois scénarios suffisent : **base**, **upside**, **downside**. Ils modifient les **hypothèses** (volumes, prix, capex), jamais les résultats à la main. Chaque scénario doit raconter une histoire cohérente (ex. downside : adoption plus lente *et* pression sur les prix).

Les **sensibilités** isolent l'effet d'une hypothèse sur un indicateur clé (VAN, EBITDA, FCF). Un diagramme *tornado* hiérarchise les hypothèses selon leur impact : concentrez le débat sur les 3 à 4 premières.
"""},
            {"title": "4. Challenger un business plan", "body": """
Grille de revue :

1. **Historique vs prévision** : la rupture de trajectoire est-elle expliquée ?
2. **Réalisme commercial** : parts de marché implicites, taux de conversion, cycle de vente.
3. **Réalisme industriel** : capacité, productivité, délais de montée en charge.
4. **Cash** : capex complet ? BFR cohérent avec la croissance ?
5. **Benchmark** : marges et ratios vs pairs.
6. **Risques** : où est le downside, qui porte les hypothèses les plus agressives ?
"""},
        ],
        "key_points": [
            "Les drivers d'abord, les formules ensuite.",
            "Les trois états se réconcilient, avec des contrôles intégrés.",
            "Les scénarios modifient des hypothèses, pas des résultats.",
            "Hiérarchiser les sensibilités concentre le débat sur ce qui compte.",
        ],
        "pitfalls": [
            "Courbe en « crosse de hockey » sans justification de la rupture.",
            "Oublier BFR et capex de croissance.",
            "Un scénario downside cosmétique (−5 % partout).",
            "Un modèle opaque, avec hypothèses codées en dur dans les formules.",
        ],
        "example": {
            "title": "Mini business plan : offre IA industrielle (hypothèses illustratives)",
            "body": "10 clients en année 1, croissance de **50 %/an** du nombre de clients, revenu moyen **120 k€**, marge brute **70 %**, coûts fixes **1,2 M€/an**.",
            "table": [
                {"Année": f"A{t+1}", "Clients": _c(_clients[t]), "CA (M€)": _c(_rev[t], 2), "Marge brute (M€)": _c(_gm[t], 2), "EBITDA (M€)": _c(_ebitda[t], 2)}
                for t in range(5)
            ],
        },
        "exercises": [
            {"title": "Revenu à l'année 3",
             "statement": "10 clients en année 1, croissance de **50 %/an** du nombre de clients, revenu moyen **120 k€** par client. Quel est le **CA de l'année 3 en M€** ?",
             "hint": "Clients A3 = 10 × 1,5² = 22,5.",
             "solution": "Clients A3 = 10 × 1,5² = 22,5 ; CA = 22,5 × 0,120 = **2,70 M€**.",
             "check": {"label": "CA année 3 (M€)", "answer": 2.7, "tol": 0.03, "unit": "M€"}},
            {"title": "Scénario downside",
             "statement": "Dans un scénario downside : revenu moyen **−10 %** et nombre de clients **−20 %** par rapport au base case de l'année 3. Quel est le **CA downside (M€)** ?",
             "hint": "2,70 × 0,9 × 0,8.",
             "solution": "CA downside = 2,70 × 0,90 × 0,80 = **1,94 M€**, soit −28 % vs base. Les effets prix et volume se **composent** : 0,9 × 0,8 = 0,72.",
             "check": {"label": "CA downside (M€)", "answer": 1.944, "tol": 0.03, "unit": "M€"}},
            {"title": "EBITDA de l'année 3",
             "statement": "Avec un CA base de **2,70 M€**, une marge brute de **70 %** et des coûts fixes de **1,2 M€**, quel est l'**EBITDA de l'année 3 (M€)** ?",
             "hint": "EBITDA = CA × marge brute − coûts fixes.",
             "solution": "EBITDA = 2,70 × 70 % − 1,2 = 1,89 − 1,2 = **0,69 M€** (marge d'EBITDA de 25,6 %). Levier opérationnel : à l'année 1, le même modèle était à −0,36 M€.",
             "check": {"label": "EBITDA A3 (M€)", "answer": 0.69, "tol": 0.03, "unit": "M€"}},
        ],
        "quiz": [
            {"q": "Un scénario downside cohérent modifie…", "choices": ["Les résultats finaux à la main", "Les drivers et hypothèses", "Uniquement la présentation"], "answer": 1, "why": "Les scénarios agissent sur les hypothèses ; les résultats en découlent."},
            {"q": "Quel contrôle est indispensable ?", "choices": ["La trésorerie du bilan = celle du tableau de flux", "Un CA en croissance", "Un EBITDA positif"], "answer": 0, "why": "La réconciliation des trois états garantit la cohérence du modèle."},
            {"q": "Un diagramme tornado sert à…", "choices": ["Hiérarchiser les hypothèses selon leur impact", "Calculer le WACC", "Présenter l'organigramme"], "answer": 0, "why": "Il identifie les hypothèses qui font bouger la décision."},
            {"q": "Une « crosse de hockey » non justifiée est…", "choices": ["Un signe de croissance saine", "Un signal d'alerte sur le réalisme du plan", "Un indicateur de BFR"], "answer": 1, "why": "Toute rupture de trajectoire doit être expliquée par un événement identifié."},
            {"q": "Le BFR dans un plan de forte croissance…", "choices": ["Peut consommer beaucoup de cash", "Est négligeable", "Diminue toujours"], "answer": 0, "why": "La croissance immobilise des stocks et des créances."},
        ],
    },
    {
        "id": 7, "title": "M&A & synergies", "axis": "M&A", "level": "M&A",
        "duration": "90 min", "lab": "synergies",
        "objective": "Évaluer le prix, les synergies et la faisabilité d'une opération, de la thèse d'investissement à l'intégration.",
        "outcomes": [
            "Formuler une thèse d'acquisition et la comparer aux alternatives",
            "Décrire le processus M&A et le rôle de la due diligence",
            "Valoriser les synergies nettes et en déduire une logique de prix plafond",
            "Comprendre structuration, goodwill, TSA et intégration",
        ],
        "sections": [
            {"title": "1. Pourquoi acquérir ? Thèse et alternatives", "body": """
Une acquisition n'est justifiée que si elle **crée plus de valeur** que les alternatives (organique, partenariat, JV). Les thèses classiques :

- **Accès à des capacités** (technologie, savoir-faire, données) plus vite ou moins cher qu'en les construisant.
- **Consolidation** : échelle, densité, parts de marché.
- **Intégration verticale** : sécuriser l'amont ou l'aval.
- **Nouvelles géographies** ou **diversification**.

Test de robustesse : *qu'apportons-nous que le vendeur ou un autre acquéreur ne peut pas apporter ?* C'est l'**avantage propriétaire** qui justifie de payer une prime.
"""},
            {"title": "2. Le processus M&A", "body": """
| Phase | Objectif | Livrables typiques |
|---|---|---|
| **Stratégie & screening** | Définir critères, identifier les cibles | Shortlist, fiches cibles |
| **Approche & NDA** | Ouvrir la discussion, accéder à l'information | Info-mémo, premiers échanges |
| **Offre indicative** | Positionner une fourchette de valeur | Valorisation, thèse, conditions |
| **Due diligence** | Vérifier : financière, juridique, fiscale, commerciale, opérationnelle, IT, RSE | Rapports, red flags, ajustements de prix |
| **Offre ferme & SPA** | Négocier et signer | Contrat, garanties, conditions suspensives |
| **Closing & J0** | Transférer le contrôle | Plan de J0, TSA |
| **Intégration (PMI)** | Capturer les synergies | Plan 100 jours, suivi des synergies |

Les décisions d'investissement se prennent sur la base d'un **dossier structuré** (thèse, valorisation, risques, plan d'intégration) examiné en comité.
"""},
            {"title": "3. Valoriser les synergies et fixer un prix plafond", "body": """
Trois familles de synergies : **de coûts** (achats, industriel, fonctions support), **de revenus** (cross-selling, nouveaux marchés), **financières** (coût du capital, fiscalité). Les synergies de coûts sont plus fiables que celles de revenus.

Valeur nette simplifiée des synergies :

```
Valeur nette = synergies run-rate × multiple × (1 − risque d'exécution) − coûts one-off
```

(Simplification pédagogique ; en pratique on actualise des flux phasés.)

**Prix plafond** : valeur autonome de la cible + **quote-part** des synergies nettes que l'acheteur accepte de céder au vendeur. Payer 100 % des synergies, c'est transférer toute la valeur au vendeur et ne conserver que le risque.
"""},
            {"title": "4. Structuration, goodwill et garanties", "body": """
- **Mode de paiement** : cash, dette, titres ; **earn-out** (complément de prix lié à la performance) pour partager le risque ; **escrow** / garantie de passif.
- **Goodwill** (écart d'acquisition) = prix payé − juste valeur des actifs nets identifiables. Il est testé annuellement pour dépréciation : un goodwill important sur un plan trop optimiste est un risque comptable.
- **Alternatives de structure** : prise de participation minoritaire, **JV**, option d'achat différée.

La structure d'une transaction répartit risques et valeur : elle se négocie autant que le prix.
"""},
            {"title": "5. Séparation, TSA et intégration : là où la valeur se perd", "body": """
Dans une acquisition d'activité (carve-out), la séparation du système d'information et des fonctions support est une source majeure de **coûts de séparation**, de **dis-synergies** et de risque opérationnel. Les **TSA** (*Transitional Service Agreements*) organisent la continuité de service pendant la transition, avec un calendrier de sortie.

*Votre atout différenciant* : maîtriser ces sujets (autonomie juridique, modèle opérationnel cible, TSA, plan J0 / 100 jours) permet de chiffrer des coûts et délais que beaucoup de dossiers sous-estiment – un argument fort pour fiabiliser un business case d'acquisition.
"""},
        ],
        "key_points": [
            "Une acquisition se compare toujours aux alternatives de croissance.",
            "Les synergies se valorisent nettes de risque et de coûts de réalisation.",
            "Le prix plafond partage les synergies, il ne les cède pas intégralement.",
            "La séparation et l'intégration conditionnent la capture de valeur.",
        ],
        "pitfalls": [
            "Payer des synergies de revenus incertaines comme si elles étaient acquises.",
            "Sous-estimer les coûts de séparation et la durée des TSA.",
            "Ignorer l'avantage propriétaire : payer une prime sans différenciation.",
            "Négliger le risque de goodwill sur un plan trop optimiste.",
        ],
        "example": {
            "title": "Cas : prix plafond avec synergies (hypothèses pédagogiques)",
            "body": "EV autonome **120 M€** ; synergies run-rate **8 M€**, capitalisées à **7x** ; risque d'exécution **30 %** ; coûts one-off **18 M€**.",
            "table": [
                {"Élément": "Synergies capitalisées (8 × 7)", "M€": "56,0"},
                {"Élément": "Après risque d'exécution (× 70 %)", "M€": "39,2"},
                {"Élément": "− Coûts one-off d'intégration", "M€": "−18,0"},
                {"Élément": "= Valeur nette des synergies", "M€": _c(SYN_NET)},
                {"Élément": "Prix plafond si 50 % cédés au vendeur", "M€": _c(CEIL_50)},
                {"Élément": "Prix maximum théorique (100 % cédés)", "M€": _c(120 + SYN_NET)},
            ],
        },
        "exercises": [
            {"title": "Valeur nette des synergies",
             "statement": "Synergies run-rate **8 M€**, multiple **7x**, risque d'exécution **30 %**, coûts one-off **18 M€**. Quelle est la **valeur nette des synergies (M€)** ?",
             "hint": "8 × 7 × (1 − 30 %) − 18.",
             "solution": f"56 × 70 % = 39,2 ; 39,2 − 18 = **{_c(SYN_NET)} M€**. Sans la prise en compte du risque et des coûts one-off, on aurait cru à 56 M€ : plus de 2,5 fois la valeur réelle.",
             "check": {"label": "Valeur nette (M€)", "answer": SYN_NET, "tol": 0.2, "unit": "M€"}},
            {"title": "Prix plafond",
             "statement": "EV autonome **120 M€**. L'acheteur accepte de céder **50 %** de la valeur nette des synergies (21,2 M€). Quel est le **prix plafond (M€)** ?",
             "hint": "120 + 50 % × 21,2.",
             "solution": f"Prix plafond = 120 + 0,5 × 21,2 = **{_c(CEIL_50)} M€**. L'acheteur conserve 10,6 M€ de valeur nette en contrepartie du risque d'exécution. Une première offre se positionnerait plus bas (autour de la valeur autonome) pour garder une marge de négociation.",
             "check": {"label": "Prix plafond (M€)", "answer": CEIL_50, "tol": 0.2, "unit": "M€"}},
            {"title": "Goodwill",
             "statement": "Prix payé **130 M€** ; juste valeur des actifs nets identifiables **80 M€**. Quel est le **goodwill (M€)** ?",
             "hint": "Goodwill = prix − juste valeur des actifs nets identifiables.",
             "solution": "Goodwill = 130 − 80 = **50 M€**, soit 38 % du prix. À surveiller : il sera testé annuellement ; si les synergies attendues ne se matérialisent pas, une dépréciation peut intervenir.",
             "check": {"label": "Goodwill (M€)", "answer": 50.0, "tol": 0.2, "unit": "M€"}},
        ],
        "quiz": [
            {"q": "Une synergie run-rate doit être…", "choices": ["Considérée comme immédiate", "Phasée et ajustée du risque d'exécution", "Toujours cédée au vendeur"], "answer": 1, "why": "Le calendrier de capture et le risque conditionnent la valeur réelle."},
            {"q": "Le prix plafond d'une acquisition…", "choices": ["Est égal à la valeur autonome + 100 % des synergies", "Partage les synergies nettes entre acheteur et vendeur", "Ne dépend que du multiple du vendeur"], "answer": 1, "why": "L'acheteur doit conserver une part de valeur pour rémunérer le risque."},
            {"q": "Un earn-out permet de…", "choices": ["Partager le risque de performance avec le vendeur", "Réduire la dette de la cible", "Éviter la due diligence"], "answer": 0, "why": "Une partie du prix dépend de la performance future."},
            {"q": "Un TSA sert à…", "choices": ["Garantir la continuité des services pendant la transition", "Financer l'acquisition", "Valoriser les synergies"], "answer": 0, "why": "Il encadre les services fournis par le vendeur après le closing, avec un plan de sortie."},
            {"q": "Quelle synergie est en général la plus fiable ?", "choices": ["Synergies de revenus", "Synergies de coûts", "Synergies fiscales exotiques"], "answer": 1, "why": "Les coûts sont plus maîtrisables que les comportements clients."},
        ],
    },
]
