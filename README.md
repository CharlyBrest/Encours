# Script de calcul des encours et des multi EFS
Script à lancer sur l'extract incident provenant de Snow IT.
Ce script crée 2 fichiers :
  - encours.csv : nouvelle table qui liste les incidents pour chaque jour d'ouverture basé sur la date de création et la date réele de fermeture
  - multi_efs : nouvelle table qui décompose le string multi_efs en 1 enregistrement par efs afin de faciliter les filtres

# Build EXE
- For Windows : py -m PyInstaller -F -c traitement_encours.py
- For Linux : pyinstaller -F -c traitement_encours.py
