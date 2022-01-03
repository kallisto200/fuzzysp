"""
==========================================
Fuzzy Control Systems
==========================================
 

We can use the `skfuzzy` control system API to model this.  First, let's
define fuzzy variables
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

import matplotlib.pyplot as plt 

# New Antecedent/Consequent objects hold universe variables and membership
# functions
 
def StoryPointsEstimate():

 print('Niepewność:')
uncertainty= float(input())
print('Złożoność:')
complexity= float(input())
print('Nakład pracy:')
workeffort = float(input())
 

niepewnosc = ctrl.Antecedent(np.arange(0, 11, 1), 'Niepewność') # Uncertainty
names = ['niska', 'wysoka']
niepewnosc.automf(names=names)
niepewnosc.view()
"""
.. image:: PLOT2RST.current_figure
"""


zlozonosc = ctrl.Antecedent(np.arange(0, 11, 1), 'Złożoność') # Complexity
names = ['niska', 'średnia', 'wysoka']
zlozonosc.automf(names=names)
zlozonosc.view()
"""
.. image:: PLOT2RST.current_figure
"""

nakladpracy = ctrl.Antecedent(np.arange(0, 11, 1), 'Nakład pracy') # Amount of Work
names = ['niski', 'średni', 'wysoki']
nakladpracy.automf(names=names)
nakladpracy.view()
"""
.. image:: PLOT2RST.current_figure
"""


# Auto-membership function population is possible with .automf(3, 5, or 7)
# niepewnosc.automf(3)
# zlozonosc.automf(3)
# nakladpracy.automf(3)


# Custom membership functions can be built interactively with a familiar,
# Pythonic API
# points['low'] = fuzz.trimf(points.universe, [0, 0, 13])
# points['medium'] = fuzz.trimf(points.universe, [0, 13, 25])
# points['high'] = fuzz.trimf(points.universe, [13, 25, 25])

"""
points = ctrl.Consequent(np.arange(0, 11, 1), 'points') # Story points
points['vlow'] = fuzz.trapmf(points.universe, [0, 0, 1, 3])
points['low'] = fuzz.trimf(points.universe, [1, 3, 4])
points['medium'] = fuzz.trimf(points.universe, [2, 3, 5])
points['high'] = fuzz.trimf(points.universe, [3, 5, 8])
points['vhigh'] = fuzz.trapmf(points.universe, [5, 8, 10, 10])
"""

points = ctrl.Consequent(np.arange(0, 16, 1), 'points') # Story points

points['vlow'] = fuzz.trapmf(points.universe, [0, 0, 1, 3])
points['low'] = fuzz.trimf(points.universe, [1, 3, 5])
points['medium'] = fuzz.trimf(points.universe, [3, 5, 8])
points['high'] = fuzz.trimf(points.universe, [5, 8, 13])
points['vhigh'] = fuzz.trapmf(points.universe, [8, 13, 15, 15])

"""
To help understand what the membership looks like, use the ``view`` methods.
"""

# You can see how these look with .view()
# niepewnosc['average'].view()

points.view()
"""
.. image:: PLOT2RST.current_figure


Fuzzy rs
-----------

Now, to make these triangles useful, we define the *fuzzy relationship*
between input and output variables. For the purposes of our example, consider
three simple rs:

1. If the food is poor OR the service is poor, then the tip will be low
2. If the service is average, then the tip will be medium
3. If the food is good OR the service is good, then the tip will be high.

Most people would agree on these rs, but the rs are fuzzy. Mapping the
imprecise rs into a defined, actionable tip is a challenge. This is the
kind of task at which fuzzy logic excels.
"""

r1 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['niska'] & nakladpracy['niski'], points['vlow'])
r2 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['niska'] & nakladpracy['średni'], points['low'])
r3 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['niska'] & nakladpracy['wysoki'], points['high'])

r4 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['średnia'] & nakladpracy['niski'], points['low'])
r5 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['średnia'] & nakladpracy['średni'], points['medium'])
r6 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['średnia'] & nakladpracy['wysoki'], points['high'])

r7 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['wysoka'] & nakladpracy['niski'], points['low'])
r8 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['wysoka'] & nakladpracy['średni'], points['medium'])
r9 = ctrl.Rule(niepewnosc['niska'] & zlozonosc['wysoka'] & nakladpracy['wysoki'], points['high'])


r10 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['niska'] & nakladpracy['niski'], points['vlow'])
r11 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['niska'] & nakladpracy['średni'], points['low'])
r12 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['niska'] & nakladpracy['wysoki'], points['high'])

r13 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['średnia'] & nakladpracy['niski'], points['low'])
r14 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['średnia'] & nakladpracy['średni'], points['medium'])
r15 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['średnia'] & nakladpracy['wysoki'], points['high'])

r16 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['wysoka'] & nakladpracy['niski'], points['medium'])
r17 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['wysoka'] & nakladpracy['średni'], points['high'])
r18 = ctrl.Rule(niepewnosc['wysoka'] & zlozonosc['wysoka'] & nakladpracy['wysoki'], points['vhigh'])



#r2 = ctrl.Rule(zlozonosc['average'], points['medium'])
#r3 = ctrl.Rule(zlozonosc['good'] | niepewnosc['good'], points['high'])

r1.view()

"""
.. image:: PLOT2RST.current_figure

Control System Creation and Simulation
---------------------------------------

Now that we have our rs defined, we can simply create a control system
via:
"""

estimate_ctrl = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9,
r10, r11, r12, r13, r14, r15, r16, r17, r18])
#points_ctrl = ctrl.ControlSystem([r1, r2, r3])

"""
In order to simulate this control system, we will create a
``ControlSystemSimulation``.
"""

estimate = ctrl.ControlSystemSimulation(estimate_ctrl)

"""
We can now simulate our control system by simply specifying the inputs
and calling the ``compute`` method.  
Suppose we rated the uncertainty 6.5 out of 10 and the service 9.8 of 10.
"""
# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
# 1-10

#Uncertainty
estimate.input['Niepewność'] = uncertainty 
#Complexity
estimate.input['Złożoność'] = complexity
#Work effort
estimate.input['Nakład pracy'] = workeffort 

# Crunch the numbers
estimate.compute()

"""
Once computed, we can view the result as well as visualize it.
"""
result = estimate.output['points']
print('Defuzzyfication point: ' + str(result))
points.view(sim=estimate)
 
value = 0
percent=0.2
if result < 1+1*percent:
  value = 1
elif result < 3+3*percent:
   value = 3
elif result < 5+5*percent:
   value = 5
elif result < 8+8*percent:
   value = 8
else:
  value = 13
  
print("Story point = " + str(value))

plt.show() 
input("Press Enter to continue...")


"""
.. image:: PLOT2RST.current_figure

The resulting suggested tip is **20.24%**.

Final thoughts
--------------

The power of fuzzy systems is allowing complicated, intuitive behavior based
on a sparse system of rs with minimal overhead. Note our membership
function universes were coarse, only defined at the integers, but
``fuzz.interp_membership`` allowed the effective resolution to increase on
demand. This system can respond to arbitrarily small changes in inputs,
and the processing burden is minimal.

"""
