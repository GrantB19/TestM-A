"""Modules 8 à 10 : investment memo, corporate strategy, cas final COMEX."""
from finance import weighted_score

_W1 = [25, 20, 20, 20, 15]
_W2 = [35, 15, 15, 20, 15]
SC = {"Acquisition": [4, 5, 1, 2, 4], "JV avec partenaire local": [3, 3, 3, 3, 5], "Développement organique": [1, 5, 4, 4, 2]}
S1 = {k: weighted_score(_W1, v) for k, v in SC.items()}
S2 = {k: weighted_score(_W2, v) for k, v in SC.items()}

EV5 = 12 * 8
STAKE = 0.5 * EV5
PV_STAKE = STAKE / 1.10 ** 5
NPV_JV = PV_STAKE - 30
NPV_10X = 0.5 * 12 * 10 / 1.10 ** 5 - 30
NPV_6X = 0.5 * 12 * 6 / 1.10 ** 5 - 30
EXP_NPV = 0.4 * 10 + 0.2 * 25 + 0.4 * (-8)


def _c(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


MODULES_C = [
    {
        "id": 8, "title": "Investment memo", "axis": "Communication COMEX", "level": "Décision",
        "duration": "75 min", "lab": "synergies",
        "objective": "Rédiger une note d'investissement nette, équilibrée et actionnable pour un comité de décision.",
        "outcomes": [
            "Structurer un memo de 2 pages avec la décision en première phrase",
            "Probabiliser des scénarios et calculer une VAN espérée",
            "Exposer risques, conditions et prochaines étapes",
            "Pratiquer le red teaming de sa propre recommandation",
        ],
        "sections": [
            {"title": "1. Structure d'un memo de comité", "body": """
Un memo de comité doit permettre de **décider en 10 minutes**. Structure recommandée (2 pages) :

1. **Décision demandée** – en une phrase (« Nous demandons l'autorisation de… pour un montant maximum de… »).
2. **Thèse d'investissement** – 3 piliers maximum, chacun appuyé par un fait chiffré.
3. **Marché et positionnement** – attractivité, concurrence, avantage différenciant.
4. **Economics** – valorisation, fourchette de prix, rendement (VAN, TRI, ROCE), scénarios.
5. **Risques et mitigations** – les 3 à 5 risques qui peuvent invalider la thèse.
6. **Conditions et prochaines étapes** – conditions suspensives, sujets de due diligence, calendrier.
"""},
            {"title": "2. Écrire pour décider", "body": """
- **La réponse d'abord** : la recommandation figure dans la première phrase, pas en conclusion.
- **Un message par paragraphe**, formulé comme une affirmation (titre-conclusion), puis ses preuves.
- **Chiffres traçables** : source, hypothèse, périmètre. Un chiffre sans source est une opinion.
- **Équilibre** : exposer le downside avec autant de soin que l'upside. Un memo uniquement enthousiaste perd sa crédibilité.
- **Clarté** : phrases courtes, pas de jargon inutile, tableaux plutôt que paragraphes pour les chiffres.
"""},
            {"title": "3. Scénarios probabilisés et VAN espérée", "body": """
Pour refléter l'incertitude, associez à chaque scénario une **probabilité** et calculez la **VAN espérée** :

```
VAN espérée = Σ (probabilité du scénario × VAN du scénario)
```

La VAN espérée ne remplace pas l'analyse du downside : un projet peut avoir une VAN espérée positive mais un scénario de perte inacceptable pour le groupe. Présentez toujours **la perte maximale plausible** et ce qui permettrait de la limiter (phasage, option de sortie, garanties).
"""},
            {"title": "4. Red teaming : attaquer sa propre thèse", "body": """
Avant le comité, jouez l'avocat du diable :

- Quelle est l'hypothèse la plus fragile, et que se passe-t-il si elle est fausse ?
- Que sait le vendeur que nous ne savons pas ?
- Pourquoi un concurrent ne paierait-il pas plus ? Pourquoi ne l'a-t-il pas déjà fait ?
- Quelle est la sortie si nous nous trompons ?
- Quelles informations manquent encore, et qui peut les confirmer ?

Intégrez les réponses au memo : un comité fait confiance à un dossier qui a déjà répondu aux objections.
"""},
        ],
        "key_points": [
            "La décision demandée ouvre le memo.",
            "Trois piliers de thèse maximum, chacun chiffré.",
            "Le downside est exposé aussi sérieusement que l'upside.",
            "Les conditions suspensives et prochaines étapes transforment l'avis en plan d'action.",
        ],
        "pitfalls": [
            "Un memo descriptif qui n'ose pas recommander.",
            "Empiler des données sans hiérarchie ni conclusion.",
            "Cacher les incertitudes pour « convaincre ».",
            "Oublier la sortie / les options de repli.",
        ],
        "example": {
            "title": "Squelette de memo (cible fictive de nutrition animale)",
            "body": "Exemple de première page – **fictif** – pour illustrer le niveau de concision attendu.",
            "table": [
                {"Rubrique": "Décision", "Contenu type": "Autoriser une offre indicative non engageante de 90 à 100 M€ d'EV pour 100 % de la cible, sous réserve de due diligence."},
                {"Rubrique": "Thèse", "Contenu type": "(1) Accès à un portefeuille clients complémentaire ; (2) synergies industrielles de 6 M€ ; (3) position de leader sur un segment à forte croissance."},
                {"Rubrique": "Economics", "Contenu type": "EV/EBITDA de 8,0x à 9,0x ; VAN espérée de +14 M€ ; ROCE > WACC dès l'année 3."},
                {"Rubrique": "Risques", "Contenu type": "Concentration clients (top 3 = 45 % du CA) ; capex de mise à niveau ; départ de dirigeants clés."},
                {"Rubrique": "Conditions", "Contenu type": "Revue de la concentration clients ; audit environnemental ; engagement de maintien du management."},
            ],
        },
        "exercises": [
            {"title": "VAN espérée",
             "statement": "Trois scénarios : **base** (40 %, VAN +10 M€), **upside** (20 %, VAN +25 M€), **downside** (40 %, VAN −8 M€). Quelle est la **VAN espérée (M€)** ?",
             "hint": "0,4 × 10 + 0,2 × 25 + 0,4 × (−8).",
             "solution": f"4,0 + 5,0 − 3,2 = **{_c(EXP_NPV)} M€**. Lecture : l'espérance est positive mais le downside pèse 40 % de probabilité pour −8 M€ : le memo doit présenter cette perte plausible et les moyens de la limiter (phasage de l'investissement, garanties, option de sortie).",
             "check": {"label": "VAN espérée (M€)", "answer": EXP_NPV, "tol": 0.1, "unit": "M€"}},
            {"title": "Rédiger la décision et la thèse",
             "statement": "Pour la cible fictive du cas précédent (nutrition animale, EV 90-100 M€), rédigez en **moins de 120 mots** : la décision demandée, 3 piliers de thèse, 3 conditions suspensives.",
             "hint": "Décision en une phrase ; piliers chiffrés ; conditions actionnables.",
             "solution": """**Corrigé modèle**

*Nous demandons l'autorisation de remettre une offre indicative non engageante de 90 à 100 M€ d'EV pour 100 % de la cible.* Trois piliers : (1) un portefeuille clients complémentaire (+25 % de couverture géographique) ; (2) des synergies industrielles de 6 M€ à horizon 3 ans, dont 4 M€ sécurisés par des achats communs ; (3) une position de leader sur un segment croissant à 8 %/an. Conditions suspensives : (a) revue de la concentration clients ; (b) audit environnemental des sites ; (c) engagement de maintien de l'équipe dirigeante pendant 24 mois.""",
             "check": None},
            {"title": "Red team",
             "statement": "Listez les **5 questions les plus difficiles** qu'un membre du comité pourrait poser sur ce dossier, et préparez une réponse d'une phrase pour chacune.",
             "hint": "Pensez prix, risque, alternatives, hypothèses fragiles et sortie.",
             "solution": """**Exemples**

1. *Pourquoi payer une prime plutôt que développer en organique ?* → Délai de 4 ans et capex de 35 M€ contre un accès immédiat à 120 clients.
2. *Quelle part du prix repose sur des synergies ?* → 20 % ; seules les synergies de coûts sont intégrées dans le prix plafond.
3. *Que se passe-t-il si le client n°1 part ?* → Impact de −7 % d'EBITDA ; clause de protection dans le SPA et earn-out.
4. *Quelle est la sortie ?* → Cession à un acteur sectoriel ; multiple de sortie de 7x intégré au downside.
5. *Qui pilote l'intégration ?* → Un responsable dédié et un plan 100 jours validé avant signature.""",
             "check": None},
        ],
        "quiz": [
            {"q": "Un bon memo de comité…", "choices": ["Cache les incertitudes pour convaincre", "Présente une décision et ses conditions", "Liste uniquement les faits"], "answer": 1, "why": "Le comité doit pouvoir arbitrer."},
            {"q": "Le red teaming consiste à…", "choices": ["Défendre le scénario central", "Chercher ce qui pourrait invalider la thèse", "Réduire le nombre de sources"], "answer": 1, "why": "Il limite les biais de confirmation."},
            {"q": "Où placer la recommandation ?", "choices": ["À la fin du memo", "En première phrase", "En annexe"], "answer": 1, "why": "Principe de la réponse d'abord."},
            {"q": "La VAN espérée est…", "choices": ["La VAN du scénario base", "La moyenne pondérée par les probabilités des VAN de chaque scénario", "Le TRI moyen"], "answer": 1, "why": "Σ probabilité × VAN."},
            {"q": "Combien de piliers de thèse au maximum ?", "choices": ["1", "3", "10"], "answer": 1, "why": "Au-delà, le message se dilue."},
        ],
    },
    {
        "id": 9, "title": "Corporate strategy", "axis": "Corporate strategy", "level": "Stratégie",
        "duration": "90 min", "lab": "decision",
        "objective": "Choisir entre croissance organique, partenariat, JV, acquisition et cession, et piloter l'exécution du plan.",
        "outcomes": [
            "Comparer les modes de croissance selon vitesse, contrôle, capital et risque",
            "Utiliser une matrice de décision pondérée et tester sa robustesse",
            "Raisonner en portefeuille d'activités et en rôles stratégiques",
            "Définir un plan de management avec jalons et KPIs",
        ],
        "sections": [
            {"title": "1. Les modes de croissance", "body": """
| Mode | Vitesse | Contrôle | Capital | Risque d'exécution | Pertinent quand… |
|---|---|---|---|---|---|
| **Organique** | Lente | Total | Moyen, étalé | Moyen | Les capacités existent ou sont constructibles |
| **Partenariat / alliance** | Rapide | Faible | Faible | Moyen | Accès ponctuel à une capacité, test de marché |
| **Joint-venture** | Rapide | Partagé | Moyen | Élevé (gouvernance) | Actifs complémentaires, risque ou marché local à partager |
| **Acquisition** | Très rapide | Total | Élevé | Élevé (intégration) | Capacité rare, fenêtre limitée, avantage propriétaire |
| **Cession / désinvestissement** | Rapide | Perte | Libère du capital | Moyen | Activité non stratégique, valeur plus élevée chez un autre propriétaire |

Il n'existe pas de meilleur mode dans l'absolu : le choix dépend des **capacités à acquérir**, du **temps disponible** et de **l'appétit pour le risque**.
"""},
            {"title": "2. Matrice de décision pondérée", "body": """
Pour comparer des options de façon explicite :

1. Choisir **5 à 7 critères** (vitesse, contrôle, capital, risque, accès aux capacités, alignement stratégique).
2. **Pondérer** les critères (total = 100 %).
3. **Noter** chaque option de 1 à 5 sur chaque critère.
4. Calculer le **score pondéré**, puis tester la **robustesse** en faisant varier les pondérations.

Un résultat serré (écart < 0,2 point) ne se tranche pas par le score : on explicite les **conditions de bascule** – ce qui doit être vrai pour que l'option B passe devant l'option A.
"""},
            {"title": "3. Raisonner en portefeuille", "body": """
Le groupe est un **portefeuille d'activités**, chacune ayant un **rôle** :

- **Croissance** : investir pour gagner des parts sur un marché attractif.
- **Génération de cash** : optimiser, financer le reste du portefeuille.
- **Option** : investissement limité sur un marché émergent, avec jalons de décision.
- **Désinvestir** : activité dont la valeur est plus élevée chez un autre propriétaire.

La **création de valeur** s'évalue en rapprochant le **ROCE** du **WACC** par activité. L'**alignement avec la mission / raison d'être** de l'entreprise est un critère de filtrage : un projet financièrement attractif mais contraire à la raison d'être n'est pas retenu.
"""},
            {"title": "4. Du choix au plan de management", "body": """
Une décision stratégique n'a de valeur que si elle est exécutée. Le **plan de management** comprend :

- les **axes stratégiques** et le **plan d'actions** (plan financier, facteurs de succès, jalons) ;
- une **gouvernance d'exécution** (qui décide, à quelle fréquence, avec quels comités) ;
- des **KPIs** et **jalons** : indicateurs financiers (EBITDA, ROCE réalisés vs plan) et indicateurs d'avancement ;
- un **suivi périodique** avec statut d'alignement (aligné / partiellement aligné / non aligné) et décisions correctives.
"""},
            {"title": "5. Gouvernance d'une joint-venture", "body": """
Une JV échoue plus souvent pour des raisons de gouvernance que de stratégie. Points à cadrer dès le term sheet :

- **Matières réservées** (budget, plan stratégique, nominations, endettement) : qui a un droit de veto ?
- **Mécanismes de blocage** (*deadlock*) : escalade, médiation, clauses de sortie.
- **Apports** : cash, actifs, savoir-faire, valorisation des contributions non cash.
- **Politique de distribution** et financement futur.
- **Sortie** : droits de préemption, *call/put*, clause de non-concurrence, valorisation à la sortie.
"""},
        ],
        "key_points": [
            "Le meilleur mode de croissance dépend des capacités visées, du temps et du risque accepté.",
            "Une matrice pondérée se teste : variez les pondérations.",
            "Un résultat serré se tranche par des conditions de bascule.",
            "L'exécution (plan de management, KPIs) fait la valeur de la stratégie.",
        ],
        "pitfalls": [
            "Aller directement au M&A sans comparer organique, partenariat et JV.",
            "Pondérations choisies pour justifier une préférence déjà arrêtée.",
            "Négliger la gouvernance d'une JV.",
            "Un plan sans KPIs ni calendrier de suivi.",
        ],
        "example": {
            "title": "Matrice de décision : nouvelle géographie (scores illustratifs)",
            "body": "Critères pondérés : Vitesse 25 %, Contrôle 20 %, Capital requis 20 % (5 = capital faible), Risque 20 % (5 = risque faible), Accès aux capacités 15 %.",
            "table": [
                {"Option": k, "Vitesse": v[0], "Contrôle": v[1], "Capital": v[2], "Risque": v[3], "Capacités": v[4], "Score": _c(S1[k], 2)}
                for k, v in SC.items()
            ],
        },
        "exercises": [
            {"title": "Score pondéré de la JV",
             "statement": "Pondérations : Vitesse 25 %, Contrôle 20 %, Capital 20 %, Risque 20 %, Capacités 15 %. Notes de la **JV** : 3, 3, 3, 3, 5. Quel est son **score pondéré** ?",
             "hint": "0,25×3 + 0,20×3 + 0,20×3 + 0,20×3 + 0,15×5.",
             "solution": f"Score JV = 0,75 + 0,60 + 0,60 + 0,60 + 0,75 = **{_c(S1['JV avec partenaire local'], 2)}**. Acquisition = {_c(S1['Acquisition'], 2)}, organique = {_c(S1['Développement organique'], 2)}. La JV arrive en tête, mais l'écart avec l'acquisition est faible.",
             "check": {"label": "Score JV", "answer": S1["JV avec partenaire local"], "tol": 0.02, "unit": ""}},
            {"title": "Test de robustesse",
             "statement": "Nouvelles pondérations : Vitesse **35 %**, Contrôle **15 %**, Capital **15 %**, Risque **20 %**, Capacités **15 %**. Notes de l'**acquisition** : 4, 5, 1, 2, 4. Quel est son **score** ?",
             "hint": "0,35×4 + 0,15×5 + 0,15×1 + 0,20×2 + 0,15×4.",
             "solution": f"Acquisition = 1,40 + 0,75 + 0,15 + 0,40 + 0,60 = **{_c(S2['Acquisition'], 2)}**. JV = {_c(S2['JV avec partenaire local'], 2)} ; organique = {_c(S2['Développement organique'], 2)}. **Égalité** entre acquisition et JV : le score ne tranche plus. Il faut expliciter les conditions de bascule (voir exercice suivant).",
             "check": {"label": "Score acquisition", "answer": S2["Acquisition"], "tol": 0.02, "unit": ""}},
            {"title": "Conditions de bascule",
             "statement": "Pour l'égalité précédente, formulez **2 conditions** qui feraient préférer l'acquisition à la JV, et **2 conditions** inverses.",
             "hint": "Qu'est-ce qui doit être vrai sur la cible, le partenaire, le capital disponible, le contrôle ?",
             "solution": """**Acquisition préférée si** : (1) une cible adéquate existe à un prix ≤ valeur autonome + 30 % des synergies ; (2) le contrôle opérationnel est requis (qualité, sécurité, intégration industrielle).

**JV préférée si** : (1) le partenaire apporte un accès client / réglementaire non réplicable ; (2) le capital ou la capacité d'intégration sont limités et un phasage (option d'achat future) est possible.""",
             "check": None},
        ],
        "quiz": [
            {"q": "Une JV est particulièrement pertinente quand…", "choices": ["Le contrôle total est impératif", "Les actifs sont complémentaires et le risque partagé", "Aucun partenaire n'apporte de capacité"], "answer": 1, "why": "La JV combine capacités mais exige une gouvernance solide."},
            {"q": "Si deux options ont un score quasi identique, il faut…", "choices": ["Tirer au sort", "Expliciter les conditions de bascule", "Retenir la moins chère"], "answer": 1, "why": "On identifie ce qui doit être vrai pour que l'une domine."},
            {"q": "Dans une JV, une « matière réservée » est…", "choices": ["Une décision soumise à l'accord des deux partenaires", "Un actif vendu", "Un indicateur financier"], "answer": 0, "why": "Elle protège les intérêts de chaque partenaire sur les décisions clés."},
            {"q": "Quel rôle de portefeuille correspond à un investissement limité avec jalons de décision ?", "choices": ["Croissance", "Option", "Cash"], "answer": 1, "why": "L'option limite le capital engagé tant que l'incertitude n'est pas levée."},
            {"q": "Une stratégie sans KPIs…", "choices": ["Reste difficile à piloter", "Est plus flexible", "Est forcément meilleure"], "answer": 0, "why": "Les jalons relient l'ambition à l'exécution."},
        ],
    },
    {
        "id": 10, "title": "Cas final COMEX", "axis": "Communication COMEX", "level": "Capstone",
        "duration": "120 min", "lab": "synergies",
        "objective": "Intégrer stratégie, finance et narration exécutive dans une recommandation complète sur un cas de JV internationale.",
        "outcomes": [
            "Construire un executive summary orienté décision",
            "Intégrer marché, economics, gouvernance et risques",
            "Défendre sa recommandation face à des questions difficiles",
            "Proposer un plan 100 jours et des conditions de bascule",
        ],
        "sections": [
            {"title": "1. Le cas (fictif)", "body": """
**Contexte** : un groupe agro-industriel étudie une **JV 50/50** avec un partenaire local d'un pays émergent (fictif) pour produire et commercialiser des ingrédients à base de protéines végétales.

**Données du dossier**
- Marché local : 300 M€, croissance de 10 %/an (hypothèse de l'étude de marché).
- Capital de la JV : 60 M€ de fonds propres, dont **30 M€ apportés par le groupe** (50 %). Pas de dette.
- Plan : EBITDA run-rate de **12 M€ en année 5**.
- Multiple de sortie / valorisation de référence : **8x EBITDA**.
- Coût du capital retenu : **10 %**.
- Partenaire : apport de licences locales, réseau commercial et un site existant.
- Risques identifiés : change, dépendance au partenaire, délai d'obtention des autorisations.
"""},
            {"title": "2. Storyline d'un executive summary", "body": """
Séquence recommandée (1 à 2 pages) :

1. **Décision demandée** : « Nous recommandons d'autoriser… sous conditions… »
2. **Pourquoi maintenant** : fenêtre de marché, avantage du partenaire.
3. **Pourquoi la JV** plutôt qu'une acquisition ou un développement organique (comparaison sur 4-5 critères).
4. **Economics** : investissement, valorisation de la part du groupe, VAN, sensibilités (multiple, délai, change).
5. **Risques & mitigations** : 3 à 5 risques majeurs avec leur parade.
6. **Gouvernance** : matières réservées, deadlock, sortie.
7. **Plan 100 jours & prochaines étapes**.
"""},
            {"title": "3. Les chiffres qui doivent « tenir »", "body": """
Avant de recommander, assurez-vous que :

- la **valeur de la part du groupe** est actualisée au coût du capital (pas une valeur à terme non actualisée) ;
- la **VAN** est confrontée à des **sensibilités** (multiple, calendrier, EBITDA) ;
- les **dividendes / flux intermédiaires** et les **synergies** éventuelles sont traités explicitement ;
- l'**effet de change** et le **risque pays** sont intégrés dans le WACC ou dans les scénarios.

Si la VAN est proche de zéro, la recommandation doit s'appuyer sur des éléments qualitatifs assumés (option stratégique, accès au marché) et sur des **conditions** qui améliorent le profil de risque (phasage, option d'achat, garanties).
"""},
            {"title": "4. Défendre sa recommandation", "body": """
Face à un comité, la qualité de la réponse aux objections compte autant que le dossier. Préparez des réponses brèves et chiffrées à : *pourquoi pas seul ?* ; *quel est le prix maximum ?* ; *que se passe-t-il si le partenaire se dérobe ?* ; *quand sort-on et à quel prix ?* ; *comment la JV s'aligne-t-elle avec notre stratégie et nos engagements ?*

Votre posture : **assertive sur la recommandation, transparente sur l'incertitude, précise sur les conditions**.
"""},
        ],
        "key_points": [
            "Une recommandation COMEX combine décision, economics, risques, gouvernance et plan d'action.",
            "La valeur doit être actualisée et soumise à des sensibilités.",
            "Une VAN proche de zéro appelle des conditions qui améliorent le profil risque / rendement.",
            "La gouvernance de la JV est un élément de valeur, pas un détail juridique.",
        ],
        "pitfalls": [
            "Recommander sans avoir comparé les alternatives.",
            "Ne pas actualiser la valeur de la quote-part.",
            "Ignorer le change et le risque pays.",
            "Présenter un plan sans calendrier ni responsables.",
        ],
        "example": {
            "title": "Lecture économique du cas (part du groupe, hypothèses du dossier)",
            "body": "Valeur à l'année 5 de la part du groupe, actualisée à 10 %, comparée à l'apport de 30 M€.",
            "table": [
                {"Élément": "EV année 5 = 12 M€ × 8", "Valeur (M€)": _c(EV5)},
                {"Élément": "Part du groupe (50 %)", "Valeur (M€)": _c(STAKE)},
                {"Élément": "Valeur actualisée (÷ 1,10^5)", "Valeur (M€)": _c(PV_STAKE)},
                {"Élément": "− Apport initial", "Valeur (M€)": "−30,0"},
                {"Élément": "= VAN (hors dividendes et synergies)", "Valeur (M€)": _c(NPV_JV)},
                {"Élément": "Sensibilité : multiple 10x → VAN", "Valeur (M€)": _c(NPV_10X)},
                {"Élément": "Sensibilité : multiple 6x → VAN", "Valeur (M€)": _c(NPV_6X)},
            ],
        },
        "exercises": [
            {"title": "VAN de la quote-part",
             "statement": "EBITDA année 5 de la JV **12 M€**, valorisation à **8x**, part du groupe **50 %**, actualisation à **10 %** sur 5 ans, apport initial **30 M€**. Quelle est la **VAN (M€)** hors dividendes et synergies ?",
             "hint": "Part du groupe = 0,5 × 96 = 48 M€ ; ÷ 1,10^5 ; puis − 30.",
             "solution": f"Valeur de la part = 48 M€ ; actualisée = **{_c(PV_STAKE, 2)} M€** ; VAN = {_c(PV_STAKE, 2)} − 30 = **{_c(NPV_JV, 2)} M€**. La VAN est **quasi nulle** : à 10x, elle monte à {_c(NPV_10X)} M€ ; à 6x, elle tombe à {_c(NPV_6X)} M€. La recommandation ne peut donc pas reposer sur la seule valeur de sortie : elle doit s'appuyer sur les dividendes, des synergies ou une option stratégique, et sur des conditions de phasage.",
             "check": {"label": "VAN (M€)", "answer": NPV_JV, "tol": 0.3, "unit": "M€"}},
            {"title": "Executive summary (400 mots)",
             "statement": "Rédigez l'**executive summary** (≈ 400 mots) recommandant ou non la JV : décision, pourquoi maintenant, comparaison avec les alternatives, economics, risques, gouvernance, plan 100 jours. Utilisez le **Coach COMEX** pour vérifier la couverture des dimensions attendues.",
             "hint": "Décision en première phrase ; assumez la VAN proche de zéro et dites ce qui crée la valeur.",
             "solution": """**Corrigé modèle (extrait)**

**Décision.** Nous recommandons d'autoriser la constitution de la JV 50/50 pour un apport maximal de 30 M€, **phasé en deux tranches** et conditionné à l'obtention des autorisations locales.

**Pourquoi maintenant ?** Le marché local croît de 10 %/an et le partenaire détient les licences et le réseau que nous mettrions plus de quatre ans à construire.

**Pourquoi une JV ?** Comparée à l'acquisition (capital et risque d'intégration élevés) et à l'organique (délai), la JV obtient le meilleur score sur la vitesse, le capital et l'accès aux capacités.

**Economics.** La valeur actualisée de notre quote-part (≈ 29,8 M€) équilibre l'apport (VAN ≈ 0 à 8x). La création de valeur repose donc sur : des dividendes à partir de l'année 3, une option d'achat sur la part du partenaire et les synergies d'approvisionnement.

**Risques.** Change (couverture partielle), dépendance au partenaire (clauses de performance), délai d'autorisations (conditions suspensives).

**Gouvernance.** Matières réservées (budget, plan stratégique, endettement), mécanisme de deadlock et droit de sortie.

**Plan 100 jours.** Signature du term sheet, constitution de l'équipe de direction, plan de montée en charge, premiers jalons de décision.""",
             "check": None},
            {"title": "Questions difficiles du COMEX",
             "statement": "Préparez une réponse d'une phrase à : (1) pourquoi pas seul ? (2) quel est le prix maximum ? (3) que se passe-t-il si le partenaire se dérobe ? (4) comment sortons-nous ? (5) quel lien avec notre stratégie ?",
             "hint": "Chiffrez chaque réponse quand c'est possible.",
             "solution": """1. *Pourquoi pas seul ?* → Délai de plus de 4 ans et accès impossible aux licences locales sans partenaire.
2. *Prix maximum ?* → 30 M€ en deux tranches ; la 2e tranche est conditionnée aux jalons.
3. *Si le partenaire se dérobe ?* → Clause de performance, droit de sortie et valeur de rachat prédéfinie.
4. *Sortie ?* → Option de vente / d'achat à partir de l'année 5 à un multiple prédéfini.
5. *Lien stratégique ?* → Elle accélère l'axe de développement des protéines végétales et la présence internationale sans mobiliser le capital d'une acquisition.""",
             "check": None},
        ],
        "quiz": [
            {"q": "Une recommandation COMEX doit commencer par…", "choices": ["L'historique détaillé", "La décision proposée", "La bibliographie"], "answer": 1, "why": "Le message principal doit être immédiat."},
            {"q": "Si la VAN d'une JV est proche de zéro, il faut…", "choices": ["Abandonner automatiquement", "Rechercher ce qui crée la valeur (dividendes, option, synergies) et imposer des conditions", "Augmenter le multiple de sortie"], "answer": 1, "why": "On améliore le profil risque / rendement plutôt que de forcer le chiffre."},
            {"q": "La valeur de la part du groupe doit être…", "choices": ["Non actualisée", "Actualisée au coût du capital", "Égale à l'apport initial"], "answer": 1, "why": "Une valeur future non actualisée surestime la création de valeur."},
            {"q": "Quel élément de gouvernance protège contre un blocage ?", "choices": ["Un mécanisme de deadlock", "Un nom de marque", "Un budget marketing"], "answer": 0, "why": "Escalade, médiation, clauses de sortie."},
            {"q": "Un insight complet combine…", "choices": ["Fait seul", "Fait, implication et action", "Opinion et jargon"], "answer": 1, "why": "C'est la chaîne logique attendue d'un dossier de décision."},
        ],
    },
]
