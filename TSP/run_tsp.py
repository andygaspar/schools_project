from TSP.tsp import Tsp
from DownloadFiles import download_file

tsp = Tsp()
# # tsp.draw()
tsp.solve()
tsp.draw_solution(name_file='SoluzioniTSP/Z ottima.png')
# download_file.get_tsp_from_drive()
tsp.draw_csv_solutions()