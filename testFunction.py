from OnsetDetectionFunc import OnsetDetectionF
from OffsetDetectionFunc2 import OfsetDetectionF
from dataExplorer import fetchFiles

#####	RETURN PATH AND FILES NAMES OF ALL THE ".WAV" OF THE DIRECTORY

listOfFiles = fetchFiles("/home/pedro/tfm/dataBase/",".wav")


##### DIRECTORY OF RESULTS
resultsDir = '/home/pedro/tfm/Results/'

#print listOfFiles[0][0] + '/' + listOfFiles[0][1]

#####	Essentia.OnsetDetection PARAMETER {hfc, complex, complex_phase, flux, melflux, rms}, default = hfc)
method = 'hfc'

#####	Essentia.Onsets PARAMETERS
alpha = 0.3
silenceThreshold = 0.04


#####	COMPUTE THE ONSETS

#for i in range (0,len(listOfFiles)):
#	Onsets,realOS= OnsetDetectionF(listOfFiles[i][0] + '/' + listOfFiles[i][1], method, alpha, silenceThreshold)


#####	COMPUTE THE OFFSETS

for i in range (0,len(listOfFiles)):
	print listOfFiles[i][0] + '/' + listOfFiles[i][1]
	realOffS= OfsetDetectionF(listOfFiles[i][0] + '/' + listOfFiles[i][1], method, alpha, silenceThreshold)
	

#####	WRITE IN A TXT THE ONSETS DETECTED AND SAVED INTO A TXT FOR SONIC VISUALISER

#	onsetsAnnotation = open( str(listOfFiles[i][0]) + '/' + str(listOfFiles[i][1]).split('.')[-2] + 'Onsets.txt', 'w' )
#	for i in range(0,len(realOS)-1):
#		onsetsAnnotation.write( str(realOS[i]) + "\n")
#	onsetsAnnotation.close()


##### WRITE IN A TXT THE ONSETS DETECTED (PUT INTO THE SAME FOR UPWARDS IF NEEDED)

#file = open("results/testFile%s.txt" %method,"w")
#file.write("REAL ONSETS " +str(method) + " alpha = "  + str(alpha) + "	silenceThreshold = " + str(silenceThreshold)+'\n' + str(Onsets) + '\n'+ '\n')
#file.write("REAL ONSETS " +str(method) + " alpha = "  + str(alpha) + "	silenceThreshold = " + str(silenceThreshold)+'\n' + str(realOS) + '\n'+ '\n')
#file.close()