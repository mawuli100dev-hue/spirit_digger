"""Chemins et registre des sources du data lake."""
from pathlib import Path


def find_root(start=None):
    """Remonte l'arborescence jusqu'au dossier qui contient data_lake/."""
    p = Path(start or Path.cwd()).resolve()
    for d in [p, *p.parents]:
        if (d / "data_lake").is_dir():
            return d
    raise FileNotFoundError("Dossier data_lake introuvable : ouvre le notebook depuis le projet.")


ROOT = find_root()
DATA_LAKE = ROOT / "data_lake"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

# Registre des sources brutes : nom court -> fichier
SOURCES = {
    "iran_us_news":    DATA_LAKE / "iran_us_news_dataset" / "iran_us_news_dataset.csv",
    "hormuz":          DATA_LAKE / "strait_of_hormuz_shipping_disruption_2026" / "strait_of_hormuz_shipping_disruption_2026 (1).csv",
    "telegram_ru_ua":  DATA_LAKE / "news_but_in_russian_lg" / "news.csv",
    "misinfo_true":    DATA_LAKE / "MisInfo_propagande" / "DataSet_Misinfo_TRUE.csv",
    "misinfo_fake":    DATA_LAKE / "MisInfo_propagande" / "DataSet_Misinfo_FAKE.csv",
    "propagande_ru":   DATA_LAKE / "MisInfo_propagande" / "EXTRA_RussianPropagandaSubset.csv",
    "welfake":         DATA_LAKE / "WELFake_Dataset" / "WELFake_Dataset.csv",
    "rumeurs":         DATA_LAKE / "rumor_dataset" / "rumor_dataset.csv",
    "trending":        DATA_LAKE / "global_trending_topics" / "global_trending_topics.csv",
    "reddit_geopol":   DATA_LAKE / "posts_information" / "top_by_score.csv",  # posts.csv est corrompu
    "cyber_threats":   DATA_LAKE / "Cybersecurity_Dataset" / "Cybersecurity_Dataset.csv",
    "cyber_synth":     DATA_LAKE / "cybersecurity synthesized data" / "cybersecurity synthesized data.csv",
}

# Chaînes Telegram du corpus Ukraine 2022-2023, rangées par « camp ».
# C'est la base du recoupement : une info confirmée par plusieurs camps opposés vaut beaucoup plus.
CAMPS_TELEGRAM = {
    "TASS": "Russie - État",
    "RIA News": "Russie - État",
    "RBK": "Russie - presse sous contrainte",
    "Ukraine Now": "Ukraine",
    "УНИАН": "Ukraine",
    "Ukraine24": "Ukraine",
    "Shocked Ukraine": "Ukraine",
    "Meduza": "Russe indépendant (exil)",
    "Novaya Gazeta": "Russe indépendant (exil)",
    "BBC Russia": "International",
    "Washington Post": "International",
    "The New York Times": "International",
}
