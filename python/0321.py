n = int(input())
list = []
maxList = []
for i in range(n):
    list.append(int(input()))
    maxList.append(1)
for i in list:
    for j in list[:i+1]:
        if(list[j] < list[i]):
            maxList[i] = max(maxList[j]+1, maxList[i])
print(max(maxList))
