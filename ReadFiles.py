from essentia.standard import *
import glob
import os
import numpy as np

path = 'ZOOM0006/'
extension = 'WAV'

def get_files_in_dir(dirname, extension):
    return glob.glob(os.path.join(dirname, "*.%s" % extension))

ListOfFIles = get_files_in_dir(path,extension)
audio = []

def main():

    for file_path in 0,len(ListOfFIles)-1:
	audio.append(MonoLoader(filename = ListOfFIles[file_path])())

return(audio)
