import time
import operator
import os
import math

#-----------------------------------------------------------------------------------------------------------------------
#Global variables.
VocabFileName = "vocab.txt"
HomeDirectory = "/home/inputfolder/"
PurityDirectory = HomeDirectory + "purity"
RankingDirectory = HomeDirectory + "ranking"

NUM_OF_FILES = 5

#determinant values given.

determinant_0 = [10047, 17326, 17988, 17999, 17820]
determinant_1 = [17326, 9674, 17446, 17902, 17486]
determinant_2 = [17988, 17446, 9959, 18077, 17492]
determinant_3 = [17999, 17902, 18077, 10161, 17912]
determinant_4 = [17820, 17486, 17492, 17912, 9845]

Determinants = [determinant_0, determinant_1, determinant_2, determinant_3, determinant_4]

with open(HomeDirectory+ "vocab.txt")as f:
    vocab_data = f.readlines()

with open(HomeDirectory+ "topic-0.txt")as f:
    topic_0_data = f.readlines()
    count_0_data = len(topic_0_data)

with open(HomeDirectory+ "topic-1.txt")as f:
    topic_1_data = f.readlines()
    count_1_data = len(topic_1_data)

with open(HomeDirectory+ "topic-2.txt")as f:
    topic_2_data = f.readlines()
    count_2_data = len(topic_2_data)

with open(HomeDirectory+ "topic-3.txt")as f:
    topic_3_data = f.readlines()
    count_3_data = len(topic_3_data)

with open(HomeDirectory+ "topic-4.txt")as f:
    topic_4_data = f.readlines()
    count_4_data = len(topic_4_data)
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#utility functions to write to a file.

def writeToFile(Data, Directory, filename):
    if not os.path.exists(Directory):
        os.makedirs(Directory)
    #fp = open(PurityDirectory + "/purity-{0}".format(int(indexOfFile)), "w")
    fp = open(Directory + filename, "w")
    for purity in Data:
        fp.write("{0}\t{1}".format(purity[1], purity[0]))
        fp.write("\n")
    fp.close()

#-----------------------------------------------------------------------------------------------------------------------
#utility functions to get index and word from vocab file.

def getItemIndexInVocab(frequentPatten):
     with open(HomeDirectory + VocabFileName) as f:
        data = f.readlines()
        index = 0
        for line in data:
            words = line.split()
            if(words[1] == frequentPatten):
                index = words[0]
                break
        return index

def getVocabWordFromIndex(index):
    val = vocab_data[int(index)]
    val = val.split("\t")
    val[1] = val[1].strip()
    return val[1]
#-----------------------------------------------------------------------------------------------------------------------

#functions to access data and count-------------------------------------------------------------------------------------
def topicDict(x):
    return {
        0: topic_0_data,
        1: topic_1_data,
        2: topic_2_data,
        3: topic_3_data,
        4: topic_4_data
        }.get(x, 9)

def countOfTopicData(x):
    return  {
        0: count_0_data,
        1: count_1_data,
        2: count_2_data,
        3: count_3_data,
        4: count_4_data
        }.get(x, 9)
#-----------------------------------------------------------------------------------------------------------------------

#functions to get count of a pattern in a file.
def getCountOfPatternInFile(patternIndexes, indexOfFile):
    data = topicDict(int(indexOfFile))
    count = 0

    for line in data:
        words = line.split()
        if(set(patternIndexes) <= set(words)):
            count = count + 1
    return count

#function to get first term of the equation.
def calculateFirstTermForPurity(frequencyPatternCount, indexOfFile):
    return math.log( float(frequencyPatternCount) / float(countOfTopicData(indexOfFile)))

#utility function to calculate the maximum value.
def getMaxValue(frequencyPatternCountInFile, frequencyPatternCountInOtherFiles, indexOfFile) :
    i = 0
    maximumValue = -1000
    while i < int(NUM_OF_FILES):
        if(i != indexOfFile):
            value = frequencyPatternCountInOtherFiles.values()[i].values()[0]
            maxValu = (float(frequencyPatternCountInFile) +  value)/ Determinants[indexOfFile][i]
            if(maxValu > maximumValue):
                maximumValue = maxValu
        i = i + 1
    return maximumValue

#function to calculate second term of the equation.
def calculateSecondTermForPurity(frequencyPatternCountInFile, frequencyPatternCountInOtherFiles, indexOfFile):
    return math.log(getMaxValue(frequencyPatternCountInFile, frequencyPatternCountInOtherFiles, int(indexOfFile)))

#function to calculate purity.
def calculatePurity(indexOfFile):
    with open(HomeDirectory + "patterns/pattern-{0}.txt".format(int(indexOfFile))) as f:
        pattern_data = f.readlines()

    purity_dict = {}

    for pattern in pattern_data:
        i = 0
        frequentpatternIndexes = []
        frequentPatternCount = []

        patterns = pattern.split("\t")
        i = 1
        while i < len(patterns) - 1:
            index = getItemIndexInVocab(patterns[i])
            frequentpatternIndexes.append(index)
            i = i + 1

        paternsDict = {}
        i = 0

        while i < (int(NUM_OF_FILES)):
            frequencyOfPatternInOtherFiles = 0
            frequencyOfPatternInOtherFiles =  getCountOfPatternInFile(frequentpatternIndexes, i)

            if (len(frequentpatternIndexes) > 0):
                paternsDict.update({i : {tuple(frequentpatternIndexes): frequencyOfPatternInOtherFiles}})

            i = i + 1

        #get the first and second terms of the equation.
        firstTerm = calculateFirstTermForPurity(patterns[0], int(indexOfFile))
        secondTerm = calculateSecondTermForPurity(patterns[0],paternsDict, indexOfFile)

        val = ""
        i = 0
        while i < len(frequentpatternIndexes):
            val += getVocabWordFromIndex(frequentpatternIndexes[i]) + "\t"
            i = i + 1

        purity_dict.update({val: (firstTerm - secondTerm) })

    sorted_purity_dict = sorted(purity_dict.items(), key=operator.itemgetter(1), reverse= True)

    writeToFile(sorted_purity_dict, PurityDirectory, "/purity-{0}.txt".format(indexOfFile))

    return sorted_purity_dict

def main():
    start_time = time.time()

    print(calculatePurity(0))
    print("---  {0} seconds ---".format(time.time() - start_time))

if __name__ == "__main__":
    main()

