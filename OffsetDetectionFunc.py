import essentia
import numpy as np
from essentia.standard import *
from essentia import pool
import os
import matplotlib.pyplot as plt


def OfsetDetectionF(fileName, method, alpha, silenceThreshold):
	
	print fileName
	#####	LOADING AUDIO
	loader = essentia.standard.MonoLoader(filename = fileName)
#	loader = essentia.standard.MonoLoader(filename = '/home/pedro/tfm/dataBase/AudioSofia/ZOOM0007/REV_ZOOM0007_Tr1.wav')
	oidua = loader()

	ALP = alpha
	ST = silenceThreshold
	METHOD = method
	#DELAY = delay

	
	#####	PREPARING FUNCTIONS
	w = Windowing(type = 'hann')
	fft = FFT() 				# this gives us a complex FFT
	c2p = CartesianToPolar() 	# and this turns it into a pair (magnitude, phase)
	pool = essentia.Pool()
	onsets = Onsets(alpha=ALP,silenceThreshold=ST)# (alpha, silenceThreshold)			#alpha, silenceThreshold



	#####	COMPUTING OnsetDetection ESSENTIA FUNCTION AND SAVING ON ESSENTIA POOL
	od = OnsetDetection(method=METHOD)		#Many possible methods, but COMPLEX PHASE works well on bow string instruments.
	mag = []
	phase = []



	for frame in FrameGenerator(oidua, frameSize = 1024, hopSize = 512):
		mag, phase = c2p(fft(w(frame)))
		pool.add('features', od(mag, phase))

	
	#####	COMPUTING ONSET FUNCTIONS USING OnsetDetection FUNCTION
	onsets_detected = onsets(essentia.array([ pool['features'] ]), [ 1 ])

	#####	DELETING REPEATED MARKERS (If two markers are too close [min_delay], then only keep the first one)
	realOnsets_detected = []
	delidx = []
	min_delay = 1	#min_delay is the minimum delay between onsets
	for z in range(1,len(onsets_detected)):
	    if (onsets_detected[z] - onsets_detected[z-1]) < min_delay:
	        delidx.append(z)
	realOnsets_detected = np.delete(onsets_detected,delidx)
	

	##### CORRECTING OFFSET TIME FOR AUDIO (COMPUTED WITH REVERSED AUDIO)

	offsets = []
	for i in range(0,len(realOnsets_detected)):
		offsets.append( len(oidua)/float(44100) - realOnsets_detected[i] )


	offsets = offsets[::-1]

	return offsets, realOnsets_detected