import math

# Euclidean distance function
def euclideanDistance(p1, p2):
    if len(p1) != len(p2):
        raise ValueError("Points are not the same dimensions")
    distance = 0
    for i in range(1, len(p1)):
        distance += (p1[i] - p2[i]) ** 2
    return math.sqrt(distance)

# Data normalization function
def normalize(data):
    numFeatures = len(data[0]) - 1
    mean = [0] * (numFeatures + 1)
    stDev = [0] * (numFeatures + 1)
    for i in range(len(data)):
        for j in range(len(data[0])):
            mean[j] += data[i][j]
            if i == len(data) - 1:
                mean[j] /= len(data)
    for i in range(len(data)):
        for j in range(len(data[0])):
            stDev[j] += ((data[i][j] - mean[j]) ** 2)
            if i == len(data) - 1:
                stDev[j] = math.sqrt(stDev[j] / len(data))
    for i in range(len(data)):
        for j in range(len(data[0])):
            if stDev[j] != 0:
                data[i][j] = (data[i][j] - mean[j]) / stDev[j]
    return data

# Classifier class
class Classifier:
    def __init__(self):
        self.data = []

    def Train(self, d):
        if isinstance(d, list) and isinstance(d[0], list) and isinstance(d[0][0], float):
            self.data.extend(d)
        elif isinstance(d, list) and isinstance(d[0], float):
            self.data.append(d)
        else:
            raise ValueError("Not of correct type")

    def Test(self, instance):
        if not (isinstance(instance, list) and isinstance(instance[0], float)):
            raise TypeError("Data must be list type in Test()")
        nearest = [float('inf'), 0]
        for i in range(len(self.data)):
            distance = euclideanDistance(self.data[i], instance)
            if distance < nearest[0]:
                nearest = [distance, i]
        return self.data[nearest[1]][0]

    def deleteData(self):
        self.data = []

# Validator class
class Validator:
    def leaveOneOut(self, featureSet, classifier, myData):
        if not (len(featureSet) and len(myData)):
            return 0
        elif not (isinstance(myData, list) and isinstance(myData[0], list) and isinstance(myData[0][0], float)):
            raise TypeError("Data must be type list<list<float>> in leaveOneOut")
        newData = [[myData[i][0]] + [myData[i][featureSet[j]] for j in range(len(featureSet))] for i in range(len(myData))]
        correct = 0
        for i in range(len(newData)):
            classifier.Train(newData[:i] + newData[i+1:])
            if classifier.Test(newData[i]) == newData[i][0]:
                correct += 1
            classifier.deleteData()
        return correct / len(newData)

# Forward selection algorithm
def forwardSelection(validator, classifier, data):
    featureAmount = len(data[0]) - 1
    currentSet = set()
    bestSet = set()
    currAccuracy = 0
    bestAccuracy = 0
    foundBetter = False

    i = 1
    while i <= featureAmount:
        if i in currentSet and not(i == featureAmount):
            i += 1
            continue
        currentSet.add(i)
        listSet = sorted(list(currentSet))
        currAccuracy = validator.leaveOneOut(listSet, classifier, data)
        print(listSet, "=", currAccuracy)

        if bestAccuracy < currAccuracy:
            print("NEW BEST ", currentSet, "=", currAccuracy, "IS BETTER THAN CURRENT", bestSet, "=", bestAccuracy)
            bestAccuracy = currAccuracy
            bestSet = currentSet.copy()
            foundBetter = True

        if foundBetter and i == featureAmount:
            currentSet = bestSet.copy()
            foundBetter = False
            i = 0
        else: 
            currentSet.remove(i)
        i += 1
    print("All features have worse accuracy!")
    print("Accuracy: ", bestAccuracy)
    return bestSet

# Backward selection algorithm
def backwardSelection(validator, classifier, data):
    featureAmount = len(data[0]) - 1
    currentSet = set()
    bestSet = set()
    oldSet = set()
    currAccuracy = 0
    bestAccuracy = 0

    i = 1
    while i <= featureAmount:
        bestSet.add(i)
        i += 1
    i -= 1
    oldSet.add(0)

    currAccuracy = validator.leaveOneOut(sorted(list(currentSet)), classifier, data)

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
                currAccuracy = validator.leaveOneOut(listSet, classifier, data)
                print(listSet, "=", currAccuracy)

                if bestAccuracy < currAccuracy:
                    print("NEW BEST ", currentSet, "=", currAccuracy, "BETTER THAN CURRENT", bestSet, " =", bestAccuracy)
                    bestAccuracy = currAccuracy
                    bestSet = currentSet.copy()
                elif bestAccuracy == currAccuracy and (len(currentSet) < len(bestSet)):
                    bestSet = currentSet.copy()
            i -= 1
    print("All features have worse accuracy!")
    print("Accuracy: ", bestAccuracy)
    return bestSet

def main():
    print("Welcome to Group 35 Feature Selection Algorithm")
    datac = int(input("Choose a file: \n1) small-test-dataset-1.txt \n2) large-test-dataset-1.txt \n3) CS170_Spring_2024_Small_data__35.txt \n4) CS170_Spring_2024_Large_data__35.txt\n"))

    file_map = {
        1: 'small-test-dataset-1.txt',
        2: 'large-test-dataset-1.txt',
        3: 'CS170_Spring_2024_Small_data__35.txt',
        4: 'CS170_Spring_2024_Large_data__35.txt'
    }

    file = file_map.get(datac, 'CS170_Spring_2024_Large_data__35.txt')

    data = []
    with open(file, 'r') as file:
        while True:
            line = file.readline().split()
            if not line:
                break
            line = [float(x) for x in line]
            data.append(line)

    print(f"This dataset has {len(data[0]) - 1} features with {len(data)} instances.")

    c = Classifier()
    v = Validator()

    selectc = int(input("Choose feature selection method: \n1) Forward Selection \n2) Backward Selection\n"))

    # Run feature selection on unnormalized data
    print("\nRunning feature selection on unnormalized data...")
    if selectc == 1:
        bestFeaturesUnnormalized = forwardSelection(v, c, data)
    else:
        bestFeaturesUnnormalized = backwardSelection(v, c, data)

    print("Best features for unnormalized data: ", bestFeaturesUnnormalized)

    # Normalize the data
    print("\nNormalizing the data...")
    normalized_data = normalize([row[:] for row in data])  # Deep copy the data to avoid modifying the original
    print("Done!")

    # Run feature selection on normalized data
    print("\nRunning feature selection on normalized data...")
    if selectc == 1:
        bestFeaturesNormalized = forwardSelection(v, c, normalized_data)
    else:
        bestFeaturesNormalized = backwardSelection(v, c, normalized_data)

    print("Best features for normalized data: ", bestFeaturesNormalized)

if __name__ == "__main__":
    main()
