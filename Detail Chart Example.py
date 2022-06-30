
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
subChart["name"]="simple bar chart"
subChart["chartType"]="bar"
subChart["categories"]=["A","B","C","D","E","F"]
subChart["values"]=[100,50,125,200,25,75]
associatedData["a-chart"]=subChart

subChart2 = json.loads("{}")
subChart2["objectType"]="chart"
subChart2["name"]="simple line chart"
subChart2["chartType"]="line"
subChart2["categories"]=["A","B","C","D","E","F"]
subChart2["values"]=[10,250,25,100,125,5]
associatedData["a-chart2"]=subChart2

subChart3 = json.loads("{}")
subChart3["objectType"]="chart"
subChart3["name"]="multi series chart 1-axis"
subChart3["chartType"]="multivalue"
subChart3["categories"]=["A","B","C","D","E","F"]
subChart3["values"]=  json.loads('{"axes":[{"values":[10,250,25,100,125,5],"axisType":"bar","axis":0},{"values":[10,250,25,100,125,5],"axisType":"line","axis":0}]}')
associatedData["a-chart3"]=subChart3


subChart4 = json.loads("{}")
subChart4["objectType"]="chart"
subChart4["name"]="multi series chart 2-axis"
subChart4["chartType"]="multivalue"
subChart4["categories"]=["A","B","C","D","E","F"]
subChart4["values"]=  json.loads('{"axes":[{"values":[10,250,25,100,125,5],"axisType":"bar","axis":0},{"values":[100,500,250,1100,1125,115],"axisType":"line","axis":1}]}')
associatedData["a-chart4"]=subChart4


output = json.dumps(dataModel)

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
                        

