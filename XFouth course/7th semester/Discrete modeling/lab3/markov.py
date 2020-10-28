import numpy

def buildCoefficientMatrix(matrix):
    matrix = numpy.array(matrix)
    count = len(matrix)
    res = numpy.zeros((count, count))
    for state in range(count - 1):
        for col in range(count):
            res[state, state] -= matrix[state, col]
        for row in range(count):
            res[state, row] += matrix[row, state]

    for state in range(count):
        res[count - 1, state] = 1
    return res

def buildAugmentationMatrix(count):
    res = [0 for i in range(count)]
    res[count - 1] = 1
    return numpy.array(res)

def getSystemTimes(matrix):
    return numpy.linalg.solve(buildCoefficientMatrix(matrix), buildAugmentationMatrix(len(matrix)))
