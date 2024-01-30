#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from tycat import read_instance

from geo.segment import Segment
from geo.point import Point


def fusion(tab1, tab2):
    """
    fusionne les deux tableaux deja ordonnes en un nouveau tableau ordonne
    """

    i = 0
    j = 0
    tab_ordonne = []
    while i != len(tab1) and j != len(tab2):
        if tab1[i][1] < tab2[j][1]:
            tab_ordonne.append(tab1[i])
            i += 1
        else:
            tab_ordonne.append(tab2[j])
            j += 1
    
    if i < len(tab1):
        tab_ordonne = tab_ordonne + tab1[i:]
    
    if j < len(tab2):
        tab_ordonne = tab_ordonne + tab2[j:]


    return tab_ordonne


def tri_fusion(tab):
    """
    trie tab
    la comparaison < doit etre définie sur les objets dans tab
    """

    if len(tab) == 0:
        return  []

    if len(tab) == 1:
        return [tab[0]]
    
    milieu = len(tab) // 2
    tab_gauche = tri_fusion(tab[:milieu])
    tab_droite = tri_fusion(tab[milieu:])
    return fusion(tab_gauche, tab_droite)


def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    if len(polygones) == 0:
        return []
    
    #vecteur d'inclusion
    sortie = [-1 for _ in range(len(polygones))]

    #trie les polygones par aire croissante
    polygones_indices = [(i, pol) for i, pol in enumerate(polygones)]
    polygones_tries = tri_fusion(polygones_indices)
    ### print(polygones_tries)
    for i, pol1 in enumerate(polygones_tries):
        #on trace un segment entre un sommet du polygone et un point en dehors aligne verticalement
        segment = Segment([Point([pol1[1].points[0].coordinates[0], 0.0]), pol1[1].points[0]])
        intersections = []
        for pol2 in polygones_tries[i+1:]:
            #compte le nombre de segment du polygone intersecte
            count = 0
            for seg in pol2[1].segments():
                inter = segment.intersection_with(seg)
                if inter and inter not in intersections:
                    count += 1
                    intersections.append(inter)
                    ### print("Intersection", pol1[0], "and", pol2[0], "at :", inter)

            #si pol1 est inclu dans pol2 on passe au prochain polygone
            if count % 2 == 1:
                sortie[pol1[0]] = pol2[0]
                break
        
    return sortie


def main(string):
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    if string == "" :
        for fichier in sys.argv[1:]:
            polygones = read_instance(fichier)
            inclusions = trouve_inclusions(polygones)
            ### print(inclusions)
    else :
        polygones = read_instance(string)
        inclusions = trouve_inclusions(polygones)
        ### print(inclusions)

if __name__ == "__main__":
    main("")
