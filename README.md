Montreal Fire Department (SIM) Intervention Visualization
English
A bilingual data visualization tool that generates animated videos showing trends and patterns in Montreal Fire Department (Service d'incendie de Montréal) interventions.
Overview
This project processes historical intervention data from the Montreal Fire Department (SIM) and creates animated visualizations showing:

Monthly intervention trends over time
Incident type breakdowns by month
12-month rolling totals by incident category

All visualizations are presented in both English and French, making them accessible to Montreal's bilingual population.
Requirements
The following Python packages are required:
pandas>=1.3.0
geopandas>=0.10.0
matplotlib>=3.5.0
numpy>=1.20.0
opencv-python>=4.5.0
tqdm>=4.62.0
shapely>=1.8.0
You can install all requirements using:
bashpip install -r requirements.txt
Data Files
The script requires the following CSV data files:

donneesouvertes-interventions-sim.csv - Recent SIM intervention data
donneesouvertes-interventions-sim_2015_2022.csv - SIM data from 2015-2022
donneesouvertes-interventions-sim_2005-2014.csv - SIM data from 2005-2014

Place these files in the same directory as the script.
Data Quality Notes
According to the analysis in date_time_quality_report.txt, there are some data quality issues to be aware of:

84.3% of records have timestamps of exactly 00:00:00, suggesting these may be default values rather than actual recorded times
When analyzing time-based patterns, it's recommended to exclude records with 00:00:00 timestamps

Usage
To generate the animation:
bashpython bilingual.py
The script will:

Load and process all CSV data files
Create a frame for each month in the dataset
Compile frames into two MP4 videos:

montreal_sim_interventions_bilingual.mp4: Standard animation
montreal_sim_interventions_bilingual_with_pause.mp4: Animation with a 3-second pause on the final frame



Temporary frames are stored in a frames directory, and final videos are saved to an output directory.
Output Visualizations
Each frame in the animation includes:

Monthly Trend Line: Shows the number of interventions per month over time
Incident Type Breakdown: Pie chart showing the proportion of different incident types for the current month
12-Month Rolling Total: Horizontal bar chart showing incident counts by type over the previous 12 months

Summary Statistics
Based on the data from 2005-2022:

Total incidents: 1,061,849
Most common incident types:

First responders (Premiers répondants): 65.2%
Other fires (Autres incendies): 34.6%


Average number of units deployed per incident: 1.81
Busiest fire station (Caserne): Caserne 65 with 36,988 incidents

License
This project is as free as a bird soaring through open skies, released under the MIT License:
MIT License

Copyright (c) 2025 Mycole Brown

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Like a friendly neighbor lending you their power tools, you're welcome to use this code however you want - just remember to keep the copyright notice as a little thank you note. This license is as simple and straightforward as a Montreal winter is long and cold. Enjoy!
Creator
Created by Mycole Brown
Note: This visualization tool only includes months with available data. Some timestamps in the source data may be default values rather than actual recorded times.

Français
Visualisation des interventions du Service d'incendie de Montréal (SIM)
Un outil de visualisation de données bilingue qui génère des vidéos animées montrant les tendances et les modèles des interventions du Service d'incendie de Montréal (SIM).
Aperçu
Ce projet traite les données historiques d'intervention du Service d'incendie de Montréal (SIM) et crée des visualisations animées montrant:

Les tendances mensuelles des interventions au fil du temps
Les répartitions des types d'incidents par mois
Les totaux mobiles sur 12 mois par catégorie d'incident

Toutes les visualisations sont présentées en anglais et en français, les rendant accessibles à la population bilingue de Montréal.
Exigences
Les packages Python suivants sont nécessaires:
pandas>=1.3.0
geopandas>=0.10.0
matplotlib>=3.5.0
numpy>=1.20.0
opencv-python>=4.5.0
tqdm>=4.62.0
shapely>=1.8.0
Vous pouvez installer toutes les dépendances en utilisant:
bashpip install -r requirements.txt
Fichiers de données
Le script nécessite les fichiers CSV suivants:

donneesouvertes-interventions-sim.csv - Données récentes d'intervention du SIM
donneesouvertes-interventions-sim_2015_2022.csv - Données du SIM de 2015 à 2022
donneesouvertes-interventions-sim_2005-2014.csv - Données du SIM de 2005 à 2014

Placez ces fichiers dans le même répertoire que le script.
Notes sur la qualité des données
Selon l'analyse du fichier date_time_quality_report.txt, il y a quelques problèmes de qualité des données à prendre en compte:

84,3% des enregistrements ont des horodatages exactement à 00:00:00, ce qui suggère qu'il pourrait s'agir de valeurs par défaut plutôt que d'heures réellement enregistrées
Lors de l'analyse des modèles temporels, il est recommandé d'exclure les enregistrements avec des horodatages à 00:00:00

Utilisation
Pour générer l'animation:
bashpython bilingual.py
Le script va:

Charger et traiter tous les fichiers de données CSV
Créer une image pour chaque mois dans l'ensemble de données
Compiler les images en deux vidéos MP4:

montreal_sim_interventions_bilingual.mp4: Animation standard
montreal_sim_interventions_bilingual_with_pause.mp4: Animation avec une pause de 3 secondes sur la dernière image



Les images temporaires sont stockées dans un répertoire frames, et les vidéos finales sont enregistrées dans un répertoire output.
Visualisations de sortie
Chaque image de l'animation comprend:

Ligne de tendance mensuelle: Montre le nombre d'interventions par mois au fil du temps
Répartition des types d'incidents: Diagramme circulaire montrant la proportion des différents types d'incidents pour le mois actuel
Total mobile sur 12 mois: Graphique à barres horizontales montrant le nombre d'incidents par type au cours des 12 mois précédents

Statistiques sommaires
Basé sur les données de 2005-2022:

Total des incidents: 1 061 849
Types d'incidents les plus courants:

Premiers répondants: 65,2%
Autres incendies: 34,6%


Nombre moyen d'unités déployées par incident: 1,81
Caserne la plus occupée: Caserne 65 avec 36 988 incidents

Licence
Ce projet est aussi libre qu'un oiseau planant dans un ciel ouvert, publié sous la licence MIT:
Licence MIT

Copyright (c) 2025 Mycole Brown

L'autorisation est accordée, gratuitement, à toute personne obtenant une copie
de ce logiciel et des fichiers de documentation associés (le "Logiciel"), de traiter
le Logiciel sans restriction, notamment les droits d'utiliser, de copier, de modifier,
de fusionner, de publier, de distribuer, de sous-licencier et/ou de vendre
des copies du Logiciel, ainsi que d'autoriser les personnes auxquelles le Logiciel est
fourni à le faire, sous réserve des conditions suivantes:

L'avis de droit d'auteur ci-dessus et cet avis d'autorisation doivent être inclus dans
toutes les copies ou parties substantielles du Logiciel.

LE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE, EXPRESSE OU
IMPLICITE, NOTAMMENT SANS GARANTIE DE QUALITÉ MARCHANDE, D'ADÉQUATION À UN USAGE
PARTICULIER ET D'ABSENCE DE CONTREFAÇON. EN AUCUN CAS, LES AUTEURS OU TITULAIRES DU
DROIT D'AUTEUR NE SERONT RESPONSABLES DE TOUT DOMMAGE, RÉCLAMATION OU AUTRE
RESPONSABILITÉ, QUE CE SOIT DANS LE CADRE D'UN CONTRAT, D'UN DÉLIT OU AUTRE, EN
PROVENANCE DE, CONSÉCUTIF À OU EN RELATION AVEC LE LOGICIEL OU SON UTILISATION, OU
AVEC D'AUTRES ÉLÉMENTS DU LOGICIEL.
Comme un voisin amical qui vous prête ses outils, vous êtes libre d'utiliser ce code comme vous le souhaitez - rappelez-vous simplement de conserver l'avis de droit d'auteur comme un petit mot de remerciement. Cette licence est aussi simple et directe qu'un hiver montréalais est long et froid. Profitez-en!
Créateur
Créé par Mycole Brown
Remarque: Cet outil de visualisation inclut uniquement les mois avec des données disponibles. Certains horodatages dans les données source peuvent être des valeurs par défaut plutôt que des heures réellement enregistrées.