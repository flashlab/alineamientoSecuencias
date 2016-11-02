from app.controllers.dataStructures import Score
from app.controllers.dataStructures import LocalAlignment
from app.controllers.dataStructures import AlignmentData
# -------------------------------------------------------------------------------
# Prints any matrix
# Receives the matrix, rows qty, cols qty

# def printMatrix(matrix, rows, cols):
#     for i in range(rows):
#         for j in range(cols):
#             print matrix[i][j].value,
#         print()

# -------------------------------------------------------------------------------
# Initialize any score matrix size
#Receives rows qty, cols qty

def initializeMatrix(rows, cols):
    newMatrix = []
    for i in range(rows):
        newLine = []
        for j in range(cols):
            if (i == 0) & (j > 0):
                newLine.append(Score(0, 'left'))
            elif (i > 0) & (j == 0):
                newLine.append(Score(0, 'up'))
            else:
                newLine.append(Score(0, {}))
        newMatrix.append(newLine)
    return newMatrix

# -------------------------------------------------------------------------------
#Calculates matrix values
#Receives strings to be aligned

def generateScoreMatrix( string1, string2):
    rows = len(string1)+1
    cols = len(string2)+1
    aMatrix = initializeMatrix(rows, cols)
    sI = 0
    for i in range(1, rows):
        sJ = 0
        for j in range(1, cols):
            aMatrix[i][j] = calculateScore(string1[sI],
                                           string2[sJ],
                                           aMatrix[i][j-1].value,
                                           aMatrix[i-1][j-1].value,
                                           aMatrix[i-1][j].value)
            sJ += 1
        sI += 1

    # printMatrix(aMatrix, rows, cols)
    return aMatrix

# -------------------------------------------------------------------------------
# Checks if score is < 0
# Receives score
def checkFor0(score):
    if (score.value <= 0):
        return Score(0,'')
    else:
        return score


# -------------------------------------------------------------------------------
# Gets max value from 3 calculated scores
# Receives left, diag, and up values

def max(a, b, c):
    if (a.value > b.value) & (a.value > c.value):
        return checkFor0(a)
    elif (c.value > b.value):
        return checkFor0(c)
    else:
        return checkFor0(b)

# -------------------------------------------------------------------------------
# Calculates score for each field in the matrix
# Receives char1, char2, leftScore, diagScore, upScore
def calculateScore(bN1, bN2, left, diag, up):

    leftRes = Score(left - 2, 'left')
    upRes = Score(up - 2, 'up')
    if bN1 == bN2:
        diagRes = Score(diag + 1, 'diag')
        # result = max(leftRes, diagRes, upRes)
    else:
        diagRes = Score(diag - 1, 'diag')
        # result = max(leftRes, diagRes, upRes)

    result = max(leftRes, diagRes, upRes)
    return result

# -------------------------------------------------------------------------------
# Print Alignments
# Receives alignments
def printAlignments(alignments):
    for i in range(len(alignments)):
        print("Sequence#{}".format(i))
        print("{} ".format(alignments[i].localAlignment.string(0)))
        print("{} ".format(alignments[i].localAlignment.string(1)))



def getHighestScore(alignments):
    hIndex = 0
    for i in range(1, len(alignments)):
        if(alignments[i].score > alignments[hIndex].score):
            hIndex = i
    return hIndex

def hasOverlap(alignHS, newAlign):
    result = False
    if ((newAlign.string(0) in alignHS.string(0)) is True) & \
       ((newAlign.string(1) in alignHS.string(1)) is True):
        result = True
    return result


def sortAlignmentArray(array):
    return quickSortArrayHelper(array)

def quickSortArrayHelper(align):
    if len(align) > 0:
        less = []
        equal = []
        greater = []
        pivot = align[0]
        for a in align:
            if (a.size() < pivot.size()):
                less.append(a)
            elif (a.size() > pivot.size()):
                greater.append(a)
            else:
                equal.append(a)
        return quickSortArrayHelper(greater)+equal+quickSortArrayHelper(less)
    else:
        return align



def getValidAlignments(alignments):
    alignments = sortAlignmentArray(alignments)
    hIndex = getHighestScore(alignments)
    newAlignments = [alignments[hIndex]]
    for i in range(len(alignments)):
        if (i != hIndex) & (hasOverlap(alignments[hIndex], alignments[i]) is False):
            newAlignments.append(alignments[i])
    return newAlignments

# -------------------------------------------------------------------------------
# Analyze matrix to get alignments
# Receives string1, string2, matrix, rows, cols
def analyzeMatrix(string1, string2, matrix, rows, cols):
    alignments = []
    for i in range(rows-1, 0, -1):
        for j in range(cols-1, 0, -1):
            if (matrix[i][j].value > 0) & (string1[i-1] == string2[j-1]) & (matrix[i][j].dir == 'diag') & \
                    (matrix[i-1][j-1].dir == 'diag'):
                    alignments.append(checkAlignmnent(matrix, i, j, string1, string2))
    getValidAlignments(alignments)
    return alignments

def checkAlignmnent (matrix, iStart, jStart, string1, string2):
    arrayString1 = []
    arrayString2 = []
    alignments = []
    i = iStart
    j = jStart
    scoring = 0
    while(matrix[i][j].dir == 'diag') & (matrix[i][j].value != 0):
        arrayString1.append(string1[i-1])
        arrayString2.append(string2[j-1])
        if (string1[i-1] == string2[j-1]):
            scoring += 1
        else:
            scoring -= 1
        i -= 1
        j -= 1
    alignments.append(LocalAlignment(''.join(arrayString1)[::-1], i, iStart))
    alignments.append(LocalAlignment(''.join(arrayString2)[::-1], j, jStart))
    return AlignmentData(alignments, scoring)

def checkSimilarStrings(substring1, substring2, string1, string2):
    sim1 = (len(substring1)*100)/len(string1)
    sim2 = (len(substring2)*100)/len(string2)
    simtotal = (sim1 + sim2) / 2
    return [substring1, substring2, string1, simtotal]

def checkContainingString(substring1, substring2, stringMinor, stringMajor):
    sim1 = (len(substring1)*100) / len(stringMinor)
    sim2 = (len(substring2)*100) / len(stringMajor)
    simtotal = (sim1 + sim2) / 2
    return [substring1, substring2, stringMinor, simtotal]

def analyzeAlignments(alignment, string1, string2):
    hIndex = getHighestScore(alignment)
    if (len(string1) == len(string2)):
        return checkSimilarStrings(alignment[hIndex].string(0), alignment[hIndex].string(0),
                            string1, string2)
    else:
        if len(string1) > len(string2):
            return checkContainingString(alignment[hIndex].string(0), alignment[hIndex].string(1),
                                  string2, string1)
        else:
            return checkContainingString(alignment[hIndex].string(0),
                                  alignment[hIndex].string(1),
                                  string1, string2)


def generateLocalAlignment(string1, string2):
    print("Starting Score Matrix Generation")
    matrix = generateScoreMatrix(string1, string2)
    print("Done Score Matrix Generation")
    print("Starting Matrix Analysis")
    alignments = analyzeMatrix(string1, string2, matrix, len(string1)+1, len(string2)+1)
    print("Done Matrix Analysis")
    print("Starting Alignments Analysis")
    return analyzeAlignments(alignments, string1, string2)
