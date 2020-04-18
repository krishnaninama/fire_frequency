#this app is working. 

import csv
#ask the level at which the user wants the info
req_unit = input('\nKindly tell us at what level you want the info: ')
#ask the user the name of the csv file.
data_name = input ('\n kindly tell us the name of the file: ')
#req_unit = 'beat'

with open(data_name, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    intrested_level = []
    for row in csv_reader:
        intrested_level.append(row[req_unit])                #created a list and appending all the values to it.
        

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

print(freq_result)
w = csv.writer(open('frequnecy_output.csv', 'w') )
for key, val in freq_result.items():
    w.writerow([key,val])
