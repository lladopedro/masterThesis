from DescriptorsExtractor import featExtraction
from dataExplorer import fetchFiles

listOfFiles = fetchFiles("/home/pedro/tfm/dataBase/CorrectedAudioSofia",".wav")

inputFile = listOfFiles[0][0]+'/'+listOfFiles[0][1]

print inputFile

featExtraction(inputFile)