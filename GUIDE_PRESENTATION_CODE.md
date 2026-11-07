# Présenter le code de Spirit Digger à une experte en NLP

Ce guide t'accompagne pendant la présentation des notebooks. Pour chacun, tu trouveras :
- **ce qu'il faut montrer** (les sections à ouvrir) ;
- **ce qu'il faut dire** ;
- **les choix techniques et leur justification** ;
- **les questions probables et comment y répondre**.

Une experte en NLP sera bienveillante avec un projet de 3e année, mais exigeante sur deux points : **la rigueur de l'évaluation** et **l'honnêteté sur les limites**. Ton meilleur atout est de dire toi-même les faiblesses avant qu'elle ne les trouve. La dernière partie de ce guide les liste.

---

## 0. Avant la séance

- **N'exécute rien en direct.** Tous les notebooks sont déjà exécutés et leurs sorties sont enregistrées. Ouvre-les simplement : les graphiques et tableaux s'affichent. Le NB 01 prend 5 minutes et le NB 02 en prend 4, donc les relancer devant elle ferait perdre du temps.
- **Prépare deux onglets de navigateur** : `outputs/04_graphe_arbre.html` (l'arbre interactif) et `outputs/bulletin_2023-23.html` (le bulletin).
- **Prévois 30 à 40 minutes** : 5 minutes de vue d'ensemble, environ 5 minutes par notebook, et du temps pour les questions.
- **Ordre conseillé** : 00 → 01 (rapidement) → 03 (le plus fort) → 02 → 04 → 05 → 06. Commencer par l'alerte (03) marque les esprits ; tu peux aussi suivre l'ordre naturel si tu préfères.

---

## 1. Vue d'ensemble (2 minutes)

**À montrer :** l'arborescence du projet dans VS Code.

```
data_lake/          sources brutes, jamais modifiées
notebooks/          00 à 06, un notebook par étape
src/spirit_digger/  code partagé : config, chargement, nettoyage, lexique, analyse du russe, style
outputs/            tout ce qui est produit : corpus Parquet, CSV, figures, bulletins
```

**À dire :**
> « C'est une chaîne de traitement en sept étapes, organisée selon le cycle du renseignement : évaluer les sources, collecter, exploiter, recouper, diffuser. Les données brutes ne sont jamais modifiées, et chaque notebook relit les produits du précédent : la chaîne complète est reproductible en une vingtaine de minutes sur processeur. Le code commun est factorisé dans le module `src/spirit_digger`. »

**Point fort à souligner :** la séparation entre données brutes, code partagé et produits. C'est une bonne pratique d'ingénierie qu'une experte remarquera.

---

## 2. NB 00 · Reconnaissance du data lake

**À montrer :**
- la section 4.1 (le jeu cyber : 24,7 % d'accord pour 25 % de hasard, 9 valeurs d'IOC distinctes) ;
- la section 4.2 (le tableau des fuites : « Getty Images » dans 9,3 % des faux articles et 0 % des vrais) ;
- le registre final (section 5).

**À dire :**
> « Avant toute modélisation, j'ai audité les données. Deux jeux étaient synthétiques : leur "prédiction" ne fait pas mieux que le hasard. Dans le jeu vrai/faux, j'ai trouvé des fuites de données, c'est-à-dire des marqueurs de source qui n'apparaissent que dans une classe. Et 66 % de WELFake est déjà contenu dans ISOT. »

**Questions probables :**
- *« Comment as-tu repéré que WELFake recoupait ISOT ? »* → Par une empreinte de texte : un hachage MD5 des 300 premiers caractères alphanumériques mis en minuscules. Les empreintes communes donnent le recouvrement.
- *« Et le sens des étiquettes de WELFake ? »* → La documentation dit 1 = vrai, mais en comparant avec les textes communs à ISOT, on voit que 1 = faux. Je l'ai vérifié sur les données plutôt que de faire confiance à la documentation.

---

## 3. NB 01 · Collecte et nettoyage

**À montrer :**
- la cellule « AVANT / APRÈS » sur Meduza (la mention légale russe « agent de l'étranger » effacée) ;
- la section 4 (tableau de contrôle des fuites : 31 % → 0,2 %) ;
- l'encadré « Découverte en cours de route » (les 4 867 textes de propagande tous présents dans le jeu « faux »).

**À dire :**
> « Le nettoyage n'est pas cosmétique : il retire tout ce qui permettrait à un modèle de reconnaître la source au lieu du contenu. Et je mesure son effet plutôt que de le supposer. »

**Choix techniques à justifier :**
- **Dédoublonnage par chaîne, pas global** : une même dépêche reprise par TASS et par UNIAN n'est pas un doublon, c'est un recoupement.
- **Détection de langue par règle** : les lettres і, ї, є, ґ n'existent qu'en ukrainien. C'est suffisant pour du russe et de l'ukrainien, sans dépendance supplémentaire. Pour l'anglais et l'indonésien du corpus Golfe, je compte les mots-outils.
- **Format Parquet** : typé, compressé, environ 10 fois plus rapide à relire que du CSV.

**Question probable :**
- *« Pourquoi des expressions régulières plutôt qu'un détecteur de langue comme fastText ou langdetect ? »* → Le besoin était simple et le corpus connu. Une règle explicable suffisait, sans dépendance. Pour un corpus plus varié, j'utiliserais un vrai détecteur.

---

## 4. NB 02 · Extraction d'entités (NER)

**À montrer :**
- les deux rendus displaCy de la phrase test : sans puis avec lexique (Fordow, GBU-57…) ;
- la cellule de translittération (tableau « fusionné en / variantes ») ;
- le rapport d'inventaire.

**À dire :**
> « J'utilise spaCy `en_core_web_sm`, un modèle pré-entraîné. Je n'entraîne rien : je l'adapte au domaine avec un EntityRuler placé avant le composant NER, puis je consolide les sorties. »

**Choix techniques à justifier :**

| Choix | Justification |
|---|---|
| `en_core_web_sm` (le plus petit modèle) | tourne sur processeur ; 2 196 articles en environ 2 minutes |
| `parser` et `lemmatizer` désactivés, `senter` activé | on n'a besoin que des entités et des frontières de phrases : 3 à 4 fois plus rapide |
| EntityRuler **avant** `ner` | les termes du lexique sont prioritaires ; le modèle statistique ne peut pas les écraser |
| `phrase_matcher_attr = LOWER` | insensible à la casse : « drone » et « Drone » |
| motifs de jetons (`USS` + mots en majuscule, `Operation` + mots en majuscule) | capture les noms de navires et d'opérations sans les lister un par un |
| textes coupés à 10 000 caractères | quelques articles « live » dépassent 60 000 caractères ; on garde l'essentiel |
| vote majoritaire, avec priorité au lieu dès 30 % | corrige « Trump » classé organisation, et « UAE said… » classé organisation au lieu de lieu |
| résolution d'un nom de famille seul d'abord **dans l'article**, sinon globalement si un nom complet domine à 80 % | évite de confondre Ali et Mojtaba Khamenei |
| clé phonétique (gh→q, kh→k, ae→a, ei→i, ou→u, lettres doublées simplifiées) | fusionne Ghalibaf et Qalibaf ; 50 personnes réunifiées |

**Questions probables :**
- *« Pourquoi pas un modèle plus gros, `en_core_web_trf` ou un transformer ? »* → Contrainte volontaire : tout doit tourner sur un portable, sans GPU. Le modèle `trf` serait plus précis, notamment sur les organisations, mais beaucoup plus lent sur processeur. C'est une amélioration naturelle.
- *« As-tu mesuré la précision et le rappel du NER ? »* → **Non**, et il faut le dire franchement. J'ai vérifié par l'exemple et corrigé les erreurs visibles, mais il n'existe pas de jeu annoté pour ce corpus. La prochaine étape serait d'annoter environ 200 phrases à la main pour calculer précision, rappel et F1.
- *« Et le NER sur le russe ? »* → Il n'est pas fait. Le NER ne porte que sur le corpus anglais. Le corpus russe est traité au NB 03 par une autre méthode, sans NER. Avec plus de temps : `ru_core_news_sm` de spaCy, ou Natasha, qui est spécialisé dans le russe.
- *« Ta clé phonétique ne risque-t-elle pas de fusionner des personnes différentes ? »* → En théorie oui, c'est pourquoi je ne l'applique qu'aux personnes, et la cellule affiche toutes les fusions pour qu'on puisse les vérifier. C'est une version très simplifiée de ce que font Soundex ou Double Metaphone.

---

## 5. NB 03 · Alerte précoce

**À montrer :**
- la cellule des racines (`racines("Взрыв на Крымском мосту…")`) ;
- la cellule du calcul du score (`attendu`, `z`, `SCORE`) ;
- la table de validation (17 / 21) ;
- la chronologie, puis le zoom de juin 2023 ;
- la section 9 (bruit éditorial : le pied de message d'UNIAN).

**À dire :**
> « Aucun mot-clé n'est donné. Pour chaque racine de mot et chaque jour, je compare le nombre de messages observé au nombre attendu d'après les 28 jours précédents, puis je pondère par le nombre de camps qui emploient ce mot ce jour-là. »

**La formule, à écrire au tableau si possible :**

```
attendu(w, t) = N(t) × [ Σ des 28 jours précédents de n(w) ] / [ Σ des 28 jours précédents de N ]
z(w, t)       = ( n(w, t) − attendu ) / √( attendu + 1 )
score(w, t)   = z × (camps qui emploient w le jour t) / 5
```

Exemple réel (6 juin 2023) : Kakhovka apparaît dans 8 messages sur 16 043 pendant les 28 jours précédents. Le 6 juin compte 1 036 messages, d'où un attendu de 0,52. On observe 438 messages, donc z = 355. Les 5 camps en parlent, donc le score vaut 355.

**Choix techniques à justifier :**

| Choix | Justification |
|---|---|
| racine = 6 premières lettres des mots de 5 lettres ou plus | absorbe les déclinaisons du russe (Пригожин, Пригожина, Пригожину) sans outil linguistique lourd |
| présence par message (un mot compte une fois par message) | un message qui répète 20 fois un mot ne doit pas créer une alerte |
| fenêtre de 28 jours | quatre semaines : neutralise l'effet du jour de la semaine et suit l'évolution de l'actualité |
| `+1` sous la racine carrée | évite une division par un nombre proche de zéro pour un mot jamais vu |
| au moins 15 messages, vocabulaire limité aux racines vues au moins 100 fois | écarte les « ruptures » de 2 à 3 messages, spectaculaires en pourcentage mais insignifiantes |
| pondération par les camps | une rupture dans un seul camp peut être éditoriale ou propagandiste ; dans les cinq, c'est un fait |
| seuils 20 / 30 / 60 | fixés pour que l'alerte reste rare : environ 1 jour sur 5 en ALERTE, 1 sur 20 en ALERTE MAXIMALE |

**Questions probables (les plus techniques de la séance) :**
- *« Ton z-score suppose une loi de Poisson. Est-ce justifié ? »* → C'est une approximation : la variance des comptages de mots est en réalité plus forte que la moyenne (surdispersion). Une loi binomiale négative serait plus juste. En pratique, les vrais événements ont des z de 50 à 355, bien au-delà de l'erreur d'approximation, mais les seuils restent empiriques.
- *« Tu fais près de 4,8 millions de tests. Et les tests multiples ? »* → Juste : avec autant de tests, des z élevés apparaissent par hasard. C'est pourquoi les seuils sont élevés (20 et plus, pas 3) et pourquoi j'impose un minimum de messages et la convergence des camps. Une correction formelle (Bonferroni, ou contrôle du taux de fausses découvertes) serait plus rigoureuse.
- *« Pourquoi tronquer les mots plutôt que lemmatiser ? »* → Rapidité et simplicité : 382 000 messages comptés en environ 30 secondes. Mais c'est grossier : deux mots différents peuvent partager une racine, et l'ukrainien n'est pas bien traité. La version propre serait une lemmatisation avec pymorphy3, Stanza ou spaCy russe.
- *« Comment as-tu choisi les 21 événements de validation ? »* → À la main, parmi des événements documentés publiquement. Il y a donc un biais possible vers les événements spectaculaires. Je ne mesure pas non plus formellement les fausses alertes. Une évaluation solide utiliserait une chronologie de référence externe.
- *« Tu ne détectes que des unigrammes ? »* → Oui. Les bigrammes, par exemple « Крымский мост », seraient plus précis. C'est une extension simple.

---

## 6. NB 04 · Graphe de relations

**À montrer :**
- la cellule de construction du graphe (co-occurrence par phrase, PMI) ;
- le tableau de tri des communautés (avec l'écart manuel « Fifa » justifié) ;
- le tableau « fréquent vs spécifique » ;
- l'arbre (section 5 bis), puis la figure du lien caché.

**À dire :**
> « Deux entités citées dans la même phrase sont reliées. Je garde les entités vues dans au moins 8 articles, et les liens attestés dans au moins 3 articles. Les sous-théâtres sont trouvés par l'algorithme de Louvain. Pour les liens cachés, je suis les liens les plus spécifiques au sens de la PMI, pas les plus fréquents. Et chaque maillon est justifié par sa phrase source. »

**La PMI, à écrire si on te la demande :**

```
PMI(a, b) = log( P(a, b) / (P(a) × P(b)) )
          = log( n(a,b) × N_phrases / (n(a) × n(b)) )
```
où n(a, b) est le nombre de phrases contenant a et b, et n(a) le nombre de phrases contenant a.

**Choix techniques à justifier :**

| Choix | Justification |
|---|---|
| fenêtre = la phrase | plus précise que l'article : deux noms dans un même article peuvent n'avoir aucun rapport |
| Louvain avec `resolution=1.2`, `seed=7` | une résolution un peu supérieure à 1 donne des communautés plus fines ; la graine rend le résultat reproductible |
| tri des communautés : au moins une entité militaire, ou au moins 25 % des membres liés à une entité militaire | règle automatique, complétée par un écart manuel justifié (la Coupe du monde) |
| plus court chemin avec un coût de 1 / max(PMI, 0,05), sur un graphe réduit aux personnes, forces et organisations | sans ce réglage, tout passe par « Iran » ou « Donald Trump », ce qui n'apprend rien |
| phrase-preuve retrouvée en relançant spaCy sur l'article | même chaîne de traitement qu'au NB 02, donc même découpage en phrases |

**Questions probables :**
- *« La PMI favorise les paires rares. »* → Oui, c'est son biais connu. Je le limite en exigeant au moins 3 articles par lien, au moins 4 phrases par maillon pour les liens cachés, et au moins 15 articles par entité dans le tableau des liens spécifiques. Une alternative est la NPMI, la PMI normalisée entre −1 et 1.
- *« Une co-occurrence ne dit pas la nature de la relation. »* → Exact, et c'est une limite assumée : le graphe dit qui est lié, pas comment. Typer les relations demanderait de l'extraction de relations (analyse syntaxique, ou un modèle de type REBEL ou un LLM). L'exemple « la BBC a contacté l'IDF et le CENTCOM » montre bien qu'une co-citation peut être un artefact.
- *« Louvain est instable. »* → Oui, d'où la graine fixée. On pourrait vérifier la stabilité sur plusieurs graines, ou utiliser Leiden, qui garantit des communautés connexes.

---

## 7. NB 05 · Guerre de l'information

**À montrer :**
- le modèle « tricheur » et ses mots décisifs (« featured image », « getty images ») ;
- le rapport de classification du modèle propre (91 %) et la matrice de confusion ;
- les mots décisifs par classe (« 2016 », « Hillary », « said on Tuesday ») ;
- le crash-test (la tour Eiffel « fiable à 100 % ») ;
- la dérive temporelle (22 %) ;
- le volet B : pieds de message détectés, mots de combat, tableau des marqueurs.

**À dire :**
> « C'est le seul modèle que j'entraîne : TF-IDF sur unigrammes et bigrammes, puis une régression logistique. Le but n'était pas d'avoir le meilleur score, mais de montrer pourquoi un bon score ne suffit pas. »

**Choix techniques à justifier :**

| Choix | Justification |
|---|---|
| TF-IDF `ngram_range=(1,2)`, `min_df=5`, `max_features=200 000`, `sublinear_tf=True` | les bigrammes captent des tournures (« said on ») ; `min_df` élimine les mots trop rares ; la TF logarithmique évite qu'un mot répété domine |
| régression logistique `C=4` | base solide et rapide pour le texte, dont les coefficients sont lisibles |
| textes coupés à 400 caractères | les textes de propagande sont environ 10 fois plus courts : la longueur seule trahirait la classe |
| découpage 80 / 20 stratifié, `random_state=7` | garde les proportions des classes, et le résultat est reproductible |
| log-odds avec un a priori tiré de la fréquence générale du mot | méthode « Fightin' Words » (Monroe et al., 2008) |

**Questions probables :**
- *« Ton découpage est aléatoire, pas temporel. »* → **C'est la bonne critique, à reconnaître.** Avec un découpage aléatoire, le test ressemble à l'entraînement : les 91 % sont optimistes. Un découpage temporel (entraîner sur les textes anciens, tester sur les récents) aurait montré la dérive dès le départ. Le test sur la presse 2026 joue ce rôle après coup.
- *« Ton a priori pour le log-odds n'est pas exactement celui de Monroe. »* → C'est vrai : c'est une version simplifiée. L'a priori vaut 10 × (fréquence générale du mot + 1) / 60 000, et le dénominateur est ajusté de 10. Le modèle de Monroe utilise un a priori de Dirichlet informatif complet. Le principe est le même : lisser les mots rares par leur fréquence de fond.
- *« Pourquoi pas un transformer, CamemBERT ou XLM-R ? »* → Contrainte du processeur, et surtout parce que le problème vient des données (fuites, époque), pas du modèle. Un transformer apprendrait les mêmes biais, en plus opaque. Avec un GPU, on pourrait tester XLM-R avec un découpage temporel.
- *« Le jeu est déséquilibré (4 867 textes de propagande). »* → Oui, d'où le rapport par classe et le F1 macro (0,91). La propagande a une précision élevée (0,97) mais un rappel plus faible (0,87).

---

## 8. NB 06 · Corrélation et bulletin

**À montrer :**
- le tableau des cotations (128 en B1, quelques D4) ;
- la fonction `coter` (la règle des belligérants) ;
- la demande d'observation JSON ;
- le bulletin dans le navigateur.

**À dire :**
> « La lettre de fiabilité est un jugement d'analyste, documenté dans le code. Le chiffre de crédibilité est calculé : un camp ne confirme une information que s'il y consacre au moins 2 % de ses messages, et au moins 5 messages. Une information confirmée par les deux belligérants et un camp neutre obtient 1. »

**Question probable :**
- *« Pourquoi 2 % et 5 messages ? »* → Calibré sur les données : avec un seuil de 3 messages, 199 alertes sur 210 sortaient en B1, ce qui ne discriminait rien. Avec 2 % et 5 messages, la répartition devient utile (B1, B2, C3, D4…).

---

## 9. Les faiblesses à reconnaître toi-même

Dis-les avant qu'on te les fasse remarquer : c'est ce qui convaincra le plus une experte.

1. **Pas d'évaluation quantitative du NER** : aucun jeu annoté, donc ni précision, ni rappel, ni F1.
2. **Validation de l'alerte limitée** : 21 événements choisis à la main, et les fausses alertes ne sont pas mesurées formellement.
3. **Traitement grossier du russe** : troncature à 6 lettres au lieu d'une lemmatisation, et l'ukrainien traité comme le russe.
4. **Statistiques simplifiées** : hypothèse de Poisson pour le z-score, pas de correction des tests multiples, seuils empiriques.
5. **Découpage aléatoire pour le classifieur** : score optimiste, et la dérive temporelle n'est constatée qu'après coup.
6. **Co-occurrence sans typage** : le graphe ne dit pas la nature des relations.
7. **Corpus archivé, pas un flux réel**, avec des messages datés au jour seulement.

**Les pistes d'amélioration à proposer :**
- annoter environ 200 phrases pour évaluer le NER ;
- lemmatiser le russe et l'ukrainien (pymorphy3, Stanza) et ajouter un NER russe (Natasha) ;
- remplacer le z-score de Poisson par une binomiale négative et contrôler le taux de fausses découvertes ;
- utiliser des bigrammes pour l'alerte ;
- adopter un découpage temporel pour le classifieur, puis tester XLM-R ;
- extraire des relations typées (règles de dépendances syntaxiques, ou un LLM avec vérification).

---

## 10. Petit lexique technique

| Terme | Définition courte |
|---|---|
| **NER** | reconnaissance d'entités nommées : repérer et typer les noms propres |
| **EntityRuler** | composant spaCy qui reconnaît des entités à partir de listes et de motifs |
| **senter** | composant spaCy léger qui découpe le texte en phrases |
| **z-score** | écart à l'attendu divisé par l'écart-type attendu |
| **surdispersion** | variance des comptages plus grande que la moyenne, contrairement à ce que suppose la loi de Poisson |
| **PMI** | log du rapport entre la probabilité de co-occurrence observée et celle attendue si les deux entités étaient indépendantes |
| **Louvain** | algorithme qui découpe un graphe en communautés en maximisant la modularité |
| **modularité** | mesure de la densité des liens à l'intérieur des communautés, comparée à un graphe aléatoire |
| **TF-IDF** | poids d'un mot : fréquent dans le document, rare dans le corpus |
| **log-odds ratio** | log du rapport des cotes d'un mot entre deux corpus ; positif d'un côté, négatif de l'autre |
| **fuite de données** | information non pertinente qui trahit la classe et fait « tricher » le modèle |
| **dérive temporelle** | baisse de performance quand les données réelles s'éloignent des données d'entraînement |
