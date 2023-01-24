import itertools
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

users = ['Dante', 'Galilei', 'Oberdan', 'Grigoletti', 'Petrarca', 'Volta']

assets = ['panino', 'pizza', 'tramezzino', 'hamburger', 'yogurt', 'pesca', 'banana', 'mela', 'acqua', 'succo',
          'energy drink', 'caffe', 'ciambella', 'cioccolato', 'cornetto', 'gelato']
categories = [assets[4 * i: 4 * (i + 1)] for i in range(4)]

q_vals = np.array([4, 5, 3, 2, 3, 5, 6, 4, 9, 7, 2, 4, 5, 10, 5, 3])
quantities = {a_i: q_i for a_i, q_i in zip(assets, q_vals)}

preferences = {(u_i, a_i): 0 for u_i, a_i in itertools.product(users, assets)}
preferences.update({
    (users[0], 'panino'): 1, (users[0], 'pizza'): 2,
    (users[1], 'tramezzino'): 3, (users[1], 'panino'): 2,
    (users[2], 'tramezzino'): 2, (users[2], 'hamburger'): 1,
    (users[3], 'pizza'): 2, (users[3], 'hamburger'): 3,
    (users[4], 'panino'): 3, (users[4], 'hamburger'): 2,
    (users[5], 'pizza'): 4, (users[5], 'tramezzino'): 1,

    (users[0], 'yogurt'): 2, (users[0], 'pesca'): 3,
    (users[1], 'banana'): 2, (users[1], 'mela'): 4,
    (users[2], 'banana'): 1, (users[2], 'yogurt'): 2,
    (users[3], 'pesca'): 2, (users[3], 'mela'): 3,
    (users[4], 'mela'): 2, (users[4], 'banana'): 1,
    (users[5], 'yogurt'): 3, (users[5], 'pesca'): 2,

    (users[0], 'acqua'): 1, (users[0], 'succo'): 3,
    (users[1], 'energy drink'): 1, (users[1], 'acqua'): 2,
    (users[2], 'acqua'): 3, (users[2], 'succo'): 5,
    (users[3], 'energy drink'): 2, (users[3], 'caffe'): 3,
    (users[4], 'caffe'): 4, (users[4], 'succo'): 2,
    (users[5], 'caffe'): 2, (users[5], 'acqua'): 3,

    (users[0], 'ciambella'): 2, (users[0], 'cioccolato'): 4,
    (users[1], 'cornetto'): 1, (users[1], 'ciambella'): 3,
    (users[2], 'cioccolato'): 3, (users[2], 'gelato'): 2,
    (users[3], 'gelato'): 1, (users[3], 'cornetto'): 3,
    (users[4], 'ciambella'): 1, (users[4], 'cioccolato'): 2,
    (users[5], 'cornetto'): 2, (users[5], 'gelato'): 3,
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

    @staticmethod
    def evaluate_csv(csv_file):
        df = pd.read_csv(csv_file)
        df.fillna(0, inplace=True)
        acc = 0
        for _, row in df.iterrows():
            name = row[0]
            vars = np.nonzero(row[1:].to_numpy())[0]
            acc += sum(preferences[name, assets[a_i]] for a_i in vars)

        return sum(q_vals) - acc


# p_solver = PaniniSolver()
# print('Optimal Solution value', p_solver.get_obj_val())
# print('Optimal Solution configuration')
# p_solver.get_solution()
#
#
# #print(evaluate_csv(csv_file_name))