import math


def euclideanDistance(p1,p2):
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

        # print(self.data)
        

    #computes the nearest neighbor
    def Test(self,instance):

        if not(isinstance(instance,list) and isinstance(instance[0],float)):
            raise TypeError("Data must be list type in Test()")

        nearest = [float('inf'),0] # nearest distance and index
        for i in range(0,len(self.data)):
            distance = euclideanDistance(self.data[i],instance)
            if distance < nearest[0]:
                nearest = [distance, i]

        print("Instance: ",instance)
        print("Nearest Point: ",self.data[nearest[1]])

        return self.data[nearest[1]][0]


    def printData(self):
        print("DATA")
        for d in self.data:
            print(d)
    def deleteData(self):
        self.data = []
        

class Validator:


    # leaving one instance out and feeding the rest. Use that instance to test and repeat for every instance
    def leaveOneOut(self,mySet,classifier,myData):

        if not(isinstance(myData, list) and isinstance(myData[0], list) and isinstance(myData[0][0], float)):
            raise TypeError("Data must be type list<list<float>> in leaveOneOut")

        # I want to truncate myData to only have the type and the features according to mySet
        # make another variable to hold data and go through each line in data. For a line, append the first element and the features in mySet
        
        newData = []
        for i in range(0,len(myData)):
            line = []
            line.append(myData[i][0])
            for j in range(0,len(mySet)):
                line.append(myData[i][mySet[j]])
            newData.append(line)

        # for d in newData:
        #     print(d)

        correct = 0
        for i in range(0,len(newData)):
            for j in range(0,len(newData)):
                if i == j:
                    continue
                # if i == 1: print(newData[j])
                classifier.Train(newData[j])
            
            # if i == 1: classifier.printData()
            if classifier.Test(newData[i]) == newData[i][0]:
                correct += 1
            classifier.deleteData()
            # if i == 1: exit()

        print("Correct: ", correct)    
        print("Total: ", len(newData))    


def main():

    c = Classifier()
    data = []
    # ratioTrain = .7 # if there are slight accuracy problems check this

    # file = 'very-small-test-dataset.txt'
    # file = 'small-test-dataset-1.txt'
    file = 'large-test-dataset-1.txt'

    with open(file, 'r') as file:
        while True:
            line = file.readline().split()      # reads a line and converts to array separating by whitespace
            if not(line):
                break
            
            line = [float(x) for x in line]     # converts each number in line to a float
            data.append(line)

    v = Validator()
    accuracy = v.leaveOneOut([1,15,27],c,data)


if __name__ == "__main__":
    main()
