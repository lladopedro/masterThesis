from OnsetDetectionFunc import OnsetDetectionF
from dataExplorer import fetchFiles

#####	RETURN PATH AND FILES NAMES OF ALL THE ".WAV" OF THE DIRECTORY

#listOfFiles = fetchFiles("/home/pedro/tfm/dataBase/",".wav")


#print listOfFiles[0][0] + '/' + listOfFiles[0][1]

#####	Essentia.OnsetDetection PARAMETER {hfc, complex, complex_phase, flux, melflux, rms}, default = hfc)
method = 'hfc'

#####	Essentia.Onsets PARAMETERS
alpha = 0.3
silenceThreshold = 0.04


#####	COMPUTE THE ONSETS

#for alpha in 0.3, 0.4, 0.5, 0.6:
#	for silenceThreshold in  0.03, 0.035, 0.04, 0.045, 0.05, 0.055:

Onsets,realOS= OnsetDetectionF(listOfFiles[0][0] + '/' + listOfFiles[0][1], method, alpha, silenceThreshold)


##### WRITE IN A TXT THE ONSETS DETECTED (PUT INTO THE SAME FOR UPWARDS IF NEEDED)

#file = open("results/testFile%s.txt" %method,"w")
#file.write("REAL ONSETS " +str(method) + " alpha = "  + str(alpha) + "	silenceThreshold = " + str(silenceThreshold)+'\n' + str(Onsets) + '\n'+ '\n')
#file.write("REAL ONSETS " +str(method) + " alpha = "  + str(alpha) + "	silenceThreshold = " + str(silenceThreshold)+'\n' + str(realOS) + '\n'+ '\n')
#file.close()