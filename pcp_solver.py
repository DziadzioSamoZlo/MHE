def checkMin(upp, low):
    return min(len(upp), len(low))     

def checkNextPath():
    if not Path:
        #print("Problem is unsolvable")
        return
    #print("Solving Path: ")
    #print(Path)
    tmp_path_list = Path[0].split()
    Path.pop(0)
    Next_upper = [tmp_path_list[0] + tmp for tmp in Upper]
    Next_lower = [tmp_path_list[1] + tmp for tmp in Lower]
    solve(Next_upper, Next_lower)

def addPosiblePath(upp, low, i):
    Path.append(upp + " " + low + " " + i)
    #print("Path added: "+ upp + " " + low + " " + i)
    
def checkBlock(upp, low, i):
    signs_To_Check = checkMin(upp, low)
    if(upp[:signs_To_Check]==low[:signs_To_Check]):
        addPosiblePath(upp, low, i)
    
def solve(Upp, Low):
    for i in range(0, len(Upper)):
        #if i==toSkip:
        #    print("skipping " + str(i))
        #    continue
        checkBlock(Upp[i], Low[i], str(i))
        if Upp[i] == Low[i]:
            #print("Solution found")
            #print(Upp[i])
            return
    checkNextPath()
    
def initiate(Upp, Low):
    global Path
    global Upper
    global Lower
    Path = list()
    Upper = Upp
    Lower = Low
    solve(Upp, Low)

