from score import Score

# -------------------------------------------------------------------------------
# Prints any matrix
# Receives the matrix, rows qty, cols qty

def printMatrix(matrix, rows, cols):
    for i in range(rows):
        for j in range(cols):
            print(" %d " %matrix[i][j].value, end='')
        print()

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
    print(string1)
    print(string2)
    aMatrix = initializeMatrix(rows, cols)
    printMatrix(aMatrix, rows, cols)
    sI = 0
    for i in range(1, rows):
        sJ = 0
        for j in range(1, cols):
            aMatrix[i][j] = calculateScore(string1[sI],
                                           string2[sJ],
                                           aMatrix[i][j-1],
                                           aMatrix[i-1][j-1],
                                           aMatrix[i-1][j])
            sJ += 1
        sI += 1

    printMatrix(aMatrix, rows, cols)
    return aMatrix


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
# def calculateScore(bN1, bN2, left, diag, up):
def calculateScore(bN1, bN2, left, diag, up):
    # result = Score(0, '')
    if bN1 == bN2:
        diag.value += 1
    else:
        diag.value -= 1
    result = max(left, diag, up)
    return result

def analyzeMatrix(string1, string2, matrix, rows, cols):
    arrayString1 = []
    arrayString2 = []
    i = rows - 1
    j = cols - 1
    sI = rows - 2
    sJ = cols - 2

    while ( i > 0 ) | (j > 0):
            if (matrix[i][j].dir == 'diag'):
                arrayString1.append(string1[sI])
                arrayString2.append(string2[sJ])
                i -= 1
                j -= 1
                sI -= 1
                sJ -= 1
            elif (matrix[i][j].dir == 'left'):
                arrayString1.append('_')
                arrayString2.append(string2[sJ])
                j -= 1
                sJ -= 1
            else:
                arrayString1.append(string1[sI])
                arrayString2.append('_')
                i -= 1
                sI -= 1
    newString1 = ''.join(arrayString1)
    newString2 = ''.join(arrayString2)
    return [newString1[::-1], newString2[::-1]]


def generateLocalAlignment(string1, string2):
    matrix = generateScoreMatrix(string1, string2)
    # alignment = analyzeMatrix(string1, string2, matrix, len(string1)+1, len(string2)+1)
    # print("{}".format(alignment[0]))
    # print("{}".format(alignment[1]))




generateLocalAlignment("gtacattcta","attgtgatcc")