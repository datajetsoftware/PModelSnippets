
import sys
import json
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

#input and output files from first 2 arguments  
#inputfile = "D:/Datajet/datajetsoftware/output/json.txt"
#outputfile = "D:/Datajet/datajetsoftware/output/model_out_63791532897586-out.txt"

inputfile = sys.argv[1]
outputfile = sys.argv[2]



#read input file into array
iFile = open(inputfile, 'r',encoding='utf8') 
data = iFile.read()
iFile.close()


dataModel = json.loads(data)
associatedData = dataModel["associatedData"]



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

#array of rows length
for c in range(0,nColumns):

    thisData = []
    
    headerType = headerInfo[c]["type"]

    if headerType=="label":
        continue

    counts = grid[c]

    for x in range(0,rows):

        val = float(counts[x])
        thisData.append(val)
        
    clusteringSource.append(thisData)
            
    
linear_regressor = LinearRegression()

linear_regressor.fit(pd.DataFrame(clusteringSource[0]), pd.DataFrame(clusteringSource[1]))  
associatedData["reg-score"]=linear_regressor.score(pd.DataFrame(clusteringSource[0]), pd.DataFrame(clusteringSource[1]))
    
##get the predict....





r = np.corrcoef(clusteringSource[0], clusteringSource[1])

associatedData["corrcoef"]=r.tolist()

x = pd.Series(clusteringSource[0])
y = pd.Series(clusteringSource[1])

associatedData["Pearson-r"]=x.corr(y)
associatedData["Spearman-rho"]=x.corr(y,method="spearman")
associatedData["Kendall-tau"]=x.corr(y,method="kendall")


headerCopy = json.loads(json.dumps(headerInfo[1]))
headerCopy["name"]="Predicted"
headerCopy["dataType"]="numeric"
headerCopy["type"]="value"
headerCopy["fieldType"]="double"
headerCopy["axisOverride"]=1
headerCopy["graphAble"]=True
headerInfo.append(headerCopy)

y_pred = linear_regressor.predict(pd.DataFrame(clusteringSource[0]))
#associatedData["y_pred"]=y_pred.tolist()

clusterData = y_pred.tolist()

if len(grid[1]) > len(clusteringSource):
    clusterData.append(0)


sdf3 = []
for x in range(0,len(clusterData)):
    val = str(clusterData[x])
    sdf3.append(val[1:len(val)-2])
    

grid.append(sdf3)

dataModel["suggestedChart"] = "XYXZScatter"

output = json.dumps(dataModel)

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
                        

