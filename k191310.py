############################################################################################################
#                                    IR Assignment 1
#                                         TF*IDF
#
#                                       19k1310
#                                   Mir Mubashir Ali
#                                       4/23/2022
############################################################################################################
import os
from pydoc import doc
from keras.preprocessing.text import text_to_word_sequence


def tokenize_remove_stopwords(data):  # create tokens and remove stop words
    f = open("Stopword-List.txt", 'r')
    if(f):
        temp = (f.read())
        stopwords = text_to_word_sequence(temp)
    else:
        print("Stop Word file does not exist")

    retreaved = text_to_word_sequence(data)  # tokenize text file

    for i in range(len(stopwords)):
        if(stopwords[i] in retreaved):  # if specific stopwords is in token
            retreaved.remove(stopwords[i])  # removing stop words
    return retreaved


def newfile():  # this function will create index and store it in the index.txt file
    for docno in range(1, 449):
        ff = open("./Abstracts/Abstracts/"+str(docno) +
                  ".txt", "r")  # reading all 448 files
        if(ff):
            data = (ff.read())
            retreaved = tokenize_remove_stopwords(data)

    f = open("index.txt", "w")

    f.close()


file = open("index.txt", "r")
if(file):  # if file exist
    filesize = os.path.getsize("index.txt")
    if(filesize == 0):  # file is empty hence we have to create index and store
        os.remove("index.txt")
        newfile()
else:  # if file does not exist
    newfile()

f = open("index.txt", "r")
if(f):
    index = (f.read())
