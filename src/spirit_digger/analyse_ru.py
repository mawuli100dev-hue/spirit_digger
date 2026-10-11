"""Versions réutilisables des outils d'analyse du corpus Telegram présentés aux NB 03 et 05."""
import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

# --- NB 03 : racines ---------------------------------------------------------
MOT_RACINE = re.compile(r"[а-яёіїєґ]{5,}")
FAUSSES_RUPTURES = {
    "января", "феврал", "марта", "апреля", "ноября", "август", "сентяб", "октябр", "декабр",
    "понеде", "вторни", "среду", "четвер", "пятниц", "суббот", "воскре",
    "подпис", "присла", "новост", "telegr",
}


def racines(texte):
    """Ensemble des racines (6 premières lettres) des mots de 5 lettres ou plus."""
    return {mot[:6] for mot in MOT_RACINE.findall(texte.lower())} - FAUSSES_RUPTURES


# --- NB 05 : pieds de message et mots de combat ------------------------------
def retirer_pieds(corpus, seuil=50):
    """Retire les fins de message répétées au moins `seuil` fois par une même chaîne."""
    fins = corpus["texte"].str.extract(r"([^.!?]{8,90})$")[0].str.strip()
    frequentes = pd.DataFrame({"s": corpus["source"], "f": fins}).dropna().value_counts()
    pieds = defaultdict(list)
    for (chaine, pied), _ in frequentes[frequentes >= seuil].items():
        pieds[chaine].append(pied)

    def nettoyer(chaine, texte):
        for pied in pieds.get(chaine, []):
            if texte.endswith(pied):
                return texte[: -len(pied)].rstrip(" /|.")
        return texte

    return [nettoyer(c, t) for c, t in zip(corpus["source"], corpus["texte"])]


MOT = re.compile(r"[а-яёіїєґ]{4,}")
MOTS_OUTILS = set("""больше того через чтобы если после также будет будут этого этом есть было были может сейчас
более когда только который которые которая которых всех свои своей него этой этот эти очень даже однако ними
можно нужно себя всего между здесь там тоже потому где какие какой""".split())


def presence(textes):
    c = Counter()
    for t in textes:
        c.update(set(MOT.findall(t.lower())) - MOTS_OUTILS)
    return c


def mots_de_combat(messages, camp_a, camp_b, fond, taille_fond, n=10, min_occ=6):
    """Log-odds ratio lissé (Monroe et al., 2008) : mots typiques du camp A face au camp B."""
    a = presence(messages.loc[messages["camp"] == camp_a, "texte"])
    b = presence(messages.loc[messages["camp"] == camp_b, "texte"])
    na, nb = max((messages["camp"] == camp_a).sum(), 1), max((messages["camp"] == camp_b).sum(), 1)
    lignes = []
    for w in set(a) | set(b):
        if a[w] + b[w] < min_occ:
            continue
        prior = 10 * (fond[w] + 1) / taille_fond
        pa, pb = (a[w] + prior) / (na + 10), (b[w] + prior) / (nb + 10)
        z = (np.log(pa / (1 - pa)) - np.log(pb / (1 - pb))) / np.sqrt(1 / (a[w] + prior) + 1 / (b[w] + prior))
        lignes.append((w, z, a[w] / na, b[w] / nb))
    df = pd.DataFrame(lignes, columns=["mot", "z", "part_a", "part_b"]).sort_values("z")
    return df.tail(n).iloc[::-1], df.head(n)


# Frontières de mots explicites : avec pandas 3 (moteur RE2), « \b » ne fonctionne pas sur le cyrillique.
D = r"(?:^|[^а-яёіїєґ])"
F = r"(?:[^а-яёіїєґ]|$)"
MARQUEURS = {
    "désigne les forces russes": r"оккупант|рашист|россиян",
    "désigne les forces ukrainiennes": D + "всу" + F + r"|киевск\w* режим",
    "vocabulaire de frappe": D + r"удар|обстрел|диверси",
    "vocabulaire d'acte délibéré": r"подрыв|подорвал|взорвал|заминир",
    "qualification (terrorisme, crime)": r"теракт|экоцид|военн\w* преступлен",
}

# --- Glossaire russe → français (racines du NB 03 et mots du NB 05) -----------
GLOSSAIRE = {
    "каховс": "Kakhovka", "каховк": "Kakhovka", "затопл": "inondation", "плотин": "barrage", "подтоп": "submersion",
    "дамбы": "digue", "крымск": "de Crimée", "мосту": "pont", "моста": "pont", "керчен": "Kertch", "паромн": "ferry",
    "землет": "séisme", "турции": "Turquie", "сирии": "Syrie", "ейске": "Ieïsk", "самоле": "avion",
    "падени": "chute", "крушен": "crash", "винниц": "Vinnytsia", "прилеп": "Prilepine", "бровар": "Brovary",
    "вертол": "hélicoptère", "еленов": "Olenivka", "пленны": "prisonniers", "новофе": "Novofedorivka",
    "аэродр": "aérodrome", "мобили": "mobilisation", "частич": "partielle", "тайван": "Taïwan", "пелоси": "Pelosi",
    "рефере": "référendum", "ижевск": "Ijevsk", "стрель": "fusillade", "школе": "école", "костро": "Kostroma",
    "брянск": "Briansk", "диверс": "sabotage", "крамат": "Kramatorsk", "вокзал": "gare", "джанко": "Djankoï",
    "вагнер": "Wagner", "ростов": "Rostov", "мятеж": "mutinerie", "пригож": "Prigojine", "кремен": "Krementchouk",
    "крейсе": "croiseur", "москва": "Moskva", "флагма": "navire amiral", "белгор": "Belgorod", "нефтеб": "dépôt pétrolier",
    "татарс": "Tatarsky", "владле": "Vladlen", "стамбу": "Istanbul", "перего": "négociations", "гершко": "Gershkovich",
    "елизав": "Elizabeth", "короле": "reine", "дугино": "Douguina", "дугина": "Douguina", "польше": "Pologne",
    "польши": "Pologne", "ракета": "missile", "херсон": "Kherson", "сурови": "Sourovikine", "днепре": "Dnipro",
    "кремль": "Kremlin", "кремле": "Kremlin", "беспил": "drone", "северн": "Nord (Stream)", "газопр": "gazoduc",
    "зверст": "atrocités", "убийст": "meurtre", "бахмут": "Bakhmout", "артемо": "Artemovsk (Bakhmout)",
    "мятежа": "mutinerie", "липецк": "Lipetsk", "вороне": "Voronej", "контрт": "antiterroriste",
    "подрыва": "dynamitage", "подрыв": "dynamitage", "дамбу": "digue", "водой": "eau", "взорвали": "ont fait sauter",
    "российские": "russes", "российскими": "par les Russes", "разрушена": "détruite", "оккупанты": "les occupants",
    "оккупантами": "par les occupants", "рашисты": "« rashistes »", "снбо": "Conseil de sécurité ukr.",
    "укргидроэнерго": "Ukrhydroenergo", "сообщил": "a annoncé", "сообщили": "ont annoncé", "разрушения": "destruction",
    "области": "région", "власти": "autorités", "администрации": "administration", "сальдо": "Saldo",
    "леонтьев": "Leontiev", "удар": "frappe", "режим": "régime", "воды": "eau", "заявил": "a déclaré",
    "вооруженного": "armée (mutinerie armée)", "ситуации": "situation", "пригожин": "Prigojine",
    "вагнеровцы": "les wagnériens", "вагнеровцев": "les wagnériens", "москву": "Moscou", "шойгу": "Choïgou",
    "сообщают": "on rapporte", "сообщается": "il est rapporté", "президента": "président", "евгения": "Evgueni",
    "владимир": "Vladimir (Saldo)", "отравл": "empoisonnement", "ульяно": "Oulianovsk", "самарс": "Samara",
    "дону": "(Rostov-sur-le-)Don", "трюдо": "Trudeau", "джасти": "Justin", "канады": "Canada", "чонгар": "Tchonhar", "титан": "Titan (sous-marin)",
    "батиск": "bathyscaphe", "атлант": "Atlantique", "липецк": "Lipetsk", "воронеж": "Voronej",
}


def traduire(mot):
    return GLOSSAIRE.get(mot, GLOSSAIRE.get(mot[:6], "–"))
