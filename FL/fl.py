import networkx as nx
import numpy as np
import gurobipy as gb

from FL.fl_graph import GraphObj


class FacilityLocation:

    def __init__(self, min_distance=500):
        self.g = GraphObj()
        self.min_dist = min_distance

        self.mat_dist = nx.floyd_warshall_numpy(self.g.g)

        self.mat = np.zeros_like(self.mat_dist)
        self.mat[self.mat_dist <= self.min_dist] = 1

        self.fl = gb.Model()
        self.fl.modelSense = gb.GRB.MINIMIZE

        self.x = self.fl.addMVar(self.g.n_facilities, vtype=gb.GRB.BINARY)
        self.y = self.fl.addMVar(self.g.n_streets, vtype=gb.GRB.BINARY)

        for i in range(self.g.n_facilities):
            self.fl.addConstr(
                gb.quicksum(self.mat[i, j] * self.x[j] for j in range(self.g.n_facilities))
                + gb.quicksum(self.mat[i, j + self.g.n_facilities] * self.y[j] for j in range(self.g.n_streets)) >= 1
            )

        self.fl.setObjective(
            gb.quicksum(self.x[j] for j in range(self.g.n_facilities)) + gb.quicksum(
                self.y[j] for j in range(self.g.n_streets))
        )

        self.fl.optimize()

        sol_x = self.x.x.astype(int)
        sol_y = self.y.x.astype(int)

        facilities = np.squeeze(np.argwhere(sol_x == 1))
        streets = np.squeeze(np.argwhere(sol_y == 1)) + self.g.n_facilities
        self.solution = np.concatenate([facilities, streets])

    def draw(self, name_file=None):
        self.g.draw_all(name_file)

    def draw_solution(self, solution=None, not_covered=None):
        solution = solution if solution is not None else self.solution
        self.g.draw_solution(solution, not_covered)

    def check_solution(self, solution=None):
        sol = np.zeros(self.g.n_points)
        solution = solution if solution is not None else self.solution
        sol[solution] = 1
        res = np.where(np.dot(self.mat, sol)[: self.g.n_facilities] == 0)
        print('facilities:', len(solution), 'uncovered:', res)
        self.draw_solution(solution, res)



