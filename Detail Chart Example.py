
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


associatedData["text info"]="short text"
associatedData["number info"]=100.23
associatedData["small array"]=[1,2,3,4,5]
associatedData["small 2darray"]=[[1,2],[2,3],[3,3],[4,5],[5,6]]

associatedData["big text"]="This is a much larger text entry\r\ncontaining carriage returns and line feeds\r\nmore than one containing carriage return and line feed to be precise. it also wraps sentences"

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


subChart5 = json.loads("{}")
subChart5["objectType"]="chart"
subChart5["name"]="pie chart"
subChart5["chartType"]="pie"
subChart5["categories"]=["A","B","C","D","E","F"]
subChart5["values"]=[100,50,125,200,25,75]
associatedData["a-chart5"]=subChart5

associatedData["some-json"] = subChart4["values"]



subChart6 = json.loads("{}")
subChart6["objectType"]="chart"
subChart6["name"]="xy scatter graph"
subChart6["chartType"]="xyscatter"
subChart6["x"]=[50,25,60,110,10,30]
subChart6["y"]=[100,50,125,200,25,75]
associatedData["a-chart6"]=subChart6


subChart7 = json.loads("{}")
subChart7["objectType"]="chart"
subChart7["name"]="xy scatter graph with z line"
subChart7["chartType"]="xyscatterxzline"
subChart7["x"]=[50,25,60,110,10,30]
subChart7["y"]=[100,50,125,200,25,75]
subChart7["z"]=[100,50,120,220,20,60]
associatedData["a-chart7"]=subChart7



output = json.dumps(dataModel)

oFile = open(outputfile, 'w',encoding='utf8') #write to file
oFile.write(output) 
oFile.close()
                        

