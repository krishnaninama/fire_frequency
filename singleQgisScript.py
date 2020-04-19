#PART 1

#import for part2

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

#import for part1
import csv
import inspect

#ask the user the name of the csv file.
#data_name = input ('\n kindly tell us the name of the file: ')
#req_unit = 'beat'


#selwcting csv file
class selectFile(QWidget):

    def __init__(self,title):
        super().__init__()
        self.title = title
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
selectCsv = selectFile('kindly select the file containing the fire points')
#this gives me path of the file selected
data_name = Path(selectCsv.openFileNameDialog())

  
#ask the level at which the user wants the info

#method to take input from user. he will select from a list and we will take that input
class selectionOfLevel(QWidget):

    def __init__(self,title):
        super().__init__()
        self.title = title
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        
    
        
    def getChoice(self,list):
        items = list
        item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
        if okPressed and item:
            print(item)
            return item

    

selection = selectionOfLevel('Kindly select the level')

with open(data_name, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    field_names = csv_reader.fieldnames
    req_unit = selection.getChoice(field_names)
    
    intrested_level = []
    
    for row in csv_reader:
        intrested_level.append(row[req_unit])                #created a list and appending all the values to it.
      

#req_unit = input('\nKindly tell us at what level you want the info: ')


# intilize a null list
unique_list = [] 
# traverse for all elements 
for any in intrested_level: 
# check if exists in unique_list or not 
    if any not in unique_list: 
         unique_list.append(any) 
#initialising null dictionary
freq_result={}
#traversing all elements of intrested_level
for i in unique_list:
    freq_result[i] = intrested_level.count(i)

#gwt the path of scrpit

#path_of_output = inspect.getfile(lambda: None)
#print(freq_result)
w = csv.writer(open('/Users/krishnaninama/fire_frequency.csv', 'w') )
for key, val in freq_result.items():
    w.writerow([key,val])


# PART 2



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


selectCsv = selectFile('kindly select the file which was outputed. it will be named fire_frequency.csv')
file = Path(selectCsv.openFileNameDialog())
#file = r'/Users/krishnaninama/Documents/test/Dewas/test.csv'
df = pd.read_csv(file, header = None)
#putting the values of names of beat/range to list1 and number fo fire to list2
list1 = list (df[0]) 
list2 = list (df[1])


#commenting this because input() doesn't work in qgis console 
#name_of_level = input ('kindly enter the name of field form the list above for which you want to enter the frequency data:')

#method to take input from user. he will select from a list and we will take that input

    
#creating another object of selectionoflevel class
selection = selectionOfLevel('Kindly select the level')
name_of_level = selection.getChoice(list_of_fields)

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
x = 0
# exec(open('/Users/nameofuser/Documents/test/test.py'.encode('utf-8')).read()) ----for mac
