
import sys
import json
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

#input and output files from first 2 arguments  
#inputfile = "D:/Datajet/datajetsoftware/output/json.txt"
#outputfile = "D:/Datajet/datajetsoftware/output/model_out_63791532897586-out.txt"

inputfile = sys.argv[1]
outputfile = sys.argv[2]

NCLUSTERS = 5


#read input file into array
iFile = open(inputfile, 'r',encoding='utf8') 
data = iFile.read()
iFile.close()


dataModel = json.loads(data)

grid = dataModel["grid"]


#create a data frame 

headerInfo = dataModel["headerInfo"]
nColumns = len(headerInfo);

if dataModel["hasTotalColumn"]:
    nColumns = nColumns-1


clusteringSource = []

for column in range(0,nColumns):

    thisData = []

    headerType = headerInfo[column]["type"]
    
    if headerType=="label":
        continue

    counts = grid[column]

    


    rows = len(counts)

    hasTotalRow = dataModel["hasTotalRow"]
    if hasTotalRow:
        rows= rows-1

    counts = grid[column]

    rows = len(counts)

        
    for x in range(0,rows):
        val = float(counts[x])
        thisData.append(val)
        
    clusteringSource.append(thisData)
            
    if hasTotalRow:
        counts[rows-1]=""



dataframe = []

for r in range(0,len(clusteringSource[0])):
    row=[]
    for c in range(0,1):
        row.append(clusteringSource[c][r])
        
    dataframe.append(row)
 

kmeans = KMeans(n_clusters=NCLUSTERS)
kmeans.fit(dataframe)
labels = kmeans.labels_
df3 = pd.DataFrame(labels)

#add df3 as a new column in results

headerCopy = json.loads(json.dumps(headerInfo[1]))
headerCopy["name"]="Cluster"
headerCopy["dataType"]="numeric"
headerCopy["type"]="value"
headerCopy["fieldType"]="integer"
headerCopy["axisOverride"]=1
headerCopy["graphAble"]=True
headerInfo.append(headerCopy)

#dataModel["headerInfo"]=headerInfo;


#clusterData = np.array(df3[0].tolist())
clusterData = df3[0].tolist()

if len(grid[1]) > len(df3):
    clusterData.append(0)





sdf3 = []
for x in range(0,len(clusterData)):
    sdf3.append(str(clusterData[x]))
    

grid.append(sdf3)


#cluster_centres_0 = kmeans.cluster_centers_[:, 0]
#cluster_centres_1 = kmeans.cluster_centers_[:, 1]


associatedData = dataModel["associatedData"]


associatedData["clusters"] = NCLUSTERS

#dataModel["grid"] = grid    


#print(len(clusteringSource))
#print(len(clusteringSource[0]))
#print(len(clusteringSource[1]))

output = json.dumps(dataModel)

    

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
                        

