import os


def fetchFiles(inputDir, fileType):

    INPUT_DIR = inputDir
    FT = fileType

    ListOfFiles = []


    for path,dir_names,files_names in os.walk(INPUT_DIR):
        for file_name in files_names:
            if FT in file_name.lower():
                ListOfFiles.append((path, file_name))

#    print ListOfFiles
    return(ListOfFiles)