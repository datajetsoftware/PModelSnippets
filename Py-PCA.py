## NOTE: This is Python 3 code.
import sys
import os
import base64
import json
import pandas as pd
import numpy as np
import random as rd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt # NOTE: This was tested with matplotlib v. 2.1.0
from sklearn.preprocessing import StandardScaler
import binascii


inputfile = sys.argv[1]
outputfile = sys.argv[2]


#read input file into array
iFile = open(inputfile, 'r',encoding='utf8') 
data = iFile.read()
iFile.close()


dataModel = json.loads(data)
grid = dataModel["grid"]
headerInfo = dataModel["headerInfo"]
associatedData = dataModel["associatedData"]

isMeasure = ("measureEntries" in dataModel)


if not isMeasure:
    sys.stderr.write("requires multi measure profile\r\n")
    exit()


nColumns = len(headerInfo);


if dataModel["hasTotalColumn"]:
    nColumns = nColumns-1



clusteringSource = []


rows = dataModel["rows"]
hasTotalRow = dataModel["hasTotalRow"]
if hasTotalRow:
    rows= rows-1

for x in range(0,rows):

    thisData = []
    
    for c in range(0,nColumns):


        headerType = headerInfo[c]["type"]
    
        if headerType=="label":
            continue

        counts = grid[c]
        
        val = float(counts[x])
        thisData.append(val)
        
    clusteringSource.append(thisData)
            
    

dataframe = pd.DataFrame(clusteringSource)    

#print(dataframe.head())
#print(dataframe.shape)

#########################
#
# Perform PCA on the data
#
#########################
# First center and scale the data
scaled_data = dataframe 
#scaled_data = preprocessing.scale(dataframe.T)
scaled_data = StandardScaler().fit_transform(scaled_data)
#print(scaled_data)

pca = PCA() # create a PCA object
pca.fit(scaled_data) # do the math
pca_data = pca.transform(scaled_data) # get PCA coordinates for scaled_data

#print(pca_data)


per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
#print(per_var)
#########################
#
# Draw a scree plot and a PCA plot
#
#########################
 
 
 
#The following code constructs the Scree plot

labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
 
plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Component')
plt.title('Scree Plot')

fig1Name = inputfile + "fig1.png"

#print(fig1Name)

plt.savefig(fig1Name)
#plt.show()
 


with open(fig1Name, "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
    #b64_string = binascii.hexlify(img_file.read())
#print(b64_string)

#delete the file
os.remove(fig1Name)
 
screeImage = json.loads("{\"objectType\": \"image\"}")
screeImage["data"]=bytes.decode(b64_string)
 
associatedData["Scree"]=screeImage
 
output = json.dumps(dataModel)

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
 

