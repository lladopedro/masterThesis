import essentia
import os
import json
from essentia.standard import *
from essentia import pool
import numpy as np
import csv



def fetchFiles(inputDir = '/home/pedro/TFM/ZOOM0006/', fileType=".wav"):
    ListOfFiles = []
    for path,dir_names,files_names in os.walk(inputDir):
        for file_name in files_names:
            if fileType in file_name.lower():
                ListOfFiles.append((path, file_name))
    return(ListOfFiles)



def extract_mfcc(ListOfFiles):

    w = Windowing(type = 'hann')
    spectrum = Spectrum()
    mfcc = MFCC()

    for path, file in ListOfFiles:
        file_name, extension = os.path.splitext(file)
        file_location = path + "/" + file
        print file_location

        #computing mfcc
        loader = essentia.standard.MonoLoader(filename = file_location)
        audio = loader()
        pool = essentia.Pool()
        for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512, startFromZero=True):
            mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
            pool.add('lowlevel.mfcc', mfcc_coeffs)
            pool.add('lowlevel.mfcc_bands', mfcc_bands)

        # saving Mfcc per frame.
        # YamlOutput(filename = path + "/"+ file_name + ".json", format = "json")(pool) t
        # saving Mfcc aggregated per audio file
        aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
        YamlOutput(filename = path + "/"+ file_name + ".json", format = "json")(aggrPool)

#extractFeatures from one file

def extractFeatures(fileName):

    extractor = Extractor(dynamics = True,
                        dynamicsFrameSize = 88200,
                        dynamicsHopSize = 44100,
                        highLevel = True,
                        lowLevel = True,
                        lowLevelFrameSize = 4096,
                        lowLevelHopSize = 2048,
                        midLevel = True,
                        namespace = "",
                        relativeIoi = False,
                        rhythm = True,
                        sampleRate  = 44100,
                        tonalFrameSize  = 4096,
                        tonalHopSize = 2048,
                        tuning = True)

    JsonFile = '/home/pedro/TFM/ZOOM0006/resultTest.json'
    JsonAggrFile = '/home/pedro/TFM/ZOOM0006/resultTestAggr.json'

    #w = Windowing(type = 'hann') #only for the spectrum
    #spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum

    loader = essentia.standard.MonoLoader(filename = fileName)
    audio = loader()
    pool = essentia.Pool()
    pool = extractor(audio)
    #for frame in FrameGenerator(audio, frameSize = 4096, hopSize = 2048, startFromZero=False):
    #    pool.add('lowLevel.spectrum', spectrum(w(frame)))

    aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
    YamlOutput(filename = JsonFile, format = "json")(pool)
    YamlOutput(filename = JsonAggrFile, format="json")(aggrPool)


    ############ CSV
    with open('/home/pedro/TFM/ZOOM0006/ZOOM0006_Tr1.csv', 'w') as file:
        writer = csv.writer(file)
        for item in pool.descriptorNames():
            writer.writerow([pool[item]])
    ############

#def main():
#    data = fetchFiles(inputDir)
#    extract_mfcc(data)


if __name__ == "__main__":
    main()
