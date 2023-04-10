# %%
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import math

# %% [markdown]
# ### Knapsack Problem

# %%
!pip install -q pyomo
!apt-get install -y -qq glpk-utils

# %%
from pyomo.environ import *

# %% [markdown]
# 1. Model the above problem as a LP.
# 2. Consider a specific instance of the problem with N = 3 and W = 4 Let v = (2,3,4) and w = (5,20,3) Use Pyomo to obtain the optimal solution

# %%
model = ConcreteModel()

# Declare decision variables
model.x1 = Var(domain = NonNegativeReals) # First Good
model.x2 = Var(domain = NonNegativeReals) # Second Good
model.x3 = Var(domain = NonNegativeReals) # Third Good

# Declare Objective
model.profit = Objective(expr = 2 * model.x1 + 3 * model.x2 + 4 * model.x3, sense = maximize)

# Declare Constraints
model.capacity_limit = Constraint(expr = 5 * model.x1 + 20 * model.x2 + 3 * model.x3 <= 4)
model.total_limit1 = Constraint(expr = model.x1 <= 1)
model.total_limit2 = Constraint(expr = model.x2 <= 1)
model.total_limit3 = Constraint(expr = model.x3 <= 1)

model.pprint()


# %%
SolverFactory('glpk', executable='/usr/bin/glpsol').solve(model).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x1 = ', model.x1())
print('x2 = ', model.x2())
print('x3 = ', model.x3())

print('\nConstraints')
print('Capacity Limit = ', model.capacity_limit())
print('Total Limit1 = ', model.total_limit1())
print('Total Limit2 = ', model.total_limit2())
print('Total Limit3 = ', model.total_limit3())


# %% [markdown]
# 3. Which constraints are tight/binding ?
# 
#   When inequalities be satisfies with equality, the constraint is tight. Hence, in this case, the capacity limit contraint and total limit 3 constraint is tight.

# %% [markdown]
# 4. Suppose a crime syndicate wants to buy out the thief. They offer to pay the thief a price y1 for the gold, a price y2 for the diamonds, a price y3 for the silver, and a price y4 per lb for the knapsack. The syndicate wants to minimize the price it pays for the goods. What is the solution for this problem. What is the connection to the previous problem ? (Assume the thief hasn't stole anything)
# 
#   The solution is listed as following, (y1, y2, y3, y4) = (0, 0, 2.8, 0.4), profit = 4.4. It's not hard to observe that the profit is as same as the first part, which is an example of duality.

# %%
model = ConcreteModel()

# Declare decision variables
model.y1 = Var(domain = NonNegativeReals) # First Good Price
model.y2 = Var(domain = NonNegativeReals) # Second Good Price
model.y3 = Var(domain = NonNegativeReals) # Third Good Price
model.y4 = Var(domain = NonNegativeReals) # Per LB in knapsack

# Declare Objective
model.profit = Objective(expr = model.y1 + model.y2 + model.y3 + 4 * model.y4, sense = minimize)

# Declare Constraints
model.dual_1 = Constraint(expr = model.y1 + 5 * model.y4 >= 2)
model.dual_2 = Constraint(expr = model.y2 + 20 * model.y4 >= 3)
model.dual_3 = Constraint(expr = model.y3 + 3 * model.y4 >= 4)

model.pprint()


# %%
SolverFactory('glpk', executable='/usr/bin/glpsol').solve(model).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('y1 = ', model.y1())
print('y2 = ', model.y2())
print('y3 = ', model.y3())
print('y4 = ', model.y4())

print('\nConstraints')
print('dual_1 = ', model.dual_1())
print('dual_2 = ', model.dual_2())
print('dual_3 = ', model.dual_3())

# %% [markdown]
# 5. Discussion Point
# 
#     (a) The above instance had a unique optimum solution. Will this be true for all instances of the knapsack problem?
# 
#     The uniqueness of the optimal solution depends on the specific instance of the Knapsack problem, i.e. the specific set of items and constraints. So it may not always be the case.
#   
#     (b) What happens if we remove the constraint x ≥ 0 in the first part?
#   
#     Removing the constraint will allow decision variable to take negative values, which does not make sense in the context of this question. (fraction of goods)
#   
#     (c) Can you list some more feasible solutions to this LP?
#   
#     (x1, x2, x3) = (0.5, 0, 0.5)
#     (x1, x2, x3) = (0.1, 0.1, 0.5)
# 
#     (d)Can you think of more realistic applications for the knapsack problem?
# 
#     It can be used for resource allocation when there is just limited amount of resource in the company. In addition, It can be used to logistics and inventory management, where goods or items need to be transported or stored in a limited space or with a limited carrying capacity.
# 
#     (e)Why might it be practically important that only one good is chosen fractionally?
#   
#     - Feasibility: It's possible that the fractional parts of multiple items can combine to form a weight that is not a multiple of any item's weight, making it impossible to completely fill(optimize) the knapsack.
#     - Real-world constraints: It may be impractical to have fractional quantities of items in real world. 
# 
# 
# 
# 
# 
# 


