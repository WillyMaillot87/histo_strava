import matplotlib.pyplot as plt
import pandas as pd

# 1. Charger le fichier ODS
# Remplacez 'activites_strava.ods' par le nom exact de votre fichier
nom_fichier = 'activites_strava.ods'

try:
  df = pd.read_ods(nom_fichier, sheet=0)
  print('Fichier chargé avec succès !')
except Exception as e:
  print(
      "Erreur lors du chargement du fichier. Vérifiez son nom et sa"
      f' présence.\nErreur : {e}'
  )
  exit()

# 2. Nettoyage et préparation des données
# Nettoyage de la colonne Distance (ex: "9,75 km" -> 9.75)
if 'Distance' in df.columns:
  df['Distance_val'] = (
      df['Distance']
      .astype(str)
      .str.replace(' km', '', regex=False)
      .str.replace('', '', regex=False)
  )
  df['Distance_val'] = df['Distance_val'].str.replace(',', '.', regex=False)
  df['Distance_val'] = pd.to_numeric(df['Distance_val'], errors='coerce')
else:
  print("Erreur : La colonne 'Distance' est introuvable.")
  exit()

# Conversion de la date (ex: "04/10/26" au format jour/mois/année)
if 'Date' in df.columns:
  df['Date_dt'] = pd.to_datetime(df['Date'], format='%d/%m/%y', errors='coerce')
  # Trier par ordre chronologique
  df = df.sort_values('Date_dt')
else:
  print("Erreur : La colonne 'Date' est introuvable.")
  exit()

# 3. Création du graphique de progression de la distance
plt.figure(figsize=(12, 6))
plt.plot(
    df['Date_dt'],
    df['Distance_val'],
    marker='o',
    linestyle='-',
    color='#fc4c02',
    linewidth=2,
    markersize=6,
    label='Distance (km)',
)  # Utilisation de la couleur orange Strava !

plt.title('Ma Progression Strava - Distance par Course', fontsize=14, pad=15)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Distance (km)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Incliner les dates pour qu'elles restent lisibles
plt.xticks(rotation=45)
plt.tight_layout()

# 4. Affichage du graphique :
plt.show()