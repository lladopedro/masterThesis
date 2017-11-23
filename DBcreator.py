from OnsetDetectionFunc import OnsetDetectionF
from OffsetDetectionFunc import OfsetDetectionF
from dataExplorer import fetchFiles

#####	RETURN PATH AND FILES NAMES OF ALL THE ".WAV" OF THE DIRECTORY

listOfFiles = fetchFiles("/home/pedro/tfm/dataBase/AudioSofia",".wav")


#####	Essentia.OnsetDetection PARAMETER {hfc, complex, complex_phase, flux, melflux, rms}, default = hfc)
method = 'hfc'

#####	Essentia.Onsets PARAMETERS
alpha = 0.3
silenceThreshold = 0.04


#####	COMPUTE THE ONSETS
listOfFilesRev = []


for i in range (0,len(listOfFiles)):
#	print listOfFiles[i][0] + '/' + listOfFiles[i][1]
	Onsets,realOS= OnsetDetectionF(listOfFiles[i][0] + '/' + listOfFiles[i][1], method, alpha, silenceThreshold)
	#####	WRITE IN A TXT THE ONSETS DETECTED AND SAVED INTO A TXT FOR SONIC VISUALISER
	onsetsAnnotation = open( str(listOfFiles[i][0]) + '/' + str(listOfFiles[i][1]).split('.')[-2] + 'Onsets.txt', 'w' )
	for k in range(0,len(realOS)-1):
		onsetsAnnotation.write( str(realOS[k]) + "\n")
	onsetsAnnotation.close()

##### OIDUA DIRECTORIES
	listOfFilesRev.append(listOfFiles[i][0].replace('Audio','Oidua'))



#####	COMPUTE THE OFFSETS

for i in range (0,len(listOfFiles)):
	offsets,osd = OfsetDetectionF(listOfFilesRev[i] + '/REV_' + listOfFiles[i][1],method, alpha, silenceThreshold)
	

#####	WRITE IN A TXT THE OFFSETS DETECTED AND SAVED INTO A TXT FOR SONIC VISUALISER

	offsetsAnnotation = open( str(listOfFiles[i][0]) + '/' + str(listOfFiles[i][1]).split('.')[-2] + 'Offsets.txt', 'w' )
	for j in range(0,len(offsets)-1):
		offsetsAnnotation.write( str(offsets[j]) + "\n")
	offsetsAnnotation.close()