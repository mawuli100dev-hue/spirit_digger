"""Habillage : bandeaux de notebook et thème des graphiques (fond blanc, prêt pour les slides)."""
import matplotlib.pyplot as plt

FOND = "#ffffff"
PANNEAU = "#ffffff"
TEXTE = "#1f1747"     # violet très foncé, lisible sur blanc
GRILLE = "#e6e2f2"
ACCENT = "#6d4ad6"    # violet Spirit Digger
ALERTE = "#d6334a"
VEILLE = "#d98a00"
OK = "#12936b"

PALETTE = [ACCENT, OK, VEILLE, ALERTE, "#2f86c9", "#c2459c", "#8a8fa6"]


def theme_ops():
    """Applique le thème clair à tous les graphiques matplotlib suivants."""
    plt.rcParams.update({
        "figure.facecolor": FOND, "axes.facecolor": PANNEAU, "savefig.facecolor": FOND,
        "axes.edgecolor": GRILLE, "axes.labelcolor": TEXTE, "axes.titlecolor": TEXTE,
        "xtick.color": TEXTE, "ytick.color": TEXTE, "text.color": TEXTE,
        "grid.color": GRILLE, "axes.grid": True, "grid.alpha": 0.9,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "font.family": "sans-serif", "figure.figsize": (12, 5), "axes.titleweight": "bold",
    })


def bandeau(titre, sous_titre="", niveau="EXERCICE"):
    """Affiche un bandeau de mission en tête de notebook."""
    from IPython.display import HTML, display
    couleur = {"EXERCICE": ACCENT, "ALERTE": ALERTE, "VEILLE": VEILLE}.get(niveau, ACCENT)
    display(HTML(f"""
    <div style="background:#f6f4fc;border-left:6px solid {couleur};padding:14px 18px;
                font-family:monospace;color:{TEXTE};border-radius:6px">
      <div style="color:{couleur};font-size:11px;letter-spacing:3px">
        SPIRIT DIGGER v1.0 // {niveau} // SOURCES OUVERTES UNIQUEMENT</div>
      <div style="font-size:22px;font-weight:bold;margin-top:4px">{titre}</div>
      <div style="opacity:.75;margin-top:2px">{sous_titre}</div>
    </div>"""))
