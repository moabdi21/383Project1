#Getting database file from: https://www.fludb.org/brc/home.spg?decorator=vipr



#Takes int he strain ID and make sure the that the strain is in the states/USA.
#restricing the program to take a limited amount of strains from each state. 5 DNA strains for each state.
def correctState(strainID, states):
    #print(strainID)
    if(strainID.find('(A/') == -1):
        return False
    index1 = strainID.index('/')+1
    length = len(strainID)
    index2 = strainID[index1: length].index('/')
    state  = strainID[index1:(index1+index2)]

    #print(state)
    limit = 5

    if state in states:
        #uncomment code below if you want to set a limitof strains for each state..
        if states[state] == limit:
            return False
        states[state] += 1
        return True
    return False

def removeEmptyStrains(strainDict):
    keyList = []
    for key, value in strainDict.items():
        if 'G' not in value and 'C' not in value and 'T' not in value and 'A' not in value:
            keyList.append(key)

    for key in keyList:
        strainDict.pop(key)
    return strainDict

#Read the file and stores the information in dictionary
def readFile(fileName): 
    file = open(fileName, 'r')
    strainDict = {}
    tempString = "" #fatsa H3N2 DNA strain.
    tempID = "" #fatsa strain ID
    is_location_USA = False

    #used by correctState fucntion
    states = {'Alabama':0,'Alaska':0,'Arizona':0,'Arkansas':0,'California':0,'Colorado':0,
        'Connecticut':0,'Delaware':0,'Florida':0,'Georgia':0,'Hawaii':0,'Idaho':0, 
        'Illinois':0,'Indiana':0,'Iowa':0,'Kansas':0,'Kentucky':0,'Louisiana':0,
        'Maine':0, 'Maryland':0,'Massachusetts':0,'Michigan':0,'Minnesota':0,
        'Mississippi':0, 'Missouri':0,'Montana':0,'Nebraska':0,'Nevada':0,
        'New Hampshire':0,'New Jersey':0,'New Mexico':0,'New York':0,
        'North Carolina':0,'North Dakota':0,'Ohio':0,    
        'Oklahoma':0,'Oregon':0,'Pennsylvania':0,'Rhode Island':0,
        'South  Carolina':0,'South Dakota':0,'Tennessee':0,'Texas':0,'Utah':0,
        'Vermont':0,'Virginia':0,'Washington':0,'West Virginia':0,
        'Wisconsin':0,'Wyoming':0}

    #read file
    print("reading file.....")
    for line in file:
        if line[0] == '>':
            if(correctState(line, states)):
                #adding the H3N2 strain to the strain ID(key) 
                #print(len(strainDict))
                is_location_USA = True
                if(tempID != ""):
                    strainDict[tempID] = tempString
                tempID = line
                tempString = "" #resets dna strain 
            else:
                is_location_USA = False
        elif (is_location_USA == True) and line != "":
            tempString += line
    
    strainDict = removeEmptyStrains(strainDict)

    print("file completed reading...")
    print('The total amount of data is', len(strainDict))
    #print(strainDict)
    return strainDict

#Read the file with fasta files that are in different format and stores the information in dictionary.
#basic fatsa reader limits for only 225 sequences.
def readFile2(fileName): 
    file = open(fileName, 'r')
    strainDict = {}
    tempID = ""
    tempString = "" #fatsa H3N2 DNA strain.
    seqCount = 0
    limit = 226

    #read file
    print("reading file.....")
    for line in file:
        if line[0] == '>':
            seqCount += 1
            if(tempID != ""):
                strainDict[tempID] = tempString

            tempID = line
            strainDict[tempID] = ''
            tempString = ""
        else:
            tempString += line
        if(seqCount == limit):
            break
    
    strainDict = removeEmptyStrains(strainDict)

    print("file completed reading...")
    print('The total amount of data is', len(strainDict))
    #print(strainDict)
    return strainDict

def printToFile(fileName, sequenceInfo):
    print('writing to file...')
    f =  open(fileName, 'w')
    f.write('This sequence was encountered: ' + str(sequenceInfo[0]) + '\n')
    f.write(str(sequenceInfo[1]))
    f.write(str(sequenceInfo[2]))
    f.close()
    print('completed writing to file.')

def findCommonStrain(strainsDict):
    strainsCounter = {}
    for key, value in strainsDict.items():
        if value in strainsCounter:
            strainsCounter[value] += 1
        else:
            strainsCounter[value] = 0

    strain = ''
    count = 0
    for key, value in strainsCounter.items():
        if value > count:
            strain = key
            count = value
    
    label = ''
    for key, value in strainsDict.items():
        if value == strain:
            label = key
            break
    print(count, label, strain)
    sequenceInfo = [count, label, strain]
    return sequenceInfo


if __name__== "__main__":
    
    strainDict = readFile('RAW_2015_H3N2_Strains.fasta')
    seqInfo = findCommonStrain(strainDict)
    printToFile('Abundant_RAW_2015_H3N2_Strain.fasta',seqInfo)


    strainDict = readFile('RAW_2016_H3N2_Strains.fasta')
    seqInfo = findCommonStrain(strainDict)
    printToFile('Abundant_RAW_2016_H3N2_Strain.fasta',seqInfo)

    strainDict = readFile('RAW_2017_H3N2_Strains.fasta')
    seqInfo = findCommonStrain(strainDict)
    printToFile('Abundant_RAW_2017_H3N2_Strain.fasta',seqInfo)


