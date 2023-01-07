import copy

import networkx as nx
import geopandas as gpd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, image as mpimg
import geopy.distance as geo_dist


class GraphObj:

    def __init__(self):

        self.kml_file = '../Data_/KML/Facility location.kml'
        self.edge_file = '../Data_/CSV/fl_edges.csv'
        self.g = nx.Graph()
        self.df = self.read_file(self.kml_file)
        self.limits = {
            'west': self.df.x.min(),
            'est': self.df.x.max(),
            'north': self.df.y.max(),
            'south': self.df.y.min()
        }

        self.df = self.df[self.df['layer'] != 'bb box']
        self.n_points = self.df.shape[0]
        self.g.add_nodes_from([i for i in range(self.n_points)])

        self.positions = dict(zip(self.g.nodes, zip(self.df.x, self.df.y)))
        self.n_facilities, self.n_streets = self.df[self.df.layer == 'facilities'].shape[0], \
            self.df[self.df.layer == 'street nodes'].shape[0]
        self.colors = self.reset_colors()
        self.sizes = [800 for _ in range(self.n_facilities)] + [600 for _ in range(self.n_streets)]

        offset = 0.0000
        pos_labels = {}
        keys = self.positions.keys()
        for key in keys:
            x, y = self.positions[key]
            pos_labels[key] = (x, y + offset)

        self.labels = {node: str(node) for node in self.g.nodes.keys()}
        df_edges = pd.read_csv(self.edge_file)
        self.edges = tuple(zip(df_edges.edge_1, df_edges.edge_2))
        edges = list(tuple(zip(df_edges.edge_1, df_edges.edge_2,
                             [geo_dist.geodesic(self.positions[edge[0]], self.positions[edge[1]]).m
                              for edge in self.edges])))

        self.g.add_weighted_edges_from(edges)

    def reset_colors(self):
        return np.array(["dodgerblue" for _ in range(self.n_facilities)] + ["yellow" for _ in range(self.n_streets)])

    def read_file(self, klm_file):
        points_layer = []
        points_x = []
        points_y = []

        with open(klm_file) as f:
            doc = f.read()
        res = 0
        doc_copy = copy.deepcopy(doc)
        while res != -1:
            res = self.remove_sub(doc_copy, 'Folder')
            if res != -1:
                sub_str, doc_copy = res
                name = self.get_name(res[0])
                while sub_str != -1:
                    sub_str = self.remove_sub(sub_str, 'Point')
                    if sub_str != -1:
                        point, sub_str = sub_str
                        coordinate_line = self.remove_sub(point, 'coordinates')
                        coordinates = coordinate_line[0].replace(' ', '')
                        coordinates = coordinates.replace('\n', '')
                        x, y, _ = coordinates.split(',')
                        x, y = float(x), float(y)
                        points_layer.append(name)
                        points_x.append(x)
                        points_y.append(y)

        return pd.DataFrame({'layer': points_layer, 'x': points_x, 'y': points_y})

    @staticmethod
    def remove_sub(s, key):
        start = s.find('<' + key + '>')
        if start == -1:
            return start
        start += 2 + len(key)
        s = s[start:]
        end = s.find('</' + key + '>')
        end += 3 + len(key)
        return s[:end], s[end:]

    @staticmethod
    def get_name(s):
        start = s.find('<name>')
        return s[start + 6: s.find('</name')]

    def draw(self, ax=None, show=False):
        nx.draw(self.g, ax=ax, pos=self.positions, node_size=self.sizes, node_color=self.colors, width=5,
                edge_color='r', font_size=22, with_labels=True)
        if show:
            plt.show()

    def draw_all(self):
        plt.rcParams['font.size'] = 22

        df_streets = pd.read_csv('../Data_/CSV/streets.csv', low_memory=False)
        cp_union = gpd.GeoDataFrame(
            df_streets.loc[:, [c for c in df_streets.columns if c != "geometry"]],
            geometry=gpd.GeoSeries.from_wkt(df_streets["geometry"]),
            crs="epsg:3005",
        )

        df = cp_union.cx[self.limits['west']:self.limits['est'], self.limits['south']:self.limits['north']]

        fig, ax = plt.subplots(figsize=(60, 25))
        ax.set_xlim((self.limits['west'], self.limits['est']))
        ax.set_ylim((self.limits['south'], self.limits['north']))
        ax.margins(0)
        ax.apply_aspect()

        df.plot(ax=ax, color='grey', figsize=(60, 25))
        self.draw(ax)

        plt.show()

    def draw_solution(self, sol, not_covered=None):
        self.colors[sol] = 'lime'
        if not_covered is not None:
            self.colors[not_covered] = 'orange'
        self.draw_all()
        self.colors = self.reset_colors()


class Point:

    def __init__(self, name, description, coordinates):
        self.name = name
        self.description = description
        self.coordinates = coordinates


