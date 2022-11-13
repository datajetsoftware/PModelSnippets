
import sys
import json
import os
import base64
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # NOTE: This was tested with matplotlib v. 2.1.0
from sklearn.metrics import silhouette_score

#input and output files from first 2 arguments  
#inputfile = "D:/Datajet/datajetsoftware/output/json.txt"
#outputfile = "D:/Datajet/datajetsoftware/output/model_out_63791532897586-out.txt"

inputfile = sys.argv[1]
outputfile = sys.argv[2]

NCLUSTERS = 5

#sys.stderr.write(str(len(sys.argv)))
#exit()

if len(sys.argv)==4:
    if sys.argv[3] != "":
        NCLUSTERS = int(sys.argv[3]);   

#read input file into array
iFile = open(inputfile, 'r',encoding='utf8') 
data = iFile.read()
iFile.close()


dataModel = json.loads(data)
associatedData = dataModel["associatedData"]

associatedData["clusters"] = NCLUSTERS

grid = dataModel["grid"]



isMeasure = ("measureEntries" in dataModel)

#create a data frame 

headerInfo = dataModel["headerInfo"]




#sys.stderr.write("measureEntries: "+str(len(measureEntries))+"\r\n")
#sys.stderr.write("fieldEntries: "+str(len(fieldEntries))+"\r\n")
#exit()


if isMeasure:
    
    measureEntries = dataModel["measureEntries"]
    nMeasures = len(measureEntries)
    
    fieldEntries = dataModel["fieldEntries"]
    nFields = len(fieldEntries)
    
    if nMeasures < 2:
        sys.stderr.write("at least 2 measures required\r\n")
        exit()
    
    if nFields != 1:
        sys.stderr.write("only 1 dimension supported\r\n")
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

    associatedData["DataRows"]=len(clusteringSource)
    associatedData["DataColumns"]=len(clusteringSource[0])
     

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

    cclist = kmeans.cluster_centers_.tolist()


    #put cluster_centers in grid mode

    ccjson = json.loads('{"objectType" : "grid", "tag" : "CLUSTER_GRID"}')
    ccjson["name"] = "Cluster Centers"


    ccdata = []
    ccheaders = []
    ccdataTypes = []

    #the cluster column header and data
    ccheaders.append("Cluster")
    ccdataTypes.append("integer")
    ccdata.append(list(range(1, len(cclist)+1)))   


    for x in range(0,len(cclist[0])):
        ccrow = []
        ccheaders.append(headerInfo[x+1]["name"])
        ccdataTypes.append("double")
        for y in range(0,len(cclist)):
            ccrow.append(cclist[y][x])    
        ccdata.append(ccrow)   

    ccjson["data"]  = ccdata
    ccjson["headers"] = ccheaders
    ccjson["dataTypes"] = ccdataTypes


    associatedData["ccgrid"]=ccjson
    associatedData["plottableCentroids"] = kmeans.cluster_centers_.tolist()
    associatedData["inertia"] = kmeans.inertia_
    dataModel["suggestedChart"]="scatter"
else:
    sys.stderr.write("profile source type not supported\r\n")
    exit()




kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}

# A list holds the SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(dataframe)
    sse.append(kmeans.inertia_)



plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
fig1Name = inputfile + "fig1.png"
#plt.show()
#quit()


plt.savefig(fig1Name)
with open(fig1Name, "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
os.remove(fig1Name)

PSSE = json.loads('{"objectType": "image", "name" : "SSE Chart"}')
PSSE["data"]=bytes.decode(b64_string)
associatedData["SSE"]=PSSE



# A list holds the silhouette coefficients for each k
silhouette_coefficients = []

# Notice you start at 2 clusters for silhouette coefficient
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(dataframe)
    score = silhouette_score(dataframe, kmeans.labels_)
    silhouette_coefficients.append(score)
    
plt.clf()    
plt.plot(range(2, 11), silhouette_coefficients)
plt.xticks(range(2, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Coefficient")
#plt.show()
plt.savefig(fig1Name)
with open(fig1Name, "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
os.remove(fig1Name)

Silhouette = json.loads('{"objectType": "image", "name" : "Silhouette Chart"}')
Silhouette["data"]=bytes.decode(b64_string)
associatedData["Silhouette"]=Silhouette


output = json.dumps(dataModel)

    

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
                        

