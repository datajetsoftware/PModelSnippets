
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

#sys.stderr.write(str(len(sys.argv)))
#exit()

if len(sys.argv)==4:
    NCLUSTERS = int(sys.argv[3]);    


#read input file into array
iFile = open(inputfile, 'r',encoding='utf8') 
data = iFile.read()
iFile.close()


dataModel = json.loads(data)
associatedData = dataModel["associatedData"]

associatedData["clusters"] = NCLUSTERS

grid = dataModel["grid"]


#create a data frame 

headerInfo = dataModel["headerInfo"]
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

associatedData["DataRows"]=len(clusteringSource)
associatedData["DataColumns"]=len(clusteringSource[0])
 









headerInfo.clear()
grid.clear()

labelHeader = json.loads("{}")
labelHeader["name"]="Clusters"
labelHeader["dataType"]="numeric"
labelHeader["type"]="label"
labelHeader["fieldType"]=""
headerInfo.append(labelHeader)

dataHeader = json.loads("{}")
dataHeader["name"]="Error"
dataHeader["dataType"]="numeric"
dataHeader["type"]="value"
dataHeader["fieldType"]=""
dataHeader["graphAble"]=True
headerInfo.append(dataHeader)



labels=[]
values=[]


for nc in range(2,NCLUSTERS+1):
    kmeans = KMeans(n_clusters=nc)
    kmeans.fit(dataframe)
    labels.append(str(nc))
    values.append(str(kmeans.inertia_))



grid=[]
grid.append(labels)
grid.append(values)


dataModel["rows"]=len(labels)
dataModel["headerInfo"]=headerInfo
dataModel["grid"]=grid


dataModel["hasTotalRow"]=False
dataModel["hasTotalColumn"]=False
dataModel["hasNullRow"]=False
dataModel["hasNullColumn"]=False




#dataModel["grid"] = grid    



output = json.dumps(dataModel)

    

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
                        

