import json

data = json.load(open("test.json", 'r'))
working = json.load(open("working.json", 'r'))

def refresh_working_json():
    #aby program dobrze czytał dane, musimy odświerzać naszego jsona
    global working
    working = json.load(open("working.json", 'r'))

def clear_working_json():
    global working
    clearJson = {"workingBlocks": ["", ""], "lastAdded": ["", ""], "checkpoint": [], "sequence": ""}
    with open("working.json", 'w') as changeWorkingJson:
        json.dump(clearJson, changeWorkingJson)
    refresh_working_json()

def check_if_solved():
    blocksToCheck = working.get(str("workingBlocks"))
    if 

clear_working_json()
#hill_climb()
#print(working.get("sequence")[7:])
#test()
#test_new_checkpoint_method()
#go_to_last_checkpoint_test()