import sys
sys.path.append("/usr/share/java/ij.jar")
from ij import *
from ij.gui import Plot
import csv
import java.io.FileReader as FileReader
import weka.core.Instances as Instances
import weka.core.converters.ConverterUtils.DataSource as DSave
import weka.core.converters.ConverterUtils.DataSink as DSink
from weka.classifiers import Classifier, SingleClassifierEnhancer, MultipleClassifiersCombiner #PredictionOutput, Kernel, KernelClassifier
import weka.classifiers.meta.FilteredClassifier
from weka.classifiers import Evaluation
from weka.filters import Filter
import java.util.Random as Random
import weka.attributeSelection.ASEvaluation as ASEvaluation
import weka.attributeSelection.ASSearch as ASSearch
from jarray import array
from java.awt import Color
#import java.io.Serializable.Saver.setDir
import weka.core.converters.AbstractSaver

#import weka.plot.classifiers as plot_cls
import weka.gui.visualize as visualize
#import weka.plot.graph as plot_graph
#import weka.core.types as types



print "Loading data..."
# load data

file_path = "/home/pedro/tfm/dataBaseFull/CorrectedAudioSofia/zzzWEKA/ZOOM00089_featSel.csv"
print str(file_path).split('.')[0]
file = DSave.read(file_path)
data = Instances(file)

numAttr = data.numAttributes()
maxNumAt = 15     #number of Attributes we want to test now
   
##### set the class Index - the index of the dependent variable
data.setClassIndex(data.numAttributes() - 1)

##### removes strings if any to avoid incompatibilities

removeType = weka.filters.unsupervised.attribute.RemoveType()   


##### We append the desired classifiers in MyClassifier array


MyClassifier = []

#MyClassifier.append(weka.classifiers.rules.ZeroR())
MyClassifier.append(weka.classifiers.rules.OneR())
MyClassifier.append(weka.classifiers.trees.J48())
MyClassifier.append(weka.classifiers.functions.Logistic())
MyClassifier.append(weka.classifiers.functions.SMO())

print (MyClassifier[0].getClass())

print ()

my_file = open(str('/home/pedro/tfm/Results/' + str(file_path).split('/')[-1].split('.')[0]) + ".csv",'w')
headers = []
for j in range(1,maxNumAt): headers.append("Acc w/ %d att." %j)
CSVtitle = "Classifier", headers
my_file.write(str(CSVtitle) + "\n")


##### We evaluate all the desired classifiers with different numbers of attributes to quantify the attribute selection and decide how many attributes we do need

for i in range(0,len(MyClassifier)): #Computing with each classifier
    
    infoGainCurve = []               #Array for infoGain curve representation
    
    for x in range(1,maxNumAt+1):    #numAttr-1):      #Computing the infoGain depending on the number of Attributes
        
        #We use a Attribute Selected Classifier
        AtSelClsf = weka.classifiers.meta.AttributeSelectedClassifier()
        AtSelClsf.classifier = MyClassifier[i]                                      #We set the current classifier
        #AtSelClsf.setEvaluator(ASEvaluation.forName("InfoGainAttributeEval",None))  #We set the Evaluator of the Attribute Selector
        AtSelClsf.setEvaluator(ASEvaluation.forName("CfsSubsetEval",None))
        #AtSelClsf.setSearch(ASSearch.forName("Ranker",["-N", str(x)]))              #We set the Search Method of the Attribute Selector
        AtSelClsf.setSearch(ASSearch.forName("GreedyStepwise",["-R","-N", str(x)]))
    
        ##### We filter just in case some string disturbs the measurements
        
        FiltClsf = weka.classifiers.meta.FilteredClassifier()                       
        FiltClsf.filter = removeType
        FiltClsf.classifier = AtSelClsf
        #print (FiltClsf)
        
        ##### Evaluation of the model with crossvalidation
        
        evl = Evaluation(data)
        evl.crossValidateModel(FiltClsf, data, 10, Random(1))
        
        ##### Printing results
        
        print(str(evl.pctCorrect()) + " % correct with " + str(x) + " attributes.\n")
        print(evl.toSummaryString())
        #print(evl.toClassDetailsString())
        print(evl.toMatrixString())
        
        
        infoGainCurve.append(evl.pctCorrect())
    print (infoGainCurve)
    

    ##### PLOT

    x_val = []
    for k in range (1,maxNumAt+1):x_val.append(k)
    xArr = array(x_val, 'd')
    yArr = array(infoGainCurve,'d') 
    plot = Plot("%s" %str(MyClassifier[i].getClass()).split("'")[1], "Number of Attributes", "Accuracy %")
    plot.setLimits(0.0, numAttr+1 ,50, 100.0)
    plot.setColor(Color.RED)
    plot.addPoints(xArr,yArr, Plot.LINE)
    plot.show()
    

    my_file.write(str(MyClassifier[i].getClass()).split("'")[1] + "," + str(infoGainCurve) + "\n")
    

    

    #print(data.type())
    #print(output.type())
    #SaveFile = DSink("/home/pedro/Descargas/test.csv")
    #SaveFile.write(output)
    #DSink.main(["/home/pedro/Descargas/test.csv", str(infoGainCurve)])


my_file.close()
