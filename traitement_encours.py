import pandas as pd
import warnings as warn
import tkinter as tk
import time
import math
import datetime as dt

from dateutil.relativedelta import relativedelta
from tkinter.filedialog import askopenfilename
from tqdm import tqdm


class DataDate:
    def __init__(self, number, date, type):
        self.number = number
        self.date = date
        self.type = type


TIME_PARAMS = "DAYS"
TICKET_PARAMS = "INCIDENT"

libelle_Created = ''
libelle_closed = ''

if TICKET_PARAMS == "INCIDENT":
    libelle_Created = 'sys_created_on'
    libelle_closed = 'u_datetime_for_real_end'
elif TICKET_PARAMS == "DS":
    libelle_Created = 'sys_created_on'
    libelle_closed = 'closed_at'

start_time = time.time()

print("Selection du fichier")
tk.Tk().withdraw()  # Ouvre l'explorateur de fichier
path = askopenfilename()

print("Fichier sélectionné : ", path)
print("Lecture du fichier")

data = []

with warn.catch_warnings(record=True):  # Supprime le warning
    warn.simplefilter("always")
    exportFile = pd.read_csv(path, encoding="ISO-8859-1", engine="c")

for index, row in tqdm(exportFile.iterrows(), total=exportFile.shape[0], desc="Tickets traités"):
    Created = pd.to_datetime(row[libelle_Created], dayfirst=True)
    data.append(vars(DataDate(row['number'], Created, 'Created')))

    #si pas de date de clôture, on set la date de clôture à aujourd'hui afin de créer des "encours" jusqu'à aujourd'hui
    #mais on ne met pas de dâte de clôture
    if pd.isnull(row[libelle_closed]):
        Closed = dt.datetime.now()
    else:
        Closed = pd.to_datetime(row[libelle_closed], dayfirst=True)
        data.append(vars(DataDate(row['number'], Closed, 'Closed')))

    #print("Created : " + str(Created) + " Closed : " + str(Closed) + " Now : " + str(dt.datetime.now()))
    if TIME_PARAMS == 'MONTHS':
        Created.replace(day=1)
        Closed.replace(day=1)

    while Created <= Closed:
        data.append(vars(DataDate(row['number'], Created, 'En cours')))

        # print("Number : " + str(row['number']) + " Created : " + str(Created))
        if TIME_PARAMS == "DAYS":
            Created += dt.timedelta(days=1)
        elif TIME_PARAMS == "MONTHS":
            Created += relativedelta(months=1)

print("Création du fichier CSV")
df = pd.DataFrame(data)
df.to_csv("encours.csv", index=False)

end_time = time.time()
print("Fichier créé. Temps total : ", math.ceil(end_time - start_time), ' secondes.')
