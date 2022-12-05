# -*- coding: utf-8 -*-
"""
Created on Fri May 21 09:23:26 2021

@author: Vénon
"""

import os
import sys
import random

#Nos données
nameTxtFile = "Radio.txt"
positionFile = os.path.abspath(os.path.dirname(sys.argv[0]))

#Récupération du fichier dll problématique
if os.path.exists( positionFile + "\\lien VLC.txt"):
    fileTxt = open(positionFile + "\\lien VLC.txt","r")
    os.add_dll_directory(r''+fileTxt.readlines()[0])
    fileTxt.close()
else: print("Il manque le fichier \"lien VLC\" ou est présent le lien du dossierVLC")

import vlc

saveRadio = None

def main():
    if os.path.exists( positionFile + "\\" + nameTxtFile):            #Si le fichier radio est présent
            
        fileTxt = open(positionFile + "\\" + nameTxtFile,"r")         #On ouvre notre fichier texte
        mesLignes = fileTxt.readlines()                               #On récupérer les lignes 
        
        AfficheRadios(mesLignes)            #On affiche les radios 
        AutreProposition()                  #On affiche les options                                                    
        maxi = MyMax(mesLignes)              #On récupère le num de la dernière radio
        
        maChaine = ChoixRadio(mesLignes,maxi)    #On définit notre readio
        
        global saveRadio
        saveRadio = maChaine
           
        #Define VLC player
        instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        player=instance.media_player_new() 
        
        QuandLaMusicEstBonne(instance,player,maChaine,mesLignes,maxi)    #On lance notre lecteur

        fileTxt.close()    #On ferme notre fichier texte   
    else:  
        print("Le fichier de donnée \"data\" doit se trouver dans le même emplacement que l'application")
        
def AfficheRadios(mesLignes):
    for x in range(len(mesLignes)):                                         #Pour toutes nos lignes
        if len(mesLignes[x].split(";"))>1:                                  #Si c'est un radio
            print(str(x) + " -> " + mesLignes[x].split(";")[0].strip())     #On affiche que le nom et son num
        else: print(mesLignes[x])                                           #Sinon on affiche la ligne

def IsRadio(mesLignes,maxi,maChaine):                                        #On renvoie l'info si c'est une radio ou pâs                                        
    if not str(maChaine).isdigit() or int(maChaine)>maxi or len(mesLignes[int(maChaine)].split(";"))<=1: 
        return False
    else: return True

def MyMax(mesLignes):
    for x in range(len(mesLignes)):             #On affiche toutes les radios présentes
        if len(mesLignes[x].split(";"))>1:      #Si c'est une radio                   
            maxi = x                             #On garde ca valeur
    return maxi

def PlayRadio(instance,player,maChaine,mesLignes):
    media=instance.media_new(mesLignes[int(maChaine)].split(";")[1].strip())    #On définit notr média   
    player.set_media(media)                                                     #On le met en place      
    player.play()                                                               #On le lance
    
def QuandLaMusicEstBonne(instance,player,maChaine,mesLignes,maxi):
    PlayRadio(instance,player,maChaine,mesLignes)                       #On lance notre musique
    AfficheRadios(mesLignes)                                            #On affiches nos radios
    AutreProposition()                                                  #On affiche nos options
    VousEcoutezActuellement(mesLignes,maChaine)                         #On affiche la radio actuelle 
    maChaine = ChoixRadio(mesLignes,maxi)                                #Nouvelle chaine quand l'utilisateur décide de changer de radio
    global saveRadio
    saveRadio = maChaine
    player.stop()                                                       #Alors on arrête la radio actuel
    QuandLaMusicEstBonne(instance,player,maChaine,mesLignes,maxi)        #Puis on lance la suivante 

def AutreProposition():                                                 #Affiche nos différentes options
    print()
    print("q -> Quitter")
    print("a -> Radio aléatoire")
    print("+ ou - -> Radio suivante/précédante")
    
def QuesCeQuOnFait(maChaine,mesLignes,maxi):
    if not str(maChaine).isdigit():                 #Si le choix est une option, on agit en conséquence
        if maChaine == "q":
            Quiter() 
        elif maChaine == "a":
            maChaine = RadioAleat(mesLignes,maxi)
        elif maChaine == "+":
            maChaine = RadioSuivante(mesLignes,maxi)
        elif maChaine == "-":
            maChaine = RadioPrecedante(mesLignes,maxi)
    
    if IsRadio(mesLignes,maxi,maChaine):             #Sinon, si c'est une radio
        return maChaine                             #On renvoie son num
    else: return False                              #Sinon, on dit que ca n'en n'est pas une
    
def Quiter():                               #On quite notre application
    sys.exit()
    
def RadioAleat(mesLignes,maxi):
    b = random.randint(1,maxi)               #On définit un nombre aléatoire
    if not IsRadio(mesLignes,maxi,b):        #Si ce n'est pas une radio, on recommence
        return RadioAleat(mesLignes,maxi)
    return b                                #On renvoie la radio

def RadioSuivante(mesLignes,maxi):
    global saveRadio
    if saveRadio == None:                               #Si c'est le choix à l'ouverture de l'application
        return maxi                                          #On retourne notre dernière radio
    else:                                               #Sinon
        if saveRadio != maxi:                               #Si on est pas sur la dernière radio
            if IsRadio(mesLignes,maxi,int(saveRadio) + 1):           #Si le num suivant est une radio
                return int(saveRadio) + 1                                #On la retourne
            else:                                               #Sinon
                saveRadio = int(saveRadio) + 1                                      #Notre radio actuelle devient la suivante
                return RadioSuivante(mesLignes,maxi)                #On retourne cette fonction
        else: return FirstRadio(mesLignes)                           #Sinon, on retourne la première radio

def RadioPrecedante(mesLignes,maxi):
    global saveRadio
    if saveRadio == None:                               #Si c'est le choix à l'ouverture de l'application
        return FirstRadio(mesLignes)                                  #On retourne notre première radio
    else:                                               #Sinon
        if saveRadio != FirstRadio(mesLignes):                        #Si on est pas sur la première radio
            if IsRadio(mesLignes,maxi,int(saveRadio) - 1):            #Si le num précédent est une radio
                return int(saveRadio) - 1                                #On la retourne
            else:                                               #Sinon
                saveRadio = int(saveRadio) - 1                                      #Notre radio actuelle devient la précédente
                return RadioPrecedante(mesLignes,maxi)                #On retourne cette fonction
        else: return maxi                                     #Sinon, on retourne la dernière radio
    
    
def ChoixRadio(mesLignes,maxi):
    maChaine = input("Choisicez votre radio : ")                        #On choisie une radio
    if not str(QuesCeQuOnFait(maChaine,mesLignes,maxi)).isdigit():       #Si c'est pas un nombre, on lui demande de rechoisir
        print("Votre choix n'est pas bon, veuillez réessayer.\n")
        return ChoixRadio(mesLignes,maxi)
    return QuesCeQuOnFait(maChaine,mesLignes,maxi)

def VousEcoutezActuellement(mesLignes,maChaine):
    for x in range(len(mesLignes)):                                                         #Pour toutes nos lignes
        if x == int(maChaine):                           #Si c'est un radio len(mesLignes[x].split(";"))>1 and
            print("Vous écoutez actuellement : " + mesLignes[x].split(";")[0].strip())      #On affiche son titre
            return

def FirstRadio(mesLignes):
    for x in range(len(mesLignes)):           #Pour toutes nos lignes
        if len(mesLignes[x].split(";"))>1:    #On retourne la première d'entre elle qui est une radio
            return x
    
main()
