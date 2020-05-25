import json
data = json.load(open("test.json"))

def blockValue(first, second):
    for i in range(0, min(len(first), len(second))):
        if first[i] != second[i]:
            return 0
    return i + 1
    
def checkBlock(block):
    firstblock = block[0]
    secondblock = block[1]
    return blockValue(firstblock, secondblock)

def compare(data):
    bestBlock = 0
    for i in range(1,4):
        checkedBlock = checkBlock(data.get(str(i)))
        if checkedBlock > bestBlock:
            bestBlock = i
    print(data.get(str(bestBlock)))

compare(data)