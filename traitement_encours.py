import pandas as pd
import warnings as warn
import tkinter as tk
import time
import math
import datetime as dt

from datetime import datetime
from tkinter.filedialog import askopenfilename
from tqdm import tqdm


class MultiEfs:
    def __init__(self, number, efs):
        self.number = number
        self.efs = efs


class DataDate:
    def __init__(self, number, date, type):
        self.number = number
        self.date = date
        self.type = type


start_time = time.time()

print("Selection du fichier")
tk.Tk().withdraw()  # Ouvre l'explorateur de fichier
path = askopenfilename()

print("Fichier sélectionné : ", path)
print("Lecture du fichier")

dataStock = []
dataMultiEfs = []
endDate = ''

with warn.catch_warnings(record=True):  # Supprime le warning
    warn.simplefilter("always")
    exportFile = pd.read_csv(path, encoding="ISO-8859-1", engine="c")

endDate = 'u_datetime_for_real_end' if exportFile['number'].loc[0].startswith('TCK') else 'closed_at'
print('Utilisation de la date réelle de clôture (spécifique à la table des incidents).' if endDate == 'u_datetime_for_real_end' else  'Utilisation de la date de clôture (Générique).')

for index, row in tqdm(exportFile.iterrows(), total=exportFile.shape[0], desc="Tickets traités"):

    #morceau de code pour le multi efs
    multiEfs = str(row['u_efs_multi']).split(', ')
    for efs in multiEfs:
        entrie = MultiEfs(row['number'], efs)
        dataMultiEfs.append(vars(entrie))

    Created = pd.to_datetime(row["sys_created_on"], dayfirst=True).date()
    dataStock.append(vars(DataDate(row['number'], Created, 'Created')))

    #si pas de date de clôture, on set la date de clôture à aujourd'hui afin de créer des "encours" jusqu'à aujourd'hui
    #mais on ne met pas de dâte de clôture
    # u_datetime_for_real_end closed_at
    if pd.isnull(row[endDate]):
        Closed = datetime.today().date()
    else:
        Closed = pd.to_datetime(row[endDate], dayfirst=True).date()
        dataStock.append(vars(DataDate(row['number'], Closed, 'Closed')))

    while Created <= Closed:
        dataStock.append(vars(DataDate(row['number'], Created, 'En cours')))
        Created += dt.timedelta(days=1)

print("Création du fichier encours.csv")
df = pd.DataFrame(dataStock)
df.to_csv("encours.csv", index=False)

print("Fichier créé. Temps total : ", math.ceil(time.time() - start_time), ' secondes.')

print("Création du fichier multi_efs.csv")
df = pd.DataFrame(dataMultiEfs)
df.to_csv("multi_efs.csv", index=False)

print("Fichier créé. Temps total : ", math.ceil(time.time() - start_time), ' secondes.')
