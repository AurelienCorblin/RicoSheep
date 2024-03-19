import fltk


def grid(board):
    '''
    fonction graphique qui permet d'afficher la grille et les 
    buissons et herbes.
    c'est a dire qui affiche tout les objets qui ne bougent pas.
    '''
    x = 0
    y = 0
    for i in range(len(board)):
        for a in range(len(board[i])):
            fltk.rectangle(x, y, x+90, y+90, remplissage='gray')
            if board[i][a] == 'B':
                fltk.image(x, y, 'media\!bush.png', 'nw')
            elif board[i][a] == 'G':
                fltk.image(x, y, 'media\grass.png', 'nw')
            x +=90
        x = 0
        y += 90

def refresh_img(sheep, board):
    '''
    fonction graphique qui affiche les moutons selon leur coordonnes , si ils sont sur une 
    case vide un mouton simple s'affiche ,si ils sont sur une herbe ,une image de mouton 
    dans une herbe s'affiche.
    '''
    fltk.efface('sheep')
    for sheeps in sheep:
        if board[sheeps[0]][sheeps[1]] == 'G':  #verifie avec les coord du moutons si il est sur une herbe
            fltk.image(sheeps[1]*90, sheeps[0]*90, 'media\sheep_grass.png', 'nw', 'sheep')
        else:
            fltk.image(sheeps[1]*90, sheeps[0]*90, 'media\sheep.png', 'nw', 'sheep')

