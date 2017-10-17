#import essentia
#from essentia.standard import *
#from essentia import pool
from OnsetDetectionFunc import OnsetDetectionF

file = open("testWAVS/testFile.txt","w")

for alpha in 0.3, 0.4, 0.5, 0.6:
	for silenceThreshold in 0.017, 0.02, 0.023, 0.026, 0.03:
		OCP,realOS= OnsetDetectionF('../ZOOM0006/ZOOM0006_Tr1.WAV', alpha, silenceThreshold)
		file.write("alpha = " + str(alpha) + "	silenceThreshold = " + str(silenceThreshold)+'\n' + str(OCP) + '\n'+ '\n')
		file.write("REAL ONSETS alpha = " + str(alpha) + "	silenceThreshold = " + str(silenceThreshold)+'\n' + str(realOS) + '\n'+ '\n')

file.close()