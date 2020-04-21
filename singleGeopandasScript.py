# import pandas to read csv file
import pandas as pd 

# import Path to deal with paths
from pathlib import Path





# import the file by taking the input of user
# input will be the path of csv file

def importingCsv():

    # get the path of file
    pathOfFile = Path(input('Kindly input the path of csv file: '))

    # /Users/krishnaninama/Documents/test/Dewas/geop/fire_points.csv ---->test path

    # read the file into pandas dataframe

    csvData = pd.read_csv(pathOfFile)


    #output the dataframe
    return csvData

# print(importingCsv())

# take the dataframe output by the method

firePointData = importingCsv()
# print (firePointData)

# print headers of data frame

coloumnInFirePointData = firePointData.columns
print(coloumnInFirePointData)

# get the input of level
selectedLevel = input ('Enter a heading: ')

#create an empty list which will contain the unique values from the said 


# get the input of level
# selectedLevel = input ('Enter a heading: ')

# create an empty list which will contain the unique values from the said 
unique_list = []
# print(firePointData['Range'])


# getting a list from a column of a dataframe
rawlist = firePointData[selectedLevel].to_list()
#remove extra space
list1=[]
for i in rawlist:
    list1.append(i.rstrip())
# print(list1)

# getting all unique values

for any in list1: 
# check if exists in unique_list or not 
    if any not in unique_list: 
         unique_list.append(any) 

#initialising null dictionary
freq_result={}
#traversing all elements of intrested_level
for i in unique_list:
    freq_result[i] = list1.count(i)

# importing csv to write csv file output
import csv

print(freq_result)
w = csv.writer(open('frequnecy_output.csv', 'w') )
for key, val in freq_result.items():
    w.writerow([key,val])

 

# now we have the frequency values
# we can move to importing the shpe file and changing
# the attribute table and enter the values of fire frequency

# import geopandas to read the csv file

import geopandas as gpd 
import matplotlib.pyplot as plt 

#get the path of shpaefile

fp = r'/Users/krishnaninama/Documents/test/Dewas/test/crs_test.shp'

# fp = Path(input('enter the path of shapefile'))

# read the file using geopandas

data = gpd.read_file(fp)

# command to acess active geoseries gdf.geometry.name
# To change which column is the active geometry column, use the GeoDataFrame.set_geometry() method.
# adding new field
data["fire_f"]= 0

# writing to new shape file

# writing to a file
# data.to_file("/Users/krishnaninama/Documents/test/Dewas/geop/crs_test.shp")

#add new field to attribute table



#dewas = data.plot()
#plt.show()


# we can use both the dictionary we outputed or we can call back
# the frequecy output file and use the two coloumns as list and 
# use those list.

# first we are going to try and use the diciotnary
# the dicitonary that contains the values is freq_result{}

for value in freq_result.keys():

    # this code will give us the index of the rows which have the string 
    index_c = data[data.Range_Name.str.match(value,case = False)].index.tolist()

    # now we want to set the fire values of the indices
    for j in index_c:
        data._set_value(j,'fire_f',freq_result[value])

# now we try to test weather it worked or not
print(data.head())

data.to_file("/Users/krishnaninama/Documents/test/Dewas/geop/crs_test.shp")


#method didn;t work becauase of an space at the end.
# to remove thhis space i will have to use srtip method at appropriate place.
# the space is coing from the input fire point csv file

