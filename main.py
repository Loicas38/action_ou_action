import fonctionnement
import graphique
from structure import Action, Word, Picture, Player


words = {
      "embrasser": Word(["fait un bisous à"], ["embrasse"], ["roule des pelles à"]),
}

players = {
      "girl": Player("Girl player", "fille"),
      "boy": Player("Boy player", "garcon")
}


pictures = {
      "bisous": Picture(".\illustrations\\bisous.gif"),
}


# normalement on peut modifier le nombre de catégories d'actions sans bug
# il est recommandé de créer autant de catégories pour chaque personne, mais on peut tout de même laisser, par exemple,
# la liste des actions du niveau 3 vide sans bug
actions_soft = {
      "mode": "soft",
      "clothes": False,

       "fille" : {
             1: [
                 Action("%word% %player1%", 
                        time=10, 
                        players=[players["boy"]],
                        words = [words["embrasser"]],
                        pictures = [pictures["bisous"]]
                  )
             ],
             2: [
                   Action("fais le tour de la pièce en courant", time = 20),
             ],
             3: [
                   Action("chante une chanson\nque %player1% a\nchoisi", players = [players["boy"]])
             ],
             4: [
                   Action("chatouille %player1%", players=[players["boy"]])
             ],
             5: [
                  Action("test")
             ],
             6: [
                  Action("test")
             ]
       },
       "garcon" : {
             1: [
                 Action("%word% %player1%", 
                        time=10, 
                        players=[players["boy"]],
                        words = [words["embrasser"]],
                        pictures = [pictures["bisous"]]
                  )
             ],
             2: [
                   Action("fais le tour de la pièce en courant", time = 20),
             ],
             3: [
                   Action("chante une chanson\nque %player1% a\nchoisi", players = [players["boy"]])
             ],
             4: [
                   Action("chatouille %player1%", players=[players["boy"]])
             ],
             5: [
                  Action("test")
             ],
             6: [
                  Action("test")
             ]
       },
       "action_a_2" : {
             1: [
                   Action("action à 2")
             ],
             2: [
                   
             ],
             3: [

             ],
             4: [
                 
             ],
             5: [

             ],
             6: [

             ]
       }
}

actions_normal = {
      "mode": "normal",
      "clothes": False,
      
       "fille" : {
             1: [
                 Action("actions normales")
             ],
             2: [
                   Action("fais le tour de la pièce en courant", time = 20),
             ],
             3: [
                   Action("chante une chanson\nque %player1% a\nchoisi", players = [players["boy"]])
             ],
             4: [
                   Action("chatouille %player1%", players=[players["boy"]])
             ],
             5: [
                  Action("test")
             ],
             6: [
                  Action("test")
             ]
       },
       "garcon" : {
             1: [
                 Action("hard action")
             ],
             2: [
                   Action("fais le tour de la pièce en courant", time = 20),
             ],
             3: [
                   Action("chante une chanson\nque %player1% a\nchoisi", players = [players["boy"]])
             ],
             4: [
                   Action("chatouille %player1%", players=[players["boy"]])
             ],
             5: [
                  Action("test")
             ],
             6: [
                  Action("test")
             ]
       },
       "action_a_2" : {
             1: [
                   Action("action à 2")
             ],
             2: [
                   
             ],
             3: [

             ],
             4: [
                 
             ],
             5: [

             ],
             6: [

             ]
       }
}

actions_hard = {
      "mode": "hard",
      "clothes": False,
      
       "fille" : {
             1: [
                 Action("actions hard")
             ],
             2: [
                   Action("fais le tour de la pièce en courant", time = 20),
             ],
             3: [
                   Action("chante une chanson\nque %player1% a\nchoisi", players = [players["boy"]])
             ],
             4: [
                   Action("chatouille %player1%", players=[players["boy"]])
             ],
             5: [
                  Action("test")
             ],
             6: [
                  Action("test")
             ]
       },
       "garcon" : {
             1: [
                 Action("hard action")
             ],
             2: [
                   Action("fais le tour de la pièce en courant", time = 20),
             ],
             3: [
                   Action("chante une chanson\nque %player1% a\nchoisi", players = [players["boy"]])
             ],
             4: [
                   Action("chatouille %player1%", players=[players["boy"]])
             ],
             5: [
                  Action("test")
             ],
             6: [
                  Action("test")
             ]
       },
       "action_a_2" : {
             1: [
                   Action("action à 2")
             ],
             2: [
                   
             ],
             3: [

             ],
             4: [
                 
             ],
             5: [

             ],
             6: [

             ]
       }
}


# création de l'inteface graphique et lancement des premières fenêtres qui demandent les paramètres du jeu 
graph = graphique.Graphique([actions_soft, actions_normal, actions_hard], players["boy"], players["girl"])
# on récupère la vitesse du jeu, qui correpond au nombre d'actions que seront à faire
vitesse = graph.get_vitesse()

# récupération du niveau de langue choisi 
langue = graph.get_niveau_langage()

# retourne le set d'actions choisies par les joueurs, qui peuvent être différentes de celles passées si modifiées 
# (la modification des actions dispo n'est pas encore implémentée)
actions = graph.get_chosen_actions()

jeu = fonctionnement.Jeu(vitesse, players["girl"], players["boy"], actions)
action = None
fin = False
while not fin:
    # on récupère la'action suivante et tout les bonus et trucs utils
    action, yeux_bandes, bonus, joueur, etape, fin = jeu.choix_action()

    action = action.get_action(langue)

    """print("action : ", action["text"])
    print("joueur : ", joueur)
    print("yeux bandés : ", yeux_bandes)
    print("etape : ", etape)
    print("temps : ", action["time"])
    print("illustration : ", action["pictures"])
    print()"""

    # puis on les passe pour l'affichage 
    graph.carte(action["text"], joueur, bonus, yeux_bandes, action["time"], action["pictures"])