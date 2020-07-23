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
#following imports for taking inputs from user
import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
#i added QFileDialog to import to take input of csv file form user.
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

from pathlib import Path

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

class selectCsvOfFrequency(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Select the csv file containing frequency data please'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
    
   
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            return fileName
selectCsv = selectCsvOfFrequency()
file = Path(selectCsv.openFileNameDialog())
#file = r'/Users/krishnaninama/Documents/test/Dewas/test.csv'
df = pd.read_csv(file, header = None)
#putting the values of names of beat/range to list1 and number fo fire to list2
list1 = list (df[0]) 
list2 = list (df[1])


#commenting this because input() doesn't work in qgis console 
#name_of_level = input ('kindly enter the name of field form the list above for which you want to enter the frequency data:')

#method to take input from user. he will select from a list and we will take that input
class selectionOfLevel(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Select level at which you want to enter frequency data'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        
    
        
    def getChoice(self):
        items = list_of_fields
        item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
        if okPressed and item:
            print(item)
            return item

    

selection = selectionOfLevel()
name_of_level = selection.getChoice()

#name_of_level = 'Beat_Name'

#item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
#list_of_fields, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)

#create an object from class Qwidget

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

#exec(open('/Users/krishnaninama/Documents/test/Dewas/final_working_script.py'.encode('utf-8')).read())
