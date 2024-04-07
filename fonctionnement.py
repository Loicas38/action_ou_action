from random import randint, choice
from structure import Player, Action, Picture

class Jeu():
    def __init__(self, vitesse: int, girl: Player, boy: Player, actions:dict[str:dict[str:list]], fin_habit: int = 3) -> None:
        """ nb_action : nombre d'actions au total
        habits fille : nb d'habits de la fille, pareil pour le garçon 
        vitesse : vitesse du jeu, compris entre 1 et 3
        action : dictionnaire des actions disponibles 
        garcon : nom du garcon
        fille : nom de la fille 
        fin_habits = à partir de quelle catégorie on joue sans habits """

        # on crée les actions avec les mots à remplacer en fonction du langage qui a été choisi
        self.actions = actions
        self.fin_habits = fin_habit

        # 1 chance sur ...
        # de devoir choisir tout seul une action à faire, sans propositions de l'ordi 
        self.proba_choisis_action = 6

        # 1 sur ...
        self.proba_yeux_bandes = 4

        # 1 sur ...
        self.proba_bonus = 4

        # 1 sur ...
        self.proba_action_a_2 = 3

        self.players = {
            0: girl,
            1: boy
        }

        # choix du premier joueur aléatoire
        self.joueur = randint(0, 1)

        self.action_a_faire_categorie = self.calcul_action_categories(vitesse)



    def calcul_action_categories(self, vitesse: int) -> dict:
        """ vitesse = vitesse du jeu 
        Calcul le nombre d'actions à faire dans chaque catégorie et le retourne sous forme de dictionnaire """
        # create a list with the number of action in each category
        actions_fille = [len(x) for x in self.actions["fille"].values()]
        actions_garcon = [len(x) for x in self.actions["garcon"].values()]
        actions_a_2 = [len(x) for x in self.actions["action_a_2"].values()]

        # count of the maximum number of actions which can be made at each stage
        nb_actions_categories = [a_2 + min(nb_fille, nb_garcon)*2 for a_2, nb_fille, nb_garcon in zip(actions_a_2, actions_fille, actions_garcon)]
        print(nb_actions_categories)
        # on définit le nombre d'actions en fonction de la vitesse 
        nb_actions = vitesse * randint(9, 11)

        # permet de calculer le nombdre d'actions à faire dans chaque catégorie
        # on suppose que tout les joueurs ont autant de catégories 
        nb_a_faire = {x+1:0 for x in range(len(self.actions["fille"]))}
        # numero de la categorie à laquelle on commence à mettre des actions, et qui en aura donc le plus
        categorie = 6
        for _ in range(nb_actions):
            if nb_a_faire[categorie] >= nb_actions_categories[categorie-1]:
                # on vérifie s'il reste des catégories qui n'ont pas le max d'actions possibles
                # s'il reste de la place on continue, sinon on arrête
                possible = []
                # on passe toutes les catégories et on check s'il reste de la place
                for id, nb in enumerate(nb_actions_categories):
                    if nb_a_faire[id+1] < nb:
                        possible.append(id+1)
                
                # si toutes les catégories sont remplies, on arrête de mettre des actions
                # sinon on choisit une catégorie aléatoire parmi les dispos
                if len(possible) == 0:
                    break
                else:
                    categorie = choice(possible)

            if categorie <= 0 or categorie >= 7:
                categorie = randint(4, 6)

            nb_a_faire[categorie] += 1
            categorie -= randint(1, 3)

            if categorie <= 0 or categorie >= 7:
                categorie = randint(4, 6)
            

        print(nb_a_faire)
        return nb_a_faire

    def choix_action_a_2(self, categorie):
        """ retourne une action à faire à 2 de la bonne categorie si dispo, sinon None"""
        nb_dispos = len(self.actions["action_a_2"][categorie])
        if nb_dispos != 0:
            action = self.actions["action_a_2"][categorie].pop(randint(0, nb_dispos-1))
            return action

        return None

    def choix_action_solo(self, categorie):
        """ choisis une action à faire en solo dans la catégorie choisie, 
        et retourne l'action si dispo, sinon None"""
        nb_dispos = len(self.actions[self.players[self.joueur].get_genre()][categorie])
        if nb_dispos != 0:
            action = self.actions[self.players[self.joueur].get_genre()][categorie].pop(randint(0, nb_dispos-1))
            return action

        return None


    def yeux_bandes(self) -> bool:
        """ retourne un booleen pour dire si yeuxbandés ou non """
        if randint(0, self.proba_yeux_bandes) == 0:
            return True
        
        return False

    def texte_yeux_bandes(self, bandes: bool) -> str:
        if bandes:
            return f"{self.players[self.joueur].get_name()} bande les yeux\nde {self.players[(self.joueur+1)%2].get_name()}"
        else:
            return ""

    def action_fin_jeu(self):
        """ pour la fin du jeu """
        action = Action(
            "Pour la dernière action,\nà vous d'inventer !",
        )

        yeux_bandes = "On bande les yeux\ndes volontaires"
        joueur = "deux joueurs"
        bonus = "triche autorisée"
        categorie_action = 7

        return action, yeux_bandes, bonus, joueur, categorie_action, True

    def choix_action(self):
        # on change de joueur
        self.joueur = (self.joueur+1)%2
        joueur = self.players[self.joueur]
        
        # on prend la catégorie de jeu 
        categorie_action = 0
        # on cherche la première catégorie où il reste des actions à faire
        for categorie in range(1, 7):
            if self.action_a_faire_categorie[categorie] != 0:
                categorie_action = categorie
                # on enlève un parce que l'action va être faite
                self.action_a_faire_categorie[categorie] -= 1
                break

        # cas où le jeu est fini
        if categorie_action == 0:
            ########## gérer a fin du jeu ##########
            return self.action_fin_jeu()
            

        yeux_bandes = self.yeux_bandes()
        yeux_bandes = self.texte_yeux_bandes(yeux_bandes)


        # choix aléatoire entre action solo ou à 2
        action = randint(0, 1)
        if action == 0:
            action = self.choix_action_solo(categorie_action)
            
            # si plus d'actions en solo pour ce joueur, on prend une action à 2
            if action == None:
                action = self.choix_action_a_2(categorie_action)
                # pour éviter qu'un joueur ait 2 actions solo à la suite 
                self.joueur = (self.joueur+1)%2
                # nom du joueur changé pour les 2 joueurs vu que action à 2
                joueur = "deux joueurs"
        else:
            action = self.choix_action_a_2(categorie_action)
            # pour éviter qu'un joueur ait 2 actions solo à la suite 
            self.joueur = (self.joueur+1)%2
            joueur = "deux joueurs"

            # si plus d'actions à 2 on prend une action en solo
            if action == None:
                self.joueur = (self.joueur+1)%2
                joueur = self.players[self.joueur]
                action = self.choix_action_solo(categorie_action)
        
        # to improve, that's just an example
        bonus = ""
        if randint(0, self.proba_bonus) == 0:
            bonus = "triche autorisée"

        return action, yeux_bandes, bonus, joueur, categorie_action, False



if __name__ == "__main__":
    import main