import sys


class System:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Variable:
    def __init__(self, name, variable_type, lower, upper, fsList=None):
        self.name = name
        self.lower = lower
        self.upper = upper
        self.variable_type = variable_type  # in or out
        if fsList is None:
            self.fsList = []
        else:
            self.fsList = fsList
    def appendFuzzySet(self,fuzzySet):
        self.fsList.append(fuzzySet)
    def __str__(self):
        return '{self.name}: \n{self.fsList}'.format(self=self)


class FuzzySet:
    def __init__(self, name, shape, ranges):
        self.name = name
        self.shape = shape
        self.ranges = ranges
        self.lower = self.ranges[0]
        self.upper = self.ranges[-1]
        self.crispValue = 0

    def __str__(self):
        return '{self.name} {self.shape} {self.ranges}'.format(self=self)


class FuzzySetList(list):
    def __str__(self):
        string = ''
        for elem in self:
            string += str(elem) + '\n'
        return string


def searchForVariableByName(variable_name, inList):
    for var in inList:
        if var.name == variable_name:
            return var


def searchForFuzzySetInVarByName(fuzzySetName, var):
    for fuzzyset in var.fsList:
        if fuzzyset.name == fuzzySetName:
            return fuzzyset


class Rule:
    def __init__(self, stringRule):
        self.stringRule = stringRule
        self.inVarList = []
        self.inVarListSet = []
        self.oper = None
        self.outVar = None
        self.outVarSet = None
        self.generateRule()

    def generateRule(self):
        stringRuleList = self.stringRule.split(" ")
        self.inVarList.append(searchForVariableByName(stringRuleList[0], inList))
        self.inVarListSet.append(searchForFuzzySetInVarByName(stringRuleList[1], self.inVarList[0]))
        self.oper = stringRuleList[2]
        self.inVarList.append(searchForVariableByName(stringRuleList[3], inList))
        self.inVarListSet.append(searchForFuzzySetInVarByName(stringRuleList[4], self.inVarList[1]))
        self.outVar = searchForVariableByName(stringRuleList[6], outList)
        self.outVarSet = searchForFuzzySetInVarByName(stringRuleList[7], self.outVar)

    def __str__(self):
        return '{self.inVarList[0]} {self.inVarListSet[0]} {self.oper} {self.inVarList[1]} {self.inVarListSet[1]} => ' \
               '{self.outVar} {self.outVarSet}'.format(self=self)


def getIntersectingFuzzySets(var, num):
    intersectingFuzzySets = []
    for fs in var.fsList:
        if fs.lower <= num <= fs.upper:
            intersectingFuzzySets.append(fs)

    return intersectingFuzzySets


def getLineCoord(FuzzySet, num, lower, upper):
    coordList = []
    if FuzzySet.shape == 'TRAP':
        if FuzzySet.ranges[0] <= num < FuzzySet.ranges[1]:
            coordList.append(FuzzySet.ranges[0])
            if FuzzySet.ranges[0] == lower:
                coordList.append(1)
            else:
                coordList.append(0)
            coordList.append(FuzzySet.ranges[1])
            coordList.append(1)
        elif FuzzySet.ranges[1] <= num < FuzzySet.ranges[2]:
            coordList.append(FuzzySet.ranges[1])
            coordList.append(1)
            coordList.append(FuzzySet.ranges[2])
            coordList.append(1)
        else:
            coordList.append(FuzzySet.ranges[2])
            coordList.append(1)
            coordList.append(FuzzySet.ranges[3])
            if FuzzySet.ranges[3] == upper:
                coordList.append(1)
            else:
                coordList.append(0)
        return coordList
    else:
        if FuzzySet.ranges[0] <= num < FuzzySet.ranges[1]:
            coordList.append(FuzzySet.ranges[0])
            if FuzzySet.ranges[0] == lower and FuzzySet.ranges[0] == FuzzySet.ranges[1]:
                coordList.append(1)
            else:
                coordList.append(0)
            coordList.append(FuzzySet.ranges[1])
            coordList.append(1)
        else:
            coordList.append(FuzzySet.ranges[1])
            coordList.append(1)
            coordList.append(FuzzySet.ranges[2])
            if FuzzySet.ranges[2] == upper and FuzzySet.ranges[1] == FuzzySet.ranges[2]:
                coordList.append(1)
            else:
                coordList.append(0)
    return coordList


def slope(coordList):
    if coordList[2] - coordList[0] != 0:
        return float(coordList[3] - coordList[1]) / (coordList[2] - coordList[0])
    return sys.maxint


def get_intercept(y, x, m):
    return y - (m * x)


def equation(x, m, c):
    return float(m * x + c)


def getValue(coordList, num):
    m = slope(coordList)
    c = get_intercept(coordList[1], coordList[0], m)
    value = equation(num, m, c)
    return value


########################################################
fs1 = FuzzySet("beginner", "TRI", [0, 15, 30])
fs2 = FuzzySet("intermediate", "TRI", [15, 30, 45])
fs3 = FuzzySet("expert", "TRI", [30, 60, 60])
fsList = FuzzySetList([fs1, fs2, fs3])
var1 = Variable('exp_level', 'IN', 0, 60, fsList)

fs1 = FuzzySet("very_low", "TRAP", [0, 0, 10, 30])
fs2 = FuzzySet("low", "TRAP", [10, 30, 40, 60])
fs3 = FuzzySet("medium", "TRAP", [40, 60, 70, 90])
fs4 = FuzzySet("high", "TRAP", [70, 90, 100, 100])
fsList = FuzzySetList([fs1, fs2, fs3, fs4])
var2 = Variable('proj_funding', 'IN', 0, 100, fsList)

fs1 = FuzzySet("low", "TRI", [0, 25, 50])
fs2 = FuzzySet("normal", "TRI", [25, 50, 75])
fs3 = FuzzySet("high", "TRI", [50, 100, 100])
fsList = FuzzySetList([fs1, fs2, fs3])
var3 = Variable('risk', 'OUT', 0, 100, fsList)

inList = [var1, var2]
outList = [var3]
crispValues = [40, 50]
# crisp values: var1: 40 var2: 50


def fuzz(inList, crispValues):
    i = 0
    for var in inList:
        intersectingFuzzySets = getIntersectingFuzzySets(var, crispValues[i])
        for elem in intersectingFuzzySets:
            coordList = getLineCoord(elem, crispValues[i], var.lower, var.upper)
            elem.crispValue = getValue(coordList, crispValues[i])
        i += 1

fuzz(inList, crispValues)
# # get intersecting fuzzy sets for var1
# intersectingFuzzySets = getIntersectingFuzzySets(inList[0], 40)
# # get line coords and calculate value for crisp Value for each intersecting fuzzy set in var1
# for elem in intersectingFuzzySets:
#     coordList = getLineCoord(elem, 40, inList[0].lower, inList[0].upper)
#     elem.crispValue = getValue(coordList, 40)

# initialize list of rules
rules = []
stringRule = 'proj_funding high or exp_level expert => risk low'
rules.append(Rule(stringRule))
stringRule = 'proj_funding medium and exp_level intermediate => risk normal'
rules.append(Rule(stringRule))
stringRule = 'proj_funding medium and exp_level beginner => risk normal'
rules.append(Rule(stringRule))
stringRule = 'proj_funding low and exp_level beginner => risk high'
rules.append(Rule(stringRule))
stringRule = 'proj_funding very_low and_not exp_level expert => risk high'
rules.append(Rule(stringRule))


def inference(rules):
    x = 0
    y = 0
    for rule in rules:
        x = rule.inVarListSet[0].crispValue
        y = rule.inVarListSet[1].crispValue
        if rule.oper == 'and':
            rule.outVarSet.crispValue = max(rule.outVarSet.crispValue, min(x, y))
        elif rule.oper == 'or':
            rule.outVarSet.crispValue = max(rule.outVarSet.crispValue, max(x, y))
        elif rule.oper == 'and_not':
            rule.outVarSet.crispValue = max(rule.outVarSet.crispValue, min(x, 1 - y))
        elif rule.oper == 'or_not':
            rule.outVarSet.crispValue = max(rule.outVarSet.crispValue, max(x, 1 - y))


inference(rules)


def getCentroids(var):
    centroids = []
    for fuzzySet in var.fsList:
        Sum = sum(fuzzySet.ranges) / len(fuzzySet.ranges)
        centroids.append(Sum)
    return centroids


def getWeightedAverage(centroids, var):
    i = 0
    numer = 0
    denom = 0
    for fuzzySet in var.fsList:
        numer += fuzzySet.crispValue * centroids[i]
        print(fuzzySet.crispValue)
        i += 1
        denom += fuzzySet.crispValue
    return numer / denom


def defuzz(var):
    centroids = getCentroids(var)
    weighted_average = getWeightedAverage(centroids, var)
    return weighted_average


weighted_average = defuzz(var3)
print(weighted_average)
