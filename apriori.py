import time
import operator
import os

#-----------------------------------------------------------------------------------------------------------------------
#Here the input files are given
InputFileName = "topic-0.txt"

#lobal directory to refer. All files are located here
HomeDirectory = "/home/inputfolder/"

PatternFileName = "pattern-0.txt"
PatternDirectory = HomeDirectory + "patterns"
#OutputFileName = "expoutput-0.txt"

VocabFileName = "vocab.txt"

MaxPatternFile = "max-0.txt"
MaxPatternDirectory = HomeDirectory + "max"

ClosePatternFile = "closed-0.txt"
ClosePatternDirectory = HomeDirectory + "closed"


with open(HomeDirectory+ InputFileName)as f:
    data = f.readlines()
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#function to read data from input file
def getInputForApriori():
        x=[]
        frequencyDict = {}
        for line in data:
            words = line.split()
            for i in words:
                if not frequencyDict.get(i):
                    frequencyDict[i] = 1
                else:
                    frequencyDict[i] = frequencyDict.get(i) + 1
        return frequencyDict

#function to prune input data. Remove transaction less than minimum support.
def getPrunedDict(frequency_dict, minSupport):
    i = 0
    valuesToDelete = []
    print(frequency_dict.values()[i])
    for i in frequency_dict:
        if (int(frequency_dict[i]) < int(minSupport)):
            valuesToDelete.append(i)

    for k in valuesToDelete:
        frequency_dict.pop(k, None)

    return frequency_dict

#function to prune further data by removing tuples less than minimum support.
def getMinimumSupportDict(values, minSupport):
    count = 0
    newDict = {}

    for value in values:
            #print(value)
        for line in data:
            words = line.split()
            if (set(value) <= set(words)):
                count = count + 1
        if (count >= int(minSupport)):
            newDict[tuple(value)] = count
           # print(count)
        count = 0
    return newDict

#function to perform self join of the tuples
def selfJoinWithSupport(dictionary, minSup):
    i = 0
    newDict = {}
    tempDict = {}
    joinList = []
    index = 0

    keys = dictionary.keys()

    for i in keys:
        j = index + 1
        del joinList[:]
        while j < len(keys):
            joinList.append([i, keys[j]])
            j = j + 1
        index = index + 1

        tempDict = getMinimumSupportDict(joinList, minSup)

        if (len(tempDict.keys())):
            newDict.update(tempDict)
    print(newDict)
    return  newDict

def secondStep_apriori(dict, minSup):
    i = 0
    newDict = {}
    tempDict = {}
    joinList = []
    index = 0
    keys = dict.keys()

    for i in keys:
        lengthOfTuple = len(i)
        j = index + 1
        del joinList[:]
        while j < len(keys):
            if(len(set(i) & set(keys[j])) and ( len(set(i) | set(keys[j])) == lengthOfTuple + 1) ):
                joinList.append(list((set(i) | set(keys[j]))))
            j = j + 1
        index = index + 1

        tempDict = getMinimumSupportDict(joinList, minSup)

        if (len(tempDict.keys())):
            #newDict.update(tempDict)
            if (len(newDict) == 0):
                 newDict.update(tempDict)
            else :
                k = 0
                found = False

                tmp = newDict.copy()
                for i in tempDict:
                    for j in tmp:
                        if (set(sorted(i)) <= set(sorted(j))):
                            found = True
                            break
                if not found:
                    newDict.update(tempDict)
    #newDict = sorted(newDict.items(), key=lambda x:x[1])
    print(newDict)
    return newDict

#-----------------------------------------------------------------------------------------------------------------------
#functions to write to a file
def writeToFile(data,key, fp):
    for line in data:
        words = line.split()
        if(int(key) == int(words[0])):
            fp.write("{0}\t".format(words[1]))

def writeToPatternFile(dictionaryData, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    var = directory + "/"+ filename
    fp = open(directory + "/"+ filename, "w")

    with open(HomeDirectory + VocabFileName)as f:
        data = f.readlines()
        x=[]
        frequencyDict = {}
        for value in dictionaryData:
            fp.write("{0}\t".format(value[1]))
            key = str(value[0])
            splitString = key.split(",")
            if "," in key:
                keyVals = value[0]
            else:
                keyVals = splitString

            for val in keyVals:
                writeToFile(data, val, fp)
            fp.write("\n")

#sort the result and write to a file
def sortAndWriteToFile(paternDic, directory, fileName):
    sorted_x = sorted(paternDic.items(), key=operator.itemgetter(1), reverse= True)


    if len(paternDic) > -0:
        writeToPatternFile(sorted_x, directory, fileName)

#-----------------------------------------------------------------------------------------------------------------------

#function to calculate closed and Max patterns
def computeClosedAndMaxPatterns(allPaterns):
    i = 0
    closePatternDict = {}
    maxPatternDict = {}


    closePatternFound = False
    maxPatternFound = False

    levels = []

    for pattern in allPaterns.values():
        levels.append(pattern)

    i = 0
    while i < len(levels) - 1:
        levelDict1 =  levels[i]
        levelDict2 = levels[i + 1]

        level1 = 0

        while level1 < len(levelDict1):
            level2 = 0
            maxPatternFound =  False
            while level2 < len(levelDict2):

                if(i == 0) :
                    x = set([levelDict1.keys()[level1]])
                else :
                    x = set(levelDict1.keys()[level1])

                y = set(levelDict2.keys()[level2])
                if (x.issubset(y)):
                    maxPatternFound = True
                    if(levelDict2.values()[level2] >= levelDict1.values()[level1]):
                        closePatternFound = False
                        break
                    else:
                        closePatternFound = True
                level2 = level2 + 1
                #maxPatternFound = False

            if (closePatternFound):
                closePatternDict.update({levelDict1.keys()[level1]: levelDict1.values()[level1]})
            if not maxPatternFound:
                maxPatternDict.update({levelDict1.keys()[level1]: levelDict1.values()[level1]})


            level1 = level1 + 1

        i = i + 1
    closePatternDict.update(levels[len(levels) - 1])
    maxPatternDict.update(levels[len(levels) - 1])

    print("closed Patterns :{0}".format(closePatternDict))
    print("Max Patterns :{0}".format(maxPatternDict))

    sortAndWriteToFile(closePatternDict, ClosePatternDirectory, ClosePatternFile)
    sortAndWriteToFile(maxPatternDict,MaxPatternDirectory, MaxPatternFile)

#-----------------------------------------------------------------------------------------------------------------------
#main function to be callled
def main():
    minSupport = 100
    dictWithAllPatterns = {}
    patternDictionary = {}

    frequency_dict = getInputForApriori()

    pruned_dict = getPrunedDict(frequency_dict, minSupport)
    print(pruned_dict)
    patternDictionary.update(pruned_dict)
    dictWithAllPatterns.update({len(dictWithAllPatterns)+1 :pruned_dict})

    apriori_sec_step = selfJoinWithSupport(pruned_dict, minSupport)
    dictWithAllPatterns.update({len(dictWithAllPatterns)+1 :apriori_sec_step})
    patternDictionary.update(apriori_sec_step)

    output = secondStep_apriori(apriori_sec_step, minSupport)
    patternDictionary.update(output)
    dictWithAllPatterns.update({len(dictWithAllPatterns)+1 :output})

    while 1:
        result = secondStep_apriori(output, minSupport)
        if len(result) != 0:
            output = result
            dictWithAllPatterns.update({len(dictWithAllPatterns)+1 :output})
            patternDictionary.update(output)
        else:
            patternDictionary.update(output)
            break

    sortAndWriteToFile(patternDictionary, PatternDirectory, PatternFileName)
    computeClosedAndMaxPatterns(dictWithAllPatterns)

if __name__ == "__main__":
    start_time = time.time()  #function to record time..
    main()
    print("---  {0} seconds ---".format(time.time() - start_time))
