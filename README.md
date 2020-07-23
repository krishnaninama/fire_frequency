# fire_frequency
Finds frequency from FSI data and adds this data to shapefile.

Hello. I am Krishna Ninama an ACF in Madhya Pradesh Forest Department. 
Forest Survey of India sends fire alerts on numbers registered on its Forest Fire Alert System. Anyone can register for these alerts. All forest division offices keep the data with them.
This data, on the request of officers is analysed and the fire sensitivity of an area is found out using this data of previous fires.
To analyse the data the first step is to find out the frequency of fire at any location like compartment, beat or range. The second step is to load this frequency data into GIS software so as to represent the data graphically/visually.
These two scripts in the QGIS Scripts folder perform/automate these two steps.

The script in GeopandaScript folder uses geopandas library and is a single script which will output the map file without using QGIS. 

