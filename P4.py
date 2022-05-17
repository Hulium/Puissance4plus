"""
P4+
"""

#---------Zone d'importation des librairies-------------
import os
import sys
import time
#---------Variable globale----------
global DEBUG

#===================================================================
#True pour afficher le debug en console et false pour ne pas l'afficher
DEBUG = False




#------------Définitions des Classes----------------
class Plateau:
    def __init__(self):
        self.Plateau2D = [[0 for _ in range(7)] for _ in range(6)] #Etat du plateau (tableau 2D) à un instant donné 
        self.statut = False #Statut de victoire (Joueur Gagnant ou plus de coup possible)
        self.tour = 1
        
        #Variables privé
        self.emplacement = None
        self.legal = True
        self.SavePlateau2D = self.Plateau2D
    
    def modif_plateau(self, joueurID, emplacement, typeCoup): #edit l'etat du plateau en fonction des informations transmises (le joueur, l'emplacement et le type de coup)
        self.emplacement = emplacement #Enregistre l'emplacement du coup du joueur en variable de la classe plateau
       
        self.SavePlateau2D = self.Plateau2D #On sauvegarde le plateau en cas de coup non legal
        self.__check_legal() #Vérifie si le coup est légal 
        if self.legal == False : #Sinon on arrete la fonction
            self.Plateau2D = self.SavePlateau2D #On remet le plateau dans on état antérieur
            self.legal = True #On remet a Vrai pour la prochaine vérification
            return False
        else : #le coup est légal 
            if typeCoup == "pion":
                if joueurID == "J1": #Si J1 on met la valeur à 1 si J2 valeur a 2      
                    self.Plateau2D[0][emplacement-1] = 1 #Pion J1
                elif joueurID == "J2":
                    self.Plateau2D[0][emplacement-1] = 2 #Pion J2
            elif typeCoup == "bombe":
                self.Plateau2D[0][emplacement-1] = 3 #Bombe
        
        self.__check_plateau() #On check et met a jour le plateau

        if self.statut == True : #On vérifie si il y a un gagnant
            affichage_console()
            print_info(" VICTOIRE pour "+str(joueurID)+" Yeahh !")
            
        
        return True #Fin de la fonction on renvoie vrai pour faire continuer les tours

      
    
    #Fonctions interne (Private)
    def __check_legal(self):  #Fonction de vérification si le coup est légal (on écrase pas un autre pion)
        if self.SavePlateau2D[0][self.emplacement-1] == 1 or self.SavePlateau2D[0][self.emplacement-1] == 2 : #Si un pion est déja présent
            LOG_print("coup : not legal")
            print_info("Le coup est illegal !")
            self.legal = False
            return 
        LOG_print("coup : legal")
        print_info("Le coup est legal")

    def __check_plateau(self): #Check le plateau
        self.__check_update_pions() #Update les pions
        self.__check_gagnant() #Vérifie si il y a un gagnant
        
             
    
    def __check_update_pions(self): #Fonction qui permet de vérifier si les pions sont positionné en bas (au sol par la gravité comme un vrai jeu)
        action = False
        for i in range(0,6) : #boucle qui parcours le tableau (Lignes)
            for y in range (0,7) : #(Colonnes)
                if PLATEAU.Plateau2D[i][y] == 1 or PLATEAU.Plateau2D[i][y] == 2 or PLATEAU.Plateau2D[i][y] == 3: #si un pion existe (ou une bombe)
                    if i+1 < 6 : #Vérifie que l'on sors pas du tableau
                        if PLATEAU.Plateau2D[i+1][y] == 0 :#et qu'un espace vide est sous celui ci 
                            #alors on deplace le pion vers le bas
                            tempo = PLATEAU.Plateau2D[i][y]
                            PLATEAU.Plateau2D[i][y] = 0
                            PLATEAU.Plateau2D[i+1][y] = tempo
                            action = True
                            ###affichage_console()
        if action == False : #Si rien a faire les pions sont actualisé, on vérifie qu'une bombe n'es pas présente et on quitte la fonction
            LOG_print("------- AUCUNES ACTION sur ce check > Vérif bombe")
            self.__check_bombe()
            return
        elif action == True : 
            LOG_print("------- ACTION FAITE > relancement pour vérification")
            self.__check_plateau() #(Recursivité) On relance le check de maniere a refaire descendre les pions jusqu'a un état correct
   
   
    def __check_bombe(self):
        for i in range(0,6) : #boucle qui parcours le tableau (Lignes)
            for y in range (0,7) : #(Colonnes)
                if PLATEAU.Plateau2D[i][y] == 3: #Si bombe alors on la fait exploser
                    #on met a 0 toutes les cases autour (en forme de croix)
                    PLATEAU.Plateau2D[i][y] = 0
                    LOG_print(" Destruction case : " + str(i) +"-"+ str(y))
                    try :
                        PLATEAU.Plateau2D[i-1][y] = 0
                        LOG_print(" Destruction case : " + str(i-1) +"-"+ str(y))
                    except IndexError:
                        pass
                    try :
                        PLATEAU.Plateau2D[i][y-1] = 0
                        LOG_print(" Destruction case : " + str(i) +"-"+ str(y-1))
                    except IndexError:
                        pass
                    try :
                        PLATEAU.Plateau2D[i+1][y] = 0
                        LOG_print(" Destruction case : " + str(i+1) +"-"+ str(y))
                    except IndexError:
                        pass
                    try :
                        PLATEAU.Plateau2D[i][y+1] = 0
                        LOG_print(" Destruction case : " + str(i) +"-"+ str(y+1))
                    except IndexError:
                        pass
                    
                    self.__check_plateau() #l'explosion a modifier le plateau on relance un check du plateau

    
    def __check_gagnant(self):
        for i in range(0,6) : #boucle qui parcours le tableau (Lignes)
            for j in range (0,7) : #(Colonnes)
                victoire = False
                #VERTICALEMENT 
                n=0  #du haut vers le bas 
                while n<4 and i+n<6 and PLATEAU.Plateau2D[i+n][j]==PLATEAU.Plateau2D[i][j] and PLATEAU.Plateau2D[i][j]!=0: 
                    n+=1 
                if n>=4: 
                    LOG_print("Victoire verticale")
                    victoire = True
                #HORIZONTALEMENT 
                n=0   #vers la gauche 
                while n<4 and j-n>=0 and PLATEAU.Plateau2D[i][j-n]==PLATEAU.Plateau2D[i][j] and PLATEAU.Plateau2D[i][j]!=0: 
                    n+=1 
                m=0   #vers la droite 
                while m<4 and j+m<7 and PLATEAU.Plateau2D[i][j+m]==PLATEAU.Plateau2D[i][j] and PLATEAU.Plateau2D[i][j]!=0: 
                    m+=1 
                if n+m-1>=4: 
                    LOG_print("Victoire horizontal")
                    victoire = True
                #Diagonale (SO->NE) 
                n=0  #vers le SO 
                while n<4 and i-n>=0 and j-n>=0  and PLATEAU.Plateau2D[i-n][j-n]==PLATEAU.Plateau2D[i][j] and PLATEAU.Plateau2D[i][j]!=0: 
                    n+=1 
                m=0  #vers le NE 
                while m<4 and i+m<6 and j+m<7 and PLATEAU.Plateau2D[i+m][j+m]==PLATEAU.Plateau2D[i][j] and PLATEAU.Plateau2D[i][j]!=0: 
                    m+=1 
                if n+m-1>=4: 
                    LOG_print("Victoire diagonal /")
                    victoire = True 
                #Diagonale (NO->SE) 
                n=0   #vers le NO 
                while n<4 and i+n<6 and j-n>=0 and PLATEAU.Plateau2D[i+n][j-n]==PLATEAU.Plateau2D[i][j] and PLATEAU.Plateau2D[i][j]!=0: 
                    n+=1 
                m=0   #vers le SE 
                while m<4 and i-m>=0 and j+m<7 and PLATEAU.Plateau2D[i-m][j+m]==PLATEAU.Plateau2D[i][j] and PLATEAU.Plateau2D[i][j]!=0: 
                    m+=1 
                if n+m-1>=4: 
                    LOG_print("Victoire diagonal \\")
                    victoire = True 
                
                if victoire == True: #si victoire est vrai alors un joueur gagne
                    self.statut = True
                    LOG_print("Victoire check")
                    return
        



class Joueurs:
    def __init__(self):
        self.Id = None #Définit l'identifiant du joueur (J1, J2, J3 ...) doit etre auto
        self.droitJouer = False #Le joueur peut jouer ou non
        self.nbBombes = 3 #Nombre de bombe que posséde le joueur
        self.coups = 0 #Nombre de coups que a jouer le joueur
        
        
    def Play(self): #Fait jouer le joueur et demande l'action
        affichage_console()
        if self.droitJouer == True :
            choix = 99 #Valeur x pour ne pas rentrer dans les conditions
            while True : #Choisie l'emplacement du pion ou jouer la bombe
                try :
                    print("\n\n | > Rentre le numéro de la colonne ou tu veux placer ton PION ou bien rentre 0 pour placer une BOMBE ")
                    choix = int(input(" | Choix : "))
                except ValueError :
                    continue
                else :
                    break
            if choix == 0 : #si on joue une bombe
                typecoup = "bombe"
                if self.nbBombes <= 0 : #On regarde si on peut jouer une bombe (assez de bombe)
                    print_info("Tu n'a plus de bombe !")
                    self.Play()
                    return
                else :
                    while True : #Choisie l'emplacement de la bombe
                        try :
                            print(" | > Rentre le numéro de la colonne ou tu veux placer ta BOMBE ")
                            choix = int(input(" | Choix : "))
                        except ValueError :
                            continue
                        else :
                            break
            else :
                typecoup = "pion" 
                
            if choix>0 and choix<8 : #on vérifie que le chiffre est bien compris entre 1 et 7 inclus
                if typecoup == "bombe":
                    self.nbBombes -= 1 #Reduit de 1 le nombre de bombe en stock
                print(" | > Tu as selectionné la colonne : ", choix)
                if PLATEAU.modif_plateau(self.Id, choix, typecoup) == False :
                    self.Play()
                    return
            else : #Sinon on relance la fonction et on détuit l'instance actuel
                self.Play()
                return
            
            
            self.coups += 1 #Incremente de 1 a chaque appel (pour connaitre le nombre de coups que a jouer le joueur)
            self.droitJouer = False
            
        
            
    def print_data(self):
        if self.droitJouer == False :
            message = "Attend ton tour"
        else :
            message = "A toi de jouer ! <<< <<< <<<"
        print(" > Joueur : "+str(self.Id)+" | Bombe Restante : "+str(self.nbBombes)+" | Coups joué : "+str(self.coups)+" | "+message)
        
    
    
    
    
#------------Definition des fonction ----------------
def main():
    header() #Affiche le logo
    
    
    #Mise en place du jeux (plateau et deux joueurs)
    global PLATEAU
    PLATEAU = Plateau() #Création de l'objet plateau 
    
    global JOUEUR1
    JOUEUR1 = Joueurs() #Création du joueur 1
    JOUEUR1.Id = "J1" 
    
    global JOUEUR2
    JOUEUR2 = Joueurs() #Création du joueur 2
    JOUEUR2.Id = "J2"
            
    #lance les tours de jeux 
    while PLATEAU.statut == False :
        JOUEUR1.droitJouer = True
        JOUEUR1.Play() # J1 joue
        if PLATEAU.statut == True :
            break
        
        JOUEUR2.droitJouer = True
        JOUEUR2.Play() # J2 joue
        if PLATEAU.statut == True :
            break
        
        PLATEAU.tour += 1 #On incrémente de 1 pour chaque tour
        
    tempofin = input("\n\n\n > 'Appuyez sur n'importe quelle touche pour quitter'") #Garde la fenetre ouverte 
    
    
    
    
#----Fonctions d'affichages
def affichage_console():
    clearConsole()
    header()
    print("\n===================\n      TOUR : " + str(PLATEAU.tour) + "\n===================\n") #Affiche le nombre de tour effectué
    JOUEUR1.print_data() #Affiche info joueur
    JOUEUR2.print_data() #Affiche info joueur
    print("\n >  J1 = 'O'  |   J2 = 'X'")
    print("\n")
    
    LOG_print("Interface graphique standard :")
    for i in range(0,6) : #Ligne
            print(i+1,">   | ",end='')
            for y in range (0,7) : #Colonnes
                if PLATEAU.Plateau2D[i][y] == 0:
                    print(".","| ",end='') #affiche la valeur des cellules
                if PLATEAU.Plateau2D[i][y] == 1:
                    print("O","| ",end='') #affiche la valeur des cellules
                if PLATEAU.Plateau2D[i][y] == 2:
                    print("X","| ",end='') #affiche la valeur des cellules    
                if PLATEAU.Plateau2D[i][y] == 3:
                    print("B","| ",end='') #affiche la valeur des cellules 
            print("")
    print("\n        ",end='')
    for p in range (0,7) :
        print("^","  ",end='')
    print("\n        ",end='')
    for j in range (0,7) :
        print(j+1,"  ",end='')
    
    #Affichage tableau DEBUG
    if DEBUG == True :
        print("\n")
        LOG_print("Tableau coordonées avec valeur :")
        for i in range(0,6) : #Ligne
            for y in range (0,7) : #Colonnes
                print(" ____ ",i,"-",y,">  ",end='') #affiche les coordonées
                print(PLATEAU.Plateau2D[i][y],end='') #affiche la valeur des cellules
            print("")
    
    ###print_info("RAS")
    
        
        
def header(): #Fonction d'affichage du nom du jeux
    if DEBUG == False :
        print(
        "  _____       _                                _  _         \n" +
        " |  __ \     (_)                              | || |    _   \n" +
        " | |__) |   _ _ ___ ___  __ _ _ __   ___ ___  | || |_ _| |_ \n" +
        " |  ___/ | | | / __/ __|/ _` | '_ \ / __/ _ \ |__   _|_   _|\n" +
        " | |   | |_| | \__ \__ \ (_| | | | | (_|  __/    | |   |_|  \n" +
        " |_|    \__,_|_|___/___/\__,_|_| |_|\___\___|    |_|        \n" + 
        "                                                            ")
        print("=====================================================================================================")
    

#----Fonctions de log/debug console et system
def LOG_print(msg):
    if DEBUG == True :
        print("---log  >  " + str(msg))

def print_info(msg):
    print("\n\n >>>\n >>> /!\ INFORMATION : ",str(msg),"\n >>>\n")
        
def clearConsole():
    if DEBUG == False :
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
    
    
    
#Code principal appelle du main
if __name__ == '__main__': #Si j'execute le programme directement depuis le fichier principal (par ligne de commande)
    main() #J'apelle la fonction principal
    
    
    