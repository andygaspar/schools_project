import osmnx as ox
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt


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


