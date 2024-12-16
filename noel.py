import random

# liste vide pour acceuillir les gens :
liste_humans = []

# Définissions un être humain : 
class Human() : 
    def __init__(self, nom, nom_partenaire = None): 
        self.nom = nom 
        self.couple = nom_partenaire # pour ne pas s'offrir un cadeau dans le même couple
        self.donne_a_qui = [None, None]  # pour stocker plus tard à qui il doit donner les cadeaux
        liste_humans.append(self) # ajoute à la liste d'humains existants

        

# Créons les personnes et leurs partenaires : 
jerome = Human("Jérôme", "Félicia")
corentin = Human("Corentin", "Mélissa")
isa = Human("Isabelle", "Manuel")
manu = Human("Manuel", "Isabelle")
etienne = Human("Etienne", "Cécile")
cecile = Human("Cécile", "Etienne")
melissa = Human("Mélissa", "Corentin")
felicia = Human("Félicia", "Jérôme")

# listons le nom des personnes pour vérifier que tout va bien : 
print("\n\n")
print("Liste des personnes créées :")
for i in liste_humans : 
    print(i.nom)
print("\n\n")
    

# Faisons le premier tirage au sort !

def tirage(round = 0): 
    for human in liste_humans : 

        selected = False # le futur choix final

        while not selected : # tant qu'une personne ne correspond pas aux prochains critères, on continue de tirer au sort !

            pick = random.choice(liste_humans) # on prend un humain au hasard
            
            # on pose les règles
            if pick.nom != human.nom : # N'a pas son propre nom
                if pick.nom != human.couple : # N'a pas le nom du partenaire
                    if all(pick != perso.donne_a_qui[round] for perso in liste_humans): # Ne doit pas être déjà choisi par quelqu'un d'autre
                        if pick not in human.donne_a_qui : # ne doit pas être déjà dans sa propre liste
                            selected = pick 

        human.donne_a_qui[round] = selected


tirage(0)
tirage(1)

# Affichons les résultats
for human in liste_humans : 
    print(f"{human.nom} ----> {' et '.join(x.nom for x in human.donne_a_qui)} !")





manu.donne_a_qui = [melissa, etienne]
isa.donne_a_qui = [felicia, cecile]
jerome.donne_a_qui = [cecile, corentin]
corentin.donne_a_qui = [etienne, felicia]
etienne.donne_a_qui = [corentin, jerome]
cecile.donne_a_qui = [isa, melissa]
melissa.donne_a_qui = [jerome, manu]
felicia.donne_a_qui = [manu, isa]


import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Préparer les données
personnes = [human.nom for human in liste_humans]

# Créer des mappings
name_to_idx = {name: idx for idx, name in enumerate(personnes)}

# Préparer les données pour le diagramme Sankey
source = []
target = []
value = []
labels = personnes

# Utiliser une palette de couleurs esthétiques
cmap = plt.cm.get_cmap('Set3', len(personnes))
node_colors = [mcolors.rgb2hex(cmap(i)) for i in range(len(personnes))]

# Créer les listes source, target et value
for human in liste_humans:
    idx_from = name_to_idx[human.nom]
    for recipient in human.donne_a_qui:
        idx_to = name_to_idx[recipient.nom]
        source.append(idx_from)
        target.append(idx_to)
        value.append(1)  # Supposons que chaque cadeau a la même valeur

# Créer le diagramme Sankey
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",  # Pour une disposition claire
    node=dict(
        pad=20,
        thickness=30,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors,
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=[node_colors[s] for s in source],  # Les liens ont la couleur du nœud source
    )
)])

# Mettre à jour la mise en page pour une meilleure esthétique et un dézoom
fig.update_layout(
    title_text='🎄 Tirage au sort des cadeaux de Noël 🎁',
    font_size=16,
    font_family='Arial',
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_font_color='darkred',
    title_font_size=24,
    width=1000,  # Augmenter la largeur pour plus de visibilité
    height=700,  # Augmenter la hauteur
    margin=dict(l=50, r=50, t=100, b=50)  # Ajouter des marges
)

# Afficher le diagramme
fig.show()