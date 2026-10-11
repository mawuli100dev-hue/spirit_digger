# Spirit Digger v1.0

> *Il s'infiltre dans le bruit. Il creuse jusqu'au signal.*

**Rôle joué :** analyste d'une cellule de veille OSINT (renseignement d'origine sources ouvertes).
**Mission :** lire des centaines de milliers de messages en plusieurs langues, là où la lecture humaine ne suffit plus. Il faut en extraire les acteurs, détecter les signaux faibles, relier les entités, démasquer la propagande et produire automatiquement un bulletin de renseignement coté.

Ce projet est le pendant « texte » de **God's Eye v2.0** (imagerie satellite). Les deux peuvent se parler : le bulletin final émet une demande d'observation satellite.

---

## Les deux théâtres d'opérations

| Théâtre | Source | Volume | Pourquoi |
|---|---|---|---|
| **UKRAINE 2022-2023** | 12 chaînes Telegram, 5 camps (État russe, Ukraine, presse russe en exil, international) | 382 000 messages, 3 langues | daté et multi-camps : idéal pour l'alerte précoce et le recoupement |
| **GOLFE 2026** | presse Iran / États-Unis et vérité terrain sur le trafic du détroit d'Ormuz | 2 236 articles, 125 jours de mesures | riche en acteurs : idéal pour l'inventaire et le graphe |

Événements de référence pour la démo : **destruction du barrage de Kakhovka** (06/06/2023), **mutinerie Wagner** (23/06/2023) et **fermeture du détroit d'Ormuz** (28/02/2026).

## Scénarios et notebooks

| NB | Scénario | Ce que Spirit Digger fait | Statut |
|---|---|---|---|
| 00 | Reconnaissance | cote chaque source (code de l'Amirauté), démasque les jeux synthétiques et les fuites | ✅ |
| 01 | Ingestion | nettoie, dédoublonne et normalise 4 corpus ; collecteur RSS en direct | ✅ |
| 02 | **Scan et inventaire** | NER spaCy et lexique militaire : personnes, forces, armements, sites, navires, opérations ; rapport d'inventaire ; recoupement terrain | ✅ |
| 03 | **Alerte précoce** | détecte les ruptures de vocabulaire et la convergence des camps, sans mot-clé ; 17 événements de référence sur 21 en ALERTE | ✅ |
| 04 | **Graphe de relations** | sous-théâtres détectés automatiquement, pivots, liens cachés sourcés phrase par phrase, carte interactive HTML | ✅ |
| 05 | **Guerre de l'information** | détecteur 3 classes (91 % en test) puis démonstration de ses limites (crash-test, dérive temporelle) ; narratifs opposés sur Kakhovka et Wagner | ✅ |
| 06 | **Corrélation et bulletin** | cotation OTAN automatique (code de l'Amirauté), bulletins HTML imprimables, demandes d'observation JSON pour God's Eye, tableau de bord final | ✅ |

## Découvertes (NB 00-06)

- `Cybersecurity_Dataset` et `cybersecurity synthesized data` sont **générés aléatoirement** : 24,7 % d'accord catégorie/prédiction (le hasard donne 25 %), IP impossibles, corrélations nulles. Ils sont **écartés**.
- Le jeu vrai/faux contient des **fuites** : crédits Getty Images, liens Twitter, « Featured image ». Un modèle naïf « tricherait ». Le nettoyage fait passer la fuite de 31 % à 0,2 %.
- Le sous-ensemble « propagande russe » est **entièrement extrait** du jeu « faux ».
- 66 % de WELFake recoupe ISOT : il faut dédoublonner avant tout test.
- 67 % des articles Golfe n'ont pas de date : ce corpus n'est pas exploitable pour l'alerte précoce.
- NER : le modèle généraliste classe Fordow comme un « produit » et Trump comme une « organisation » dans la moitié des cas. Le lexique militaire et le vote majoritaire corrigent ces erreurs. La presse ne nomme que 2 des 13 navires attaqués à Ormuz : c'est un angle mort.
- Alerte précoce, sans mot-clé : Kakhovka, pont de Crimée, mobilisation et Wagner sont détectés le jour même et par les 5 camps. Bakhmout (événement graduel) et Boutcha passent sous le seuil. Le système détecte, il ne prédit pas.
- La plupart des ruptures portées par un seul camp sont du bruit éditorial : un changement de pied de message chez UNIAN en est l'exemple type.
- Graphe : 7 sous-théâtres émergent sans supervision (pouvoir iranien, Ormuz naval, Israël-Liban, médiation, nucléaire…). La translittération éclatait 50 personnes en plusieurs orthographes (Ghalibaf / Qalibaf) et créait de faux « liens cachés » ; c'est corrigé au NB 02. Certaines co-citations sont des artefacts journalistiques (« la BBC a contacté l'IDF et le CENTCOM »), d'où l'importance de sourcer chaque lien.
- Détecteur de désinformation : le modèle « tricheur » apprend les crédits photo ; le modèle propre apprend le style et l'époque (« 2016 », « Hillary »). Un mensonge rédigé en style d'agence passe pour fiable à 100 %, et 22 % des articles de presse de 2026 sont signalés à tort. C'est le « cas Beyrouth » du texte, d'où le choix du recoupement multi-sources pour juger la fiabilité.
- WELFake : contrairement à sa documentation, l'étiquette 1 signifie « faux ». Vérifié sur les textes communs avec ISOT.
- Kakhovka : les chaînes ukrainiennes nomment les « occupants » (33 %) et l'acte délibéré (60 %) ; les médias d'État russes désignent les ВСУ (14 %) et parlent de frappes (25 %), et consacrent moins d'antenne à l'événement (22 % contre 33 %).
- Cotation : avec une règle de recoupement exigeante (un camp ne confirme que s'il consacre au moins 2 % de ses messages au sujet), les grands événements sortent en B1 ou B2. Les alertes D4, portées par les seuls médias d'État russes, sont à vérifier.
- Piège technique : avec pandas 3, le `` des expressions régulières (moteur RE2) ne fonctionne pas sur le cyrillique.

## Données

Les données brutes ne sont **pas incluses dans ce dépôt** : elles sont trop lourdes (jusqu'à 273 Mo par fichier) et appartiennent à leurs auteurs. Ce sont des jeux publics, à placer dans un dossier `data_lake/` à la racine du projet, avec cette arborescence :

| Dossier et fichier attendus | Contenu |
|---|---|
| `news_but_in_russian_lg/news.csv` | 386 889 messages de 12 chaînes Telegram russes et ukrainiennes (2022-2023) |
| `iran_us_news_dataset/iran_us_news_dataset.csv` | 2 286 articles de presse Iran / États-Unis (2025-2026) |
| `strait_of_hormuz_shipping_disruption_2026/strait_of_hormuz_shipping_disruption_2026 (1).csv` | trafic quotidien du détroit d'Ormuz (2026) |
| `MisInfo_propagande/DataSet_Misinfo_TRUE.csv` · `DataSet_Misinfo_FAKE.csv` · `EXTRA_RussianPropagandaSubset.csv` | articles vrais / faux (ISOT) et propagande (EUvsDisinfo) |
| `WELFake_Dataset/WELFake_Dataset.csv` | articles vrais / faux (WELFake) |
| `rumor_dataset/rumor_dataset.csv` | rumeurs sur Twitter (PHEME) |
| `global_trending_topics/global_trending_topics.csv` | sujets tendance mondiaux (2026) |
| `posts_information/top_by_score.csv` | posts Reddit r/geopolitics |
| `Cybersecurity_Dataset/Cybersecurity_Dataset.csv` · `cybersecurity synthesized data/cybersecurity synthesized data.csv` | jeux cyber (écartés au NB 00 : synthétiques) |

Le registre complet des sources est dans `src/spirit_digger/config.py`. Les fichiers Parquet de `outputs/` sont régénérés par les notebooks 01 et 02 ; les images, graphes HTML, bulletins et fichiers CSV de résultats sont inclus dans le dépôt.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
jupyter lab
```

Ouvre ensuite `notebooks/` et exécute les notebooks **dans l'ordre**. Le NB 01 crée les fichiers de `outputs/` dont tous les suivants ont besoin.

Aucun GPU n'est nécessaire : tous les modèles sont choisis pour tourner sur un ordinateur portable.

## Livrables de démo (dans `outputs/`)

| Fichier | Usage |
|---|---|
| `bulletin_2023-23.html` · `bulletin_2023-25.html` | bulletins de renseignement (Kakhovka, Wagner), à ouvrir ou imprimer en PDF |
| `tasking_gods_eye_*.json` | demandes d'observation satellite pour God's Eye |
| `04_graphe_golfe.html` | carte interactive des relations (théâtre GOLFE) |
| `02_rapport_inventaire.png` · `03_chronologie_alertes.png` · `04_graphe_coeur.png` · `05_kakhovka_recits.png` | visuels pour les slides |

## Structure

```
data_lake/         sources brutes (ne jamais modifier)
notebooks/         un notebook par scénario
src/spirit_digger/ code partagé : chemins, chargement, nettoyage, style
outputs/           produits générés : corpus propres, graphes, bulletins
```

## Compétences démontrées (vocabulaire des offres défense)

Qualité et provenance des données · détection de fuites (data leakage) · NLP multilingue et NER · détection d'anomalies sur séries temporelles · analyse de graphes · classification par transformers · génération automatique de rapports · cotation des sources (code de l'Amirauté, STANAG 2511) · éthique OSINT.
