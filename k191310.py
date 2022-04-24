############################################################################################################
#                                    IR Assignment 1
#                                         TF*IDF
#
#                                       19k1310
#                                   Mir Mubashir Ali
#                                       4/23/2022
############################################################################################################
from multiprocessing.sharedctypes import Value
import os
from this import s
from keras.preprocessing.text import text_to_word_sequence
from nltk.stem import WordNetLemmatizer
import string
import numpy as np
import json
from os.path import exists

# create tokens and remove stop words and lemmatize


# ____________________________use re____________________________
def tokenize_remove_stopwords(data, stopwords):
    for character in string.punctuation:
        data.replace(character, '')
        data.replace("'", '')
        data.replace("/", '')
        data.replace("\\", '')

    retreaved = text_to_word_sequence(data)  # tokenize text file
    for i in range(len(stopwords)):
        if(stopwords[i] in retreaved):  # if specific stopwords is in token
            retreaved.remove(stopwords[i])  # removing stop words
    lemmatizer = WordNetLemmatizer()
    for i in range(len(retreaved)):
        retreaved[i] = lemmatizer.lemmatize(retreaved[i])
    return retreaved


def populate_index(vector, stopwords):
    index = dict()
    # initializing the main index vector that will be storing VSM including (Tf,IDF,Documentfreq,TF*IDF)
    for i in vector:
        index.setdefault(i, {})
        index[i].setdefault("TF", [])
        index[i].setdefault("DocumentFreq", 0)
        index[i].setdefault("IDF", 0)
        index[i].setdefault("TF*IDF", [])
        for j in range(448):
            index[i]["TF"].append(0)
            index[i]["TF*IDF"].append(0)

    for docno in range(1, 449):
        f = open("./Abstracts/Abstracts/"+str(docno) +
                 ".txt", "r")  # reading all 448 files
        if(f):
            data = (f.read())
            f.close()
            data = tokenize_remove_stopwords(data, stopwords)

            for i in data:
                index[i]["TF"][docno-1] += 1
        else:
            print("File failed to open")

    DF = 0
    for i in vector:
        for docno in range(448):  # counting document freq and IDF
            if(index[i]["TF"][docno] != 0):
                DF += 1
        index[i]["DocumentFreq"] = DF
        DF = 0
        index[i]["IDF"] = np.log10(index[i]["DocumentFreq"])/448  # log(df/N)

        for docno in range(448):  # calculating TF*IDF simultaionsly to reduce running cost
            if(index[i]["TF"][docno] != 0):
                index[i]["TF*IDF"][docno] = index[i]["TF"][docno]*index[i]["IDF"]
            else:
                index[i]["TF*IDF"][docno] = 0

    return (index)


def newfile(stopwords):  # this function will create index and store it in the index.json file
    vector = []
    for docno in range(1, 449):
        ff = open("./Abstracts/Abstracts/"+str(docno) +
                  ".txt", "r")  # reading all 448 files
        if(ff):
            data = (ff.read())
            ff.close()
            # now we will get a list with stopword removed+lemmatized
            retreaved = tokenize_remove_stopwords(data, stopwords)
            for i in retreaved:
                if(i not in vector):
                    vector.append(i)

    print("Number of unique terms: ", len(vector))
    index = populate_index(vector, stopwords)

    with open('index.json', 'w') as cf:
        json.dump(index, cf, indent=4)


def Mag(vec):  # this is a utility function to calculate magnitude and return
    temp = np.array(vec)
    mag = np.linalg.norm(temp)
    return mag


def dotproduct(vec1, vec2):
    temp1 = np.array(vec1)
    temp2 = np.array(vec2)
    dotp = np.dot(temp1, temp2)
    return dotp


def calrank(dv, qv):
    rank = []
    mq = Mag(qv)
    md = 0
    if(mq != 0):
        for i in range(448):
            md = Mag(dv[i])
            temp = ((dotproduct(dv[i], qv)) / (md*mq))
            if(temp>=0.05):
                rank.append(i+1)
    else:
        print("No such term exist!!!")
    
    rank.sort(reverse=True)
    return rank

file = exists("index.json")
if(file):  # if file exist
    filesize = os.path.getsize("index.json")
    if(filesize == 0):  # file is empty hence we have to create index and store
        print("Empty File")
        f = open("Stopword-List.txt", 'r')
        if(f):
            temp = (f.read())
            f.close()
            stopwords = text_to_word_sequence(temp)
        else:
            print("Stop Word file does not exist")
        newfile(stopwords)
else:  # if file does not exist
    f = open("Stopword-List.txt", 'r')
    if(f):
        temp = (f.read())
        f.close()
        stopwords = text_to_word_sequence(temp)
        del temp
    else:
        print("Stop Word file does not exist")
    newfile(stopwords)

with open("index.json", "r") as read_file:
    index = json.load(read_file)
print(index)


f = open("Stopword-List.txt", 'r')
if(f):
    temp = (f.read())
    f.close()
    stopwords = text_to_word_sequence(temp)
    del temp

query = input("Enter Query: ")
vector = list(index.keys())
queryindex = {}
queryvec = []
for i in range(len(vector)):
    queryvec.append(0)

for i in (vector):
    queryindex.setdefault(i, {})
    queryindex[i].setdefault("TF", 0)
    queryindex[i].setdefault("TF*IDF", 0)

query = tokenize_remove_stopwords(query, stopwords)

for i in query:
    queryindex[i]["TF"] += 1  # this will calculate query term freq

for i in query:
    # this will create a basic vector on which we will apply cos similarity
    queryindex[i]["TF*IDF"] = queryindex[i]["TF"]*index[i]["IDF"]
# print(queryindex)

for i in query:
    queryvec[vector.index(i)] = queryindex[i]["TF*IDF"]
# print(queryvec)

# make a vector for each document now
docvec = {}
for i in range(448):
    docvec.setdefault(i, [])
    for j in range(len(vector)):
        docvec[i].append(0)
print("Length of vector is: ", len(vector))
for i in range(448):
    loc = 0
    for j in vector:
        docvec[i][loc] = index[j]["TF*IDF"][i]
        loc += 1

print(calrank(docvec,queryvec))