"""Chargement des sources brutes du data lake."""
import pandas as pd

from .config import SOURCES


def charger(nom, **kwargs):
    """Charge une source du registre SOURCES en DataFrame (kwargs transmis à read_csv)."""
    options = dict(encoding="utf-8", encoding_errors="replace", low_memory=False)
    options.update(kwargs)
    df = pd.read_csv(SOURCES[nom], **options)
    return df.drop(columns=[c for c in df.columns if str(c).startswith("Unnamed")])
