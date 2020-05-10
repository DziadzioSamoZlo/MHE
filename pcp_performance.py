import pcp_solver as pcp
import time

def pcp_performance(Upp, Low, howManyTimes=20000):
    timeTaken = 0
    for x in range(0, howManyTimes):
        start = time.perf_counter()
        pcp.initiate(Upp, Low)
        end = time.perf_counter()
        timeTaken = timeTaken + (end - start)
    return timeTaken
    
#PLOT:
import matplotlib.pyplot as plt

Upper = ["aba", "bbb", "bb", "abbbaaa", "babb"]
Lower = ["a", "aaa", "babba", "baa", "aa"]
timeTaken = pcp_performance(Upper, Lower)
print(timeTaken)
plt.bar(1, timeTaken, color="teal", width=0.7)

Upper = ["a", "ab", "bba"]
Lower = ["baa", "aa", "bb"]
timeTaken = pcp_performance(Upper, Lower)
print(timeTaken)
plt.bar(2, timeTaken, color="forestgreen", width=0.7)

Upper = ["ab", "b", "a"]
Lower = ["b", "a", "ab"]
timeTaken = pcp_performance(Upper, Lower)
print(timeTaken)
plt.bar(3, timeTaken, color="cyan", width=0.7)

plt.title('Czas rozwiązywania problemu PCP')
plt.ylabel('czas w sekundach')
plt.xticks([])
plt.legend(('Problem nierozwiązywalny', 'Problem trudniejszy', 'Problem łatwiejszy'))
plt.show()
