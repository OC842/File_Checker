import os, sys
import pandas as pd
import numpy as np

#Read excel file with all the file names to be checked
df = pd.read_excel('Names.xlsx', sheet_name = 'Sheet1')

#Converting dataframe to lists for easier manipulation
pmacs = df['PMAC'].tolist()
names = df['Name'].tolist()

#Raw string to old folder path name
path = r"C:\Users\ochambers\Documents\pmac\data\tempcello"

#Files are stored with a unique ID (PMAC). Each PMAC will have a varying
#number of files, anywhere from 1 - 7. The format is 'PMAC_0x.dat'

#Inserting an '_' at the end of every unique number and adding '0' to the start
# as the PMAC must be at least 4 digits
for i in range(len(pmacs)):

	if(len(str(pmacs[i])) < 4):
		
		n = 4 - len(str(pmacs[i]))
		pmacs[i] = ("0" * n) + str(pmacs[i]) + "_"
		
	else:
		pmacs[i] = str(pmacs[i]) + "_"

#Creating array for tests. Unused
#data = [names, pmacs]
#data = np.transpose(data)


#Initalising arrays
files = []
all_files = []


#This loop looks through every file and creates an array of every files which
# contains the PMAC.
#These arrays are then combined into a larger array

#For every PMAC to be checked
for i in range(len(data)):

	#For every file in the folder
	for fname in os.listdir(path):
	
		#Test to check if file name contains 'PMAC_'
		#Returns -1 if 'PMAC_' is not found
		index = fname.find(data[i][1])
		
		#If file name contains PMAC
		if(index == 0):
			
			#Append files array
			files.append(fname)
	
	#If files contains file names then add all these file names to the larger
	# all_files array
	if(len(files) > 0):
	
		#Not needed currently
		#files.insert(0, str(i))
		
		#Changing to numpy array for ease of use
		all_files.append(np.array(files))
	
	#After checking every file start checking the next PMAC and clear files
	files = []
	
#Changing to numpy array for ease of use
all_files = np.array(all_files)

#Initalising marker and array
pressure = False
output = []

#This loop checks all the files with a PMAC as only files ending with '01' or
# '04' are useful
#'01' is always useful. '04' is only useful when there are 2 files present.

#This is due to different logger configurations, it's too complicated to explain
# here.
for i in range(len(all_files)):

	#To hold the length of the array with matching PMACs
	x = len(all_files[i])
	
	
	if(x != 2):
	
		#Search the files array to check if a file ends with '01'
		for j in range(len(all_files[i])):
		
			index = all_files[i][j].find("_01")
			
			if(index > 0):
			
				pressure = True
	
	else:
		#'01' has not been found so now check for '04' if there are only
		# 2 files with matching PMACs
		for j in range(len(all_files[i])):
		
			index = all_files[i][j].find("_04")
			
			if(index > 0):
			
				pressure = True
		
	#If either '01' or '04' has been found the data file contains a pressure reading.
	# This program was made to find files with pressure readings
	if(pressure == True):
	
		#Through my manipulations of the arrays I've lost the unique PMAC I started with.
		#This code finds the '_' in the file name and returns the number before it, this is the PMAC.
		pmac_index = all_files[i][0].find("_")
		
		
		#Every file in all_files[][x] contains the PMAC so the first item is chosen.
		pmac = all_files[i][0][0:pmac_index]
	
		#Create array of all PMACs with pressure data
		output.append(pmac)

	#reset pressure marker for next file array
	pressure = False



output = np.array(output)

#Outputting result to excel.
#It's ok that the names have been lost. I could add some code to retrieve them
# but it's easier to do it in excel.
df1 = pd.DataFrame(output)
df1.to_excel('output.xlsx', index = False, header = False)







