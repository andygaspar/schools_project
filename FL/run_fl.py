import numpy as np
import pandas as pd

from FL.fl import FacilityLocation
import networkx as nx

f = FacilityLocation()
# MAT = nx.to_numpy_array(f.g.g, weight='weight')
# streets = np.nonzero(MAT)

# (64, 67),509.45766
# (41, 22),479.38134

# dist = pd.DataFrame({'points': zip(streets[0], streets[1]), 'dist': MAT[streets]})

f.check_and_draw_solution(name_file='ottima.png')
f.draw_csv_solutions()

