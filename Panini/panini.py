import itertools
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

users = ['Alice', 'Mauro', 'Roberto', 'Chiara', 'Luca', 'Paola']

assets = ['panino', 'pizza', 'tramezzino', 'hamburger', 'yogurt', 'pesca', 'banana', 'mela', 'acqua', 'succo',
          'energy drink', 'caffe', 'ciambella', 'cioccolato', 'cornetto', 'gelato']
categories = [assets[4 * i: 4 * (i + 1)] for i in range(4)]

q_vals = np.array([4, 5, 3, 2, 3, 5, 6, 4, 9, 7, 2, 4, 5, 10, 5, 3])
quantities = {a_i: q_i for a_i, q_i in zip(assets, q_vals)}

preferences = {(u_i, a_i): 0 for u_i, a_i in itertools.product(users, assets)}
preferences.update({
    ('Alice', 'panino'): 1, ('Alice', 'pizza'): 2,
    ('Mauro', 'tramezzino'): 3, ('Mauro', 'panino'): 2,
    ('Roberto', 'tramezzino'): 2, ('Roberto', 'hamburger'): 1,
    ('Chiara', 'pizza'): 2, ('Chiara', 'hamburger'): 3,
    ('Luca', 'panino'): 3, ('Luca', 'hamburger'): 2,
    ('Paola', 'pizza'): 4, ('Paola', 'tramezzino'): 1,

    ('Alice', 'yogurt'): 2, ('Alice', 'pesca'): 3,
    ('Mauro', 'banana'): 2, ('Mauro', 'mela'): 4,
    ('Roberto', 'banana'): 1, ('Roberto', 'yogurt'): 2,
    ('Chiara', 'pesca'): 2, ('Chiara', 'mela'): 3,
    ('Luca', 'mela'): 2, ('Luca', 'banana'): 1,
    ('Paola', 'yogurt'): 3, ('Paola', 'pesca'): 2,

    ('Alice', 'acqua'): 1, ('Alice', 'succo'): 3,
    ('Mauro', 'energy drink'): 1, ('Mauro', 'acqua'): 2,
    ('Roberto', 'acqua'): 3, ('Roberto', 'succo'): 5,
    ('Chiara', 'energy drink'): 2, ('Chiara', 'caffe'): 3,
    ('Luca', 'caffe'): 4, ('Luca', 'succo'): 2,
    ('Paola', 'caffe'): 2, ('Paola', 'acqua'): 3,

    ('Alice', 'ciambella'): 2, ('Alice', 'cioccolato'): 4,
    ('Mauro', 'cornetto'): 1, ('Mauro', 'ciambella'): 3,
    ('Roberto', 'cioccolato'): 3, ('Roberto', 'gelato'): 2,
    ('Chiara', 'gelato'): 1, ('Chiara', 'cornetto'): 3,
    ('Luca', 'ciambella'): 1, ('Luca', 'cioccolato'): 2,
    ('Paola', 'cornetto'): 2, ('Paola', 'gelato'): 3,
})


class PaniniSolver:

    def __init__(self):
        self.__m = gp.Model()
        self.__m.setParam('LogToConsole', 0)
        self.__x = self.__m.addVars(users, assets, obj=preferences, vtype=GRB.BINARY, name='x')
        self.__m.update()

        for cat_i in categories:
            self.__m.addConstrs((gp.quicksum([self.__x[u_i, it_i] for it_i in cat_i]) == 1 for u_i in users))

        self.__m.addConstrs((self.__x[u_i, a_i] <= preferences[u_i, a_i] for u_i in users for a_i in assets), name='c2')
        self.__m.addConstrs((self.__x.prod(preferences, '*', a_i) <= quantities[a_i] for a_i in assets), name='c3')

        self.__m.setObjective(self.__x.prod(preferences), GRB.MAXIMIZE)

        self.__m.optimize()

    def get_solution(self):
        for x_i in self.__x:
            if self.__x[x_i].getAttr('X') != 0:
                print(x_i)

    def get_obj_val(self):
        return sum(q_vals) - self.__m.ObjVal


def evaluate_csv(csv_file):
    df = pd.read_csv(csv_file)
    df.fillna(0, inplace=True)
    acc = 0
    for _, row in df.iterrows():
        name = row[0]
        vars = np.nonzero(row[1:].to_numpy())[0]
        acc += sum(preferences[name, assets[a_i]] for a_i in vars)

    return sum(q_vals) - acc


p_solver = PaniniSolver()
print('Optimal Solution value', p_solver.get_obj_val())
print('Optimal Solution configuration')
p_solver.get_solution()


#print(evaluate_csv(csv_file_name))