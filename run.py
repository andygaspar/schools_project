from FL.fl import FacilityLocation
from TSP.tsp import Tsp


# FL

f = FacilityLocation()
f.draw('fl.png')
sol = [4, 6, 9, 70, 12, 30, 40]
f.check_solution()


# TSP

tsp = Tsp()
tsp.draw()
# tsp.solve()
tsp.draw_solution()