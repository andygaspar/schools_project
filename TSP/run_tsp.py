from TSP.tsp import Tsp




tsp = Tsp()
# # tsp.draw()
tsp.solve()
tsp.draw_solution(name_file='ottima.png')
tsp.draw_csv_solutions()