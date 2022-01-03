
# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions

import matplotlib.pyplot as plt 

analiza = ctrl.Antecedent(np.arange(0, 31, 1), 'Analiza')
programowanie = ctrl.Antecedent(np.arange(0, 61, 1), 'Programowanie')
testy = ctrl.Antecedent(np.arange(0, 31, 1), 'Testy')
walidacja = ctrl.Antecedent(np.arange(0, 31, 1), 'Walidacja')

# effort
zlozonosc = ctrl.Consequent(np.arange(0, 31, 1), 'Zlozonosc')

# Auto-membership function population is possible with .automf(3, 5, or 7)
# analiza.automf(4)
analiza['BK'] = fuzz.trapmf(analiza.universe, [0, 0, 7, 10]) #'bardzo krotka'
analiza['K'] = fuzz.trapmf(analiza.universe, [7, 10, 14, 17]) #'krotka'
analiza['D'] = fuzz.trapmf(analiza.universe, [14, 17, 21, 24]) #'dluga'
analiza['BD'] = fuzz.trapmf(analiza.universe, [21, 24, 31, 31]) #'bardzo dluga'





# programowanie.automf(3)
programowanie['BK'] = fuzz.trapmf(programowanie.universe, [0, 0, 10, 15])
programowanie['K'] = fuzz.trapmf(programowanie.universe, [10, 15, 25, 30])
programowanie['D'] = fuzz.trapmf(programowanie.universe, [25, 30, 40, 45])
# programowanie['K'] = fuzz.trimf(programowanie.universe, [7, 15, 30])
# programowanie['D'] = fuzz.trimf(programowanie.universe, [14, 17, 21])
programowanie['BD'] = fuzz.trapmf(programowanie.universe, [40, 45, 55, 60])

testy['BK'] = fuzz.trapmf(testy.universe, [0, 0, 7, 10])
testy['K'] = fuzz.trapmf(testy.universe, [7, 10, 14, 17])
testy['D'] = fuzz.trapmf(testy.universe, [14, 17, 21, 24])
testy['BD'] = fuzz.trapmf(testy.universe, [21, 24, 31, 31])

walidacja['BK'] = fuzz.trapmf(walidacja.universe, [0, 0, 7, 10])
walidacja['K'] = fuzz.trapmf(walidacja.universe, [7, 10, 14, 17])
walidacja['D'] = fuzz.trapmf(walidacja.universe, [14, 17, 21, 24])
walidacja['BD'] = fuzz.trapmf(walidacja.universe, [21, 24, 31, 31])




"""
zlozonosc['S'] = fuzz.trapmf(zlozonosc.universe, [0, 0, 7, 10])
zlozonosc['M'] = fuzz.trapmf(zlozonosc.universe, [7, 10, 14, 17])
zlozonosc['L'] = fuzz.trapmf(zlozonosc.universe, [14, 17, 21, 24])
zlozonosc['XL'] = fuzz.trapmf(zlozonosc.universe, [21, 24, 31, 31])
"""

zlozonosc['S'] = fuzz.trimf(zlozonosc.universe, [0, 5, 10])
zlozonosc['M'] = fuzz.trimf(zlozonosc.universe, [5, 10, 15])
zlozonosc['L'] = fuzz.trimf(zlozonosc.universe, [10, 15, 20])
zlozonosc['XL'] = fuzz.trimf(zlozonosc.universe, [15, 20, 25])


names = ['BK', 'K', 'D', 'BD']
analiza.automf(names=names)
programowanie.automf(names=names)
testy.automf(names=names)
walidacja.automf(names=names)

names = ['S', 'M' ,'L', 'XL']
zlozonosc.automf(names=names)

"""
analiza.view()
programowanie.view()
testy.view()
walidacja.view()
zlozonosc.view()
"""

r1 = ctrl.Rule(analiza['BK'] & programowanie['BK'] & testy['BK'] & walidacja['BK'], zlozonosc['S'])
r2 = ctrl.Rule(analiza['K'] & programowanie['K'] & testy['K'] & walidacja['K'], zlozonosc['M'])
r3 = ctrl.Rule(analiza['D'] & programowanie['D'] & (testy['D'] | walidacja['D']), zlozonosc['L'])
r4 = ctrl.Rule(analiza['BD'] & programowanie['BD'] & testy['BD'] & walidacja['BD'], zlozonosc['XL'])
r5 = ctrl.Rule(analiza['K'] & programowanie['D'] & testy['D'], zlozonosc['M'])
r6 = ctrl.Rule(analiza['BD'] & programowanie['D'] & testy['D'] | walidacja['D'], zlozonosc['M'])
r7 = ctrl.Rule(analiza['D'] & programowanie['BD'] & testy['BD'] & walidacja['D'], zlozonosc['XL'])
r8 = ctrl.Rule(analiza['K'] & programowanie['D'] & testy['K'] & walidacja['K'], zlozonosc['S'])


r9 = ctrl.Rule(analiza['BK'] & programowanie['K'] & testy['K'] & walidacja['K'], zlozonosc['S'])
r10 = ctrl.Rule(analiza['K'] & programowanie['K'], zlozonosc['S'])


r11 = ctrl.Rule(analiza['K'] & programowanie['BD'], zlozonosc['XL'])
r12 = ctrl.Rule(analiza['D'] & programowanie['BD'], zlozonosc['XL'])


# r1.view()

# Control system
estimate_ctrl = ctrl.ControlSystem([  r3, r4, r6, r7,r8, r9, r10, r11])
estimate = ctrl.ControlSystemSimulation(estimate_ctrl)

estimate.input['Analiza'] = 15.5  # 0-30
estimate.input['Programowanie'] = 25 # 0-60
estimate.input['Testy'] = 5 # 0-30
estimate.input['Walidacja'] = 5 # 0-30

# Crunch the numbers
estimate.compute()

"""
Once computed, we can view the result as well as visualize it.
"""

# wynik
print('Wynik złożoność systemu:')
print(estimate.output['Zlozonosc'])
zlozonosc.view(sim=estimate)
 

plt.show() 
input("Press Enter to continue...")

 
