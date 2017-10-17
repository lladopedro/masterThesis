import essentia
import numpy as np
from essentia.standard import *
from essentia import pool
import os

onsets_complex_phase = []

def OnsetDetectionF(fileName, alpha, silenceThreshold):
	
	#####	LOADING AUDIO
	loader = essentia.standard.MonoLoader(filename = fileName)
	audio = loader()
	ALP = alpha
	ST = silenceThreshold
	#####	PREPARING FUNCTIONS
	w = Windowing(type = 'hann')
	fft = FFT() 				# this gives us a complex FFT
	c2p = CartesianToPolar() 	# and this turns it into a pair (magnitude, phase)
	pool = essentia.Pool()
	onsets = Onsets(alpha=ALP,silenceThreshold=ST)# (alpha, silenceThreshold)			#alpha, silenceThreshold

	
	##### COMPUTING OnsetDetection ESSENTIA FUNCTION AND SAVING ON ESSENTIA POOL
	od = OnsetDetection(method='complex_phase')		#Many possible methods, but COMPLEX PHASE works well on bow string instruments.
	mag = []
	phase = []

	for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
		mag, phase, = c2p(fft(w(frame)))
		pool.add('features.complex_phase', od(mag, phase))

	
	#####COMPUTING ONSET FUNCTIONS USING OnsetDetection FUNCTION
	onsets_complex_phase = onsets(essentia.array([ pool['features.complex_phase'] ]), [ 1 ])

	#####FANTASIA
	realOnsets = []

	delidx = []
	for x in range(1,len(onsets_complex_phase)):
	    if (onsets_complex_phase[x] - onsets_complex_phase[x-1]) < 1:
	        delidx.append(x)
	realOnsets = np.delete(onsets_complex_phase,delidx)

	

	##### WRITE BEEP MARKERS ON THE AUDIO
	marker = []
	marker = AudioOnsetsMarker(onsets=onsets_complex_phase, type='beep')


	marked_audio = marker(audio)
	#MonoWriter(filename='testWAVS/onsets_complex_phase-a-a%s-st%s.wav'%(str(ALP),str(ST)))(marked_audio)

	return onsets_complex_phase,realOnsets