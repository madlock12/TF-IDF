############################################################################################################
#                                    IR Assignment 1
#                                         TF*IDF 
#
#                                       19k1310
#                                   Mir Mubashir Ali
#                                       4/23/2022
############################################################################################################
import os
import spacy

def tokenize():#create tokens


def newfile():#this function will create index and store it in the index.txt file
    for docno in range(1,449):
        ff=open("./Abstracts/Abstracts/"+str(docno) +
             ".txt", "r")  # reading all 448 files
        if(ff):
            data=(ff.read())

    
    
    f=open("index.txt","w")



    f.close()

file=open("index.txt","r")
if(file):#if file exist
    filesize=os.path.getsize("index.txt")
    if(filesize==0):#file is empty hence we have to create index and store
        os.remove("index.txt")
        newfile()
else: #if file does not exist
    newfile()

f=open("index.txt","r")
if(f):
    index=(f.read())