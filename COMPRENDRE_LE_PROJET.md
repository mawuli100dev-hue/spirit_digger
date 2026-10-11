# Comprendre Spirit Digger : ce qu'on a construit, et pourquoi

> Ce document répond à une question simple : **« Qu'est-ce qu'on est en train de faire ? »**
> Tu viens de la vision par ordinateur (God's Eye). Ici, la logique est différente, et c'est normal de s'y perdre. On va tout reprendre depuis le début.

---

## 1. La réponse courte

**God's Eye est un modèle. Spirit Digger est une chaîne de traitement.**

- Dans **God's Eye**, tu as **entraîné** un modèle (YOLOv8), une fois, sur DOTA et xView. Ensuite, tu lui donnais une image et il prédisait des boîtes. Tout le projet tourne autour de *ce* modèle.
- Dans **Spirit Digger**, il n'y a **pas un seul gros modèle central**. Il y a **six outils différents mis bout à bout**, comme une chaîne de montage. Certains utilisent un modèle déjà entraîné par d'autres, un seul est entraîné par nous, et la plupart sont **de la statistique et des règles**, sans aucun entraînement.

Le but n'est pas de produire « un modèle avec un bon score ». Le but est de **répondre aux questions d'un état-major** à partir de textes :

> *« Que se passe-t-il ? Qui est impliqué ? Est-ce fiable ? Qui raconte quoi ? Que doit-on faire ? »*

---

## 2. Le changement de paradigme : ton habitude et ce projet

### Ce à quoi tu es habitué : l'apprentissage supervisé

```
Données étiquetées  ──►  ENTRAÎNEMENT  ──►  MODÈLE  ──►  nouvelles données  ──►  prédictions
(images + boîtes)        (des heures)       (best.pt)     (image test)           (avions, navires…)
```

Les données servent **d'abord à apprendre**. Le « vrai » travail commence quand le modèle est prêt.

### Ce qu'on fait ici : l'analyse de renseignement

```
Flux de textes  ──►  NETTOYER  ──►  EXTRAIRE  ──►  DÉTECTER  ──►  RELIER  ──►  COTER  ──►  BULLETIN
(Telegram,           (NB 01)       (NB 02)        (NB 03)        (NB 04)      (NB 06)     + demande
 presse…)                                                                                  à God's Eye
```

Ici, **les données ne servent pas à apprendre : elles sont le terrain lui-même.** On les traite **comme si on était en opération**. Les 382 000 messages Telegram, ce ne sont pas des « exemples d'entraînement ». C'est **le flux qu'un analyste recevrait** pendant la guerre, et on cherche ce qu'il contient.

**L'image qui aide :** dans God's Eye, quand tu passais une image satellite de Beyrouth dans ton modèle, tu étais « en opération ». Dans Spirit Digger, **on est en opération dès le début**. Les données Telegram *sont* nos « images de Beyrouth ».

---

## 3. Les trois rôles des données (ta question principale)

C'est le point qui crée la confusion : **nos données ne jouent pas toutes le même rôle.**

| Rôle | Jeux de données | À quoi ils servent | Équivalent dans God's Eye |
|---|---|---|---|
| **1. Le terrain** (le « cas réel ») | Telegram Ukraine (382 000 messages), presse Golfe 2026 (2 200 articles) | On les **analyse** pour produire du renseignement : alertes, inventaire, graphe, bulletins | Les images que tu passais au modèle en démo (Beyrouth, port, zone interdite) |
| **2. L'entraînement** | ISOT vrai/faux, propagande russe | On **entraîne** un détecteur de désinformation, dans le NB 05 uniquement | DOTA + xView |
| **3. La vérification** | Vérité terrain Ormuz, liste des 21 événements historiques, WELFake | On **vérifie** que nos outils disent vrai | Ton jeu de validation, et le mAP50 |

Donc :
- **la majorité du projet** (NB 02, 03, 04, 06) travaille sur le **rôle 1** : on est en situation réelle ;
- **un seul notebook** (NB 05, volet A) suit ta logique habituelle : entraînement, test, score ;
- le **rôle 3** sert à prouver que ça marche. C'est notre « mAP » : **17 événements sur 21 détectés**.

---

## 4. Est-ce un « noyau intelligent » réutilisable ?

**Oui, mais pas au sens d'un fichier `best.pt`.** Le « noyau », c'est **la chaîne de méthodes**. On peut lui donner **n'importe quel nouveau flux de textes**, et elle produira les mêmes types de résultats.

**Exemple concret :** demain, une crise éclate à Taïwan.
1. Tu branches de nouvelles sources : le collecteur RSS du NB 01, ou un nouvel export Telegram.
2. Tu relances les notebooks.
3. Tu obtiens **sans rien réentraîner** :
   - les alertes sur ce qui sort de l'ordinaire (NB 03) ;
   - l'inventaire des acteurs (NB 02) ;
   - la carte des relations (NB 04) ;
   - le bulletin coté (NB 06).

**Ce qu'il faut adapter à chaque théâtre**, comme on réglerait un capteur :

| Élément | Où | Pourquoi |
|---|---|---|
| Le **lexique militaire** (armements, sites…) | `src/spirit_digger/lexique_militaire.py` | Le modèle généraliste ne connaît pas Fordow ni les missiles Shahed |
| Les **camps** des sources | `config.py` (`CAMPS_TELEGRAM`) | Le recoupement compare des camps opposés |
| Le **répertoire des sites** et leurs coordonnées | NB 06 (`SITES`) | Pour savoir où envoyer God's Eye |
| Le **glossaire** de traduction | `analyse_ru.py` | Pour lire le russe en français |

C'est exactement comme God's Eye : le modèle était générique, mais tu choisissais tes **22 classes** selon la mission.

---

## 5. Chaque notebook en une phrase, avec son équivalent God's Eye

| NB | Ce qu'on fait | Y a-t-il un « modèle » ? | Équivalent God's Eye |
|---|---|---|---|
| **00** Reconnaissance | On note la fiabilité de chaque jeu de données et on démasque les jeux truqués | Non : de l'analyse de données | Vérifier que DOTA et xView sont propres avant d'entraîner |
| **01** Ingestion | On nettoie les textes et on les met tous au même format | Non : des règles de nettoyage | Le prétraitement et le découpage des images |
| **02** Scan et inventaire | On repère les personnes, armées, armes, sites et navires dans 2 200 articles | **Oui, mais pré-entraîné** (spaCy), complété par notre lexique | **Scénario 1 : l'inventaire YOLO** (avions, véhicules…) |
| **03** Alerte précoce | On détecte les jours où un mot « explose » chez tous les camps à la fois | Non : de la statistique (comparaison avec les 28 jours précédents) | **Scénarios 2 et 3 : comparer T0 et T1**, avec un score de risque |
| **04** Graphe | On relie les acteurs cités ensemble et on trouve les liens cachés | Non : des algorithmes de graphe | (nouveau, pas d'équivalent) |
| **05** Guerre de l'information | A : on entraîne un détecteur de propagande et on montre ses limites. B : on compare les récits russe et ukrainien | **Oui, entraîné par nous** (volet A) | **Le cas Beyrouth** : un modèle bon en labo, mauvais sur le terrain |
| **06** Bulletin | On cote chaque info selon la grille OTAN, on rédige le bulletin et on envoie une demande à God's Eye | Non : des règles et de l'assemblage | **Scénario 4 : la corrélation**, avec « ALERTE MAXIMALE » |

**Ce qu'il faut retenir :** sur les 7 notebooks, **un seul entraîne un modèle**. Ce n'est pas un défaut, c'est un choix délibéré, et c'est un argument fort pour toi (voir la section 7).

---

## 6. Comment ça marche « en vrai » : une journée d'opération

Imagine le 6 juin 2023 au matin, dans la cellule de veille :

1. **6 h, collecte (NB 01).** Les messages de la nuit arrivent des 12 chaînes et sont nettoyés automatiquement.
2. **6 h 05, détection (NB 03).** Le mot « Каховка » apparaît dans 446 messages, alors que la normale est proche de 0. Et ce n'est pas un seul camp : **les 5 camps** en parlent. Le score d'alerte atteint **355**, soit une **ALERTE MAXIMALE**.
3. **6 h 06, cotation (NB 06).** TASS (russe) et UNIAN (ukrainien), qui se contredisent sur tout, rapportent tous les deux l'événement. Le fait est donc certain : cotation **B1**.
4. **6 h 07, décryptage (NB 05).** Côté ukrainien, on lit « dynamitage », « par les Russes ». Côté russe, « frappe », « ВСУ » (l'armée ukrainienne). **Chacun accuse l'autre.**
5. **6 h 08, action (NB 06).** Un bulletin est rédigé, et une **demande d'observation satellite** part vers God's Eye : *« Barrage de Kakhovka, 46,78° N / 33,37° E, image avant le 30/05, image après le 07/06, appliquer le scénario 2 (évaluation des sinistres). »*

**Personne n'a lu les 800 messages de la nuit. Personne n'a dit à la machine de chercher « Kakhovka ».** C'est ça, la valeur du projet.

---

## 7. Pourquoi « pas de gros modèle », c'est une force (à dire en entretien)

Les acteurs de la défense (DGA, Thales, Naval Group, Airbus Defence, OTAN) se méfient des « boîtes noires ». Pour eux, un système doit être :

| Exigence défense | Comment Spirit Digger y répond |
|---|---|
| **Explicable** : « pourquoi cette alerte ? » | La réponse tient en une ligne : « le mot X est 50 fois plus fréquent que d'habitude, dans 5 camps » |
| **Traçable** : « d'où vient cette info ? » | Chaque lien du graphe est justifié par **la phrase source** |
| **Frugal** : il doit tourner sur le terrain | Tout tourne **sur un PC portable, sans GPU ni internet** |
| **Honnête sur ses limites** | Le NB 05 *prouve* qu'un détecteur à 91 % est trompé par une phrase bien écrite |
| **Conforme à la doctrine** | Cotation selon le **code de l'Amirauté** (OTAN), bulletin au format **BLUF** |

**La phrase à retenir :** *« J'ai volontairement utilisé des méthodes explicables plutôt qu'un grand modèle opaque, parce qu'en renseignement, un analyste doit pouvoir justifier chaque conclusion devant un officier. »*

---

## 8. Comment présenter le projet

### Le pitch en 30 secondes

> « Spirit Digger, c'est un analyste OSINT automatique. Il lit 380 000 messages Telegram en russe et en ukrainien, détecte seul les événements majeurs de la guerre, sans qu'on lui dise quoi chercher, et vérifie leur fiabilité en recoupant des camps qui se contredisent. Il cote chaque information comme le fait l'OTAN, et demande à mon autre projet, God's Eye, d'aller confirmer par satellite. **Le texte détecte, l'image confirme.** »

### Le déroulé de la démo, calqué sur ta présentation God's Eye

| Diapo | Contenu | Visuel (dans `outputs/`) |
|---|---|---|
| 1 | Titre : *Spirit Digger v1.0 · « Il s'infiltre dans le bruit, il creuse jusqu'au signal »* | – |
| 2 | La mission : trop de textes pour des humains | – |
| 3 | Avant de creuser : 2 jeux de données truqués démasqués (NB 00) | tableau du registre |
| 4 | **Scénario 1, inventaire** : les acteurs du Golfe 2026 | `02_rapport_inventaire.png` |
| 5 | **Scénario 2, alerte précoce** : 16 mois de guerre, 17 événements sur 21 trouvés seuls | `03_chronologie_alertes.png` |
| 6 | **Scénario 3, graphe** : les sous-théâtres et un lien caché | `04_graphe_coeur.png`, puis la carte HTML en direct |
| 7 | **Scénario 4, guerre de l'information** : chaque camp accuse l'autre | `05_kakhovka_recits.png` |
| 8 | **Le cas Beyrouth du texte** : la tour Eiffel « saisie » passe pour fiable à 100 % | tableau du crash-test (NB 05) |
| 9 | **Le bulletin** et la demande envoyée à God's Eye | `bulletin_2023-23.html`, `tasking_*.json` |
| 10 | Bilan et limites | tableau de bord (NB 06) |

### Les questions qu'on te posera, et quoi répondre

**« Quel modèle avez-vous entraîné ? »**
> « Un seul, un détecteur de désinformation, et je montre justement pourquoi il ne faut pas lui faire confiance seul. Le reste de la chaîne repose sur un modèle de langue pré-entraîné (spaCy) et sur des méthodes statistiques explicables. Le cœur du système, c'est le recoupement entre sources indépendantes. »

**« Quelle est la précision de votre système ? »**
> « On l'a validé sur 21 événements historiques documentés : 17 déclenchent une alerte, le jour même ou le lendemain, sans aucun mot-clé fourni. Les 4 restants sont expliqués : deux événements graduels (Bakhmout), deux éclipsés par d'autres actualités. »

**« Votre système prédit-il les événements ? »**
> « Non, et je le dis clairement. Il **détecte** très vite, il ne **prédit** pas. Avec des données horodatées à la minute, le délai de détection se compterait en minutes. »

**« Pourquoi ne pas utiliser ChatGPT ou un LLM ? »**
> « C'est l'extension naturelle, pour traduire et rédiger les bulletins. Mais le cœur du système doit rester explicable, frugal et capable de tourner hors ligne. Un LLM peut rédiger, il ne doit pas décider seul de ce qui est vrai. »

**« Quelle est la principale limite ? »**
> « Le graphe dit *qui* est lié, pas *comment* (alliés ou ennemis). Et un détecteur de style vieillit vite : sur la presse de 2026, il signale à tort un article sur cinq. »

---

## 9. Petit lexique (les mots qu'on a utilisés)

| Terme | En clair |
|---|---|
| **NLP** | *Natural Language Processing* : faire travailler un ordinateur sur du texte, comme la vision par ordinateur travaille sur des images |
| **OSINT** | Renseignement d'origine sources ouvertes : presse, réseaux sociaux, Telegram… Tout ce qui est public |
| **NER** | Reconnaissance d'entités nommées : repérer dans un texte les noms de personnes, lieux, organisations. C'est **le YOLO du texte** |
| **Lexique (gazetteer)** | Une liste de termes métier ajoutée au modèle (« Fordow » = site stratégique) |
| **Score z** | « Combien de fois c'est plus que d'habitude », en tenant compte du hasard. 3 = inhabituel, 50 = séisme |
| **Ligne de base** | Ce qui est « normal » : la fréquence d'un mot sur les 28 jours précédents. C'est le **T0** de God's Eye |
| **Convergence des camps** | Combien de camps opposés parlent de la même chose. C'est la base de la fiabilité |
| **Co-citation** | Deux entités citées dans la même phrase. C'est ce qui crée un lien dans le graphe |
| **PMI** | Mesure si deux entités apparaissent ensemble *plus souvent que par hasard*. Elle sépare les vrais liens des évidences |
| **Communauté** | Un groupe d'acteurs très liés entre eux, comme un sous-théâtre du conflit |
| **Intermédiarité** | Un acteur qui fait le **pont** entre des groupes |
| **TF-IDF** | Une façon de transformer un texte en nombres, selon les mots importants qu'il contient |
| **Fuite de données (data leakage)** | Quand le modèle triche grâce à un détail sans rapport, comme un crédit photo qui n'apparaît que dans les faux articles |
| **Dérive (drift)** | Un modèle qui marche sur les données d'hier mais plus sur celles d'aujourd'hui. C'est le **cas Beyrouth** |
| **Log-odds ratio (« mots de combat »)** | Mesure quels mots sont typiques d'un camp par rapport à l'autre |
| **Code de l'Amirauté** | La grille OTAN : une lettre pour la fiabilité de la source (A à F), un chiffre pour la crédibilité de l'info (1 à 6). « B1 » = source fiable, info confirmée |
| **BLUF** | *Bottom Line Up Front* : l'essentiel en premier, format militaire des notes |
| **Tasking** | Une demande d'observation adressée à un capteur, ici le satellite de God's Eye |

---

## 10. Le cycle du renseignement : le cadre que connaissent les militaires

Si tu ne retiens qu'un schéma pour ta présentation, retiens celui-ci. Les services de renseignement travaillent selon un **cycle**, et Spirit Digger **automatise chacune de ses étapes** :

```
        ┌──────────────────────────────┐
        │ 1. ORIENTATION               │   Quelles questions ? Quelles sources ?   → NB 00
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────┐
        │ 2. RECHERCHE (collecte)      │   Aller chercher l'information            → NB 01
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────┐
        │ 3. EXPLOITATION (analyse)    │   Extraire, détecter, relier, décrypter   → NB 02 · 03 · 04 · 05
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────┐
        │ 4. DIFFUSION                 │   Bulletin coté + demande à God's Eye     → NB 06
        └──────────────┬───────────────┘
                       └──────► retour à l'orientation (God's Eye confirme ou infirme)
```

**C'est ça, le projet :** pas « un modèle qui prédit », mais **le cycle du renseignement automatisé sur du texte**. Et God's Eye en est le prolongement sur l'image.
