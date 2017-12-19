import essentia
import os
import json
from essentia.standard import *
from essentia import pool
import numpy as np
import csv


def featExtraction (inputFile)

    #fileName = inputFile
    fileName = '/tfm/dataBase/CorrectedAudioSofia/ZOOM0007/ZOOM0007_Tr1.WAV'
    SR = 44100

    #####   LOADING AUDIO
    loader = essentia.standard.MonoLoader(filename = fileName)
    audio = loader()

    ##### IMPORT ONSETS

    onsetsList = []
    onsets = []

    with open('/home/pedro/tfm/dataBase/CorrectedAudioSofia/ZOOM0007/ZOOM0007_Tr1Onsets.txt', 'r') as f:
        onsetsList = f.readlines()
    
    for i in range(0,len(onsetsList)):
        onsets.append(float(str(onsetsList[i]).split("\n",1)[0]))


    ##### IMPORT ONSETS

    offsetsList = []
    offsets = []

    with open('/home/pedro/tfm/dataBase/CorrectedAudioSofia/ZOOM0007/ZOOM0007_Tr1Offsets.txt', 'r') as f:
        offsetsList = f.readlines()
    
    for i in range(0,len(offsetsList)):
        offsets.append(float(str(offsetsList[i]).split("\n",1)[0]))

    ##### CALCULATE ONSETS AND OFFSETS SAMPLES

    s_onsets=[]
    s_offsets=[]
    for i in range (0,len(onsets)): s_onsets.append(int(round(onsets[i]*SR,0)))
    for i in range (0,len(offsets)): s_offsets.append(int(round(offsets[i]*SR,0)))


    wmargin = int(round(0.1*SR))    #MARGIN FOR NOTES ISOLATION : 100 ms  
    note = []
    for i in range(0,len(s_onsets)):
        note.append(audio[s_onsets[i]-wmargin:s_offsets[i]+wmargin])



    extractor = Extractor(dynamics = True,
                        dynamicsFrameSize = 88200,
                        dynamicsHopSize = 44100,
                        highLevel = False,
                        lowLevel = True,
                        lowLevelFrameSize = 4096,
                        lowLevelHopSize = 2048,
                        midLevel = False,
                        namespace = "",
                        relativeIoi = False,
                        rhythm = False,
                        sampleRate  = 44100,
                        tonalFrameSize  = 4096,
                        tonalHopSize = 2048,
                        tuning = False)

    JsonFile = '/home/pedro/tfm/dataBase/CorrectedAudioSofia/ZOOM0007/resultTest.json'
    JsonAggrFile = '/home/pedro/tfm/dataBase/CorrectedAudioSofia/ZOOM0007/resultTestAggr.json'

    #w = Windowing(type = 'hann') #only for the spectrum
    #spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum

    #loader = essentia.standard.MonoLoader(filename = fileName)
    #audio = loader()
    pool = essentia.Pool()
    pool = extractor(note[0])   #to get all the descriptorNames
    aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)   #creating a pool for MEAN and VAR of descriptors
    #YamlOutput(filename = JsonFile, format = "json")(pool)
    #YamlOutput(filename = JsonAggrFile, format="json")(aggrPool)




    ##### WRITING CSV FILES

    fieldNames = pool.descriptorNames()[0:4]
    fieldNamesAggr = aggrPool.descriptorNames()[0:8]


    with open('/home/pedro/tfm/dataBase/CorrectedAudioSofia/ZOOM0007/test.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldNames)
        for i in range(0, len(note)):
            pool = extractor(note[i])
            for j in range(0,10):#len(note[i]/2048 +2)):
                arr = [pool[f][j] for f in fieldNames]
                writer.writerow(arr)


  


    ############

#def main():
#    data = fetchFiles(inputDir)
#    extract_mfcc(data)

#def extract_mfcc(ListOfFiles):
#
#    w = Windowing(type = 'hann')
#    spectrum = Spectrum()
#    mfcc = MFCC()

#    for path, file in ListOfFiles:
#        file_name, extension = os.path.splitext(file)
#        file_location = path + "/" + file
#        print file_location

        #computing mfcc
#        loader = essentia.standard.MonoLoader(filename = file_location)
#        audio = loader()
#        pool = essentia.Pool()
#        for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512, startFromZero=True):
#            mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
#            pool.add('lowlevel.mfcc', mfcc_coeffs)
#            pool.add('lowlevel.mfcc_bands', mfcc_bands)

        # saving Mfcc per frame.
        # YamlOutput(filename = path + "/"+ file_name + ".json", format = "json")(pool) t
        # saving Mfcc aggregated per audio file
#        aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
#        YamlOutput(filename = path + "/"+ file_name + ".json", format = "json")(aggrPool)

#extractFeatures from one file


if __name__ == "__main__":
    main()
