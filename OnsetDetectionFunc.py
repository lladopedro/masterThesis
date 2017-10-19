import essentia
import numpy as np
from essentia.standard import *
from essentia import pool
import os

onsets_complex_phase = []

def OnsetDetectionF(fileName, method, alpha, silenceThreshold):
	
	#####	LOADING AUDIO
	loader = essentia.standard.MonoLoader(filename = fileName)
	audio = loader()
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

	for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
		mag, phase, = c2p(fft(w(frame)))
		pool.add('features', od(mag, phase))
	
	#####	COMPUTING ONSET FUNCTIONS USING OnsetDetection FUNCTION
	onsets_detected = onsets(essentia.array([ pool['features'] ]), [ 1 ])

	#####	DELETING REPEATED MARKERS (If two markers are too close [min_delay], then only keep the first one)
	realOnsets = []
	delidx = []
	min_delay = 1	#min_delay is the minimum delay between onsets
	for x in range(1,len(onsets_detected)):
	    if (onsets_detected[x] - onsets_detected[x-1]) < min_delay:
	        delidx.append(x)
	realOnsets = np.delete(onsets_detected,delidx)

	

	#####	WRITE BEEP MARKERS ON THE AUDIO
	#marker = []
	#marker = AudioOnsetsMarker(onsets=onsets_detected, type='beep')
	#marked_audio = marker(audio)
	#MonoWriter(filename='results/onsets_detected-a%s-st%s-%s.wav'%(str(ALP),str(ST),str(METHOD)))(marked_audio)


	#####	WRITE BEEPS ON MODIFIED MARKERS
	realMarker = []
	realMarker = AudioOnsetsMarker(onsets=realOnsets, type='beep')
	realMarked_audio = realMarker(audio)

	#####	SAVING DIR AND FILE NAMES

	fileDir = fileName.rsplit('/', 1)[-2]

	fileName_only = fileName.rsplit('/', 1)[-1]
	fileName_only = fileName_only.rsplit('.', 1)[-2]
	resultsDir = '/home/pedro/tfm/Results/'

#	print fileName_only
#	print fileDir
#	print fileDir + '/realonsets_detected-a%s-st%s-%s.wav'%(str(ALP),str(ST),str(METHOD))
	print resultsDir + fileName_only + '-a%s-st%s-%s.wav'%(str(ALP),str(ST),str(METHOD))
	MonoWriter(filename= resultsDir + fileName_only + '-a%s-st%s-%s.wav'%(str(ALP),str(ST),str(METHOD)))(realMarked_audio)


	return onsets_detected,realOnsets