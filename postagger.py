import nltk
import json
from itertools import permutations


#word tokenizer NLTK m. = 1 token
#sdgkn data yg digunakan m.= 2 token(m dan .)

#tiap kata di sentence diberi tag
def getSentenceTags():
    result = []
    kalimat = []
    c=0
    with open('file.txt') as data:
        while True:
            tag = []
            sentence_id= data.readline()
            sentence_id= sentence_id.lower()
            if(len(sentence_id.strip())==0):
                continue
            if "#eof" in sentence_id:
                break
            sentence = ""
            if("#" in sentence_id):
                if("# text" in sentence_id):
                    c+=1
                    x = sentence_id.split("# text = ")
                    x = nltk.word_tokenize(x[1])
                    x.insert(0, "<start>")
                    kalimat.append(x)
                    for m in range(len(x)):
                        y = data.readline()
                        if ("#" in y):
                            break
                        y = y.replace("\n", "")
                        y = y.split("\t")
                        if(len(y)<3):
                            continue
                        if(y[2]=="_"):
                            tagnya = y[3]
                        else:
                            tagnya = y[2]
                        tag.append(tagnya)
                    result.append(tag)
    return kalimat, result

#i = tag 1
#j = tag 2
def fillTransitionTable(i, j, sentence, sentence_tag):
    count = 0
    for n in range(len(sentence)-1):
        if(sentence_tag[n] == i):
            if(sentence_tag[n+1] == j):
                count +=1
    print("INI BOI",sentence_tag[n])



    return count


def buildTransitionTable(info, all_tag):
    # sentence_tag.insert(0, "start")
    # for i in range(len(sentence)):
    transition_table ={}
    #iterasi tiap kalimat di data
    for i in range(len(info[0])):
        info[1][i].insert(0, "start")
        #iterasi tiap kata di kalimat
        for j in range(len(info[1][i])-2):
            # if(info[1][i][j])
            # print(info[1][i][2])
            # if(len(info[1][j]) != len(info[0][j])):
            #     print(i,len(info[1][j]), len(info[0][j]))
            #     print(info[0][j])
            #     print(info[1][j])
            #     print("==================================")
            # print (info[1][i][j], "|", info[0][i][j])
            #masukan current word's tag dan next word tag ke dict
            #kalau tag pertama sudah ada di table
            a = info[1][i][j]
            b = info[1][i][j+1]
            if(a in transition_table):
                #kalau tag ke 2 sudah ada di table
                if(b in transition_table[a]):
                    transition_table[a][b] +=1
                #kalau tag ke 2 blm ada di table
                else:
                    transition_table[a][b] = 1
            else:
                transition_table[a] = {}
                transition_table[a][b] = 1
    transition_table_sum ={}
    result = {}
    for i in transition_table:
        for j in transition_table[i]:
            transition_table_sum[i] = 0
            
            #klo kt ada di result
            if(i not in result):
                result[i] ={}
            result[i][j] =0
    for i in transition_table:
        for j in transition_table[i]:
            # print(i,j,transition_table[i][j])
            transition_table_sum[i] += transition_table[i][j]
    # print(transition_table_sum)

    for i in transition_table:
        for j in transition_table[i]:
            # print(i, j, transition_table[i][j])
            # print(i, transition_table_sum[i])
            result[i][j] = transition_table[i][j]/ float(transition_table_sum[i])
            # print(transition_table[i][j])

    return result

def getAllAvailableTags():
    result = []
    tagnya=""
    kalimat = []
    with open('file.txt') as data:
        while True:
            sentence_id= data.readline()
            sentence_id= sentence_id.lower()
            if(len(sentence_id.strip())==0):
                continue
            if "#eof" in sentence_id:
                break
            sentence = ""
            if("#" in sentence_id):
                continue

            else:
                sentence = sentence_id
                sentence = sentence.split("\t")
                if(sentence[2]=="_"):
                    tagnya = sentence[3]
                else:
                    tagnya = sentence[2]
                if(tagnya not in result):
                    result.append(tagnya)
    return result


def read():
    kamus = {}
    sentence_list = []
    with open('file.txt') as data:
        while True:
            sentence_id = data.readline()
            sentence_id = sentence_id.lower()
            if len(sentence_id.strip()) == 0 :
                continue
            if "#eot#" in sentence_id:
            	break
            sentence= ""
            if("#" in sentence_id):
                if("# text" in sentence_id):
                    sentence_list.append(sentence_id)
            else:
                sentence = sentence_id
                sentence = sentence.split("\t")
                if(sentence[2]=="_"):
                    tagnya = sentence[3]
                else:
                    tagnya = sentence[2]
                # print(sentence[1], tagnya)
                #kalau kata tsb sudah ada di kamus
                if(sentence[1] in kamus):
                    #kalau tag nya sudah ada terdaftar di kata tsb
                    if(tagnya in kamus[sentence[1]]):
                        #frequensi +1
                        kamus[sentence[1]][tagnya] +=1
                    #kalau tagnya belum terdaftar di kata tsb
                    else:
                        kamus[sentence[1]][tagnya] = 1
                #kalau kata tsb blm terdaftar di kamus
                else:
                    kamus[sentence[1]] = {}
                    kamus[sentence[1]][tagnya] = 1
    return kamus, sentence_list

def readTestData():
    with open('file.txt') as data:
        sentence = data.readline()
        #loop sampai muncul eot, atau end of training data
        while True:
            if("#eot#" in sentence):
                break
            else:
                sentence = data.readline()
        test_sentence = []
        #loop dari awal test data sampai end of file
        while True:
            if("#eof#" in sentence):
                break
            else:
                if("# text" in sentence):
                    sentence = sentence.lower()
                    sentence = sentence.split("=")
                    test_sentence.append(sentence[1])
                sentence = data.readline()

    return test_sentence

#ambil semua tag yg posible dari 1 data
def getwordAllTag(kata,kamus):
    #loop tiap kata
    try:
        get = kamus[kata]
    except KeyError:
        get = {'unknown' : 0}
    return (kata, get)

def getEmission(get):
    emission = {}
    n= 0
    for i in get:
        n += get[i]
    for i in get:
        if (n==0):
            emission[i] = 0
        else:
            emission[i] = get[i]/float(n)
            # print(get, i, "jumlah n: ", n)
    return emission
def loadKalimat():
    with open('file.txt') as data:
        sentence = data.readline()
        while "#eot" not in sentence:
            sentence = data.readline()
        hasil =[]
        while True:
            sentence = data.readline()
            sentence = sentence.lower()
            # if "#eot" in sentence:
            #     continue
            if "#eof" in sentence:
                break
            if "# text = " in sentence:
                # print(sentence)
                sentence = sentence.split("# text =")
                sentence = sentence[1]
                sentence = sentence.replace("\n", "")
                hasil.append(sentence)
    return hasil

a = read()
b = getSentenceTags()
all_tag = getAllAvailableTags()
# print(b[0][0])   
transition_table = buildTransitionTable(b, all_tag) 
count = 0
# for i in transition_table:
#     print(count,i , transition_table[i])
#     print("=================================================")
#     count +=1

c=loadKalimat()
print(c[0])
# for i in transition_table:
#     print(i, len(transition_table[i]))
# data_test = readTestData()

# for i in range(len(b[0])):
#     print(b[0][i])
#     print(b[1][i])

tags = getAllAvailableTags()
tags.insert(0, "<start>")
# tags.append("end")


#====================================
#GET TAG BASED ON EMISSION TABLE
# for sentences in b[0]:
#     for j in sentences:
#         if(j=="<start>"):
#             continue
#         word_tag = getwordAllTag(j, a[0])
#         word_emission = getEmission(word_tag[1])
#         print(j, word_emission)
#=====================================


# with open('kamus.txt', 'w') as file:
#     file.write(json.dumps(a))
    
        

# print(a)

