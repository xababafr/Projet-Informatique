## fonction qui affiche une map

def afficher_map(MAP):
    for ligne in MAP:
        for c in ligne:
            print(c,end='')
        print('')
        
# faire une classe map, qui permet de l'afficher, recuperer les informations à telle ou telle case, 
# ec.... sachant qu'il faudra une deuxieme "epaisseur" pour gérer la position des animaux        

M = [
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103',
    '00011203000103'
]

afficher_map(M)