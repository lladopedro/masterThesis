import essentia
import os
import json
from essentia.standard import *
from essentia import pool
import numpy as np
import csv

def featExtraction (inputFile):

    #fileName = inputFile
    fileName = inputFile
    SR = 44100

    #####   LOADING AUDIO
    loader = essentia.standard.MonoLoader(filename = fileName)
    audio = loader()

    ##### IMPORT ONSETS

    onsetsList = []
    onsets = []


    with open(fileName.split('.')[0]+'Onsets.txt', 'r') as f:
        onsetsList = f.readlines()
    
    for i in range(0,len(onsetsList)):
        onsets.append(float(str(onsetsList[i]).split("\n",1)[0]))


    ##### IMPORT OFFSETS

    offsetsList = []
    offsets = []

    with open(fileName.split('.')[0]+'Offsets.txt', 'r') as f:
        offsetsList = f.readlines()
    
    for i in range(0,len(offsetsList)):
        offsets.append(float(str(offsetsList[i]).split("\n",1)[0]))

    ##### CALCULATE ONSETS AND OFFSETS SAMPLES

    s_onsets=[]
    s_offsets=[]
    for i in range (0,len(onsets)): s_onsets.append(int(round(onsets[i]*SR,0)))
    for i in range (0,len(offsets)): s_offsets.append(int(round(offsets[i]*SR,0)))


    starts = []
    ends = []

    wmargin = int(round(0.1*SR))    #MARGIN FOR NOTES ISOLATION : 100 ms  
    note = []
    for i in range(0,len(s_onsets)):
        note.append(audio[s_onsets[i]-wmargin:s_offsets[i]+wmargin])
        starts.append((s_onsets[i]-wmargin)/float(SR))
        ends.append((s_offsets[i]+wmargin)/float(SR))

    duration = []
    for i in range(0,len(starts)): duration.append(ends[i]-starts[i])

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



    #w = Windowing(type = 'hann') #only for the spectrum
    #spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum

    #loader = essentia.standard.MonoLoader(filename = fileName)
    #audio = loader()
    pool = essentia.Pool()
    pool = extractor(note[0])   #to get all the descriptorNames
    aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)   #creating a pool for MEAN and VAR of descriptors


    ##### NEED JSON FILES?

    #JsonFile = str(fileName.rsplit('/',1)[0]) + '/resultTest.json'
    #JsonAggrFile = str(fileName.rsplit('/',1)[0]) + '/resultTestAggr.json'
    #YamlOutput(filename = JsonFile, format = "json")(pool)
    #YamlOutput(filename = JsonAggrFile, format="json")(aggrPool)


    ##### NOTES SENTENCE
    annotatedNote = []
    annotatedNote = ['la3', 'mi4', 'la4', 'do4', 'do3', 'fa3', 're4', 'mi4']


    ##### CSV FILES HEADERS

    fieldNames = pool.descriptorNames()
    #LOUDNESS RETURNS INDEX OUT OF BOUNDS
    fieldNames.remove("lowLevel.loudness")
    fieldNamesAggr = aggrPool.descriptorNames()


    fieldNamesCSV = []
    #fieldNamesCSV.append('Class')
    fieldNamesCSV.append('Note')
    fieldNamesCSV.append('Frame')    
    fieldNamesCSV.append('StartTime')
    fieldNamesCSV.append('EndingTime')
    fieldNamesCSV.append('Duration')
    for i in range(0,len(fieldNamesAggr)): fieldNamesCSV.append(fieldNamesAggr[i])
    for i in range(0,len(fieldNames)): fieldNamesCSV.append(fieldNames[i])
    fieldNamesCSV.append('Class')


    ##### WRITING CSV CONTENT
    with open(str(fileName.rsplit('/',1)[0]) + '/' + (fileName.split('_')[0]).split('/')[-1] + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldNamesCSV)
        for i in range(0, len(note)):
            pool = extractor(note[i])
            aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
            arrAggr = []
            for k in fieldNamesAggr: arrAggr.append(aggrPool[k])
            for j in range(0,len(note[i])/2048):
                arr = []
                #arr.append((fileName.split('_')[0]).split('/')[-1])
                arr.append(annotatedNote[i])
                arr.append(j)
                arr.append(starts[i])
                arr.append(ends[i])
                arr.append(duration[i])
                for t in range(0,len(arrAggr)):arr.append(arrAggr[t])
                for f in fieldNames:
                    arr.append(pool[f][j])
                arr.append((fileName.split('_')[0]).split('/')[-1])
                writer.writerow(arr)


    #ADD THE fieldNamesAggrCSV to write the needed columns!
    #ALREADY INTEGRATED IN test.csv

#    with open(str(fileName.rsplit('/',1)[0]) + '/testAggr.csv', 'w') as csvfile:
#        writer = csv.writer(csvfile)
#        writer.writerow(fieldNamesAggr)
#        for i in range(0, len(note)):
#            pool = extractor(note[i])
#            aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
#            arr = [aggrPool[f] for f in fieldNamesAggr]
#            writer.writerow(arr)

  


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
