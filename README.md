# Script de calcul des encours et des multi EFS
Script à lancer sur les extract de tickets (incidents, demandes ou autres) provenant de Snow IT.
Ce script crée 2 fichiers :
  - encours.csv : nouvelle table qui liste les incidents pour chaque jour d'ouverture basé sur la date de création et la date réele de fermeture
  - multi_efs : nouvelle table qui décompose le string multi_efs en 1 enregistrement par efs afin de faciliter les filtres

En fonction du type de ticket différentes dates sont utilisées :
  - Pour les **Incidents** c'est la date réelle de clôture qui correspond à la dernière fois ou le statut est passé à **Résolut**.
  - Pour les **Demandes** c'est la date de clôture qui correspond à la dernière fois ou le statut est passé à **Fermé**.

# Build EXE
- For Windows : py -m PyInstaller -F -c traitement_encours.py
- For Linux : pyinstaller -F -c traitement_encours.py
