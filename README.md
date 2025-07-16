# Gestionnaire de Cadeaux, pour famille ou entre amis
Une petite appli pour organiser un tirage au sort de cadeaux avec gestion des couples et visualisation des échanges.

![screenshot1](/screenshot1.png)

## Fonctionnalités
- **Ajout/suppression** de participants via une interface graphique.  
- **Définition d’un partenaire** (couple) pour éviter de s’offrir un cadeau dans le même foyer.  
- **Tirage aléatoire** garantissant :  
  - chaque personne offre deux cadeaux,  
  - personne ne se tire elle‑même,  
  - personne ne tire son partenaire.  
- **Affichage des résultats** dans une fenêtre texte.  
- **Diagramme Sankey** (Plotly) pour visualiser les flux de cadeaux.

![screenshot2](/screenshot2.png)

## Lancement
### Lancement depuis l'exécutable
Solution la plus simple.
Téléchargez et lancez l'application compliée dans la rubrique "releases" pour MacOS et Windows. 

### Lancer le script python
#### 1. Prérequis
python >= 3.9
```
pip install plotly matplotlib
```

### 2. Lancer l’application
```
python gestionnaire_cadeaux.py
```

## Utilisation

	1.	Saisissez les noms des participants puis cliquez sur Ajouter.
	2.	Spécifiez éventuellement les couples via la liste déroulante.
	3.	Cliquez sur Lancer le tirage pour générer les résultats et le diagramme.


