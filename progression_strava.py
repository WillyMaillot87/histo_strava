import pandas as pd
import plotly.express as px

# 1. Charger le fichier CSV
nom_fichier = 'activites_strava.csv'

try:
  # sep=None détecte automatiquement si le CSV utilise des virgules ou des points-virgules
  df = pd.read_csv(nom_fichier, sep=';', engine='python',encoding='latin-1')
  print('Fichier CSV chargé avec succès !')
except Exception as e:
  print(
      "Erreur lors du chargement du fichier. Vérifiez son nom et sa"
      f' présence.\nErreur : {e}'
  )
  exit()

# 2. Nettoyage de la colonne Distance (ex: "9,75 km" -> 9.75)
if 'Distance' in df.columns:
  df['Distance_val'] = (
      df['Distance']
      .astype(str)
      .str.replace(' km', '', regex=False)
      .str.replace(' ', '', regex=False)
      .str.replace(',', '.', regex=False)
  )
  df['Distance_val'] = pd.to_numeric(df['Distance_val'], errors='coerce')
else:
  print("Erreur : La colonne 'Distance' est introuvable.")
  exit()

# Conversion de la date (ex: "04/10/26")
if 'Date' in df.columns:
  df['Date_dt'] = pd.to_datetime(df['Date'], format='%d/%m/%y', errors='coerce')
  df = df.sort_values('Date_dt')
else:
  print("Erreur : La colonne 'Date' est introuvable.")
  exit()

# 3. Création du graphique interactif avec Plotly
fig = px.line(
    df,
    x='Date_dt',
    y='Distance_val',
    markers=True,
    title='Ma Progression Strava - Distance par Course (Interactif)',
    labels={'Date_dt': 'Date', 'Distance_val': 'Distance (km)'},
    hover_data=['Activité', 'Durée', 'Dénivelé +'],
)

# Personnalisation du style (couleur orange Strava)
fig.update_traces(
    line=dict(color='#fc4c02', width=3),
    marker=dict(size=8, color='#fc4c02'),
)

fig.update_layout(
    xaxis_title='Date', yaxis_title='Distance (km)', hovermode='x unified'
)

# 4. Affichage dans le navigateur
fig.show()