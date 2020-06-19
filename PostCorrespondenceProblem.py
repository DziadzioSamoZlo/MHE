import json
import time

data = json.load(open("testEasy.json", 'r'))
working = json.load(open("working.json", 'r'))

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
        if checkedBlockValue == 0:
            howMuchBestBlocks += 1
            if howMuchBestBlocks > 1:
                add_checkpoint(working.get("sequence") + str(toCheck))
            else:
                bestPair = toCheck
    if howMuchBestBlocks == 0:
            return 0
    return bestPair

#Aby Brute Force byl zgodny z definicja, rozwiazywany problem 
#musi byc w jakis sposob ograniczony, dlatego też używamy limitu
#użytych bloczków
def best_block_to_add_with_limit(maxOccurs = 22):
    howMuchBestBlocks = 0
    #pobieramy aktualny stan bloczków
    baseBlock = working.get(str("workingBlocks"))

    #pobieramy nowy bloczek do dodania
    for toCheck in range(1,5):
        numberOfOccurs = 0
        checkedBlock = data.get(str(toCheck))
        firstsqnc = baseBlock[0] + checkedBlock[0]
        secondsqnc = baseBlock[1] + checkedBlock[1]
        checkedBlockValue = block_value(firstsqnc, secondsqnc)
        newSequence = working.get("sequence") + str(toCheck)
        #sprawdzamy ile razy nowy bloczek został użyty:
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
    blocksUsed = working.get("blocksAdded")
    
    #dodanie nowego bloczka do całego jsona working
    baseBlockFirst = baseBlock[0] + blockToAdd[0]
    baseBlockSecond = baseBlock[1] + blockToAdd[1]
    baseSequence = working.get("sequence") + str(whichBlock)
    
    #sprawdzenie czy wszystkie bloczki zostały użyte
    if whichBlock not in blocksUsed:
        blocksUsed.append(whichBlock)
        
    #tworzenie zmienionego jsona
    changedJson["workingBlocks"] = [baseBlockFirst, baseBlockSecond]
    changedJson["blocksAdded"] = blocksUsed
    changedJson["sequence"] = baseSequence
    with open("working.json", 'w') as changeWorkingJson:
        json.dump(changedJson, changeWorkingJson)

    #odświerzamy plik z którym pracujemy
    refresh_working_json()

def add_checkpoint(checkpointSequence):
    changedJson = json.load(open("working.json", 'r'))
    changedJson["checkpoint"].append(checkpointSequence)
    with open("working.json", 'w') as changeWorkingJson:
        json.dump(changedJson, changeWorkingJson)
    refresh_working_json()

def go_to_last_checkpoint():
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

def refresh_working_json():
    global working
    working = json.load(open("working.json", 'r'))

def clear_working_json():
    global working
    clearJson = {"workingBlocks": ["", ""], "blocksAdded": [], "checkpoint": [], "sequence": ""}
    with open("working.json", 'w') as changeWorkingJson:
        json.dump(clearJson, changeWorkingJson)
    refresh_working_json()
    
def measure_time(function, limit):
    start = time.perf_counter()
    function(limit)
    end = time.perf_counter()
    print(function.__name__, "took:", end-start, "s")

def Bruteforce(limit = 22):
    clear_working_json()
    for i in range(0,20000):
        if working["workingBlocks"][0] == working["workingBlocks"][1] and i > 0 and len(working["blocksAdded"]) == 4:
            print("solution found on iteration: ", i)
            break
        added = best_block_to_add_with_limit(limit)
        if added == 0:
            go_to_last_checkpoint()
            continue
        add_next_block(added)
    print("Brute Force found:")
    print(working["sequence"])
    print("Solution:")
    print(data["sol"])

#go_to_last_checkpoint_test()
measure_time(Bruteforce, 2)