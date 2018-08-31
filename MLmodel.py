import sys

import java.io.FileReader as FileReader
import weka.core.Instances as Instances
import weka.classifiers#.rules.ZeroR as ZeroR
import weka.core.converters.CSVLoader as CSVLoader

import weka.core.converters.ConverterUtils.DataSource as DS
import os


from weka.classifiers import Classifier, SingleClassifierEnhancer, MultipleClassifiersCombiner #PredictionOutput, Kernel, KernelClassifier
import weka.classifiers.meta.FilteredClassifier
from weka.classifiers import Evaluation
from weka.filters import Filter
import java.util.Random as Random

import weka.attributeSelection.ASEvaluation as ASEvaluation
import weka.attributeSelection.ASSearch as ASSearch

#from weka.core.classes import Random, from_commandline
#import weka.plot.classifiers as plot_cls
#import weka.plot.graph as plot_graph
#import weka.core.types as types



print "Loading data..."
# load data
file = DS.read("/home/pedro/tfm/dataBaseFull/CorrectedAudioSofia/zzzWEKA/ZOOM00089_featSel.csv")
data = Instances(file)

numAttr = data.numAttributes()

   
# set the class Index - the index of the dependent variable
data.setClassIndex(data.numAttributes() - 1)

#removes strings if any to avoid incompatibilities
removeType = weka.filters.unsupervised.attribute.RemoveType()   

#The REAL classifier
MyClassifier = []
#MyClassifier.append(weka.classifiers.rules.ZeroR())
MyClassifier.append(weka.classifiers.rules.OneR())

print MyClassifier

#numAttr = -1
for i in range(0,len(MyClassifier)):
    for x in range(-1,numAttr):
    AtSelClsf = weka.classifiers.meta.AttributeSelectedClassifier()
    AtSelClsf.classifier = MyClassifier[i]
    AtSelClsf.setEvaluator(ASEvaluation.forName("InfoGainAttributeEval",None))
    AtSelClsf.setSearch(ASSearch.forName("Ranker",["-N", str(x)]))

    FiltClsf = weka.classifiers.meta.FilteredClassifier()
    FiltClsf.filter = removeType
    FiltClsf.classifier = AtSelClsf
    print (FiltClsf)
    
    # evaluation
    evl = Evaluation(data)
    evl.crossValidateModel(FiltClsf, data, 10, Random(1))
    
    print(str(evl.pctCorrect()) + " % correct\n")
    #print(evl.toSummaryString())
    #print(evl.toClassDetailsString())
    print(evl.toMatrixString())
    #print (evl.getHeader())
