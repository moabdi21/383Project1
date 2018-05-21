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

    if state in states:
        return state
    return None

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
    states = {'Alabama':{},'Alaska':{},'Arizona':{},'Arkansas':{},'California':{},'Colorado':{},
        'Connecticut':{},'Delaware':{},'Florida':{},'Georgia':{},'Hawaii':{},'Idaho':{}, 
        'Illinois':{},'Indiana':{},'Iowa':{},'Kansas':{},'Kentucky':{},'Louisiana':{},
        'Maine':{}, 'Maryland':{},'Massachusetts':{},'Michigan':{},'Minnesota':{},
        'Mississippi':{}, 'Missouri':{},'Montana':{},'Nebraska':{},'Nevada':{},
        'New Hampshire':{},'New Jersey':{},'New Mexico':{},'New York':{},
        'North Carolina':{},'North Dakota':{},'Ohio':{},    
        'Oklahoma':{},'Oregon':{},'Pennsylvania':{},'Rhode Island':{},
        'South  Carolina':{},'South Dakota':{},'Tennessee':{},'Texas':{},'Utah':{},
        'Vermont':{},'Virginia':{},'Washington':{},'West Virginia':{},
        'Wisconsin':{},'Wyoming':{}}

    #read file
    print("reading file.....")
    previousState = None
    for line in file:
        if line[0] == '>':
            state = correctState(line, states)
            if(correctState(line, states) != None):
                #adding the H3N2 strain to the strain ID(key) 
                #print(len(strainDict))
                is_location_USA = True
                if(tempID != "" and previousState != False):
                    strainDict = states.get(previousState)
                    strainDict[tempID] = tempString
                    states[previousState] = strainDict
                    strainDict = {}
                tempID = line
                tempString = "" #resets dna strain 
                previousState = state
            else:
                is_location_USA = False
        elif (is_location_USA == True) and line != "":
            tempString += line
    
    strainDict = removeEmptyStrains(strainDict)

    print("file completed reading...")
    print('The total amount of data is', len(strainDict))
    #print(strainDict)
    return states

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

def printToFile(year, dictionary):
    print('writing to file...')
    #f =  open(fileName, 'w')
    count = 0
    #f.write('Total amount of H3N2 strains:' + str(len(dictionary)))
    for key, value in dictionary.items():
        if(key != False):
            fileName = str('H3N2_Strains_'+ key + '_' +year)    
            f = open(fileName,'w')
            for key2, value2 in value.items():
                if count == len(value) or not value2 :
                    break
                f.write(key2)
                f.write(value2)
                count += 1
            count = 0
    f.close()
    print('completed writing to file.')

if __name__== "__main__":
    #first fastfa file
    states = readFile('RAW_2016_H3N2_Strains.fasta')
    printToFile('2016', states)

    states = readFile('RAW_2017_H3N2_Strains.fasta')
    printToFile('2017', states)

