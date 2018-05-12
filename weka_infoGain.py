import sys
import java.io.FileReader as FileReader
import weka.core.Instances as Instances
import weka.core.converters.ConverterUtils.DataSource as DS
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

   
##### set the class Index - the index of the dependent variable
data.setClassIndex(data.numAttributes() - 1)

##### removes strings if any to avoid incompatibilities

removeType = weka.filters.unsupervised.attribute.RemoveType()   


##### We append the desired classifiers in MyClassifier array

MyClassifier = []

#MyClassifier.append(weka.classifiers.rules.ZeroR())
MyClassifier.append(weka.classifiers.rules.OneR())




##### We evaluate all the desired classifiers with different numbers of attributes to quantify the attribute selection and decide how many attributes we do need

for i in range(0,len(MyClassifier)): #Computing with each classifier
    
    for x in range(-1,numAttr):      #Computing the infoGain depending on the number of Attributes
        
        #We use a Attribute Selected Classifier
        AtSelClsf = weka.classifiers.meta.AttributeSelectedClassifier()
        AtSelClsf.classifier = MyClassifier[i]                                      #We set the current classifier
        AtSelClsf.setEvaluator(ASEvaluation.forName("InfoGainAttributeEval",None))  #We set the Evaluator of the Attribute Selector
        AtSelClsf.setSearch(ASSearch.forName("Ranker",["-N", str(x)]))              #We set the Search Method of the Attribute Selector
    
        ##### We filter just in case some string disturbs the measurements
        
        FiltClsf = weka.classifiers.meta.FilteredClassifier()                       
        FiltClsf.filter = removeType
        FiltClsf.classifier = AtSelClsf
        print (FiltClsf)
        
        ##### Evaluation of the model with crossvalidation
        
        evl = Evaluation(data)
        evl.crossValidateModel(FiltClsf, data, 10, Random(1))
        
        ##### Printing results
        
        print(str(evl.pctCorrect()) + " % correct\n")
        #print(evl.toSummaryString())
        #print(evl.toClassDetailsString())
        print(evl.toMatrixString())
        #print (evl.getHeader())
