import numpy as np
import geopandas as gpd
import networkx as nx
import pandas as pd
import geopy.distance as geo_dist

from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from shapely.geometry.point import Point
import gurobipy as gb

plt.rcParams['font.size'] = 25


class Tsp:

    def __init__(self):

        friuli = pd.read_csv('Data_/CSV/friuli.csv', low_memory=False)
        self.friuli = gpd.GeoDataFrame(
            friuli.loc[:, [c for c in friuli.columns if c != "geometry"]],
            geometry=gpd.GeoSeries.from_wkt(friuli["geometry"]),
            crs="epsg:3005",
        )
        cities = pd.read_csv('Data_/CSV/FriuliCitta.csv', low_memory=False)
        self.cities_to_consider = pd.read_csv('Data_/CSV/citta.csv', low_memory=False)
        self.cities_to_consider.name = [str(i) + '\n' + name for i, name in enumerate(self.cities_to_consider.name)]
        cities = cities[cities.name.isin(self.cities_to_consider.city)]
        self.cities = gpd.GeoDataFrame(
            cities.loc[:, [c for c in cities.columns if c != "geometry"]],
            geometry=gpd.GeoSeries.from_wkt(cities["geometry"]),
            crs="epsg:3005",
        )

        points = self.cities.geometry.tolist()
        points_x, points_y = [p.x for p in points], [p.y for p in points]

        self.g = nx.Graph()
        self.n_nodes = cities.shape[0]
        self.g.add_nodes_from([i for i in range(self.n_nodes)])

        self.positions = dict(zip(self.g.nodes, zip(points_x, points_y)))

        df_edges = pd.read_csv('Data_/CSV/tsp_edges.csv')
        self.edges = tuple(zip(df_edges.edge_1, df_edges.edge_2))

        edges = list(tuple(zip(df_edges.edge_1, df_edges.edge_2,
                               [geo_dist.geodesic(self.positions[edge[0]], self.positions[edge[1]]).m
                                for edge in self.edges])))

        self.g.add_weighted_edges_from(edges)

        self.solution, self.obj_val = None, None
        self.labels = nx.get_edge_attributes(self.g, 'weight')
        for key in self.labels.keys():
            self.labels[key] = np.round(self.labels[key] / 1000, decimals=1)
        self.edge_color = 'grey'

        self.mat_dist = nx.to_numpy_matrix(self.g)[1:, 1:]
        self.ts_monfalcon_dist = 31.8 * 2

    def solve(self):
        adj_mat = np.zeros_like(self.mat_dist)
        adj_mat[self.mat_dist > 0] = 1

        n_nodes = self.mat_dist.shape[0]

        tsp = gb.Model()
        tsp.modelSense = gb.GRB.MINIMIZE

        x = tsp.addMVar((n_nodes, n_nodes), vtype=gb.GRB.BINARY)
        u = tsp.addMVar(n_nodes, vtype=gb.GRB.INTEGER)

        for i in range(n_nodes):
            tsp.addConstr(
                gb.quicksum(adj_mat[i, j] * x[i, j] for j in range(n_nodes)) == 1
            )
            tsp.addConstr(
                gb.quicksum(adj_mat[j, i] * x[j, i] for j in range(n_nodes)) == 1
            )
            if i > 0:
                for j in range(1, n_nodes):
                    if i != j:
                        tsp.addConstr(
                            u[i] + 1 <= u[j] + n_nodes * (1 - x[i, j])
                        )

        tsp.setObjective(
            gb.quicksum(self.mat_dist[i, j] * x[i, j] for i in range(n_nodes) for j in range(n_nodes))
        )

        tsp.optimize()

        sol = np.argwhere(x.x > 0.5) + 1
        self.solution = tuple(zip(sol[:, 0], sol[:, 1]))
        self.solution = ((0, 1),) + self.solution
        self.obj_val = np.round(tsp.getObjective().getValue()/1000 + self.ts_monfalcon_dist, decimals=1)
        print(self.obj_val)
        print(self.g.edges)
        print(self.solution)

    def draw(self, team=None, sol_val=None, name_file=None):
        fig, ax = plt.subplots(figsize=(40, 28))
        ax.patch.set_alpha(1.)

        fig.gca().add_artist(ScaleBar(dx=100, units="km", fixed_value=50, border_pad=3))

        self.friuli.plot(ax=ax)

        nx.draw(self.g, ax=ax, pos=self.positions, node_color='r', edge_color=self.edge_color, node_size=100, width=5)
        for i, tup in enumerate(zip(self.cities.geometry.x, self.cities.geometry.y, self.cities_to_consider.name)):
            x, y, label = tup
            x_eps = 0 if i != 16 else -0.01
            y_eps = -0.018 if i in [8, 10, 15] else 0.01

            ax.annotate(label, xy=(x + x_eps, y + y_eps), xytext=(3, 3), textcoords="offset points", ha='center', fontsize=30)
        nx.draw_networkx_edge_labels(self.g, edge_labels=self.labels, pos=self.positions, font_size=26)

        if team is not None:
            plt.title(team + '   Distanza totale: ' + str(sol_val), fontsize=40)

        plt.tight_layout()
        if name_file is not None:
            plt.savefig(name_file, transparent=True)
        else:
            plt.show()

    def draw_solution(self, team=None, solution=None, sol_val=None, name_file=None):
        solution = solution if solution is not None else self.solution
        team = team if team is not None else 'Soluzione ottima'
        sol_val = sol_val if sol_val is not None else self.obj_val

        self.edge_color = ['lime' if (edge in solution or edge[::-1] in solution) else 'grey' for edge in self.g.edges]
        self.draw(team=team, sol_val=sol_val, name_file=name_file)
        self.edge_color = ['grey' for _ in self.edges]

    def draw_csv_solutions(self):
        df = pd.read_csv('TSP/solutions.csv')
        df.fillna(1000, inplace=True)
        for column in df.columns:
            df[column] = df[column].astype(int)
        unfeasible = []
        for team in df.columns:
            if df[team][df[team] < 1000].unique().shape[0] != 20:
                print(team, ' soluzione non ammissibile')
                unfeasible.append(team)

        for team in df.columns:
            if team not in unfeasible:
                sol = df[team][df[team] < 1000][1:-1].to_numpy()
                sol_len = sol.shape[0]
                edges = [(sol[i] - 1, sol[i+1] - 1) for i in range(sol_len - 1)]
                obj = np.round(sum([self.mat_dist[edge]/1000 for edge in edges]) + self.ts_monfalcon_dist, decimals=1)
                solution = [(sol[i], sol[i+1]) for i in range(sol_len - 1)]
                solution += [(0, 1)]
                self.draw_solution(team=team, sol_val=obj, solution=solution, name_file=team + '.png')
