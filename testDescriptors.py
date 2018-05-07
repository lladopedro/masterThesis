from DescriptorsExtractor import featExtraction
from dataExplorer import fetchFiles

listOfFiles = fetchFiles("/home/pedro/tfm/dataBaseFull/CorrectedAudioSofia",".wav")

for i in range (0,len(listOfFiles)):
	print (listOfFiles[i][0]+'/'+listOfFiles[i][1])
	featExtraction(listOfFiles[i][0]+'/'+listOfFiles[i][1])
