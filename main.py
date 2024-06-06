import math
count = 0 # for counting how many times euclideanDistance is called (Line 5,6)

# AGENDA
# still need to make backward selection
# need to normalize
# add the trace
# extra: we can speed up by using a precomputed distance values for pairs of instances?

def euclideanDistance(p1,p2):
    global count
    count += 1

    if len(p1) != len(p2):
        raise ValueError("Points are not the same dimensions")

    distance = 0
    for i in range(1,len(p1)):
        distance += (p1[i] - p2[i]) ** 2

    
    return math.sqrt(distance)


class Classifier:

    def __init__(self):
        self.data = []

    def Train(self,d):
        if isinstance(d, list) and isinstance(d[0], list) and isinstance(d[0][0], float):
            self.data.extend(d)
        elif isinstance(d, list) and isinstance(d[0], float):
            self.data.append(d)
        else:
            raise ValueError("Not of correct type")
        
    #computes the nearest neighbor
    def Test(self,instance):

        if not(isinstance(instance,list) and isinstance(instance[0],float)):
            raise TypeError("Data must be list type in Test()")

        nearest = [9999999,0] # nearest distance and index
        for i in range(0,len(self.data)):
            distance = euclideanDistance(self.data[i],instance)
            if distance < nearest[0]:
                nearest = [distance, i]

        # print("Instance: ",instance)
        # print("Nearest Point: ",self.data[nearest[1]])

        return self.data[nearest[1]][0]

    def deleteData(self):
        self.data = []
        

class Validator:

    # leaving one instance out and feeding the rest. Use that instance to test and repeat for every instance
    def leaveOneOut(self,featureSet,classifier,myData):

        if not(len(featureSet) and len(myData)):
            return 0
        elif not(isinstance(myData, list) and isinstance(myData[0], list) and isinstance(myData[0][0], float)):
            raise TypeError("Data must be type list<list<float>> in leaveOneOut")

        # I want to truncate myData to only have the type and the features according to mySet
        # make another variable to hold data and go through each line in data. For a line, append the first element and the features in mySet
        
        newData = []
        for i in range(0,len(myData)):
            line = []
            line.append(myData[i][0])
            for j in range(0,len(featureSet)):
                line.append(myData[i][featureSet[j]])
            newData.append(line)

        correct = 0
        for i in range(0,len(newData)):
            for j in range(0,len(newData)):
                if i == j:
                    continue
                classifier.Train(newData[j])
            
            if classifier.Test(newData[i]) == newData[i][0]:
                correct += 1
            classifier.deleteData()

        # print("Correct: ", correct)    
        # print("Total: ", len(newData))  

        return correct / len(newData)  


def forwardSelection(validator,classifier,data):
    featureAmount = len(data[0])-1
    currentSet = set()
    bestSet = set()
    currAccuracy = 0
    bestAccuracy = 0
    foundBetter = False

    i = 1
    while i <= featureAmount:
        if i in currentSet:
            i += 1
            continue
        currentSet.add(i)

        listSet = sorted(list(currentSet))

        currAccuracy = validator.leaveOneOut(listSet,classifier,data)

        if bestAccuracy < currAccuracy:
            print("NEW BEST ",currentSet, " WITH ACCURACY ",currAccuracy)
            print("IS BETTER THAN")
            print("CURRENT ",bestSet, " WITH ACCURACY ",bestAccuracy)

             
            bestAccuracy = currAccuracy
            bestSet = currentSet.copy()
            foundBetter = True
                       
        elif bestAccuracy == currAccuracy and (len(currentSet) < len(bestSet)):
            bestSet = currentSet.copy()

        # also check if equal and choose the one with less features
        if foundBetter and i == featureAmount:
            currentSet = bestSet.copy()
            foundBetter = False
            i = 0
        else: 
            currentSet.remove(i)
        i += 1

    print("Best: ",bestSet)
    print("Accuracy: ",bestAccuracy)
    

def backwardSelection(validator,classifier,data):
    featureAmount = len(data[0])-1
    currentSet = set()
    bestSet = set()
    oldSet = set()
    currAccuracy = 0
    bestAccuracy = 0
    #foundBetter = False

    i = 1
    while i <= featureAmount:
        bestSet.add(i)
        i += 1
    
    i -= 1
    oldSet.add(0)
    while len(bestSet) > 1:
        if oldSet == bestSet:
            break
        oldSet = bestSet.copy()
        i = list(bestSet)[-1]
        while i > 0:
            currentSet = oldSet.copy()
            test = i in currentSet
            if test:
                currentSet.remove(i)

                listSet = sorted(list(currentSet))

                currAccuracy = validator.leaveOneOut(listSet,classifier,data)

                if bestAccuracy < currAccuracy:
                    print("NEW BEST ",currentSet, " WITH ACCURACY ",currAccuracy)
                    print("IS BETTER THAN")
                    print("CURRENT ",bestSet, " WITH ACCURACY ",bestAccuracy)
                    
                    bestAccuracy = currAccuracy
                    bestSet = currentSet.copy()
                    #foundBetter = True
                
                elif bestAccuracy == currAccuracy and (len(currentSet) < len(bestSet)):
                    bestSet = currentSet.copy()


            i -= 1



def main():

    datac = int(input("Choose a datase: \n1) small test \n2) large test \n3) small data \n4) large data\n"))
   
    if datac == 1:
        file = 'small-test-dataset-1.txt'
    elif datac == 2:
        file = 'large-test-dataset-1.txt'
    elif datac == 3:
        file = 'CS170_Spring_2024_Small_data__35.txt'
    else:
        file = 'CS170_Spring_2024_Large_data__35.txt'

    selectc = int(input("Choose feature selection method: \n1) Foward Selection \n2) Backwards Elimination\n"))

    data = []
    
    with open(file, 'r') as file:
        while True:
            line = file.readline().split()      # reads a line and converts to array separating by whitespace
            if not(line):
                break
            
            line = [float(x) for x in line]     # converts each number in line to a float
            data.append(line)

    c = Classifier()
    v = Validator()

    if selectc == 1:
        bestFeatures = forwardSelection(v,c,data)
    else:
        bestFeatures = backwardSelection(v,c,data)

    print("BEST: ",bestFeatures)

if __name__ == "__main__":
    main()
