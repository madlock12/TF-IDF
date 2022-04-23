############################################################################################################
#                                    IR Assignment 1
#                                         TF*IDF
#
#                                       19k1310
#                                   Mir Mubashir Ali
#                                       4/23/2022
############################################################################################################
import os
from keras.preprocessing.text import text_to_word_sequence
from nltk.stem import WordNetLemmatizer

def tokenize_remove_stopwords(data):  # create tokens and remove stop words and lemmatize
    f = open("Stopword-List.txt", 'r')
    if(f):
        temp = (f.read())
        f.close()
        stopwords = text_to_word_sequence(temp)
    else:
        print("Stop Word file does not exist")

    retreaved = text_to_word_sequence(data)  # tokenize text file

    for i in range(len(stopwords)):
        if(stopwords[i] in retreaved):  # if specific stopwords is in token
            retreaved.remove(stopwords[i])  # removing stop words
    lemmatizer=WordNetLemmatizer()
    for i in range (len(retreaved)):
        retreaved[i]=lemmatizer.lemmatize(retreaved[i])
    return retreaved


def newfile():  # this function will create index and store it in the index.txt file
    for docno in range(1, 2):
        ff = open("./Abstracts/Abstracts/"+str(docno) +
                  ".txt", "r")  # reading all 448 files
        if(ff):
            data = (ff.read())
            ff.close()
            retreaved = tokenize_remove_stopwords(data)#now we will get a list with stopword removed+lemmatized
            
    # f = open("index.txt", "w")#here we will store all indexes

    # f.close()


file = open("index.txt", "r")
if(file):  # if file exist
    filesize = os.path.getsize("index.txt")
    if(filesize == 0):  # file is empty hence we have to create index and store
        newfile()
else:  # if file does not exist
    newfile()

f = open("index.txt", "r")
if(f):
    index = (f.read())
