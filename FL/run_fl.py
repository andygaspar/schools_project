import numpy as np
import pandas as pd

from FL.fl import FacilityLocation
import networkx as nx

f = FacilityLocation()
f.draw('Pictures/fl.png')
# f.check_and_draw_solution()
# f.draw_csv_solutions()
f.g.g
MAT = nx.to_numpy_array(f.g.g, weight='weight')
streets = np.nonzero(MAT)

dist = pd.DataFrame({'points': zip(streets[0], streets[1]),'dist': MAT[streets]})