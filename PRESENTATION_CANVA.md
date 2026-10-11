# Spirit Digger v1.0 · Présentation (22 diapositives)

## Consignes pour l'IA de Canva

Crée une présentation de 22 diapositives au format 16:9, en français, à partir du contenu ci-dessous.

**Style attendu : sobre, épuré, haut de gamme.**
- Fond blanc légèrement lavé de violet (#FBFAFE), avec de fines lignes ondulées violettes très discrètes en arrière-plan.
- Titres en dégradé violet, du violet clair (#8A5CF6) au violet profond (#4B2BA8). Police géométrique moderne (Sora, Poppins ou Montserrat).
- Texte courant en gris-violet foncé (#4D4675), police lisible (DM Sans ou Inter).
- Cartes à coins arrondis sur fond violet très pâle (#F3F0FB) pour les chiffres clés.
- Une seule couleur d'alerte, orange brûlé (#B9530F), réservée aux chiffres négatifs ou critiques.
- Les graphiques de résultats sont sur fond blanc : les poser tels quels, avec au plus une fine bordure violet pâle (#E4DEF6) et des coins arrondis.
- La dernière diapositive est sur fond sombre (#1A1240), texte clair.
- Peu de texte par diapositive : une idée par diapositive, de grands chiffres plutôt que des listes.
- Les diapositives « Scénario » sont des diapositives de transition : texte centré, gros caractères en dégradé violet, rien d'autre.
- Numéro de page discret en bas à gauche : « SPIRIT DIGGER · 02 ».

Pour chaque diapositive ci-dessous :
- **À l'écran** = le texte à afficher ;
- **Visuel** = l'image ou la mise en page à prévoir ;
- **Notes orateur** = à placer dans les notes, pas sur la diapositive.

---

## Diapositive 1 · Couverture

**À l'écran**
- Petite ligne en capitales, au-dessus : RENSEIGNEMENT D'ORIGINE SOURCES OUVERTES · NLP
- Grand titre : **Spirit Digger v1.0 :**
- Sous-titre : Extraction de renseignement, détection de signaux faibles et guerre de l'information
- En italique, en bas : « Il s'infiltre dans le bruit. Il creuse jusqu'au signal. »

**Visuel** : texte centré, lignes ondulées en fond.

**Notes orateur** : Spirit Digger est le pendant « texte » de mon projet God's Eye. God's Eye regardait le monde par satellite ; Spirit Digger le lit, à travers des centaines de milliers de messages en russe, en ukrainien et en anglais. À la fin de cette présentation, les deux projets vont se parler.

---

## Diapositive 2 · La mission

**À l'écran**
- Titre : **La Mission :**
- Phrase forte : Lire en continu ce qu'aucun analyste n'a le temps de lire, et en tirer un renseignement coté, sourcé et actionnable.
- Trois cartes de chiffres :
  - **382 000** · messages Telegram, guerre en Ukraine (2022-2023)
  - **2 236** · articles de presse, crise du Golfe (2026)
  - **5 camps** · 12 chaînes, 3 langues, des récits qui se contredisent

**Visuel** : titre et phrase à gauche, les trois cartes empilées à droite.

**Notes orateur** : Environ 800 messages par jour, venant de médias d'État russes, de la presse ukrainienne, de médias russes en exil et de médias internationaux. Aucun humain ne peut tout lire. La question d'un état-major est simple : est-ce qu'il vient de se passer quelque chose d'important, et est-ce fiable ?

---

## Diapositive 3 · Avant de creuser, évaluer ses sources

**À l'écran**
- Petite ligne : RECONNAISSANCE DU TERRAIN
- Titre : **Avant de creuser, évaluer ses sources**
- Trois cartes :
  - **12** · sources cotées · selon le code de l'Amirauté (OTAN) : fiabilité de A à F
  - **2** *(en orange)* · jeux truqués démasqués · « prédiction » juste à 24,7 % pour 25 % de hasard ; adresse IP impossible 123.456.78.9
  - **31 % → 0,2 %** · fuites neutralisées · crédits « Getty Images » et liens Twitter qui trahissaient les faux articles
- Phrase de conclusion : Un modèle entraîné sur une source truquée produit un renseignement truqué, même à 99 % de précision.

**Visuel** : trois cartes alignées.

**Notes orateur** : Un analyste du renseignement commence toujours par évaluer ses sources. Deux jeux de données cyber étaient générés au hasard : un modèle entraîné dessus aurait produit du faux renseignement. Dans le jeu vrai/faux, les faux articles portaient des crédits photo que les vrais n'avaient pas : un modèle aurait « triché ». On a aussi découvert que le jeu « propagande russe » était entièrement extrait du jeu « faux ».

---

## Diapositive 4 · Scénario 1 (transition)

**À l'écran**
- **Scénario 1 : Scan et inventaire.**
- 2 200 articles sur la crise Iran – États-Unis de 2026. L'état-major veut savoir, en un coup d'œil : qui agit, avec quels moyens, où, et dans quelles opérations.

**Visuel** : diapositive de transition, texte centré en dégradé violet.

**Notes orateur** : C'est l'équivalent du scénario 1 de God's Eye. Là où YOLO repérait des avions et des navires sur une image satellite, ici un modèle de reconnaissance d'entités nommées repère des personnes, des forces armées et des armements dans du texte.

---

## Diapositive 5 · Mécanique du scan

**À l'écran**
- Titre : **Mécanique du Scan**
- Sous-titre : Reconnaissance d'entités nommées, le « YOLO du texte »
- À gauche, quatre étapes empilées (blocs violet foncé, texte blanc) : Modèle généraliste → Lexique militaire → Consolidation → Inventaire
- À droite, trois cartes « pièges évités » :
  - **Fordow, site nucléaire enterré** · modèle seul : « produit » · avec le lexique : **site stratégique**
  - **« Trump » classé organisation 1 647 fois** · vote majoritaire sur tout le corpus : **personne**
  - **Ghalibaf, Qalibaf, Baqer, Bagher…** · clé phonétique : **50 personnes** réunifiées sous un seul nom

**Visuel** : comme la diapositive « Mécanique du Scan » de God's Eye (étapes à gauche, exemples à droite).

**Notes orateur** : Le modèle spaCy, pré-entraîné sur de l'actualité générale, ne connaît pas le vocabulaire militaire. On le complète par un lexique métier, comme le font les cellules de renseignement. Puis on consolide : alias, vote majoritaire sur la catégorie, translittération des noms persans. Piège évité : « Khamenei » seul peut désigner Ali ou son fils Mojtaba ; on ne devine pas quand c'est ambigu. Le tout tourne en 2 minutes sur un ordinateur portable.

---

## Diapositive 6 · Résultats : rapport d'inventaire

**À l'écran**
- Titre : **Résultats – Rapport d'inventaire**
- Pied de page : 2 196 articles scannés · 82 000 mentions · 11 000 entités

**Visuel** : insérer l'image `outputs/02_rapport_inventaire.png` en grand, sur fond blanc.

**Notes orateur** : C'est le même livrable que le rapport d'inventaire de God's Eye, mais pour du texte. On voit émerger les opérations nommées (Epic Fury, Midnight Hammer), les armements (GBU-57, missiles balistiques, Shahed) et les navires (USS Abraham Lincoln), que le modèle seul ignorait. Recoupement avec la vérité terrain : la presse ne nomme que 2 des 13 navires attaqués à Ormuz. C'est un angle mort à signaler.

---

## Diapositive 7 · Scénario 2 (transition)

**À l'écran**
- **Scénario 2 : Alerte précoce.**
- 16 mois de guerre, 12 chaînes Telegram de camps opposés.
- Le défi : trouver l'événement sans savoir ce qu'on cherche. Aucun mot-clé n'est fourni.

**Visuel** : diapositive de transition.

**Notes orateur** : La veille de la destruction du barrage de Kakhovka, personne ne savait qu'il fallait surveiller le mot « Kakhovka ». Le système doit trouver seul les mots qui sortent de l'ordinaire.

---

## Diapositive 8 · Mécanique de l'alerte

**À l'écran**
- Titre : **Mécanique de l'Alerte**
- Sous-titre : Rupture de vocabulaire et convergence des camps
- Trois cartes numérotées :
  - **01 · Ligne de base** · combien de messages devraient contenir ce mot, d'après les 28 jours précédents
  - **02 · Rupture** · l'écart à la normale, corrigé du hasard : 3 = inhabituel, 50 = séisme
  - **03 · Convergence** · combien de camps, sur 5, emploient ce mot le même jour
- Bandeau violet foncé, texte blanc : **Score d'alerte = rupture × camps / 5**
  - en dessous : Comme le Risk Score de God's Eye : une rupture dans un seul camp pèse peu, car ce peut être de la propagande. Dans les cinq camps à la fois, c'est un fait.

**Visuel** : trois cartes, puis le bandeau de la formule.

**Notes orateur** : Pas de réseau de neurones ni de GPU : de la statistique robuste et explicable. Si un officier demande « pourquoi cette alerte ? », la réponse tient en une ligne : ce mot est cinquante fois plus fréquent que d'habitude, et les cinq camps l'emploient. Les mots russes sont réduits à leurs six premières lettres pour gérer les déclinaisons (Пригожина, Пригожину → пригож).

---

## Diapositive 9 · Résultats : 16 mois de guerre

**À l'écran**
- Titre : **Résultats – 16 mois de guerre**
- Trois chiffres sous l'image :
  - **17 / 21** · événements majeurs en alerte
  - **≤ 1 jour** · de décalage avec l'événement
  - **0** · mot-clé fourni au système
- Pied de page : 382 000 messages analysés en moins d'une minute, sur processeur

**Visuel** : insérer l'image `outputs/03_chronologie_alertes.png` en largeur, sur fond blanc.

**Notes orateur** : Validation sur 21 événements documentés publiquement : gare de Kramatorsk, croiseur Moskva, Olenivka, mobilisation partielle, pont de Crimée, retrait de Kherson, missile en Pologne, drones sur le Kremlin, Kakhovka, Wagner… Les quatre restants s'expliquent : Bakhmout est un événement graduel, Nord Stream a été éclipsé par la fusillade d'Ijevsk. Le système fait aussi ressortir le séisme en Turquie ou la mort d'Elizabeth II : il détecte l'inattendu, quel qu'il soit.

---

## Diapositive 10 · Résultats : barrage de Kakhovka

**À l'écran**
- Titre : **Résultats – Barrage de Kakhovka**
- Sous-titre : 6 juin 2023, à l'aube
- Trois cartes :
  - **0 → 446** · messages par jour contenant « каховс »
  - **5 / 5** · camps qui en parlent, TASS et UNIAN compris
  - **355** *(en orange)* · score d'alerte : ALERTE MAXIMALE
- Encadré avec un trait violet à gauche :
  - **Le système détecte, il ne prédit pas.**
  - Rien n'annonçait la mutinerie Wagner : Prigojine était déjà partout dans l'actualité. Elle est détectée le jour même, par les cinq camps. Avec un horodatage à la minute, le délai se compterait en minutes.

**Visuel** : trois cartes de chiffres, puis l'encadré.

**Notes orateur** : Personne n'a dit au système de chercher Kakhovka. Il a vu un mot passer de quasiment zéro à 446 messages en une journée, chez des médias qui se contredisent sur tout le reste. Le message représentatif de l'alerte relaie déjà la publication d'images satellite Planet Labs du barrage détruit : le texte annonce ce que l'image va confirmer.

---

## Diapositive 11 · Scénario 3 (transition)

**À l'écran**
- **Scénario 3 : Graphe de relations.**
- On sait qui est présent. L'état-major demande maintenant qui est lié à qui, et s'il existe un lien caché entre deux acteurs qu'on ne voit jamais ensemble.

**Visuel** : diapositive de transition.

**Notes orateur** : Principe : deux entités citées dans la même phrase sont reliées. Plus elles le sont souvent, plus le lien est fort. La phrase est la bonne unité : deux noms dans le même article peuvent n'avoir aucun rapport, deux noms dans la même phrase en ont presque toujours un.

---

## Diapositive 12 · Résultats : le lien caché

**À l'écran**
- Titre : **Résultats – Le lien caché**
- À droite, sous-titre : **Par qui passe le lien ?**
- La chaîne est dans l'image (voir Visuel) : Mojtaba Khamenei → Conseil suprême de sécurité nationale → IRGC → IDF → CENTCOM
- Texte : Jamais cités ensemble. Chaque maillon est sourcé ; le dernier est un artefact (« la BBC a contacté l'IDF et le CENTCOM »). La machine propose, l'analyste qualifie.
- Pied de page : 386 acteurs · 8 sous-théâtres détectés sans supervision

**Visuel** : l'image `outputs/04_lien_cache.png` en grand, à gauche ou au centre. Elle montre les cinq maillons de haut en bas et, à côté de chaque lien, la phrase source qui le justifie. Le texte de la diapo se place à droite. Si tu veux montrer le réseau entier, ajoute une diapo avec l'arbre `outputs/04_graphe_arbre.png`.

**Notes orateur** : Les sous-théâtres émergent seuls : pouvoir iranien, front naval d'Ormuz, front Israël-Liban, médiation pakistanaise et qatarie, dossier nucléaire. Deux pièges évités : sur le graphe brut, tout passe par « Iran » ou « Donald Trump » ; on suit donc les liens les plus spécifiques, pas les plus fréquents. Et la translittération : Ghalibaf et Qalibaf créaient un faux lien caché, corrigé. La carte interactive (`outputs/04_graphe_golfe.html`) s'ouvre en direct dans le navigateur pendant la démo.

---

## Diapositive 13 · Scénario 4 (transition)

**À l'écran**
- **Scénario 4 : Guerre de l'information.**
- Peut-on détecter automatiquement la propagande ? Et comment chaque camp raconte-t-il le même événement ?

**Visuel** : diapositive de transition.

**Notes orateur** : Deux volets. A : un détecteur fiable / désinformation / propagande, entraîné sur 66 000 textes, le seul modèle que l'on entraîne nous-mêmes. B : la destruction du barrage de Kakhovka racontée par les médias d'État russes et par la presse ukrainienne.

---

## Diapositive 14 · Le cas Beyrouth du texte

**À l'écran**
- Titre : **Le cas Beyrouth du texte**
- Sous-titre : Un détecteur de propagande excellent en laboratoire, fragile sur le terrain
- À gauche, deux grands chiffres :
  - **91 %** · d'exactitude sur le jeu de test
  - **22 %** *(en orange)* · de la presse 2026 signalée à tort comme désinformation
- À droite, deux cartes « crash-test » :
  - MENSONGE RÉDIGÉ EN STYLE D'AGENCE · « Le Pentagone a déclaré mardi que les forces iraniennes avaient saisi la tour Eiffel… » · **Verdict : fiable à 100 %**
  - FAIT RÉEL RÉDIGÉ EN STYLE RACOLEUR · « WATCH: Iran just closed the Strait of Hormuz… » · **Verdict : désinformation à 98 %**
- Pied de page : Il reconnaît une forme, pas la vérité : on juge par le recoupement

**Visuel** : chiffres à gauche, cartes à droite. Faire écho à la diapositive « Port de Beyrouth » de God's Eye.

**Notes orateur** : Le modèle « tricheur » apprenait les crédits photo. Le modèle propre apprend le style et l'époque : « said on Tuesday » d'un côté, « 2016 » et « Hillary » de l'autre, parce que les faux articles du jeu datent de la présidentielle américaine. Un acteur de propagande sérieux contourne ce détecteur en soignant sa forme. C'est exactement le phénomène observé sur Beyrouth avec God's Eye : un bon score en laboratoire ne garantit rien sur le terrain. Le détecteur sert à trier, jamais à juger.

---

## Diapositive 15 · Résultats : un événement, deux récits

**À l'écran**
- Titre : **Résultats – Un événement, deux récits**
- Deux colonnes sous l'image :
  - **Chaînes ukrainiennes** (trait jaune) · « dynamitage », « par les Russes » : un acte délibéré, un coupable nommé
  - **Médias d'État russes** (trait rouge) · « a annoncé », « frappe », « ВСУ » : un récit administratif, l'Ukraine accusée
- Pied de page : Méthode des « mots de combat » (log-odds ratio), sans traducteur ni GPU

**Visuel** : insérer l'image `outputs/05_kakhovka_recits.png` en largeur, sur fond blanc.

**Notes orateur** : Chaque camp accuse l'autre. Les chaînes ukrainiennes nomment les forces russes dans un message sur trois et décrivent un acte délibéré dans 60 % des cas. Les médias d'État russes ne nomment presque jamais les forces russes (1 %), mais désignent l'armée ukrainienne (14 %) et parlent de frappes (25 %). Le silence se mesure aussi : les médias russes consacrent 22 % de leurs messages à la catastrophe, contre 33 % côté ukrainien.

---

## Diapositive 16 · Scénario final (transition)

**À l'écran**
- **Scénario final : Corrélation et bulletin.**
- Coter l'information comme l'OTAN, rédiger le bulletin… et demander à God's Eye d'aller voir.

**Visuel** : diapositive de transition.

**Notes orateur** : C'est le pendant du scénario 4 de God's Eye, qui croisait une intrusion et des destructions pour conclure à une attaque. Ici, on croise des sources textuelles de camps opposés, puis on passe la main à l'imagerie.

---

## Diapositive 17 · Mécanique de la cotation

**À l'écran**
- Titre : **Mécanique de la Cotation**
- Sous-titre : Le code de l'Amirauté, la grille OTAN des services de renseignement
- À gauche, un tableau à deux colonnes :

| Source (lettre) | Information (chiffre) |
|---|---|
| A · complètement fiable | 1 · confirmée |
| B · habituellement fiable | 2 · probablement vraie |
| C · assez fiable | 3 · possiblement vraie |
| D · habituellement peu fiable | 4 · douteuse |
| E · peu fiable | 5 · improbable |
| F · ne peut être jugée | 6 · ne peut être jugée |

- À droite, en très grand : **B1**
  - Kakhovka : source habituellement fiable, information confirmée par les **deux belligérants** et un camp neutre.
  - Le chiffre est calculé : un camp ne « confirme » que s'il consacre au moins 2 % de ses messages au sujet.
- Pied de page : 210 alertes cotées : 128 en B1, 43 en B2… et 4 en D4, portées par les seuls médias d'État russes

**Visuel** : tableau à gauche, grand « B1 » à droite.

**Notes orateur** : La lettre est un jugement d'analyste, documenté et révisable : médias internationaux et russes en exil en B, presse ukrainienne et russe sous contrainte en C, médias d'État russes en D. Le chiffre, lui, est calculé par recoupement. Quand la Russie et l'Ukraine, qui se contredisent sur tout, rapportent toutes les deux qu'un fait a eu lieu, ce fait est quasi certain. Un renseignement D1 vaut plus qu'un A4. Les alertes cotées 3 ou 4 sont celles à revérifier avant transmission.

---

## Diapositive 18 · Résultats : la boucle avec God's Eye

**À l'écran**
- Titre : **Résultats – La boucle avec God's Eye**
- Sous-titre : Le texte détecte, l'image confirme
- À gauche, une carte violet foncé, texte blanc :
  - DEMANDE SD-20230606
  - **Barrage de Kakhovka**
  - 46,78° N · 33,37° E
  - T0 : 30/05 · T1 : 07/06
  - Scénario 2 : sinistres
  - Classes : bridge, building, harbor
  - Priorité : IMMÉDIATE · cotation B1
- Une flèche vers la droite
- Phrase de conclusion : bridge 2 → 0, harbor 0 → 5 : le barrage est devenu des débris. Image et texte concordent : ALERTE MAXIMALE, destruction confirmée.
- Pied de page : God's Eye v2 : analyse spatiale des transformations, images Google Earth avant et après

**Visuel** : à droite de la flèche, l'image `god_eye/result/Rapport_Transformations_Kakhovka_avant_1.png_vs_Kakhovka_apres_1.png.png` sur fond blanc.

**Notes orateur** : La boucle complète. Le 6 juin, Spirit Digger détecte la rupture et cote l'information B1. Il émet une demande d'observation au format JSON : coordonnées, dates d'acquisition, scénario à appliquer, classes à surveiller. God's Eye compare l'image avant et l'image après : le pont du barrage disparaît, des débris apparaissent au même endroit, ce qu'il qualifie de transformation plausible. Un changement d'étiquette seul pourrait être une hésitation du modèle ; la source textuelle indépendante lève le doute.

---

## Diapositive 19 · Limites et enjeux terrain

**À l'écran**
- Titre : **Limites & Enjeux Terrain**
- Sous-titre : Connaître les limites de son outil, c'est la moitié du métier
- Six cartes (grille 3 × 2) :
  - **Détecter n'est pas prédire** · horodatage au jour : l'alerte arrive le jour même, pas avant
  - **Les lents échappent** · un événement graduel, comme la chute de Bakhmout, ne crée pas de rupture
  - **Un lien sans nature** · le graphe dit qui est lié, pas comment : alliés, ennemis ou négociateurs
  - **Le style trompe** · un détecteur de propagande vieillit et se laisse duper par une forme soignée
  - **Les noms voyagent** · translittération persane et arabe : Ghalibaf, Qalibaf, Baqer…
  - **Un jugement humain** · la fiabilité des sources reste une cotation d'analyste, révisable

**Visuel** : grille de six cartes.

**Notes orateur** : Chacune de ces limites est mesurée dans les notebooks, pas supposée. Pistes d'évolution : traduction et rédaction des bulletins par un LLM, horodatage à la minute, extraction de relations typées, nouvelles sources comme l'AIS pour couvrir l'angle mort maritime, et retour automatique de la réponse satellite dans la cotation.

---

## Diapositive 20 · Architecture et données

**À l'écran**
- Titre : **Architecture & Données**
- Sous-titre : Une chaîne de renseignement, pas un modèle unique
- À gauche, un tableau :

| Étape | Méthode | Modèle |
|---|---|---|
| Reconnaissance | cotation des sources, fuites | aucun |
| Ingestion | nettoyage, langue, dédoublonnage | aucun |
| Inventaire | spaCy + lexique militaire | pré-entraîné |
| Alerte | rupture statistique, 28 jours | aucun |
| Graphe | NetworkX, Louvain, PMI | aucun |
| Propagande | TF-IDF + régression logistique | **entraîné** |
| Bulletin | Amirauté, tasking JSON | aucun |

- À droite, trois blocs :
  - **Données** · Telegram Ukraine 2022-23 · presse Golfe 2026 · vérité terrain Ormuz · ISOT et EUvsDisinfo
  - **Exécution** · 100 % processeur, hors ligne, sans GPU : 7 notebooks Python
  - **Principe** · explicable, traçable, frugal : chaque conclusion remonte à sa phrase source

**Visuel** : tableau à gauche, trois blocs à droite. Écho à la diapositive « Architecture & Données : YOLOv8 » de God's Eye.

**Notes orateur** : Un seul modèle entraîné sur sept étapes, et c'est un choix assumé. En défense, un système doit être explicable devant un officier, traçable jusqu'à la source et capable de tourner sur le terrain sans infrastructure. Le cœur du système, c'est le recoupement entre sources indépendantes, pas la puissance d'un modèle.

---

## Diapositive 21 · Performances

**À l'écran**
- Titre : **Performances**
- Sous-titre : Bilan de l'opération, relu dans les fichiers produits
- Huit tuiles (grille 4 × 2) :
  - **12** · sources évaluées, 2 truquées démasquées
  - **384 448** · documents ingérés, en 3 langues
  - **82 192** · entités extraites, 10 986 distinctes
  - **17 / 21** · événements majeurs détectés sans mot-clé
  - **386** · acteurs reliés, 537 liens cachés sourcés
  - **91 / 22 %** *(en orange)* · détecteur : exactitude en test, faux positifs en 2026
  - **210** · alertes cotées OTAN, dont 128 en B1
  - **1** · destruction confirmée par God's Eye

**Visuel** : grille de tuiles avec de grands chiffres violets.

**Notes orateur** : Tous ces chiffres sont relus dans les fichiers produits par les notebooks, aucun n'est recopié à la main. Le chiffre qui compte le plus n'est pas le 91 % du détecteur : c'est le 17 sur 21, obtenu sans qu'on dise au système quoi chercher, et la destruction de Kakhovka confirmée par deux capteurs indépendants.

---

## Diapositive 22 · Conclusion

**À l'écran**
- Grand texte clair : **Spirit Digger ne remplace pas l'analyste : il lui rend du temps.**
- En dessous, en dégradé violet clair : **Le texte détecte, l'image confirme.**
- Petite ligne en capitales : SPIRIT DIGGER v1.0 · GOD'S EYE v2.0

**Visuel** : fond sombre (#1A1240), lignes ondulées violettes discrètes, texte centré.

**Notes orateur** : Il lit 380 000 messages en trois langues, signale l'inattendu, cote ce qu'il trouve comme le fait l'OTAN, montre ses preuves, et demande à God's Eye d'aller voir. Merci.

---

## Images à insérer à la main dans Canva

L'IA de Canva n'a pas accès à tes fichiers : importe ces images toi-même, puis place-les sur les diapositives indiquées.

| Diapositive | Fichier (dans le dossier du projet) |
|---|---|
| 6 | `outputs/02_rapport_inventaire.png` |
| 9 | `outputs/03_chronologie_alertes.png` |
| 12 | `outputs/04_lien_cache.png` (la chaîne Mojtaba Khamenei → CENTCOM) |
| diapo optionnelle sur le réseau | `outputs/04_graphe_arbre.png` (l'arbre) ou `outputs/04_graphe_coeur.png` (la toile) |
| 15 | `outputs/05_kakhovka_recits.png` |
| 18 | `god_eye/result/Rapport_Transformations_Kakhovka_avant_1.png_vs_Kakhovka_apres_1.png.png` |

Pour la démo en direct : la carte interactive `outputs/04_graphe_golfe.html`, l'arbre interactif `outputs/04_graphe_arbre.html` et le bulletin `outputs/bulletin_2023-23.html` s'ouvrent dans un navigateur.
