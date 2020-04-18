#imports
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
from qgis.core import (
  QgsApplication,
  QgsDataSourceUri,
  QgsCategorizedSymbolRenderer,
  QgsClassificationRange,
  QgsPointXY,
  QgsProject,
  QgsExpression,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsFeatureRequest,
  QgsFeatureRenderer,
  QgsGeometry,
  QgsGraduatedSymbolRenderer,
  QgsMarkerSymbol,
  QgsMessageLog,
  QgsRectangle,
  QgsRendererCategory,
  QgsRendererRange,
  QgsSymbol,
  QgsVectorDataProvider,
  QgsVectorLayer,
  QgsVectorFileWriter,
  QgsWkbTypes,
  QgsSpatialIndex,
)
from qgis.utils import iface
from PyQt5.QtCore import QVariant #to add attribute QVariant gives the type of attribute<string or integer

#creation of field of fire frequency_of_fire
lyr = iface.activeLayer()
dp = lyr.dataProvider()
#check if the field is already there or not

list_of_fields = lyr.fields().names()
if 'fire_f' not in list_of_fields:
    dp.addAttributes( [QgsField ("fire_f" , QVariant.String)])
    lyr.updateFields()
#setting the default value to 0
index_of_fire_f = dp.fieldNameIndex('fire_f')
features=lyr.getFeatures()

lyr.startEditing()
for f in features:
    id=f.id()
    
    attr_value={index_of_fire_f:0}
    dp.changeAttributeValues({id:attr_value})
lyr.commitChanges()


#creating empy lists
list1 = []
list2 = []
#reading the csv file
file = r'D:\Fire analysis\Dewas\test.csv'
df = pd.read_csv(file, header = None)
#putting the values of names of beat/range to list1 and number fo fire to list2
list1 = list (df[0]) 
list2 = list (df[1])

#name_of_level = input('input the name of the field of the intrested level in the attribute table')
name_of_level = 'Beat_Name'
list_of_features = list1               #this will be taken from the csv file. the features can be range, beat, compartment,etc
frequency_of_fire = list2
#now i want to select the feature form this list.for this.
x = 0
#select all features 
for i in list_of_features:
    
    y = list_of_features[x].rstrip()
    lyr.selectByExpression ( " {} ILIKE '{}' ".format(name_of_level,y)) #this will select the feature
    selected_ids = lyr.selectedFeatureIds()         #get their ids of the selected features
    attr = {dp.fieldNameIndex('fire_f'):frequency_of_fire[x] }
    for j in selected_ids:
        dp.changeAttributeValues ( {j : attr})
    x +=1
    lyr.removeSelection()

lyr.updateFields()


#code to execute a python script form python console
exec(open('D:/Fire analysis/Untitled-0.py'.encode('utf-8')).read())
