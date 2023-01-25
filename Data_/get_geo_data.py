import osmnx as ox
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt

'''
friuli = ox.geocode_to_gdf('Friuli Venezia Giulia')
street = ox.geometries_from_place('Friuli Venezia Giulia', {'place': ['city', 'town']})

fig, ax = plt.subplots()

friuli.plot(ax=ax)
street.plot(ax=ax, color='r')
# for idx, row in gdf_swk.iterrows():
#    plt.annotate(s=row[‘nama_wilayah’], xy=row[‘coords’], horizontalalignment=’center’, color=’blue’)
# plt.show()

# Get place boundary related to the place name as a geodataframe
area = ox.geocode_to_gdf('Trieste')
area.plot()
plt.show()
'''

cities_to_consider = ['Trieste', 'Ronchi dei Legionari', 'Monfalcone', 'Opicina / Opčine', 'Muggia / Milje', 'Grado', 'Gorizia', 'Cividale del Friuli', 'Tarvisio', 'Palmanova', 'Latisana', 'Cervignano del Friuli', 'Udine', 'Spilimbergo / Spilimberc', 'Gemona del Friuli', 'Codroipo / Codroip', 'Tarcento', 'San Daniele del Friuli', 'Tolmezzo / Tumieç', 'Azzano Decimo', 'San Vito al Tagliamento / San Vît dal Tiliment', 'Pordenone', 'Fontanafredda', 'Fiume Veneto', 'Sacile', 'Maniago / Manià']

tags = {'building': True, 'roads': True}

buildings = ox.geometries_from_place('Trieste', tags)
buildings.head()

buildings.plot()
plt.show()

street = ox.geometries_from_place({'city':'Trieste'}, {'highway': True, 'road': True})

street.plot()
plt.show()

street.to_csv('streets.csv', index_label=False, index=False)

build = buildings.loc[buildings.geometry.type=='Polygon']
build.to_file('Data_/SHP/buildings/buildings.shp')


import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt

df_streets = pd.read_csv('Data_/CSV/streets.csv', low_memory=False)
cp_union = gpd.GeoDataFrame(
    df_streets.loc[:, [c for c in df_streets.columns if c != "geometry"]],
    geometry=gpd.GeoSeries.from_wkt(df_streets["geometry"]),
    crs="epsg:5195",
)

5195
32619

fig, ax = plt.subplots(figsize=(60, 25))


ax.margins(0)
ax.apply_aspect()

df = cp_union

df.plot(ax=ax, color='grey', figsize=(60, 25))
plt.show()

dm = ox.geometries_from_bbox(45.6611, 45.6353, 13.8151, 13.7477, tags={'highway': True, 'road': True})
dm.head()
plt.rcParams["figure.figsize"] = (60, 25)
dm.plot()
plt.show()

df = pd.DataFrame(dm)

df.to_csv('Data_/CSV/trieste.csv', index_label=False, index=False)
dm.crs

