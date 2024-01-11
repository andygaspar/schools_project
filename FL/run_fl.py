from DownloadFiles import download_file
from FL.fl import FacilityLocation

f = FacilityLocation()
# MAT = nx.to_numpy_array(f.g.g, weight='weight')
# streets = np.nonzero(MAT)

# (64, 67),509.45766
# (41, 22),479.381343

# dist = pd.DataFrame({'points': zip(streets[0], streets[1]), 'dist': MAT[streets]})

f.check_and_draw_solution(name_file='SoluzioniFL/Z** Ottima **Z.png')
# download_file.get_fl_from_drive()
f.draw_csv_solutions()

