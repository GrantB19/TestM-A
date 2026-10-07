"""Modules 1 à 4 : diagnostic stratégique, marché & concurrence, états financiers, création de valeur."""
from finance import npv, irr, payback, cagr

_A = [-3.0] + [0.9] * 5
_B = [-5.0] + [1.35] * 5
NPV_A, NPV_B = npv(0.09, _A), npv(0.09, _B)
IRR_A, IRR_B = irr(_A), irr(_B)
PB_A, PB_B = payback(_A), payback(_B)
PI_A, PI_B = NPV_A / 3.0, NPV_B / 5.0
CAGR_EX = cagr(120, 190, 4)


def _c(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


MODULES_A = [
    {
        "id": 1, "title": "Diagnostic stratégique", "axis": "Diagnostic stratégique", "level": "Fondamentaux",
        "duration": "60 min", "lab": "market",
        "objective": "Transformer une analyse en décision : structurer une fact base et formuler des options comparables.",
        "outcomes": [
            "Formuler une décision stratégique avec la structure Situation – Complication – Question",
            "Choisir le bon outil (PESTEL, 5 forces, chaîne de valeur, matrice) pour la bonne question",
            "Construire une fact base : faits sourcés, hypothèses, implications",
            "Passer d'un diagnostic à 2-3 options MECE et à une recommandation",
        ],
        "sections": [
            {"title": "1. Une analyse sert une décision", "body": """
Une analyse stratégique n'est pas un exercice académique : elle sert à **éclairer une décision**. Avant d'ouvrir un framework, écrivez la décision attendue en une phrase, avec la structure **SCQ** :

- **Situation** : ce qui est établi et partagé par tous.
- **Complication** : ce qui change, bloque ou crée une tension.
- **Question** : la décision à arbitrer, formulée de façon fermée (« faut-il… et comment ? »).

**Exemple d'école** – *Situation* : le groupe souhaite renforcer sa présence sur un segment à forte croissance. *Complication* : ses capacités actuelles ne couvrent qu'une partie de la chaîne de valeur. *Question* : faut-il investir, et par quel mode (organique, partenariat, JV, acquisition) ?

Une bonne question de décision est **bornée** (périmètre, horizon), **arbitrable** (il existe plusieurs réponses possibles) et **partagée** avec le commanditaire avant de démarrer les travaux.
"""},
            {"title": "2. Un outil = une question", "body": """
Les frameworks ne sont pas des formulaires à remplir. Chacun répond à une question précise :

| Question à traiter | Outil adapté | Livrable attendu |
|---|---|---|
| Quels changements externes peuvent modifier la donne ? | **PESTEL** | 5 à 6 facteurs hiérarchisés par impact × probabilité |
| Le secteur est-il structurellement attractif ? | **5 forces de Porter** | Intensité de chaque force + conclusion sur la rentabilité attendue |
| D'où vient (ou pourrait venir) l'avantage compétitif ? | **Chaîne de valeur**, ressources & capacités | Activités où l'on est meilleur / moins bon que les pairs |
| Où se situe l'activité dans le portefeuille ? | **Matrice attractivité × position compétitive** | Positionnement et rôle (croître, sélectionner, récolter, céder) |
| Comment synthétiser le diagnostic ? | **SWOT** | 1 page, construite *après* l'analyse – jamais avant |

Règle pratique : si vous ne pouvez pas dire quelle question un outil tranche, ne l'utilisez pas.
"""},
            {"title": "3. Construire une fact base solide", "body": """
La **fact base** est le socle factuel du diagnostic : description de l'activité et du marché, risques et opportunités, enjeux clés.

Pour chaque élément, tracez systématiquement : **source, date, périmètre, unité**. Puis séparez trois niveaux :

1. **Fait** – vérifiable et sourcé (« le volume vendu a progressé de 4 % en 2025, source : reporting interne »).
2. **Hypothèse** – plausible mais à valider (« le segment devrait croître de 8 % par an »).
3. **Interprétation** – votre lecture (« nous perdons en compétitivité »).

Pour les chiffres structurants, **triangulez** : au moins deux sources indépendantes, ou deux méthodes de calcul. Chaque fait doit se terminer par un **so what** : qu'est-ce que cela change pour la décision ?
"""},
            {"title": "4. Du diagnostic à la recommandation", "body": """
Une démarche classique de planification stratégique enchaîne trois étapes :

1. **Fact base** : diagnostic du positionnement (attractivité du marché, compétitivité) et enjeux clés.
2. **Scénarios financiarisés** : un scénario de **continuité** (sans changement majeur de périmètre ni d'investissement) + 1 ou 2 scénarios alternatifs (croissance, repositionnement, désinvestissement), chiffrés.
3. **Plan de management** : plan d'actions, jalons, KPIs et gouvernance d'exécution du scénario retenu.

Le scénario de continuité est indispensable : il sert de **référence** pour mesurer la valeur réellement créée par les alternatives.

Pour présenter la recommandation, appliquez le **principe de la pyramide** : la réponse d'abord, puis 3 arguments maximum, puis les preuves. Les options doivent être **MECE** (mutuellement exclusives, collectivement exhaustives) et comparées sur les mêmes critères.
"""},
        ],
        "key_points": [
            "Une analyse sans décision est un exercice de style.",
            "Un outil = une question ; la SWOT vient en synthèse, jamais en point de départ.",
            "Faits, hypothèses et interprétations sont toujours séparés et sourcés.",
            "Un scénario de continuité sert de référence pour valoriser les alternatives.",
        ],
        "pitfalls": [
            "Remplir des matrices pour « faire sérieux » sans conclusion.",
            "SWOT = liste de platitudes non hiérarchisées.",
            "Options « homme de paille » ajoutées uniquement pour faire ressortir la préférée.",
            "Chiffres sans source, sans date ou sans périmètre.",
            "Oublier le so what : l'analyse décrit mais ne recommande pas.",
        ],
        "example": {
            "title": "Du fait à l'action : lecture d'un diagnostic (données illustratives)",
            "body": "Les chiffres ci-dessous sont **fictifs** et servent uniquement à illustrer le raisonnement fait → so what → action.",
            "table": [
                {"Fait (illustratif)": "Le segment cible croît de 10 %/an contre 3 %/an pour le marché global", "Niveau": "Hypothèse à trianguler", "So what": "Ne pas investir a un coût d'opportunité croissant", "Action": "Chiffrer un scénario de croissance"},
                {"Fait (illustratif)": "Notre taux d'utilisation des capacités est de 92 %", "Niveau": "Fait (reporting interne)", "So what": "La croissance organique est contrainte sans investissement", "Action": "Évaluer capex vs partenariat"},
                {"Fait (illustratif)": "Deux concurrents ont annoncé des acquisitions", "Niveau": "Fait (communiqués)", "So what": "La fenêtre d'accès aux cibles se referme", "Action": "Prioriser un screening de cibles"},
            ],
        },
        "exercises": [
            {"title": "Formuler la décision (SCQ)",
             "statement": "Un groupe agro-industriel envisage d'accélérer dans les protéines végétales. Rédigez la décision en **Situation – Complication – Question**, puis listez **3 faits** (avec type : fait / hypothèse) à collecter en priorité.",
             "hint": "La question doit être arbitrable et inclure le *mode* d'accélération, pas seulement le *quoi*.",
             "solution": """**Corrigé modèle**

- **Situation** : le groupe a identifié les protéines végétales comme axe de croissance prioritaire et dispose de positions industrielles amont.
- **Complication** : ses capacités de transformation et d'accès client ne couvrent qu'une partie des segments à plus forte croissance ; le rythme de consolidation du secteur réduit la fenêtre d'entrée.
- **Question** : *faut-il investir pour accélérer sur ce segment d'ici 2030 et, si oui, par quel mode (organique, partenariat, JV, acquisition) ?*

**3 faits à collecter** : (1) croissance et taille du segment par sous-marché – *fait/hypothèse sourcée* ; (2) capacité utilisée et capex nécessaire – *fait interne* ; (3) cibles / partenaires potentiels et leur valorisation – *fait de marché*.""",
             "check": None},
            {"title": "Comparer des options",
             "statement": "Proposez **2 options réellement distinctes** pour la question précédente, **3 critères** de choix pondérés (total 100 %) et formulez une **recommandation provisoire** en 2 phrases.",
             "hint": "Vitesse, capital mobilisé, contrôle, risque d'exécution et accès aux capacités sont des critères classiques.",
             "solution": """**Corrigé modèle**

- **Option A – Croissance organique** : extension de capacité interne.
- **Option B – Partenariat / JV** avec un acteur disposant des capacités manquantes.

| Critère | Poids | A | B |
|---|---|---|---|
| Vitesse d'accès au marché | 35 % | 2 | 4 |
| Capital mobilisé | 25 % | 2 | 4 |
| Contrôle | 20 % | 5 | 3 |
| Risque d'exécution | 20 % | 3 | 3 |

Score A = 0,35×2 + 0,25×2 + 0,20×5 + 0,20×3 = **2,8** ; score B = 0,35×4 + 0,25×4 + 0,20×3 + 0,20×3 = **3,6**.

**Recommandation provisoire** : privilégier la JV, qui accélère l'accès au marché avec moins de capital, sous réserve d'une gouvernance préservant le contrôle des décisions stratégiques. À valider par une due diligence partenaire.""",
             "check": None},
        ],
        "quiz": [
            {"q": "Quel est le meilleur point de départ d'une analyse stratégique ?", "choices": ["Remplir une matrice SWOT", "Formuler la décision à éclairer", "Lister tous les concurrents"], "answer": 1, "why": "Le cadre d'analyse est dicté par la décision, pas l'inverse."},
            {"q": "À quoi sert la SWOT dans une démarche rigoureuse ?", "choices": ["À collecter les données", "À synthétiser un diagnostic déjà réalisé", "À remplacer l'analyse financière"], "answer": 1, "why": "La SWOT synthétise ; utilisée en premier, elle produit des platitudes."},
            {"q": "Les 5 forces de Porter permettent d'évaluer…", "choices": ["L'attractivité structurelle d'un secteur", "La performance d'un manager", "La valeur d'une entreprise"], "answer": 0, "why": "Elles analysent l'intensité concurrentielle et le pouvoir de négociation, donc la rentabilité attendue du secteur."},
            {"q": "Laquelle de ces affirmations est un FAIT au sens de la fact base ?", "choices": ["Le marché est mature", "Le volume vendu a progressé de 4 % en 2025 (source : reporting interne)", "Nos concurrents sont meilleurs que nous"], "answer": 1, "why": "Un fait est vérifiable, sourcé, daté et chiffré. Les deux autres sont des interprétations."},
            {"q": "Pourquoi inclure un scénario de continuité ?", "choices": ["Pour rassurer le comité", "Pour servir de référence et mesurer la valeur créée par les alternatives", "Pour réduire le nombre de scénarios"], "answer": 1, "why": "Sans référence, impossible de savoir ce que les alternatives apportent réellement."},
        ],
    },
    {
        "id": 2, "title": "Marché & concurrence", "axis": "Diagnostic stratégique", "level": "Fondamentaux",
        "duration": "60 min", "lab": "market",
        "objective": "Dimensionner un marché (TAM, SAM, SOM), mesurer sa croissance et cartographier la concurrence.",
        "outcomes": [
            "Distinguer TAM, SAM et SOM et construire un market sizing bottom-up",
            "Réconcilier approche top-down et bottom-up",
            "Calculer et interpréter un CAGR",
            "Construire un competitive landscape décisionnel",
        ],
        "sections": [
            {"title": "1. TAM, SAM, SOM", "body": """
Trois niveaux, de la demande théorique à la part réellement capturable :

- **TAM** (*Total Addressable Market*) : demande totale si 100 % des clients concernés achetaient la solution.
- **SAM** (*Serviceable Available Market*) : part du TAM que votre offre, votre géographie et votre modèle commercial permettent réellement d'adresser.
- **SOM** (*Serviceable Obtainable Market*) : part du SAM réalistement capturable à un horizon donné, compte tenu de la concurrence et de vos capacités.

```
TAM  =  nombre de clients × volume moyen par client × prix moyen
SAM  =  TAM × % adressable (périmètre, maturité, canal)
SOM  =  SAM × part de marché réaliste à N ans
```

Le SOM est le chiffre qui compte pour un business plan : c'est lui qui doit être cohérent avec les capacités commerciales et industrielles.
"""},
            {"title": "2. Top-down, bottom-up et triangulation", "body": """
- **Top-down** : on part d'un grand agrégat sectoriel (études, statistiques) et on réduit par segment. Rapide mais dépendant de la qualité de la source.
- **Bottom-up** : on part des unités élémentaires (sites, clients, volumes) et on multiplie par le prix. Plus robuste car chaque hypothèse est explicite.

La bonne pratique est de **faire les deux** et de comparer : un écart important (par exemple supérieur à 30 %) signale une hypothèse à revisiter. Documentez systématiquement le **périmètre** (géographie, segments), l'**unité** (M€, tonnes) et l'**année de référence**.
"""},
            {"title": "3. Croissance et CAGR", "body": """
Le taux de croissance annuel composé (**CAGR**) lisse la croissance sur plusieurs années :

```
CAGR = (valeur finale / valeur initiale) ^ (1 / nombre d'années) − 1
```

Décomposez toujours la croissance en **volume**, **prix** et **mix** : une croissance portée uniquement par les prix n'a pas les mêmes implications qu'une croissance en volumes. Analysez aussi la **cyclicité** et les **ruptures** (réglementation, technologie) qui rendent l'extrapolation du passé dangereuse.
"""},
            {"title": "4. Cartographier la concurrence", "body": """
Un competitive landscape utile ne liste pas des logos : il explique **qui gagne, où et pourquoi**.

| Dimension | Questions |
|---|---|
| Proposition de valeur | Quel besoin client, quel positionnement prix / qualité ? |
| Segments & géographies | Où est présent chaque acteur, avec quelle part de marché ? |
| Capacités critiques | Technologie, accès matières, réseau commercial, échelle industrielle |
| Économie | Marges, intensité capitalistique, structure de coûts |
| Barrières à l'entrée | Capital, savoir-faire, accès client, réglementation |

Regroupez les acteurs en **groupes stratégiques** (échelle, modèle, géographie) pour identifier les espaces concurrentiels libres et les consolidateurs probables.
"""},
        ],
        "key_points": [
            "Le SOM, pas le TAM, alimente le business plan.",
            "Bottom-up et top-down se confrontent : l'écart révèle les hypothèses fragiles.",
            "Le CAGR lisse ; toujours décomposer volume / prix / mix.",
            "Un benchmark concurrentiel doit conclure sur « qui gagne et pourquoi ».",
        ],
        "pitfalls": [
            "Annoncer un TAM mondial gigantesque sans passer par le SAM et le SOM.",
            "Mélanger des périmètres ou des années de référence.",
            "Un seul chiffre sans fourchette ni sensibilité.",
            "Citer des parts de marché sans définir le marché.",
        ],
        "example": {
            "title": "Market sizing bottom-up (hypothèses illustratives)",
            "body": "Solution de vision par ordinateur pour lignes de production agroalimentaires – hypothèses **fictives** pour illustrer la méthode.",
            "table": [
                {"Étape": "Sites cibles", "Hypothèse": "2 000 sites", "Résultat": "2 000"},
                {"Étape": "Sites avec lignes pertinentes", "Hypothèse": "40 %", "Résultat": "800 sites"},
                {"Étape": "Lignes équipables", "Hypothèse": "2 lignes / site", "Résultat": "1 600 lignes"},
                {"Étape": "TAM", "Hypothèse": "50 k€ / ligne / an", "Résultat": "80 M€"},
                {"Étape": "SAM", "Hypothèse": "30 % adressable (maturité, canal)", "Résultat": "24 M€"},
                {"Étape": "SOM à 3 ans", "Hypothèse": "10 % du SAM", "Résultat": "2,4 M€"},
            ],
        },
        "exercises": [
            {"title": "Calculer le SOM",
             "statement": "Hypothèses : **1 200 sites**, **3 lignes** équipables par site, **45 k€** par ligne et par an. SAM = **35 %** du TAM. SOM à 3 ans = **8 %** du SAM. Quel est le **SOM en M€** ?",
             "hint": "TAM = 1 200 × 3 × 45 k€ = 162 M€ ; puis appliquez les deux pourcentages.",
             "solution": "TAM = 1 200 × 3 × 45 k€ = **162 M€** → SAM = 162 × 35 % = **56,7 M€** → SOM = 56,7 × 8 % = **4,54 M€**. Lecture : le SOM représente environ 2,8 % du TAM ; un business plan doit s'appuyer sur ce chiffre, pas sur le TAM.",
             "check": {"label": "SOM (M€)", "answer": 4.536, "tol": 0.1, "unit": "M€"}},
            {"title": "Calculer un CAGR",
             "statement": "Un marché passe de **120 M€** à **190 M€** en **4 ans**. Quel est le **CAGR en %** ?",
             "hint": "(190 / 120)^(1/4) − 1.",
             "solution": f"(190 / 120)^(1/4) − 1 = **{_c(CAGR_EX*100, 1)} %** par an. À comparer au CAGR du marché global et à la croissance de vos propres volumes pour juger de la dynamique relative.",
             "check": {"label": "CAGR (%)", "answer": round(CAGR_EX * 100, 2), "tol": 0.2, "unit": "%"}},
            {"title": "Competitive landscape",
             "statement": "Listez **4 dimensions** de comparaison pour un benchmark concurrentiel et identifiez, pour un marché de votre choix, **2 groupes stratégiques**.",
             "hint": "Pensez échelle, modèle économique, géographie, capacités critiques.",
             "solution": "**Dimensions** : proposition de valeur, segments & géographies, capacités critiques (technologie, accès matières, réseau), économie (marges, capex/EBITDA). **Groupes stratégiques (exemple)** : (1) consolidateurs globaux, intégrés, à forte échelle industrielle ; (2) spécialistes de niche, agiles, à forte valeur ajoutée mais capacités limitées. Conclusion attendue : quels espaces sont libres et qui est un partenaire / une cible plausible.",
             "check": None},
        ],
        "quiz": [
            {"q": "Que représente le SOM ?", "choices": ["La demande mondiale théorique", "Le marché adressable par l'offre", "La part réalistement capturable à un horizon donné"], "answer": 2, "why": "Le SOM intègre concurrence et capacités d'exécution."},
            {"q": "Un bon market sizing…", "choices": ["Repose sur une seule source officielle", "Compare plusieurs approches et explicite ses hypothèses", "Évite les fourchettes"], "answer": 1, "why": "La triangulation renforce la crédibilité."},
            {"q": "Un marché passe de 100 à 121 M€ en 2 ans. Le CAGR est de…", "choices": ["10 %", "21 %", "11 %"], "answer": 0, "why": "(121/100)^(1/2) − 1 = 10 %."},
            {"q": "Une croissance de marché due uniquement aux hausses de prix signale…", "choices": ["Une demande en volume dynamique", "Qu'il faut analyser la soutenabilité et la répercussion des prix", "Une barrière à l'entrée forte"], "answer": 1, "why": "Toujours décomposer volume / prix / mix."},
            {"q": "Un écart de 40 % entre top-down et bottom-up indique…", "choices": ["Que le top-down a forcément raison", "Une hypothèse à revisiter dans l'une des deux méthodes", "Qu'il faut retenir la moyenne"], "answer": 1, "why": "L'écart est un signal de contrôle, pas un chiffre à moyenner."},
        ],
    },
    {
        "id": 3, "title": "Lire les états financiers", "axis": "Finance & valorisation", "level": "Finance",
        "duration": "75 min", "lab": "ratios",
        "objective": "Relier compte de résultat, bilan et cash-flow pour diagnostiquer rentabilité, cash et solidité financière.",
        "outcomes": [
            "Lire la cascade du compte de résultat et ses leviers (volume, prix, mix, coûts)",
            "Comprendre le BFR et calculer DSO, DIO, DPO",
            "Reconstituer un free cash-flow et mesurer la conversion cash",
            "Identifier les signaux faibles dans un jeu d'états financiers",
        ],
        "sections": [
            {"title": "1. Le compte de résultat : de la marge au résultat net", "body": """
```
Chiffre d'affaires
 − coûts directs                     = Marge brute
 − charges opérationnelles           = EBITDA (EBE)
 − amortissements & dépréciations    = EBIT (résultat d'exploitation)
 − charges financières, impôts       = Résultat net
```

Questions clés : la croissance vient-elle du **volume**, du **prix** ou du **mix** ? La marge brute progresse-t-elle plus vite que le CA ? Les charges fixes sont-elles maîtrisées ? Quelle part du résultat est **récurrente** ?

L'**EBITDA** est un indicateur de performance opérationnelle avant amortissements ; ce n'est **pas** du cash disponible : il ignore le BFR, les capex, les impôts et le service de la dette.
"""},
            {"title": "2. Le bilan : capitaux employés et BFR", "body": """
Vue économique simplifiée :

```
Capitaux employés = Actifs immobilisés + BFR
Financés par      = Capitaux propres + Dette nette
```

Le **BFR** (besoin en fonds de roulement) mesure le cash immobilisé dans le cycle d'exploitation :

```
BFR = Stocks + Créances clients − Dettes fournisseurs
```

Trois ratios en jours : **DSO** (créances / CA × 365), **DIO** (stocks / coûts des ventes × 365), **DPO** (dettes fournisseurs / achats × 365). Une croissance rentable peut consommer beaucoup de cash si le BFR dérive.
"""},
            {"title": "3. Le cash-flow : de l'EBITDA au free cash-flow", "body": """
```
FCF = EBITDA − impôts cash − variation de BFR − CAPEX
Conversion cash = FCF / EBITDA
```

Distinguez les **capex de maintenance** (maintien de l'outil) des **capex de croissance** (nouvelle capacité). Un EBITDA élevé avec un FCF faible signale souvent un secteur capitalistique ou un BFR sous tension.

Le **levier** = dette nette / EBITDA mesure la capacité de remboursement ; il doit toujours être lu avec la visibilité sur les flux futurs (cyclicité, contrats).
"""},
            {"title": "4. Les ratios à connaître", "body": """
| Ratio | Formule | Ce qu'il dit |
|---|---|---|
| Marge d'EBITDA | EBITDA / CA | Profitabilité opérationnelle |
| Conversion cash | FCF / EBITDA | Part de l'EBITDA transformée en cash libre |
| Levier | Dette nette / EBITDA | Capacité d'endettement et solidité |
| ROCE | NOPAT / capitaux employés | Rentabilité du capital engagé |
| DSO / DIO / DPO | en jours | Qualité du cycle d'exploitation |
| Couverture des intérêts | EBIT / charges financières | Aisance du service de la dette |
"""},
            {"title": "5. Signaux faibles à repérer", "body": """
- DSO ou DIO en hausse alors que le CA est stable (créances ou stocks de moindre qualité).
- Marge brute en baisse masquée par une baisse des charges fixes.
- Capex durablement inférieur aux amortissements (sous-investissement).
- Dette court terme élevée ou levier proche des covenants.
- Résultats portés par des éléments non récurrents (cessions, reprises de provisions).
- Écart croissant entre résultat net et flux de trésorerie opérationnel.
"""},
        ],
        "key_points": [
            "EBITDA ≠ cash : toujours descendre jusqu'au free cash-flow.",
            "Le BFR est le premier consommateur de cash dans une croissance rapide.",
            "Lire les trois états ensemble : un chiffre isolé ne dit rien.",
            "Les signaux faibles se trouvent dans les écarts entre résultat et cash.",
        ],
        "pitfalls": [
            "Confondre EBITDA et cash-flow.",
            "Comparer des ratios sans homogénéiser les définitions (IFRS 16, éléments non récurrents).",
            "Ignorer la saisonnalité du BFR (clôture à un point haut ou bas).",
            "Juger la dette sur le montant sans la rapporter à l'EBITDA.",
        ],
        "example": {
            "title": "Cas : société cible – CA 120 M€, EBITDA 15 M€",
            "body": "Impôts cash 3 M€, hausse du BFR 4 M€, CAPEX 7 M€.",
            "table": [
                {"Poste": "EBITDA", "M€": "15,0"},
                {"Poste": "− Impôts cash", "M€": "−3,0"},
                {"Poste": "− Variation du BFR", "M€": "−4,0"},
                {"Poste": "− CAPEX", "M€": "−7,0"},
                {"Poste": "= Free cash-flow", "M€": "1,0"},
                {"Poste": "Marge d'EBITDA", "M€": "12,5 %"},
                {"Poste": "Conversion cash (FCF / EBITDA)", "M€": "6,7 %"},
            ],
        },
        "exercises": [
            {"title": "Calculer le free cash-flow",
             "statement": "EBITDA **15 M€**, impôts cash **3 M€**, hausse du BFR **4 M€**, CAPEX **7 M€**. Quel est le **FCF en M€** ?",
             "hint": "FCF = EBITDA − impôts − ΔBFR − CAPEX.",
             "solution": "FCF = 15 − 3 − 4 − 7 = **1 M€**. Conversion cash = 1 / 15 = **6,7 %**. Lecture : malgré une marge d'EBITDA de 12,5 %, l'entreprise génère très peu de cash – à investiguer : capex de croissance ? dérive du BFR ? Cela pèsera sur la capacité de désendettement et sur la valorisation DCF.",
             "check": {"label": "FCF (M€)", "answer": 1.0, "tol": 0.05, "unit": "M€"}},
            {"title": "Calculer le DSO",
             "statement": "Créances clients **24 M€** pour un chiffre d'affaires de **120 M€**. Quel est le **DSO en jours** (année de 365 jours) ?",
             "hint": "DSO = créances / CA × 365.",
             "solution": "DSO = 24 / 120 × 365 = **73 jours**. À comparer aux conditions de paiement contractuelles : un DSO supérieur au délai contractuel signale des retards de paiement ou des litiges.",
             "check": {"label": "DSO (jours)", "answer": 73.0, "tol": 1.0, "unit": "jours"}},
            {"title": "Calculer le levier",
             "statement": "Dette nette **35 M€**, EBITDA **15 M€**. Quel est le **levier** (dette nette / EBITDA, en x) ?",
             "hint": "35 / 15.",
             "solution": "Levier = 35 / 15 = **2,33x**. Niveau généralement jugé confortable pour une activité stable, mais à lire avec la cyclicité, le FCF (ici très faible) et les éventuels covenants.",
             "check": {"label": "Levier (x)", "answer": 2.33, "tol": 0.05, "unit": "x"}},
        ],
        "quiz": [
            {"q": "Une hausse du BFR…", "choices": ["Consomme généralement du cash", "Augmente l'EBITDA", "Réduit mécaniquement le CA"], "answer": 0, "why": "Le BFR immobilise du cash dans le cycle d'exploitation."},
            {"q": "L'EBITDA mesure…", "choices": ["Le cash disponible pour les actionnaires", "Une performance opérationnelle avant amortissements", "La valeur des fonds propres"], "answer": 1, "why": "Il ignore BFR, capex, impôts et dette."},
            {"q": "Le free cash-flow simplifié se calcule…", "choices": ["EBITDA − impôts − ΔBFR − CAPEX", "Résultat net + dividendes", "CA − charges"], "answer": 0, "why": "C'est le cash réellement libre après l'exploitation et les investissements."},
            {"q": "Un DSO qui augmente alors que le CA est stable signale…", "choices": ["Une amélioration du recouvrement", "Une dégradation possible du recouvrement ou des litiges", "Une baisse des stocks"], "answer": 1, "why": "Les créances croissent plus vite que l'activité."},
            {"q": "Dette nette 60 M€, EBITDA 20 M€ : le levier est de…", "choices": ["0,33x", "3,0x", "30x"], "answer": 1, "why": "60 / 20 = 3,0x."},
        ],
    },
    {
        "id": 4, "title": "Création de valeur", "axis": "Finance & valorisation", "level": "Finance",
        "duration": "75 min", "lab": "npv",
        "objective": "Arbitrer des investissements avec ROCE, EVA, VAN, TRI et payback, et comprendre le rôle du WACC.",
        "outcomes": [
            "Calculer ROCE et EVA et les rapprocher du coût du capital",
            "Comprendre le WACC et son rôle de taux d'actualisation",
            "Calculer et comparer VAN, TRI, payback et indice de profitabilité",
            "Recommander entre deux projets en intégrant les risques non financiers",
        ],
        "sections": [
            {"title": "1. Créer de la valeur = rendement > coût du capital", "body": """
Une activité crée de la valeur lorsque la rentabilité des capitaux engagés **dépasse leur coût**.

```
ROCE = NOPAT / capitaux employés
EVA  = NOPAT − WACC × capitaux employés
     = (ROCE − WACC) × capitaux employés
```

- **NOPAT** : résultat d'exploitation après impôt théorique, avant frais financiers.
- **EVA** (valeur économique ajoutée) positive : l'activité rémunère tous les apporteurs de capitaux et crée de la valeur ; négative : elle en détruit, même si elle est comptablement bénéficiaire.

C'est le principe du *Value Based Management* : **ROCE > WACC**.
"""},
            {"title": "2. Le WACC : le coût moyen pondéré du capital", "body": """
```
WACC = E/(E+D) × Ke + D/(E+D) × Kd × (1 − t)
```

- **Ke** : coût des fonds propres (rendement exigé par les actionnaires, souvent via le CAPM).
- **Kd** : coût de la dette, après économie d'impôt (1 − t).
- Pondérations selon la structure financière cible.

Le WACC sert de **taux d'actualisation** des flux et de **seuil de rentabilité** exigé pour un projet. Il doit refléter le **risque du projet** : un projet plus risqué que l'activité courante mérite une prime de risque.
"""},
            {"title": "3. VAN, TRI, payback, indice de profitabilité", "body": """
```
VAN = Σ FCFt / (1 + WACC)^t − investissement initial
```

| Critère | Définition | Atouts | Limites |
|---|---|---|---|
| **VAN** | Valeur actuelle des flux − investissement | Mesure directe de la valeur créée | Dépend du taux retenu |
| **TRI** | Taux qui annule la VAN | Parlant (comparable au WACC) | Trompeur pour comparer des projets de tailles ou profils différents |
| **Payback** | Délai de récupération | Simple, lisible sur le risque de liquidité | Ignore la valeur temps et les flux après récupération |
| **Indice de profitabilité** | VAN / investissement | Utile en cas de rationnement du capital | Ne remplace pas la VAN en absolu |
"""},
            {"title": "4. Choisir entre deux projets", "body": """
Quand les projets sont **mutuellement exclusifs**, la VAN est le critère de référence ; l'indice de profitabilité éclaire les arbitrages sous contrainte de capital. Ensuite, élargissez : **risques non financiers** (exécution, réglementaire, dépendance), **flexibilité** (possibilité de phaser), alignement avec la stratégie et la raison d'être de l'entreprise.

Testez enfin la **robustesse** : scénarios (base, upside, downside) et sensibilités sur les hypothèses qui changent réellement la décision (prix, volumes, capex, WACC).
"""},
        ],
        "key_points": [
            "Un projet crée de la valeur si ROCE > WACC, ou VAN > 0.",
            "La VAN mesure la valeur créée ; le TRI donne un ordre de grandeur de rendement.",
            "Le payback n'est qu'un indicateur de liquidité et de risque.",
            "Le WACC reflète le risque du projet, pas seulement celui de l'entreprise.",
        ],
        "pitfalls": [
            "Choisir sur le TRI le plus élevé sans regarder la taille des projets.",
            "Actualiser avec un WACC unique pour des projets de risques très différents.",
            "Oublier capex de maintenance et BFR dans les flux.",
            "Ignorer les risques non financiers.",
        ],
        "example": {
            "title": "Cas : projet A vs projet B (WACC 9 %)",
            "body": "A : investissement 3 M€, FCF 0,9 M€/an sur 5 ans. B : investissement 5 M€, FCF 1,35 M€/an sur 5 ans.",
            "table": [
                {"Critère": "VAN (M€)", "Projet A": _c(NPV_A), "Projet B": _c(NPV_B)},
                {"Critère": "TRI", "Projet A": f"{_c(IRR_A*100, 1)} %", "Projet B": f"{_c(IRR_B*100, 1)} %"},
                {"Critère": "Payback (années)", "Projet A": _c(PB_A, 1), "Projet B": _c(PB_B, 1)},
                {"Critère": "Indice de profitabilité", "Projet A": _c(PI_A), "Projet B": _c(PI_B)},
            ],
        },
        "exercises": [
            {"title": "VAN du projet A",
             "statement": "Projet A : investissement **3 M€**, FCF **0,9 M€/an** pendant **5 ans**, WACC **9 %**. Quelle est la **VAN en M€** ?",
             "hint": "Facteur d'annuité à 9 % sur 5 ans = 3,8897.",
             "solution": f"VAN = 0,9 × 3,8897 − 3 = **{_c(NPV_A)} M€**. TRI ≈ {_c(IRR_A*100, 1)} % (> 9 %), payback {_c(PB_A, 1)} ans, indice de profitabilité {_c(PI_A)}.",
             "check": {"label": "VAN A (M€)", "answer": round(NPV_A, 3), "tol": 0.03, "unit": "M€"}},
            {"title": "VAN du projet B",
             "statement": "Projet B : investissement **5 M€**, FCF **1,35 M€/an** pendant **5 ans**, WACC **9 %**. Quelle est la **VAN en M€** ? Quel projet recommandez-vous ?",
             "hint": "1,35 × 3,8897 − 5.",
             "solution": f"VAN = 1,35 × 3,8897 − 5 = **{_c(NPV_B)} M€**. **Recommandation** : le projet A crée plus de valeur ({_c(NPV_A)} vs {_c(NPV_B)} M€) avec moins de capital (indice {_c(PI_A)} vs {_c(PI_B)}). B reste créateur de valeur mais moins efficient ; il ne serait préférable que si le capital n'était pas rationné et si un avantage stratégique non financier le justifiait.",
             "check": {"label": "VAN B (M€)", "answer": round(NPV_B, 3), "tol": 0.03, "unit": "M€"}},
            {"title": "Calculer l'EVA",
             "statement": "NOPAT **12 M€**, capitaux employés **100 M€**, WACC **8,5 %**. Quelle est l'**EVA en M€** ?",
             "hint": "EVA = NOPAT − WACC × capitaux employés.",
             "solution": "ROCE = 12 / 100 = 12 %. EVA = 12 − 8,5 % × 100 = **3,5 M€**. Le ROCE dépasse le WACC de 3,5 points : l'activité crée de la valeur.",
             "check": {"label": "EVA (M€)", "answer": 3.5, "tol": 0.05, "unit": "M€"}},
        ],
        "quiz": [
            {"q": "Le critère le plus directement lié à la valeur créée est…", "choices": ["La VAN", "Le payback seul", "Le chiffre d'affaires"], "answer": 0, "why": "La VAN mesure la valeur actuelle créée au-delà du coût du capital."},
            {"q": "Si ROCE > WACC…", "choices": ["L'activité crée de la valeur économique", "L'activité est forcément sans dette", "La VAN est nulle"], "answer": 0, "why": "L'EVA est positive : le rendement dépasse le coût du capital."},
            {"q": "Le TRI est trompeur lorsque…", "choices": ["On compare des projets de tailles très différentes", "Le projet est rentable", "Le WACC est faible"], "answer": 0, "why": "Un petit projet à fort TRI peut créer moins de valeur absolue qu'un grand projet à TRI plus faible."},
            {"q": "Le WACC est…", "choices": ["Le taux d'intérêt de la dette uniquement", "Le coût moyen pondéré de l'ensemble des financements", "Le rendement de l'actionnaire sortant"], "answer": 1, "why": "Il pondère coût des fonds propres et coût de la dette après impôt."},
            {"q": "Le payback ignore…", "choices": ["La valeur temps et les flux après récupération", "L'investissement initial", "Les flux positifs"], "answer": 0, "why": "C'est un indicateur de liquidité, pas de création de valeur."},
        ],
    },
]
