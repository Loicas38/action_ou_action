import tkinter as tk
from functools import partial
from PIL import ImageTk, Image
from structure import Player, Picture

class Graphique():
    def __init__(self, actions:list[dict], garcon:Player, fille:Player) -> None:
        """ initialise l'interface graphique et gère l'affichage des premières fenêtres
        actions : liste des différents dictionnaire de ce qui pourra être joué 
        garcon : nom du garcon
        fille : nom de la fille"""

        # on cré le canvas
        self.fenetre = tk.Tk()
        self.fenetre.title("action ou action...")
        # empêche que l'on puisse redimensionner la fenêtre
        #self.fenetre.resizable(0, 0)
        # fait passer la fenêtre à l'avant plan
        #self.fenetre.wm_attributes("-topmost", 1)
        self.canvas = tk.Canvas(self.fenetre, height = 825, width = 1530, bg="white")
        self.canvas.pack()

        self.garcon = garcon
        self.fille = fille

        # stock les images des positions à afficher
        self.images_illustrations = []
        # stocke l'id sur le canvas de l'image affichée
        self.illustrations = []

        self.actions = actions

        # lance la partie 
        self.debut_partie()
        # choix de la vitesse de jeu
        self.choix_vitesse()
        # choix du mode 
        self.choix_mode()
        # choix du niveau de langue
        self.choix_niveau_langage()
        # infos des joueurs
        self.infos_joueurs()
        # lance le jeu pour de vrai 
        self.commencement()

        self.canvas.create_rectangle(500, 70, 950, 750, fill = "#FFB275")
        # crée les images et le texte

        self.creation_textes()

        self.nb_tours = 0
        self.canvas.pack()


    def creation_textes(self) -> None:
        """ crée les textes qui seront ensuite modifiés tout au long du programme """
        # creation du prénom à afficher pour faire l'action
        self.nom_garcon = self.canvas.create_text(725, 110, text = self.garcon.get_name(), font = (("MS Serif", 35)), fill="#D08CFF", justify="center")
        self.nom_fille = self.canvas.create_text(725, 110, text = self.fille.get_name(), font = (("MS Serif", 35)), fill="#8CFFF5", justify="center")
        self.nom_a_2 = self.canvas.create_text(725, 110, text = f"{self.garcon.get_name()} et {self.fille.get_name()}", font = (("MS Serif", 35)), fill="#F83610", justify="center")

        # text pour les yeux bandés
        self.yeux_bandes = self.canvas.create_text(725, 250, text = "", font=("Helvetica", 25), fill="#239E12", justify="center")
        # text de l'action
        self.action = self.canvas.create_text(725, 380, text = "", font = (("Helvetica", 25)), justify="center")
        # affiche le mot "bonus" quand il y en a un
        self.bonus_titre = self.canvas.create_text(725, 550, text = "Bonus:", font = ("Helvetica", 35), fill="#7CFFF9", justify="center")
        # texte du bonus
        self.bonus = self.canvas.create_text(725, 675, text="", font = ("Helvetica", 30), fill = "#7C9EFF", justify="center")

        # texte temps chrono
        self.temps_chrono = self.canvas.create_text(1200, 150, text="", font=("Helvetica", 30), justify="center")


    def  fin_debut_partie(self, _):
        """ enlève le texte de la page d'accueil et désactive l'attente de touche et arrête la minloop"""
        self.canvas.itemconfigure(self.text_debut_partie, state = "hidden")
        self.fenetre.unbind('<Return>')
        self.fenetre.quit()

    def debut_partie(self):
        """ texte de la page d'accueil """
        self.text_debut_partie = self.canvas.create_text(700, 400, text = "Bonjour et bienvenue à toi.\nN'appuie sur entrée que quand tu te sentiras prête...", font = ("Helvetica, 30"), fill = "red", justify = "center")
        self.fenetre.bind('<Return>', self.fin_debut_partie)
        self.canvas.pack()
        self.fenetre.mainloop()



    def set_vitesse(self, vitesse):
        self.vitesse = vitesse

        self.fenetre.quit()

        self.v1.destroy()
        self.v2.destroy()
        self.v3.destroy()
        self.canvas.itemconfigure(self.v_texte, state= "hidden")

    def get_vitesse(self):
        return self.vitesse

    def choix_vitesse(self):
        self.v_texte = self.canvas.create_text(780, 350, text = "Choix de la vitesse du jeu (1 = rapide et 3 = lent)", font=("Helvetica", 20))

        # creation des boutons de choix de la vitesse
        self.v1 = tk.Button(self.fenetre, height=2, width = 10, text = 1, font=("Helvetica", 15), command = partial(self.set_vitesse, 1))
        self.v2 = tk.Button(self.fenetre, height=2, width = 10, text = 2, font=("Helvetica", 15), command = partial(self.set_vitesse, 2))
        self.v3 = tk.Button(self.fenetre, height=2, width = 10, text = 3, font=("Helvetica", 15), command = partial(self.set_vitesse, 3))

        # tentative deco marchait pas, à modifier plus tard
        """self.image_escargot = tk.PhotoImage(file="images_deco/escargot.gif")
        self.image_escargot = self.image_escargot.subsample(15, 15)
        self.image_escargot = self.canvas.create_image(1200, 300, image = self.image_escargot)

        self.image_ferrari = tk.PhotoImage(file="")
        self.image_ferrari = self.image_ferrari.subsample(5, 5)
        self.image_ferrari = self.canvas.create_image(1200, 300, image = self.image_ferrari)

        self.canvas.pack()"""


        self.v1.pack()
        self.v2.pack()
        self.v3.pack()

        self.v1.place(x=550, y=400)
        self.v2.place(x=700, y=400)
        self.v3.place(x=850, y=400)

        self.canvas.pack()
        self.fenetre.mainloop()



    def get_chosen_actions(self) -> dict:
        """ return the dict with all the actions selected """
        return self.chosen_actions

    def set_mode(self, actions):
        """ get the actions wich have been chosen, and destroy the buttons and the text """
        self.fenetre.quit()

        for button in self.boutons_choix_mode:
            button.destroy()

        self.canvas.delete(self.text_choix_mode)
        
        self.chosen_actions = actions

    def choix_mode(self):
        """ allow to choose the mode of the game """
        self.text_choix_mode = self.canvas.create_text(750, 300, text="Choisissez le mode de jeu", font=("Helvetica", 20))
        self.canvas.pack()

        # store the buttons which allow to chose the mode to play
        self.boutons_choix_mode = []

        # we add 1 because the first button is too far otherwise 
        x = 1500 // (len(self.actions)+1) - 60

        # we suppose that ther isn't enough modes to get out of the page
        y = 400

        # to increase the abscisse
        step = x
        for action in self.actions:
            # transmitt the actions which have been chosen
            bouton = tk.Button(self.fenetre, height = 2, width = 15, text=action["mode"], font=("Helvetica", 15), command=partial(self.set_mode, action))
            bouton.place(x=x, y=y)
            self.boutons_choix_mode.append(bouton)
            x += step


        self.fenetre.mainloop()




    def fin_commencement(self, _):
        self.fenetre.quit()
        self.canvas.itemconfigure(self.text_commencement, state = "hidden")
        self.fenetre.unbind("<Return>")

    def commencement(self):
        """ juste avant le début du jeu """
        self.text_commencement = self.canvas.create_text(700, 400, text = "Puisque tu as décidé de jouer, jouons...\nIl est encore temps de renoncer en fermant cette fenêtre.\nEn revanche si tu te sens prête, presse entrée", font = ("Helvetica, 30"), fill = "red", justify = "center")
        self.fenetre.bind('<Return>', self.fin_commencement)
        self.canvas.pack()
        self.fenetre.mainloop()



    def infos_joueurs(self, habit: bool = False):
        """ demande les infos nécessaires sur les joueurs """
        self.text_nom_default = self.canvas.create_text(720, 150, text = f"Le joueur 1 par défaut est {self.garcon.get_name()} et le joueur 2 {self.fille.get_name()},\npour modifier cliquer sur le bouton", justify = "center", font=("Helvetica", 30))
        self.changer_noms = tk.Button(self.fenetre, height=3, width = 30, text = "changer de joueurs", font=("Helvetica", 15), 
                                      command = partial(self.changer_joueurs, habit))
        self.changer_noms.pack()
        self.changer_noms.place(x=580, y=225)
        
        self.fenetre.bind('<Return>', self.delete_widget_changer_joueur)

        self.fenetre.mainloop()
        self.fenetre.quit()


    def set_nom_joueurs(self, _):
        """ récupère le nom des joueurs entré"""
        self.garcon.change_name(self.entre_nom_garcon.get())
        self.fille.change_name(self.entre_nom_fille.get())

    def get_nom_joueurs(self) -> tuple[str]:
        return self.garcon.get_name(), self.fille.get_name()

    def delete_changer_joueur(self):
        """supprime tout ce qui est relatif au changement de nom des joueurs"""
        self.canvas.delete(self.texte_nom_fille)
        self.canvas.delete(self.texte_nom_garcon)

        self.entre_nom_fille.destroy()
        self.entre_nom_garcon.destroy()

        self.retour_info_joueurs.destroy()

        self.fenetre.unbind("<Return>")

        self.fenetre.quit()
        #self.infos_joueurs()

    def delete_widget_changer_joueur(self, _):
        """ delete the text and the button which allow to change the name af the players """
        self.canvas.delete(self.text_nom_default)
        self.changer_noms.destroy()
        self.fenetre.unbind('<Return>')
        self.fenetre.quit()


    def changer_joueurs(self, habits: bool):
        """ habit = si on a demandé le nombre d'habits des joueurs
        permet de changer le nom des joueurs"""

        self.changer_noms.destroy()
        self.canvas.itemconfigure(self.text_nom_default, state = 'hidden')
      
        self.texte_nom_garcon = self.canvas.create_text(300, 300, text = "nom du garçon", justify = "center", font=("Helvetica", 30))
        self.entre_nom_garcon = tk.Entry(self.fenetre, background="#D1D1D3", borderwidth=2, font=("Helvetica", 20))

        # affiche le nom actuel du garcon 
        self.entre_nom_garcon.insert(0, self.garcon.get_name())

        self.entre_nom_garcon.pack()
        self.entre_nom_garcon.place(x=150, y=400)



        self.texte_nom_fille = self.canvas.create_text(1050, 300, text = "nom de la fille", justify = "center", font=("Helvetica", 30))
        self.entre_nom_fille = tk.Entry(self.fenetre, background="#D1D1D3", borderwidth=2, font=("Helvetica", 20))

        # affiche le nom actuel de la fille 
        self.entre_nom_fille.insert(0, self.fille.get_name())

        self.entre_nom_fille.pack()
        self.entre_nom_fille.place(x=900, y=400)

        self.fenetre.bind("<Return>", self.set_nom_joueurs)



        self.retour_info_joueurs = tk.Button(self.fenetre, text = "retour fenetre précédente", font = ("Helvetica", 20), command = self.delete_changer_joueur)

        self.retour_info_joueurs.pack()
        self.retour_info_joueurs.place(x = 500, y=600)

        self.fenetre.mainloop()
        self.infos_joueurs(habits)


    def choix_niveau_langage(self):
        """permet de choisir un langage métaphore, normale ou cru"""
        # ne crée le texte que lors du premier appel
        try:
            self.canvas.itemconfigure(self.texte_niveau_langue, state = "normal")
            self.canvas.itemconfigure(self.text_actions, state = "hidden")
            for x in self.buttons_niveaux:
                x.destroy()
        except:
            self.texte_niveau_langue = self.canvas.create_text(720, 200, text = "choix du langage des actions", font = ("Helvetica", 30), justify = "center")
        
        langage = ["métaphores", "courant", "déplacé", "aléatoire"]

        self.buttons_niveau_langage = []
        for id, text in enumerate(langage):
            self.buttons_niveau_langage.append(tk.Button(self.fenetre, height=2, width = 15, text = text, font=("Helvetica", 15), command = partial(self.set_niveau_langue, id)))
            self.buttons_niveau_langage[-1].pack()
            self.buttons_niveau_langage[-1].place(x=(220 + 300*id), y=350)

        # ne crée le bouton que lors du premier appel
        try:
            self.button_afficher_actions.configure(command = None, text = "voir les actions\net en ajouter")
        except: 
            self.button_afficher_actions = tk.Button(self.fenetre, heigh = 3, width = 20, text = "voir les actions\net en ajouter", font = ("Helvetica", 15), justify="center", command = None)
            self.button_afficher_actions.pack()
            self.button_afficher_actions.place(x=600, y=600)

        self.fenetre.mainloop()

    def set_niveau_langue(self, choix):
        """ définit le niveau de langue choisit
        0 = métaphores, 1 = normal, 2 = cru, 3 = aléatoire"""
        l = ["soft", "normal", "hard", "random"]
        self.niveau_langue = l[choix]
        # on ne permet de quitter la page qu'une fois le niveau de langue choisit
        self.fenetre.bind("<Return>", self.continuer_langage)

        # plus besoin (normalement)
        #self.fenetre.quit()

    def get_niveau_langage(self):
        return self.niveau_langue

    def continuer_langage(self, _):
        """arrete les trucs là pour passer à la suite"""
        self.fenetre.unbind("<Return>")
        self.cacher_choix_niveau_langue()
        
        try:
            for x in self.buttons_niveaux:
                x.destroy()
            self.canvas.itemconfigure(self.text_actions, state = "hidden")
        except:
            pass

        self.fenetre.quit()


    def cacher_choix_niveau_langue(self):
        """ enlève les boutons de choix de niveau de langage et modifie l'action de celui en bas ou l'enlève aussi 
        actions = actions du jeu, None si pour détruire le bouton """
        self.canvas.itemconfigure(self.texte_niveau_langue, state = "hidden")

        for x in self.buttons_niveau_langage:
            x.destroy()
        

        self.button_afficher_actions.destroy()


    def cacher_choix_categorie(self):
        """ supprime les boutons de choix des catégories """
        # supprime les boutons
        for x in self.buttons_niveaux:
            x.destroy()

        self.buttons_niveaux = []

        self.canvas.delete(self.text_actions)


    def display_categorie(self, name):
        """ name = name of the category in the dict of the actions 
        not the mode of the game, but the number inside a dict """
        
        pass




    def consulter_actions(self):
        """affiche les actions et permet d'en ajouter
        actions = actions du jeu """
        self.cacher_choix_niveau_langue()

        self.text_actions = self.canvas.create_text(710, 200, text = "choisir la catégorie à consulter", font = ("Helvetica", 30), justify = "center")
        
        # continent le nom des catégories d'actions 
        texts = [x for x in self.actions["fille"].keys()]
        self.buttons_niveaux = []

        # affiche les boutons pour choisir la catégorie à consulter
        x = 150
        y = 300
        for text in enumerate(texts):
            self.buttons_niveaux.append(tk.Button(self.fenetre, height=2, width = 10, text = text, font=("Helvetica", 15), command = partial(self.display_categorie, text)))
            self.buttons_niveaux[-1].pack()
            self.buttons_niveaux[-1].place(x=x, y=y)

            x += 200

            if x > 1200:
                x = 150
                y += 100



    def fin_chrono(self, _ = None):
        """ supprime les trucs du chrono """
        self.canvas.itemconfigure(self.temps_chrono, state = "hidden")
        self.fenetre.quit()
        self.canvas.configure(background="white")
        self.continuer = False
        self.fenetre.unbind("<Return>")

    def stop_chrono(self, _):
        """ appeler quand on veut arrêter le chrono avant qu'il soit finit """
        self.temps = -1
        # évite que ca clignote 
        self.continuer = False
        # gère la fin 
        self.fin_chrono()

    def chrono(self,temps , _):
        """ gère le chrono """
        self.fenetre.quit()

        self.temps = temps
        self.continuer = True

        self.fenetre.unbind("<Return>")
        self.fenetre.bind('<Return>', self.stop_chrono)

        self.button_chrono.destroy()
        self.canvas.itemconfigure(self.temps_chrono, state = "normal")
        while self.temps > -1:
            self.canvas.itemconfigure(self.temps_chrono, text = f"temps restant:\n{self.temps}")
            self.canvas.pack()
            self.temps -= 1
            self.fenetre.after(1000, self.fenetre.quit)
            self.fenetre.mainloop()

        #self.fenetre.bind('<Return>', self.fin_chrono)
        background = ["white", "red"]
        nb = 0
        while self.continuer:
            self.canvas.configure(background=background[nb])
            # pourc changer la couleur de fond
            nb = (nb+1)%2
            self.fenetre.after(500, self.fenetre.quit)
            self.fenetre.mainloop()            


    def affichage_nom_joueur(self, nom):
        """ gère l'affichage du bon nom de joueur"""
        # affichage du bon nom 
        # cache l'un et affiche l'autre
        print(nom)
        if nom == "fille":
            self.canvas.itemconfigure(self.nom_fille, state = "normal")
            self.canvas.itemconfigure(self.nom_garcon, state = "hidden")
            self.canvas.itemconfigure(self.nom_a_2, state = "hidden")
        elif nom == "garcon":
            self.canvas.itemconfigure(self.nom_fille, state = "hidden")
            self.canvas.itemconfigure(self.nom_garcon, state = "normal")
            self.canvas.itemconfigure(self.nom_a_2, state = "hidden")
        elif nom == "deux joueurs":
            self.canvas.itemconfigure(self.nom_fille, state = "hidden")
            self.canvas.itemconfigure(self.nom_garcon, state = "hidden")
            self.canvas.itemconfigure(self.nom_a_2, state = "normal")

    def affichage_bonus(self, bonus):
        """ gère l'affichage du bonus """
        # affiche ou cache le bonus
        if bonus == "":
            self.canvas.itemconfigure(self.bonus, state = "hidden")
            self.canvas.itemconfigure(self.bonus_titre, state = "hidden")
        else:
            self.canvas.itemconfigure(self.bonus, text = bonus, state = "normal")
            self.canvas.itemconfigure(self.bonus_titre, state = "normal")

    def affichage_yeux_bandes(self, yeux_bandes):
        """ gère l'affichage du message des teux bandés """
        # affiche si l'action se fait les yeux bandés et pour quel joueur
        if yeux_bandes == "":
            self.canvas.itemconfigure(self.yeux_bandes, state = "hidden")
        else:
            self.canvas.itemconfigure(self.yeux_bandes, text = yeux_bandes, state = "normal")
            #print(yeux_bandes)

    def affichage_illustration(self, illustration: list[Picture]):
        """ illustration = liste des adresses des images possibles n'impporte quel nombre autorisé
        affiche les illustrations des actions lorsque disponibles """
        if len(self.illustrations) != 0:
            for x in self.illustrations:
                self.canvas.delete(x)
            self.illustrations = []

        # affichage des images "d'exemple"
        if illustration != None:
             # coordonées des images
            coordones = [(380, 250), (1100, 250), (380, 500), (1100, 500)]
            for coords, file in zip(coordones, illustration):
                self.images_illustrations.append(tk.PhotoImage(file=file.get_file_name()))
                # un resize si besoin ?
                self.illustrations.append(self.canvas.create_image(coords[0], coords[1], image = self.images_illustrations[-1]))

    def carte(self, texte:str , nom: Player, bonus: str, yeux_bandes: str, temps: int = 0, illustration: list[str] = None):
        """ affiche la carte avec l'action et ce qui va avec :
        texte = text de l'action
        nom = nom du joueur qui fait l'action
        bonus = text du bonus, ou "None" si pas de bonus
        yeux_bandés = text des yeux bandés, ou "non" si pas les yeux bandés
        etape = numero de l'étape du jeu 
        fin = si c'est la fin du jeu, true si c'est la fin 
        """
        # modifie le texte de l'action 
        self.canvas.itemconfigure(self.action, text = str(texte))

        # on a un str quand c'est deux joueur et un objet Player quand on a un joueur
        # un peu bancale, à modif plus tard peut être, avec un objet deux joueurs ? (peut être pas très logique)
        if type(nom) == str:
            self.affichage_nom_joueur(nom)
        else:
            self.affichage_nom_joueur(nom.get_genre())

        self.affichage_bonus(bonus)
        self.affichage_yeux_bandes(yeux_bandes)
        self.affichage_illustration(illustration)

        self.canvas.pack()
        
        # si action avec chrono alors on crée le bouton du chrono
        if temps != None:
            self.button_chrono = tk.Button(self.fenetre, text = "lancer le chrono",width = 20, height = 2, font=("Helvetica", 15), justify = "center", command=partial(self.chrono, temps))
            self.fenetre.bind('<Return>', partial(self.chrono, temps))
            self.button_chrono.pack()
            self.button_chrono.place(x=1100, y=140)
        else:
            # on attend que le joueur presse entré pour passer à la suite
            self.fenetre.bind('<Return>', self.suivant)

        
        self.fenetre.mainloop()

    def suivant(self, _):
        self.fenetre.quit()
        self.fenetre.unbind("<Return>")






if __name__ == "__main__":
    import main