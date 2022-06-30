
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


associatedData["info"]="some info"

dataModel["suggestedChart"] = "XYXZScatter"


subChart = json.loads("{}")
subChart["objectType"]="chart"
subChart["name"]="Example 'bar' chart "
subChart["chartType"]="bar"
subChart["categories"]=["A","B","C","D","E","F"]
subChart["values"]=["100","50","125","200","25","75"]

associatedData["a-chart"]=subChart

subChart2 = json.loads("{}")
subChart2["objectType"]="chart"
subChart2["name"]="Example 'line' chart "
subChart2["chartType"]="line"
subChart2["categories"]=["A","B","C","D","E","F"]
subChart2["values"]=["100","50","125","200","25","75"]
associatedData["a-chart2"]=subChart2



output = json.dumps(dataModel)

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
                        

