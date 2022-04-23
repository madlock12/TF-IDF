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
import string


# create tokens and remove stop words and lemmatize
def tokenize_remove_stopwords(data, stopwords):
    for character in string.punctuation:
        data.replace(character," ")

    retreaved = text_to_word_sequence(data)  # tokenize text file
    for i in range(len(stopwords)):
        if(stopwords[i] in retreaved):  # if specific stopwords is in token
            retreaved.remove(stopwords[i])  # removing stop words
    lemmatizer = WordNetLemmatizer()
    for i in range(len(retreaved)):
        retreaved[i] = lemmatizer.lemmatize(retreaved[i])
    return retreaved


def populate_index(vector,stopwords):
    index = dict()
    for i in vector:
        index.setdefault(i,[0])
        for j in range(448):
            index[i].append(0)

    for docno in range(1, 449):
        f = open("./Abstracts/Abstracts/"+str(docno) +
                 ".txt", "r")  # reading all 448 files
        if(f):
            data = (f.read())
            f.close()
            data=tokenize_remove_stopwords(data,stopwords)
            
            for i in vector:
                if(i in data):
                    index[i][docno]+=1
    print(index)

def newfile(stopwords):  # this function will create index and store it in the index.txt file
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
    print(vector)
    print(len(vector))
    populate_index(vector,stopwords)
    # f = open("index.txt", "w")#here we will store all indexes

    # f.close()


file = open("index.txt", "r")
if(file):  # if file exist
    filesize = os.path.getsize("index.txt")
    if(filesize == 0):  # file is empty hence we have to create index and store
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
    else:
        print("Stop Word file does not exist")
    newfile(stopwords)

f = open("index.txt", "r")
if(f):
    index = (f.read())
