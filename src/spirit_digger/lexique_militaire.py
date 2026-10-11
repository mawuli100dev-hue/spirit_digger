"""Lexique militaire : ce qu'un modèle NER généraliste ne connaît pas (ou classe mal).

Un modèle entraîné sur de l'actualité générale voit « Fordow » comme un produit et
« Shahed » comme une personne. Les cellules de renseignement complètent toujours le
modèle statistique par des listes métier (gazetteers) : c'est ce qu'on fait ici.
"""

LEXIQUE = {
    "FORCE_ARMEE": [
        "IRGC", "Islamic Revolutionary Guard Corps", "Revolutionary Guard", "Revolutionary Guards",
        "Quds Force", "Basij", "Artesh", "CENTCOM", "US Central Command", "Pentagon", "US Navy",
        "Fifth Fleet", "US Air Force", "IDF", "Israel Defense Forces", "Israeli Air Force", "Mossad",
        "Hezbollah", "Houthis", "Houthi", "Hamas", "Kataib Hezbollah", "NATO", "Wagner",
    ],
    "ARMEMENT": [
        "ballistic missile", "ballistic missiles", "cruise missile", "cruise missiles", "hypersonic missile",
        "drone", "drones", "Shahed", "Shahed-136", "kamikaze drone", "naval mine", "naval mines", "sea mines",
        "B-2", "B-2 bomber", "B-2 bombers", "B-52", "F-35", "F-35s", "F-15", "F-16", "A-10", "AH-64", "Apache helicopters",
        "GBU-57", "GBU-72", "bunker buster", "bunker busters", "bunker-buster", "Tomahawk", "Tomahawks",
        "THAAD", "Patriot missile", "Patriot missiles", "Iron Dome", "S-300", "S-400", "Fattah", "Kheibar", "Sejjil",
        "fast attack craft", "speedboats", "minelayers",
    ],
    "SITE_STRATEGIQUE": [
        "Fordow", "Natanz", "Isfahan", "Arak", "Bushehr", "Parchin", "Kharg Island", "Kharg",
        "Bandar Abbas", "Strait of Hormuz", "Hormuz", "Gulf of Oman", "Persian Gulf", "Ras Tanura",
        "Diego Garcia", "Al Udeid", "Bab el-Mandeb", "Red Sea", "Larak", "Qeshm", "Abu Musa",
    ],
    "NAVIRE": [
        "aircraft carrier", "aircraft carriers", "destroyer", "destroyers", "frigate", "warship", "warships",
        "tanker", "tankers", "oil tanker", "oil tankers", "VLCC", "supertanker", "container ship",
        "bulk carrier", "LNG carrier", "minesweeper", "minesweepers",
    ],
    "AGENCE_INTERNATIONALE": [
        "IAEA", "International Atomic Energy Agency", "UN Security Council", "UNSC", "OPEC", "IMO",
    ],
}

# Motifs (règles sur les jetons) pour les noms propres à structure fixe.
MOTIFS = [
    # « USS Gerald R. Ford » : jusqu'à 3 mots après le préfixe
    ("NAVIRE", [{"TEXT": "USS"}, {"IS_TITLE": True}, {"IS_TITLE": True, "OP": "?"}, {"IS_TITLE": True, "OP": "?"}]),
    ("NAVIRE", [{"TEXT": "HMS"}, {"IS_TITLE": True}, {"IS_TITLE": True, "OP": "?"}]),
    ("OPERATION", [{"TEXT": "Operation"}, {"IS_TITLE": True}, {"IS_TITLE": True, "OP": "?"}]),
]

# Formes équivalentes → forme canonique (sinon « US », « U.S. » et « United States » comptent pour 3).
ALIAS = {
    "us": "United States", "u.s.": "United States", "u.s": "United States", "usa": "United States", "america": "United States",
    "the united states": "United States", "washington": "United States",
    "islamic republic": "Iran", "tehran": "Iran", "islamic republic of iran": "Iran",
    "uk": "United Kingdom", "britain": "United Kingdom", "u.k.": "United Kingdom",
    "uae": "United Arab Emirates", "emirates": "United Arab Emirates",
    "islamic revolutionary guard corps": "IRGC", "revolutionary guard": "IRGC", "revolutionary guards": "IRGC",
    "us central command": "CENTCOM", "u.s. central command": "CENTCOM", "central command": "CENTCOM",
    "israel defense forces": "IDF", "security council": "UN Security Council",
    "united nations security council": "UN Security Council", "un security council": "UN Security Council",
    "international atomic energy agency": "IAEA", "unsc": "UN Security Council",
    "houthi": "Houthis", "fordo": "Fordow", "hormuz": "Strait of Hormuz", "kharg": "Kharg Island",
    "un": "United Nations", "eu": "European Union",
    "seyyed ali khamenei": "Ali Khamenei", "bibi netanyahu": "Benjamin Netanyahu",
    "bunker busters": "bunker buster", "bunker-buster": "bunker buster",
    "b-2 bomber": "B-2", "shahed-136": "Shahed", "drones": "drone",
}

# Navires attaqués d'après le journal de la vérité terrain (Ormuz 2026).
NAVIRES_ATTAQUES_TERRAIN = [
    "Safeen Prestige", "Prima", "Louis P", "Mayuree Naree", "Al Salmi", "Aqua 1", "MSC Ishyka",
    "Sanmar Herald", "Epaminondas", "MSC Francesca", "Express Rome", "Iron Maiden", "Bogazici",
]


def ajouter_lexique(nlp):
    """Insère un EntityRuler AVANT le NER statistique : le lexique métier a priorité."""
    ruler = nlp.add_pipe("entity_ruler", before="ner", config={"phrase_matcher_attr": "LOWER"})
    motifs = [{"label": label, "pattern": terme} for label, termes in LEXIQUE.items() for terme in termes]
    motifs += [{"label": label, "pattern": motif} for label, motif in MOTIFS]
    ruler.add_patterns(motifs)
    return nlp


TITRES = ("ayatollah ", "president ", "supreme leader ", "prime minister ", "foreign minister ",
          "defense secretary ", "defence secretary ", "secretary of state ", "secretary ", "general ",
          "gen. ", "sheikh ", "mr ", "mr. ", "vice president ")

_FORMES = {terme.lower(): terme for termes in LEXIQUE.values() for terme in termes}


def canonique(texte):
    """Forme normalisée d'une entité : sans article, titre ni possessif ; casse, pluriels et alias unifiés."""
    t = texte.strip().strip("\"'“”‘’()[],.:;")
    t = t.removesuffix("'s").removesuffix("’s").strip()
    bas = t.lower()
    for prefixe in ("the ", *TITRES):
        if bas.startswith(prefixe):
            t, bas = t[len(prefixe):], bas[len(prefixe):]
    if bas.endswith("s") and bas[:-1] in _FORMES:  # pluriel d'un terme du lexique → singulier
        bas = bas[:-1]
    if bas in ALIAS:
        return ALIAS[bas]
    return _FORMES.get(bas, t)
