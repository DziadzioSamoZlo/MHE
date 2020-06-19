import json

data = json.load(open("test.json", 'r'))
working = json.load(open("working.json", 'r'))

#Dążymy do tego, żeby wartość była jak największa
def block_value(first, second):
    value = 0
    for i in range(0, min(len(first), len(second))):
        if first[i] != second[i]:
            value = value + 1
    return value

def best_block_to_add():
    howMuchBestBlocks = 0
    #pobieramy aktualny stan bloczków
    baseBlock = working.get(str("workingBlocks"))

    for toCheck in range(1,5):
        #pobieramy nowy bloczek do dodania
        checkedBlock = data.get(str(toCheck))
        firstsqnc = baseBlock[0] + checkedBlock[0]
        secondsqnc = baseBlock[1] + checkedBlock[1]
        checkedBlockValue = block_value(firstsqnc, secondsqnc)
        #print("sprawdzany: ", firstsqnc, " i ", secondsqnc, " wartość: ", checkedBlockValue)
        if checkedBlockValue == 0:
            howMuchBestBlocks += 1
            if howMuchBestBlocks > 1:
                add_checkpoint(working.get("sequence") + str(toCheck))
            else:
                bestPair = toCheck
    if howMuchBestBlocks == 0:
            return 0
    return bestPair

def best_block_to_add_with_limit(maxOccurs = 22):
    howMuchBestBlocks = 0
    #pobieramy aktualny stan bloczków
    baseBlock = working.get(str("workingBlocks"))

    for toCheck in range(1,5):
        #pobieramy nowy bloczek do dodania
        checkedBlock = data.get(str(toCheck))
        firstsqnc = baseBlock[0] + checkedBlock[0]
        secondsqnc = baseBlock[1] + checkedBlock[1]
        checkedBlockValue = block_value(firstsqnc, secondsqnc)
        newSequence = working.get("sequence") + str(toCheck)
        numberOfOccurs = 0
        for a in newSequence:
            if a == str(toCheck):
                numberOfOccurs += 1
        if numberOfOccurs > maxOccurs:
            continue
        if checkedBlockValue == 0:
            howMuchBestBlocks += 1
            if howMuchBestBlocks > 1:
                add_checkpoint(newSequence)
            else:
                bestPair = toCheck
    if howMuchBestBlocks == 0:
            return 0
    return bestPair

def add_next_block(whichBlock):
    #tworzymy chwilowy json którego zmienimy i zastapimy nim json working
    changedJson = json.load(open("working.json", 'r'))
    blockToAdd = data.get(str(whichBlock))
    baseBlock = working.get("workingBlocks")
    
    #dodanie nowego bloczka do całego jsona working
    baseBlockFirst = baseBlock[0] + blockToAdd[0]
    baseBlockSecond = baseBlock[1] + blockToAdd[1]
    baseSequence = working.get("sequence") + str(whichBlock)
    
    #tworzenie zmienionego jsona
    changedJson["workingBlocks"] = [baseBlockFirst, baseBlockSecond]
    changedJson["lastAdded"] = blockToAdd
    changedJson["sequence"] = baseSequence
    with open("working.json", 'w') as changeWorkingJson:
        json.dump(changedJson, changeWorkingJson)

    #odświerzamy plik z którym pracujemy
    refresh_working_json()

def add_checkpoint(checkpointSequence):
    changedJson = json.load(open("working.json", 'r'))
    changedJson["checkpoint"].append(checkpointSequence)
    #print("Adding checkpoint: ", checkpointSequence)
    with open("working.json", 'w') as changeWorkingJson:
        json.dump(changedJson, changeWorkingJson)
    refresh_working_json()

def go_to_last_checkpoint():
    #print("Reversing last sequence.")
    changedJson = json.load(open("working.json", 'r'))
    checkpoints = changedJson["checkpoint"]
    lastCheckpoint = checkpoints.pop(0)
    reversedBlockFirst = ""
    reversedBlockSecond = ""
    for i in lastCheckpoint:
        block = data.get(str(i))
        reversedBlockFirst = reversedBlockFirst + block[0]
        reversedBlockSecond = reversedBlockSecond + block[1]
    changedJson["workingBlocks"][0] = reversedBlockFirst
    changedJson["workingBlocks"][1] = reversedBlockSecond
    changedJson["checkpoint"] = checkpoints
    changedJson["sequence"] = lastCheckpoint

    with open("working.json", 'w') as changeWorkingJson:
        json.dump(changedJson, changeWorkingJson)
    refresh_working_json()

def go_to_last_checkpoint_test():
    changedJson = json.load(open("working.json", 'r'))
    killCheckpoint = changedJson["sequence"]
    checkpoints = changedJson["checkpoint"]
    checkpointsToKill = [s for s in checkpoints if killCheckpoint in s]
    if len(checkpointsToKill) == 0:
        lastCheckpoint = checkpoints.pop(0)
    else:
        checkpoints = [i for i in checkpoints if i not in checkpointsToKill]
        lastCheckpoint = checkpoints.pop(0)
    
    reversedBlockFirst = ""
    reversedBlockSecond = ""
    for i in lastCheckpoint:
        block = data.get(str(i))
        reversedBlockFirst = reversedBlockFirst + block[0]
        reversedBlockSecond = reversedBlockSecond + block[1]
    changedJson["workingBlocks"][0] = reversedBlockFirst
    changedJson["workingBlocks"][1] = reversedBlockSecond
    changedJson["checkpoint"] = checkpoints
    changedJson["sequence"] = lastCheckpoint

    with open("working.json", 'w') as changeWorkingJson:
        json.dump(changedJson, changeWorkingJson)
    refresh_working_json()

def refresh_working_json():
    global working
    working = json.load(open("working.json", 'r'))

def clear_working_json():
    global working
    clearJson = {"workingBlocks": ["", ""], "lastAdded": ["", ""], "checkpoint": [], "sequence": ""}
    with open("working.json", 'w') as changeWorkingJson:
        json.dump(clearJson, changeWorkingJson)
    refresh_working_json()

def checkIfSimilar(test):
    res = None
    for i in range(1, len(test)//2 + 1): 
        if (not len(test) % len(test[0:i]) and test[0:i] *
            (len(test)//len(test[0:i])) == test): 
            res = test[0:i] 
    return res

def Bruteforce():
    for i in range(0,20000):
        #print("najlepszy możliwy bloczek:")
        if working.get("sequence") == data.get("sol"):
            print("solution found on iteration: ", i)
            break
        added = best_block_to_add_with_limit()
        if added == 0:
            go_to_last_checkpoint()
            continue
        #print(added)
        #print("dodawany bloczek:")
        #print(data.get(str(added)))
        add_next_block(added)
    print("Brute Force found:")
    print(working["sequence"])
    print("Solution:")
    print(data["sol"])

clear_working_json()
Bruteforce()
#print(working.get("sequence")[7:])
#test()
#test_new_checkpoint_method()
#go_to_last_checkpoint_test()