#!/usr/bin/env python3
# coding: utf-8

"""
Genreation of problem depending on parameters
"""

from matplotlib.pyplot import *
import random as rd
import sys

PROBA_SPLIT = 0.1
NUMBER_SPLIT = [2,3,4]
NUM_POLYGON = 0
FILE_NAME = "test.poly"
            
def point_segment(P1,P2,P) :
    return (P2[0]-P1[0])*(P[1]-P1[1])-(P2[1]-P1[1])*(P[0]-P1[0])>0

def sort_key(tab, idx) :
    assert ( 0 <= idx <= 1)  # 0 represent x, 1 represent y 
    def cle(P):
        return P[idx]
    tab.sort(key=cle)

def radix_sort(tab) :
    """
    Radix sort, first on y then on x 
    """
    sort_key(tab, 1)
    sort_key(tab, 0)

def enveloppe_convexe(points):
    radix_sort(points)
    N = len(points)
    enveloppe = [points[0],points[1]]
    for i in range(2,N):
        enveloppe.append(points[i])
        valide = False
        while not(valide) and len(enveloppe)>2:
            P3 = enveloppe.pop()
            P2 = enveloppe.pop()
            P1 = enveloppe.pop()
            if point_segment(P1,P2,P3):
                enveloppe.append(P1)
                enveloppe.append(P3)
            else:
                enveloppe.append(P1)
                enveloppe.append(P2)
                enveloppe.append(P3)
                valide = True
    enveloppe.append(points[N-2])
    for i in range(N-3,-1,-1):
        enveloppe.append(points[i])
        valide = False
        while not(valide) and len(enveloppe)>2:
            P3 = enveloppe.pop()
            P2 = enveloppe.pop()
            P1 = enveloppe.pop()
            if point_segment(P1,P2,P3):
                enveloppe.append(P1)
                enveloppe.append(P3)
            else:
                enveloppe.append(P1)
                enveloppe.append(P2)
                enveloppe.append(P3)
                valide = True
    return enveloppe

def create_points(n) :
    """
    Create n points randomly 
    """ 
    global FILE_NAME
    global NUM_POLYGON
    NUM_POLYGON = 0
    
    with open(FILE_NAME, 'w', encoding="utf8") as file :
        file.close()
    
    taille = 100
    points = []
    for i in range(n) :
        points.append([rd.random()*taille,rd.random()*taille])
    return points

def generate_complex(points) :
    global NUM_POLYGON
    global PROBA_SPLIT
    global NUMBER_SPLIT
    global FILE_NAME
    
    while points != [] :
        if len(points) <= 2 :
            break 
        do_split = rd.random()
        if do_split <= PROBA_SPLIT :
            nb = rd.randint(0,len(NUMBER_SPLIT) - 1)
            sort_key(points, rd.randint(0,1))
            step = len(points)//NUMBER_SPLIT[nb] 
            for i in range(0, NUMBER_SPLIT[nb]) :
                temp_points = []
                for _ in range(0,step) :
                    temp_points.append(points.pop(0))
                generate_complex(temp_points)
        else : 
            with open(FILE_NAME, 'a', encoding="utf8") as file :
                env = enveloppe_convexe(points)
                for i in range(0, len(env)-1) :
                    file.write(f"{NUM_POLYGON} {env[i][0]} {env[i][1]}\n")
                NUM_POLYGON += 1
                while len(env) != 1 :
                    elem = env.pop(0)
                    points.remove(elem)
                file.close()
    
def generate_simple(points) :
    """
    Generate a simple compositions of polygons
    """
    global NUM_POLYGON
    global FILE_NAME
    with open(FILE_NAME, 'a', encoding="utf8") as file :
        while points != [] :
            if len(points) <= 2 :
                break 
            env = enveloppe_convexe(points)
            for i in range(0, len(env)-1) :
                file.write(f"{NUM_POLYGON} {env[i][0]} {env[i][1]}\n")
            NUM_POLYGON += 1
            while len(env) != 1 :
                elem = env.pop(0)
                points.remove(elem)
        file.close()
        
def main() :
    N = int(input("Combien de points ? "))
    points = create_points(N)
    if sys.argv[1] == "complex" :
        generate_complex(points)
    elif sys.argv[1] == "simple" :
        generate_simple(points)
    else : 
        print("Veuillez entrer un parametre valide")

if __name__ == '__main__' :
    main()        
        