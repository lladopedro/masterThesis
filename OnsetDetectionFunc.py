import essentia

from essentia.standard import *
from essentia import pool


def OnsetDetectionF(fileName):
	
	#####	LOADING AUDIO
	loader = essentia.standard.MonoLoader(filename = fileName)
	audio = loader()

	#####	PREPARING FUNCTIONS
	w = Windowing(type = 'hann')
	fft = FFT() 				# this gives us a complex FFT
	c2p = CartesianToPolar() 	# and this turns it into a pair (magnitude, phase)
	pool = essentia.Pool()
	onsets = Onsets(alpha=0.6) 			#no parameter needed for basic result. These ones work well for the test audio but need to be checked.

	
	##### COMPUTING OnsetDetection ESSENTIA FUNCTION AND SAVING ON ESSENTIA POOL
	od = OnsetDetection(method='complex_phase')		#Many possible methods, but COMPLEX PHASE works well on bow string instruments.

	for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
		mag, phase, = c2p(fft(w(frame)))
		pool.add('features.complex_phase', od(mag, phase))

	#####COMPUTING ONSET FUNCTIONS USING OnsetDetection FUNCTION
	onsets_complex_phase = onsets(essentia.array([ pool['features.complex_phase'] ]), [ 1 ])

	##### WRITE BEEP MARKERS ON THE AUDIO
	marker = AudioOnsetsMarker(onsets=onsets_complex_phase, type='beep')
	marked_audio = marker(audio)
	MonoWriter(filename='onsets_complex_phase.wav')(marked_audio)

