def swapList(newList):
    temp = newList[0]
    newList[0] = newList[size - 1]
    newList[size - 1] = temp
     
    return newList

print(swapList([1,2,3]))