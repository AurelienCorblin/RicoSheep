import fltk
import graphic
import time
import sys


sys.setrecursionlimit(10000)

                                    ##### variables #####
                                    
map = {'huge1' : 'maps\huge\Big1.txt', 'huge2' : 'maps\huge\huge.txt', 'square1' : 'maps\square\map2.txt', 'square2' : 'maps\square\map3.txt', 
'wide1' : 'maps\wide\wide2.txt', 'wide2' : 'maps\wide\wide4.txt', 'theme1' : 'maps\Theme\one_sheep.txt', 'theme2' : 'maps\Theme\onegrass.txt'}
ricosheep = True
menuPrincipal = True
menuGridChoice = False
menuHuge = False
menuSquare = False
menuWide = False
menuTheme = False
game = False
play = False
solver = False
visite = set()
saveCoord = []
fichier = 'maps\!test.txt'
                                    ###### functions ######

def jouer(plateau, moutons, direction):
    '''
    fonction qui permet de deplacer les moutons ensemble dans une direction choisi par 
    le joueur.

    :param plateau: list, liste de liste representant le jeu
    :param moutons: list, liste des coordonnees des moutons
    :param direction: str, direction dans laquelle le joueur veut envoyer les moutons

    >>>plateau = [[None, 'B' , None, 'B' , None],
    ['B' , 'B' , None, None, None],
    [None, 'G' , 'B' , 'B' , None],
    [None, 'B' , 'G' , None, None],
    [None, None, None, 'B' , None]]
    >>>moutons = [(0,4), (1,3), (2,4), (4,4)]

    >>>jouer(plateau, moutons, 'Left')
    >>>print(moutons)
    [(0, 4),(1, 2),(2, 4),(4, 4)]

    >>>jouer(plateau, moutons, 'Down')
    >>>print(moutons)
    [(1, 3),(2, 4),(3, 4),(4, 4)]
    '''
    moutons.sort()
    if direction == 'Left':
        for i in range(len(moutons)):
            while plateau[moutons[i][0]][moutons[i][1]-1] != 'B' and moutons[i][1]-1 >= 0 and (moutons[i][0], moutons[i][1]-1) not in moutons:
                x, y = moutons[i]
                moutons.remove(moutons[i])
                moutons.insert(i, (x, y-1))

    elif direction == 'Up':
        for i in range(len(moutons)):
            while plateau[moutons[i][0]-1][moutons[i][1]] != 'B' and moutons[i][0] > 0 and (moutons[i][0]-1, moutons[i][1]) not in moutons:
                x, y = moutons[i]
                moutons.remove(moutons[i])
                moutons.insert(i, (x-1, y))   

    elif direction == 'Right':
        moutons.reverse()
        for i in range(len(moutons)):
            while moutons[i][1]+1 < len(plateau[0]) and plateau[moutons[i][0]][moutons[i][1]+1] != 'B' and  (moutons[i][0], moutons[i][1]+1) not in moutons:
                x, y = moutons[i]
                moutons.remove(moutons[i])
                moutons.insert(i, (x, y+1))

    elif direction == 'Down':
        moutons.reverse()
        for i in range(len(moutons)):
            while moutons[i][0]+1 < len(plateau) and plateau[moutons[i][0]+1][moutons[i][1]] != 'B' and  (moutons[i][0]+1, moutons[i][1]) not in moutons:
                x, y = moutons[i]
                moutons.remove(moutons[i])
                moutons.insert(i, (x+1, y))
    moutons.sort()

def victoire(plateau, moutons):
    '''
    fonction qui permet de detecter si le joueur a gagner 
    selon la position des moutons.

    :param plateau: list, liste de liste representant le jeu
    :param moutons: list, liste des coordonnees des moutons

    >>>plateau = [[None, 'B' , None, 'B' , None],
    ['B' , 'B' , None, None, None],
    [None, 'G' , 'B' , 'B' , None],
    [None, 'B' , 'G' , None, None],
    [None, None, None, 'B' , None]]
    >>>moutons = [(0,4), (2,1), (3,2), (4,4)]
    >>>victoire(plateau, moutons)
    True

    >>>moutons2 = [(0,4), (2,0), (3,2), (4,4)]
    >>>victoire(plateau, moutons2)
    None
    '''
    grass = 0
    sheepOnGrass = 0
    for i in range(len(plateau)):
        for a in range(len(plateau[i])):
            if plateau[i][a] == 'G':
                grass +=1
    for mouton in moutons:
        if plateau[mouton[0]][mouton[1]] == 'G':
            sheepOnGrass += 1
    if sheepOnGrass == grass or sheepOnGrass == len(moutons):  #2 eme partie du if sert si il y a plus d'herbe que de mouton
        return True

def charger(fichier):
    '''
    fonction qui recupere un fichier texte pour en recuperer
    le plateau de jeu ainsi que la position des moutons qui 
    sont renvoyer dans une liste de liste pour le plateau et 
    une liste de tuples pour les moutons.

    :param fichier: str, chaine de caractere qui donne le chemin d'acces vers le fichier txt.

    >>>fichier = 'maps\square\map2.txt'
    >>>charger(fichier)
    [[None, 'B' , None, 'B' , None],['B' , 'B' , None, None, None],[None, 'G' , 'B' , 'B' , None],[None, 'B' , 'G' , None, None],[None, None, None, 'B' , None]], [(0,4), (1,3), (2,4), (4,4)]
    '''

    pl = []
    m = []
    l =0
    file = open(fichier, "r")
    line = file.readline()
    oldline = len(line)-1  #-1 a cause du caractere non visible a la fin de la ligne
    while line:
        a = []
        for i in range(len(line)):
            if line[i] == '_':
                a.append(None)
            elif line[i] == 'B':
                a.append('B')
            elif line[i] == 'G':
                a.append('G')
            elif line[i] == 'S':
                a.append(None)
                m.append((l, i))
            
        pl.append(a)
        l+=1

        if oldline != len(a):
            print('mauvais format')
            return None
        oldline = len(a)

        line = file.readline()
    file.close()
    return pl, m


def solveur(plateau, moutons, visite):
    '''
    fonction qui recoit le plateau de jeu la liste des 
    coordonnees des moutons et un set pour stoker les etats 
    par lesquelles on est passer.
    la fonction renvoie une liste de direction qui nous 
    permet de gagner le jeu.
    '''
    if victoire(plateau, moutons) == True:
        return []
    if tuple(moutons) in visite:
        return None
    visite.add(tuple(moutons))
    copySheep = tuple(moutons)
    saveCoord.append(copySheep)
    jouer(plateau, moutons, 'Left')
    res = solveur(plateau, moutons, visite)
    if res is not None:
        return ['Left'] + res
    else:
        moutons = list(saveCoord[-1])
    jouer(plateau, moutons, 'Right')
    res = solveur(plateau, moutons, visite)
    if res is not None:
        return ['Right'] + res
    else:
        moutons = list(saveCoord[-1])
    jouer(plateau, moutons, 'Down')
    res = solveur(plateau, moutons, visite)
    if res is not None:
        return ['Down'] + res
    else:
        moutons = list(saveCoord[-1])
    jouer(plateau, moutons, 'Up')
    res = solveur(plateau, moutons, visite)
    if res is not None:
        return ['Up'] + res
    else:
        moutons = list(saveCoord[-1])
    saveCoord.pop(-1)
    return None

                                    #### principal program ####
###########################################################################################################
                                    ########## menu ##########

while ricosheep:
    fltk.cree_fenetre(700, 500)
    while menuPrincipal:  # menu principal pour lancer avec ou sans solveur
        fltk.image(350, 250, 'media\!background.png')
        fltk.rectangle((700//2)-(700*0.15), (500//2)-(500*0.08), (700//2)+(700*0.15), (500//2)+(500*0.08), remplissage='Salmon')
        fltk.texte((700//2), (500//2), 'PLAY', ancrage='center')
        fltk.image(30, 500-30, 'media\exit.png')
        if solver:
            fltk.texte(650, 480, 'solver', couleur='green', ancrage='center', tag='solver')
        else:
            fltk.texte(650, 480, 'solver', couleur='red', ancrage='center', tag='solver')
        x, y = fltk.attend_clic_gauche()
        if x>(700//2)-(700*0.15) and x<(700//2)+(700*0.15) and y>(500//2)-(500*0.08) and y<(500//2)+(500*0.08):
            menuPrincipal = False
            menuGridChoice = True
            #game = True  #pour tester une grille manuellement depuis la variable 'fichier'(et mettre en com ligne juste au dessus)
        if x>5 and x<55 and y>500-55 and y<500-5:
            menuPrincipal = False
            ricosheep = False
        if x>600 and x<700 and y>460 and y<500:
            solver = not solver

        fltk.efface_tout()

    while menuGridChoice:  # menu pour choisir la categorie de grille que l'on veut
        fltk.image(350, 250, 'media\!background.png')
        fltk.image(30, 500-30, 'media\exit.png')
        fltk.rectangle(225, 5, 475, 105, remplissage='Salmon')
        fltk.texte(350, 55, 'huge', ancrage='center')
        fltk.rectangle(225, 110, 475, 210, remplissage='Salmon')
        fltk.texte(350, 160, 'square', ancrage='center')
        fltk.rectangle(225, 215, 475, 315, remplissage='Salmon')
        fltk.texte(350, 265, 'wide', ancrage='center')
        fltk.rectangle(225, 320, 475, 420, remplissage='Salmon')
        fltk.texte(350, 370, 'theme', ancrage='center')
        x, y = fltk.attend_clic_gauche()
        if x>5 and x<55 and y>500-55 and y<500-5:
            menuGridChoice = False
            menuPrincipal = True
        if x>225 and x<475 and y>5 and y<105:
            menuHuge = True
            menuGridChoice = False
        if x>225 and x<475 and y>110 and y<210:
            menuSquare = True
            menuGridChoice = False
        if x>225 and x<475 and y>215 and y<315:
            menuWide = True
            menuGridChoice = False
        if x>225 and x<475 and y>320 and y<420:
            menuTheme = True
            menuGridChoice = False

        fltk.efface_tout()

    while menuHuge:
        fltk.image(350, 250, 'media\!background.png')
        fltk.image(30, 500-30, 'media\exit.png')
        fltk.image(220, 250, 'media\huge1.png')
        fltk.image(480, 250, 'media\huge2.png')
        x, y = fltk.attend_clic_gauche()
        if x>5 and x<55 and y>500-55 and y<500-5:
            menuHuge = False
            menuGridChoice = True
        if x>95 and x<345 and y>125 and y<375:
            menuHuge = False
            fichier = map['huge1']
            game = True
        if x>355 and x<605 and y>125 and y<375:
            menuHuge = False
            fichier = map['huge2']
            game = True

        fltk.efface_tout()
    while menuSquare:
        fltk.image(350, 250, 'media\!background.png')
        fltk.image(30, 500-30, 'media\exit.png')
        fltk.image(220, 250, 'media\square1.png')
        fltk.image(480, 250, 'media\square2.png')
        x, y = fltk.attend_clic_gauche()
        if x>5 and x<55 and y>500-55 and y<500-5:
            menuSquare = False
            menuGridChoice = True
        if x>95 and x<345 and y>125 and y<375:
            menuSquare = False
            fichier = map['square1']
            game = True
        if x>355 and x<605 and y>125 and y<375:
            menuSquare = False
            fichier = map['square2']
            game = True

        fltk.efface_tout()
    while menuWide:
        fltk.image(350, 250, 'media\!background.png')
        fltk.image(30, 500-30, 'media\exit.png')
        fltk.image(350, 170, 'media\wide1.png')
        fltk.image(350, 330, 'media\wide2.png')
        x, y = fltk.attend_clic_gauche()
        if x>5 and x<55 and y>500-55 and y<500-5:
            menuWide = False
            menuGridChoice = True
        if x>175 and x<525 and y>95 and y<245:
            menuWide = False
            fichier = map['wide1']
            game = True
        if x>175 and x<525 and y>255 and y<405:
            menuWide = False
            fichier = map['wide2']
            game = True

        fltk.efface_tout()
    while menuTheme:
        fltk.image(350, 250, 'media\!background.png')
        fltk.image(30, 500-30, 'media\exit.png')
        fltk.image(220, 250, 'media\!theme1.png')
        fltk.image(480, 250, 'media\!theme2.png')
        x, y = fltk.attend_clic_gauche()
        if x>5 and x<55 and y>500-55 and y<500-5:
            menuTheme = False
            menuGridChoice = True
        if x>95 and x<345 and y>125 and y<375:
            menuTheme = False
            fichier = map['theme1']
            game = True
        if x>355 and x<605 and y>125 and y<375:
            menuTheme = False
            fichier = map['theme2']
            game = True

        fltk.efface_tout()


###########################################################################################################
                                    ########## game ##########
    while game:
        if charger(fichier) != None:
            board, sheep = charger(fichier)
        else:  # si la grille n'a pas un bon format le jeu renvoie au menu principal (+ un message dans le terminal venant de la fonction charger)
            game = False
            menuPrincipal = True
            break

        fltk.ferme_fenetre()
        width = len(board[0]) * 90  # comme les images font 90px sur 90px on cree une fenetre en fonction de leur taille
        length = len(board) * 90
        fltk.cree_fenetre(width, length)
        graphic.grid(board)
        graphic.refresh_img(sheep, board)

        if solver == True:  # si le solveur est activer le solveur s'executera sur la grille
            s = solveur(board, sheep, visite)
            print(s)
            if s != None:
                for elem in s:
                    ev = fltk.donne_ev()
                    ty = fltk.type_ev(ev) 
                    if ty == 'Touche':
                        if fltk.touche(ev) == 'Escape':
                            break
                    jouer(board, sheep, elem)
                    graphic.refresh_img(sheep, board)
                    fltk.mise_a_jour()
                    time.sleep(0.2)
            fltk.attend_ev()
            menuPrincipal = True
            game = False
        else:
            play = True
        
        while play == True:
            ev = fltk.donne_ev()
            ty = fltk.type_ev(ev)  # on recupere les touches sur lesquelles on appuies 
            if ty == 'Quitte':
                game = False
                play = False
                ricosheep = False
            if ty == 'Touche':
                if fltk.touche(ev) == 'r':
                    break
                elif fltk.touche(ev) == 'Escape':
                    game = False
                    play = False
                    menuGridChoice = True
                jouer(board, sheep, fltk.touche(ev))
                graphic.refresh_img(sheep, board)
            if victoire(board, sheep):
                fltk.rectangle((width//2)-(width*0.1), (length//2)-(length*0.05), (width//2)+(width*0.1), (length//2)+(length*0.05), remplissage='yellow')
                fltk.texte(width//2, length//2, 'WIN', 'green', 'center', taille=30)
                game = False
                play = False
                menuPrincipal = True
                fltk.attend_ev()
            fltk.mise_a_jour()
    fltk.ferme_fenetre()
