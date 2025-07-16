import random
import tkinter as tk
from tkinter import ttk
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tkinter import messagebox


# liste vide pour acceuillir les gens :
liste_humans = []

# Définissions un être humain : 
class Human() : 
    def __init__(self, nom, nom_partenaire = None): 
        self.nom = nom 
        self.couple = nom_partenaire # pour ne pas s'offrir un cadeau dans le même couple
        self.donne_a_qui = [None, None]  # pour stocker plus tard à qui il doit donner les cadeaux
        liste_humans.append(self) # ajoute à la liste d'humains existants
    
    def reset(self):
        self.donne_a_qui = [None, None]

def tirage(round = 0): 
    
    destinataires_disponibles = liste_humans[:]
    random.shuffle(destinataires_disponibles) 

    for human in liste_humans:
        selected = False
        attempts = 0 # Compteur de tentatives

        while not selected:
            # Si on a tout essayé, c'est sûrement un blocage
            if not destinataires_disponibles or attempts > len(liste_humans):
                messagebox.showerror("Erreur de tirage", 
                                     "Impossible de trouver une solution avec les contraintes actuelles. "
                                     "Essayez avec plus de participants ou moins de contraintes.")
                return # On arrête tout pour éviter de geler

            # On prend le prochain destinataire disponible
            pick = destinataires_disponibles.pop(0)
            attempts += 1 # On incrémente le compteur

            # On vérifie les règles
            if pick.nom != human.nom and \
               pick.nom != human.couple and \
               pick not in human.donne_a_qui:
                selected = pick
            else:
                # Si le choix n'est pas bon, on le remet à la fin de la liste pour lui donner une autre chance
                destinataires_disponibles.append(pick)

        if selected:
            human.donne_a_qui[round] = selected
        else:
            # Si on sort de la boucle sans solution (grâce à la sécurité), on arrête.
            return 



def launch_tirage(): 
    for i in liste_humans : 
        i.reset()

    tirage(0)
    tirage(1)

    result = ""
    print(liste_humans)
    for human in liste_humans: 
        txt = f"{human.nom} ----> {human.donne_a_qui[0].nom} et {human.donne_a_qui[1].nom}!\n"
        print(txt.strip())
        result += txt

    top = tk.Toplevel()
    top.geometry("500x400")
    top.title("Résultats du tirage")

    label = tk.Label(top, text=result, justify=tk.LEFT)
    label.pack(fill=tk.BOTH, expand=True)

    display_results()




def display_results(): 

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

def ajouter_personne(event=None):
    nom_personne = entree_nom.get()
    if nom_personne: # S'assure que le champ n'est pas vide
        Human(nom=nom_personne)
        entree_nom.delete(0, tk.END) # Vide la boite
        maj_liste_participants()

def delete_person(person=None): 
    if person :
        for i in liste_humans: 
            if i.nom == person.nom : 
                liste_humans.remove(person)
                print(f"{person.nom} a été supprimé !")
                del person
    maj_liste_participants()


def maj_liste_participants():
    # Reset l'ancien widget
    for widget in frame_liste.winfo_children():
        widget.destroy()

    noms_participants = [h.nom for h in liste_humans]
    noms_participants.append(" ")

    # Label et menu
    tk.Label(frame_liste, text="Nom", font=("Helvetica", 11)).grid(row=0, column=1, padx=12, pady=5, sticky="w")
    tk.Label(frame_liste, text="Partenaire", font=("Helvetica", 11)).grid(row=0, column=2, padx=5, pady=5, sticky="w")


    for i, humain in enumerate(liste_humans):
        button_del = tk.Button(frame_liste, text="❌",command=lambda h=humain: delete_person(h))
        button_del.grid(row=i+1, column=0, padx=0, pady=0)        
        label_nom = tk.Label(frame_liste, text=humain.nom, padx = 10, font=("Helvetica", 15, "bold"))
        label_nom.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")

        # Combobox
        combo_partenaire = ttk.Combobox(frame_liste, values=noms_participants, state="readonly")
        combo_partenaire.grid(row=i+1, column=2, padx=5, pady=5)
        
        if humain.couple:
            combo_partenaire.set(humain.couple)

        # Lie la sélection dans le menu à la mise à jour de l'objet Human
        # Utilise une lambda fonction pour passer l'humain concerné et le combobox
        combo_partenaire.bind("<<ComboboxSelected>>",
                              lambda event, h=humain, c=combo_partenaire: definir_partenaire(h, c.get()))

def definir_partenaire(humain, nom_partenaire):
    if nom_partenaire == " " : 
        nom_partenaire = None
    humain.couple = nom_partenaire
    

window = tk.Tk()
window.title("Gestionnaire de Cadeaux !")
window.geometry("600x700") 

titre = tk.Label(window, text="🎅 Gestionnaire de Cadeaux ! 🎁", font=("Helvetica", 22, "bold"), pady=15)
titre.pack()

# Frame ajout personne
frame_ajout = tk.Frame(window)
frame_ajout.pack(pady=10)

label_ajout = tk.Label(frame_ajout, text="Ajouter une personne :", font=("Helvetica", 11))
label_ajout.pack(side=tk.LEFT, padx=5)

entree_nom = tk.Entry(frame_ajout,text="Nom...", font=("Helvetica", 11))
entree_nom.pack(side=tk.LEFT, padx=5)
entree_nom.bind("<Return>", ajouter_personne)


bouton_ajouter = tk.Button(frame_ajout, text="Ajouter", command=ajouter_personne)
bouton_ajouter.pack(side=tk.LEFT, padx=5)
ttk.Separator(window, orient='horizontal').pack(fill='x', pady=10, padx=20)

bouton_lancer = tk.Button(window, text="Lancer le tirage", command=launch_tirage)
bouton_lancer.pack(padx=5)

ttk.Separator(window, orient='horizontal').pack(fill='x', pady=10, padx=20)

# Frame pour liste et couples
frame_liste = tk.Frame(window)
frame_liste.pack(pady=5, padx = 20, fill=tk.BOTH, expand=True)

window.mainloop()


