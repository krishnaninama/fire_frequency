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
from PyQt5.QtCore import QVariant
class krishna:
    def test():
        #setting up global variables
        list1 = []
        list2 = []
        lyr = iface.activeLayer()
        dp = lyr.dataProvider()
        #name_of_level = input('input the name of the field of the intrested level in the attribute table')
        name_of_level = 'Beat_Name'
        #reading the csv file.
        file = r'D:\Fire analysis\Dewas\test.csv'
        df = pd.read_csv(file, header = None)
        #Assigning the values of two coloumns to seperate lists.
        list1 = list (df[0]) 
        list2 = list (df[1])
        #Checking if the field of fire_f is present or not. If not create it.
        list_of_fields = lyr.fields().names()
        if 'fire_f' not in list_of_fields:
            dp.addAttributes( [QgsField ("fire_f" , QVariant.String)])
            lyr.updateFields()
        #method which will set values of field fire_f of all features to 0.
        index_of_fire_f = dp.fieldNameIndex('fire_f')
        features=lyr.getFeatures()
        lyr.startEditing()
        for f in features:
            id=f.id()
            default_value = 0
            attr_value = {index_of_fire_f:default_value}
            dp.changeAttributeValues({id:attr_value})
        lyr.commitChanges()
        #main method to fill the frequencies
        #this will be taken from the csv file. the features can be range, beat, compartment,etc
        list_of_features = list1               
        frequency_of_fire = list2
        #now i want to select the feature form this list.for this.
        x = 0 
        for i in list_of_features:
            #selecting
            lyr.selectByExpression ( " {} ILIKE '{}' ".format(name_of_level,list_of_features[x].rstrip())) #this will select the feature
            #getting ids of selected features
            selected_ids = lyr.selectedFeatureIds()         
            attr = {dp.fieldNameIndex('fire_f'):frequency_of_fire[x] }
            for j in selected_ids:
                dp.changeAttributeValues ( {j : attr})
            x +=1
            lyr.removeSelection()
        lyr.updateFields()
krishna.test()