#!/usr/bin/env python3
# coding: utf-8

"""
Genreation of performance's curves
"""

import matplotlib.pyplot as plt
import numpy as np
from math import log2
import time
import generate as gen
import main as mn
import sys

STEP = 1000

def constant1_fct() :
    return 1

def identity_fct(x) :
    return x

def square_fct(x) :
    return x**2

def cube_fct(x) :
    return x**3

def log2_fct(x) :
    return log2(x)

def get_problem_length() :
    length = int(input("Entrez le nombre de point voulu pour le probleme ( >= 6 ) : "), 10)
    while length < 6 :
        length = int(input("Ce nombre n'est pas valide, veuillez en entrer un autre ( >= 6 ) : "))
    return length

def get_number_step() :
    step = int(input(f'Entrez le nombre de pas voulus pour le probleme (taille du pas : {STEP}) : '), 10)
    while step < 6 :
        step = int(input("Ce nombre n'est pas valide, veuillez en entrer un autre  : "))
    return step

def draw_perf() :
    lenght = get_problem_length()
    
    x = []
    f0 = []
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    
    t0 = []
    
    for i in range(6, lenght+1) :
        plt.xlabel("Taille de l'entree")
        plt.ylabel("Temps d'execution en sec")
        x.append(i)
        
        gen.generate_complex(gen.create_points(i))
        start0 = time.time_ns()
        mn.main("test.poly")
        end0 = time.time_ns()
        t0.append((end0 - start0)*1E-9)
        plt.plot(x, t0, 'black')
        
        #f0.append(constant1_fct())
        #plt.plot(x, f0, 'r')

        # f1.append(identity_fct(i))
        # plt.plot(x, f1, 'b')
        
        #f2.append(square_fct(i))
        #plt.plot(x, f2, 'r')
        
        #f3.append(cube_fct(i))
        #plt.plot(x, f3, 'o')
        
        # f4.append(log2_fct(i))
        # plt.plot(x, f4, 'g')
        
        plt.pause(0.00001)
    plt.show()
    
def get_perf() :
    length = get_problem_length()
    gen.generate_complex(gen.create_points(length))
    start0 = time.time_ns()
    mn.main("test.poly")
    end0 = time.time_ns()
    print("Runtime :", (end0 - start0)*1E-9, "sec")

def draw_smooth() :
    nb_steps = get_number_step()
    
    x = []
    fx = []
    
    for i in range(6, STEP*nb_steps + 7, STEP) :
        print("Valeur de i : ", i)
        x.append(i)
        gen.generate_complex(gen.create_points(i))
        start0 = time.time_ns()
        mn.main("test.poly")
        end0 = time.time_ns()
        fx.append((end0 - start0)*1E-9) 
    plt.xlabel("Taille de l'entree")
    plt.ylabel("Temps d'execution en sec")
    plt.plot(x, fx, "black")
    plt.show()

def main() :
    if sys.argv[1] == "one" :
        get_perf()
    elif sys.argv[1] == "draw":
        draw_perf()
    elif sys.argv[1] == "smooth":
        draw_smooth()
    else :
        print("Veuillez entrer un parametre valide")
        
if __name__ == '__main__' :
    main()
    