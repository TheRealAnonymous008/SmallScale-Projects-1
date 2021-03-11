import matplotlib
import matplotlib.pyplot as plt

def generateDieDist(faces):
    output = []
    for i in range(0, faces):
        output.append(1)

    return output

def getPrefix(arr):
    output = []
    sum = 0

    for i in arr:
        sum+=i
        output.append(sum)
    return output


def calculateDie(probabilities, faces):
    tmp = [0 for i in range(0, faces)]
    
    for p in probabilities:
        tmp.append(p)

    for i in range(1, len(probabilities)):
        tmp.append(0)

    prefix = getPrefix(tmp)
    final = len(tmp) - faces

    output = []
    for i in range(0, final):
        output.append(prefix[i + faces] - prefix[i])

    return output

def generateInputs(dice):
    s = len(dice)
    l = sum(dice)
    inputs = []
    for i in range(s, l + 1):
        inputs.append(i)

    return inputs

def generateOutputs(inputs, res):
    outputs = []
    for i in range(0, inputs):
        outputs.append(res[i])
    return outputs

def generateOutputsAsRatio(inputs, res):
    outputs = []
    cursum = 0
    for i in range(0, inputs):
        cursum += res[i]
    
    for i in range(0, inputs):
        outputs.append(res[i] / cursum)

    return outputs

def main():
    dice = [2 for i in range(0, 16)]
    res = generateDieDist(dice[0])

    for i in range(1, len(dice)):    
        res = calculateDie(res, dice[i])

    inputs = generateInputs(dice)
    outputs = generateOutputsAsRatio(len(inputs), res)

    plt.bar(inputs , outputs)
    plt.show()

main()

