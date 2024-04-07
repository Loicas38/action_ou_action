from random import choice, randint, choices, sample
from enum import unique, IntEnum


# to register type of the actions and avoid errors in the code
# not use in the current app
@unique
class Type_action(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


@unique
class Type_joueur(IntEnum):
    GIRL = 1
    BOY = 2



class Word:
    SOFT: list
    NORMAL: list
    HARD: list 

    def __init__(self, soft_words: list[str], normal_words: list[str], hard_words: list[str]) -> None:
        self.SOFT = soft_words
        self.NORMAL = normal_words
        self.HARD = hard_words


    def get_easy_word(self):
        """ return a word of the soft category """

        if len(self.SOFT) >= 1:
            return choice(self.SOFT)
        else:
            return None
    
    def get_easy_word_and_delete(self):
        """ return a word and delete it """

        if len(self.SOFT) >= 1:
            return self.SOFT.pop(randint(0, len(self.SOFT)-1))
        else:
            return None
        
    
    def get_normal_word(self):
        """ return a word of the soft category """
        
        if len(self.NORMAL) >= 1:
            return choice(self.NORMAL)
        else:
            return None
    
    def get_normal_word_and_delete(self):
        """ return a word and delete it """

        if len(self.NORMAL) >= 1:
            return self.NORMAL.pop(randint(0, len(self.SOFT)-1))
        else:
            return None
        
    
    def get_hard_word(self):
        """ return a word of the soft category """
        
        if len(self.HARD) >= 1:
            return choice(self.HARD)
        else:
            return None
    
    def get_hard_word_and_delete(self):
        """ return a word and delete it """

        if len(self.HARD) >= 1:
            return self.HARD.pop(randint(0, len(self.SOFT)-1))
        else:
            return None
        

    def get_random_word(self):
        """ return a word of the soft category """
        
        # store the categories which still have some words
        words = []
        if len(self.SOFT) > 0:
            words += self.SOFT
        if len(self.NORMAL) > 0:
            words += self.NORMAL
        if len(self.HARD) > 0:
            words += self.HARD
        
        # return a rando word from a random category
        if len(words) > 0:
            return choice(words)
        else:
            return None
    
    def get_random_word_and_delete(self):
        """ return a word and delete it """

        if len(self.SOFT) > 0 or len(self.NORMAL) > 0 or len(self.HARD) > 0:
            category = randint(0, 2)
            while True:
                if category == 0 and len(self.SOFT) > 0:
                    return self.SOFT.pop(randint(0, len(self.SOFT)-1))
                

                if category == 1 and len(self.NORMAL) > 0:
                    return self.NORMAL.pop(randint(0, len(self.NORMAL)-1))
                

                if category == 1 and len(self.HARD) > 0:
                    return self.NORMAL.pop(randint(0, len(self.HARD)-1))
                
                category += 1
                category %= 3
                
        else:
            return None      


class Picture:

    def __init__(self, files: str, format: tuple = None) -> None:
        """ format corresponds to (height, width) of the pictures for tkinter """
        self.picture_files = files
        self.tkinter_pictures = []

    def create_picture_for_tkinter(self):
        """ create a picture for tkinter """
        pass

    def get_random_picture_file(self, nb: int) -> list[str]:
        """ return a list of random file names chosen among the availables """
        if len(self.picture_files) < nb:
            return self.picture_files
        else:
            return sample(self.picture_files, k=nb)
        
    def get_random_tkinter_pictures(self, nb: int) -> list[str]:
        """ return a list of random file names chosen among the availables """
        if len(self.tkinter_pictures) < nb:
            return self.tkinter_pictures
        else:
            return sample(self.tkinter_pictures, k=nb)

    def get_file_name(self) -> list[str]:
        """ return the list of all the pictures file name"""
        return self.picture_files

    def get_picture_for_tkiner(self):
        """ return all the pictures ready to be displayed """
        return self.tkinter_pictures

class Player:
    GENRE: str
    NAME: str
    SURNAMES: list[str]

    def __init__(self, name, genre) -> None:
        self.NAME = name
        self.GENRE = genre
    
    def change_name(self, name: str) -> None:
        """ change the name of the player """
        self.NAME = name

    def get_name(self) -> str:
        """ return the name of the player """
        return self.NAME
    
    def get_genre(self) -> str:
        """ return the genre of the player """
        return self.GENRE


class Action:
    TEXT: str
    PICTURES: list[Picture]
    TIME: int
    TYPE: list[Type_action]
    # register if an action has already been played
    PLAYED: bool

    def __init__(self, text: str, pictures: list[Picture] = None, time: int = None, words: list[Word] = [], players: list[Player] = []) -> None:
        """ text: text of the action. If you want to replace a word, you have to put "%word%" in your text, and the first
        one will be replace by the first word in 'words', the second by the second, ...
        pictures : list of the files name of the pictures which can be display for that action 
        time : time of the action 
        words : words to put in place of %word% """
        
        self.TEXT = text
        self.PICTURES = pictures
        self.words = words
        self.TIME = time
        self.players = players
        self.PLAYED = False

    def replace_words(self, mode: str) -> None:
        """ mode : soft, normal, hard or random -> among which list will be chosen the word
        replace the "%word%" by the words provided."
        and %player{nb}% by the player provided, nb is 1 or 2, according to the position in the list of players provided """

        # new text to replace the old one
        modify_text = ""


        # id of the next word to replace in the liste of words provided
        nb = 0
        n = len(self.TEXT)

        place = 0
        char = self.TEXT[place]

        while place < len(self.TEXT):
            char = self.TEXT[place]
            placed = False

            # we meet the first % which probably announce a word to place
            if char == "%":

                if n >= place + 8:

                    # case of a player
                    if self.TEXT[place:place+9] == "%player1%":
                        modify_text += self.players[0].get_name()

                        placed = True
                        place += 8

                    # case of a player
                    elif self.TEXT[place:place+9] == "%player2%":
                        modify_text += self.players[1].get_name()

                        placed = True
                        place += 8


                # check if there is enough characters to avod errors
                if n >= place+5:
                    # if it's easy, we put aneasy word
                    if self.TEXT[place:place+6] == "%word%":
                        if mode == "soft":
                            modify_text += self.words[nb].get_easy_word()
                            placed = True
                            place += 5
                            nb += 1

                        elif mode == "normal":
                            modify_text += self.words[nb].get_normal_word()
                            placed = True
                            place += 5
                            nb += 1

                        elif mode == "hard":
                            modify_text += self.words[nb].get_hard_word()
                            placed = True
                            place += 5
                            nb += 1

                        elif mode == "random":
                            modify_text += self.words[nb].get_random_word()
                            placed = True
                            place += 5
                            nb += 1


                if not placed:
                    modify_text += char

            else:
                modify_text += char


            place += 1      

        # we change the original text by the new one
        self.TEXT = modify_text

    def get_text_action(self, mode: str) -> str:
        """ mode : mode for the words to replace, to choose among "soft", "normal", "hard" and "random" 
        return the text of the action """
        self.replace_words(mode)
        return self.TEXT
    
    def get_time(self):
        return self.TIME
    
    def get_all_pictures(self) -> list[Picture]:
        return self.PICTURES
    
    def get_one_picture(self) -> Picture:
        if len(self.PICTURES) > 0:
            return self.PICTURES[randint(0, len(self.PICTURES)-1)]
        else:
            return None
        
    def get_some_pictures(self, nb: int) -> list[Picture]:
        """ return the number of picture asked """
        if nb > len(self.PICTURES) - 1:
            nb = len(self.PICTURES) - 1
        if len(self.PICTURES) == 0:
            return None
        
        return choices(self.PICTURES, k=nb)
    
    def get_action(self, mode: str) -> dict:
        """ return a dict whch contains all the informations about the action """

        return {
            "text": self.get_text_action(mode),
            "time": self.get_time(),
            "pictures": self.get_all_pictures()
        }