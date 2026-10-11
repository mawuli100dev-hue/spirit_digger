"""Nettoyage de texte : la « décontamination » avant toute analyse."""
import hashlib
import html
import re
import unicodedata

HTML_TAG = re.compile(r"<[^>]+>")
URL = re.compile(r"https?://\S*|www\.\S+")
ESPACES = re.compile(r"\s+")
# « …in Tehran.Leaders from… » : phrases collées par la suppression des retours à la ligne.
# On ne sépare qu'après deux minuscules, pour ne pas casser les sigles (« U.S.A »).
PHRASES_COLLEES = re.compile(r"(?<=[a-zа-яё]{2}[.!?])(?=[A-ZА-ЯЁ])")

# Mentions légales russes « agent de l'étranger » imposées à Meduza, Novaya Gazeta...
# Si on les garde, un modèle apprend à reconnaître la source au lieu du contenu.
AGENT_ETRANGER = re.compile(
    r"\*?\s*(?:ДАННОЕ СООБЩЕНИЕ|НАСТОЯЩИЙ МАТЕРИАЛ)[А-ЯЁ0-9\s()\-,«»\"*]+\.?"
)

# Signatures qui trahissent la source dans les jeux « vrai / faux » (fuite de données).
SIGNATURES_SOURCE = [
    re.compile(r"^.{0,80}?\(Reuters\)\s*-\s*"),                    # "WASHINGTON (Reuters) - "
    re.compile(r"\(Reuters\)"),
    re.compile(r"featured image\b[^\n]{0,150}$", re.I),            # crédit photo en fin d'article
    re.compile(r"(?:photo|image)s? (?:by|via|credit|courtesy)[^\n]{0,150}$", re.I),
    re.compile(r"[\w .,'/-]{0,60}Getty Images[\w .,'/-]{0,60}"),
    re.compile(r"21st Century Wire", re.I),
    re.compile(r"pic\.twitter\.com/\S+"),
]


# Résidus de pages web aspirées (lecteurs vidéo, boutons de partage...).
BOILERPLATE_WEB = re.compile(
    r"To view this video please enable JavaScript[^.]*?HTML5 video"
    r"|To play this video you need to enable JavaScript in your browser\."
    r"|This video can ?not be played"
    r"|JavaScript seems to be disabled\. Please enable JavaScript to take full advantage[^.]*\.?"
    r"|- BBC iPlayer Close menu Home"
    r"|Share close panel Share page Copy link About sharing"
    r"|Close More on this story\.?"
    r"|Baca juga:",
    re.I,
)

MOTS_OUTILS = {
    "en": {"the", "and", "of", "to", "in", "is", "that", "for", "with", "was", "on", "said"},
    "id": {"yang", "dan", "di", "dengan", "untuk", "dari", "ini", "itu", "akan", "juga", "pada"},
    "fr": {"le", "la", "les", "et", "des", "est", "une", "dans", "pour", "que", "du"},
    "de": {"der", "die", "und", "das", "ist", "nicht", "mit", "von", "den", "auf"},
}


def detecter_langue_latine(texte):
    """Devine la langue d'un texte en alphabet latin en comptant ses mots-outils."""
    mots = re.findall(r"[a-zà-ÿ]+", texte.lower()[:3000])
    scores = {langue: sum(m in outils for m in mots) for langue, outils in MOTS_OUTILS.items()}
    return max(scores, key=scores.get)


def nettoyer_texte(texte, retirer_urls=True):
    """Normalise un texte brut : entités HTML, unicode, balises, URLs, mentions légales, espaces."""
    if not isinstance(texte, str):
        return ""
    t = unicodedata.normalize("NFC", html.unescape(texte))
    t = HTML_TAG.sub(" ", t)
    if retirer_urls:
        t = URL.sub(" ", t)
    t = AGENT_ETRANGER.sub(" ", t)
    t = BOILERPLATE_WEB.sub(" ", t)
    t = t.replace(" ", " ").replace("�", " ")
    t = PHRASES_COLLEES.sub(" ", t)
    return ESPACES.sub(" ", t).strip()


def retirer_signatures(texte):
    """Supprime les marqueurs de source (Reuters, crédits photo...) pour éviter la triche du modèle."""
    t = texte
    for motif in SIGNATURES_SOURCE:
        t = motif.sub(" ", t)
    return ESPACES.sub(" ", t).strip()


def empreinte(texte, n=300):
    """Empreinte courte d'un texte : sert à repérer les doublons (même dépêche reprise)."""
    base = re.sub(r"[^\w]", "", texte.lower())[:n]
    return hashlib.md5(base.encode("utf-8")).hexdigest()
