#!/usr/local/bin/python3
import sys
import re

RULE_ID = 0
FACT_ID = 0
OPERATION_ID = 0

def end(reason): #coucou toi
    print(reason)
    exit()

def addOperationId():
    global OPERATION_ID
    OPERATION_ID = OPERATION_ID + 1

def addRuleId():
    global RULE_ID
    RULE_ID = RULE_ID + 1

def addFactId():
    global FACT_ID
    FACT_ID = FACT_ID + 1
current_file = None

RULE_LIST = [
    "+",
    "|",
    "=>",
    "<=>",
    "^",
]

class File:
    def __init__(self, path):
        self.path = path
        self.facts = []
        self.rules = []


    def displayFacts(self):
        for f in self.facts:
            if len(f.name) > 0:
                print(f.name + " : " + str(f.value))

    def createOperation(self, operation, operation_lvl):
        if self.checkRule(operation):
            op = Operation(operation, OPERATION_ID, operation_lvl)
            self.rules.append(op)
            print(str(RULE_ID) + " Operation added")
            addOperationId()
            return op
        print(operation)
        end("Error")
        # else:
        #     print("Operation not added")

    
    def createFact(self, name, is_not):
        fact = self.checkFactAlreadyExist(name)
        if not fact or name == "":
            t_fact = Fact(name, FACT_ID, is_not)
            self.facts.append(t_fact)
            addFactId()
            return t_fact
        return fact
        # else: 
        #     print("Fact not added")

    def checkRule(self, operation):
        return next((x for x in RULE_LIST if x == operation), None)

    def checkFactAlreadyExist(self, name):
        return next((x for x in self.facts if x.name == name), None)

    def setFactNameTo(self, name,value):
        print(self.checkFactAlreadyExist(name))

    def orderOperationInRules(self):
        self.rules = sorted(self.rules, key=lambda operation: operation.op_lvl, reverse=True)

    def display(self):
        for op in self.rules:
            if type(op) is Operation:
                lhs = factValue(op.lhs)
                rhs = factValue(op.rhs)
                print(str(op.id) + "Operation : " + str(op.op) + ", left : " +  lhs + ", right : " + rhs + ", level : " + str(op.op_lvl) + ", solvable : "+str(op.solvable) + ", result :" + str(op.result))
            else :
                lhs = str(op.value)
                rhs = "idk"
                print(str(op.id) + " Fact value : " + lhs)

    def checkChangeOp(self, op):
        if op and type(op.lhs) is Fact and type(op.rhs) is Fact:
            result = op.makeOperation()
            fact = Fact("",FACT_ID, 0)
            fact.value = result
            self.replaceAllOp(op, fact)
            addFactId()

    def replaceAllOp(self, op, fact):
        j = -1
        for ope in self.rules:
            j += 1
            if type(ope) is Operation:
                if type(ope.lhs) is Operation and ope.lhs.id == op.id:
                    self.rules[j].lhs = fact
                elif type(ope.rhs) is Operation and ope.rhs.id == op.id:
                    self.rules[j].rhs = fact

    def checkIfSolved(self):
        for ope in self.rules:
            if type(ope) is Operation and ope.solvable == 0:
                return 0
        return 1

    def makeItSolvable(self):
        self.display()
        solvableArray = []

        i = -1
        for op in self.rules:
            i += 1
            if op.solvable == 0:
                if type(op.lhs) is Fact and type(op.rhs) is Fact and op.lhs.value == 1 and op.rhs.value == 1:
                    self.rules[i].solvable = 1
                    solvableArray.append(op)
                if type(op.lhs) is Fact and type(op.rhs) is Fact and op.op == "|" and (op.rhs.value == 1 or op.lhs.value == 1):
                    self.rules[i].solvable = 1
                    solvableArray.append(op)
                if type(op.lhs) is Fact and type(op.rhs) is Fact and op.op_lvl < 0 and op.lhs.value != None:
                    self.rules[i].solvable = 1
                    solvableArray.append(op)
        print(len(self.rules))
        print(len(solvableArray))

        for op in solvableArray:
                op.solvable = 1
                result = op.makeOperation()
                print("making operation id : " + str(op.id))
                print(str(result) + " result of " + str(op.lhs.value) + " " + op.op + " " +str(op.rhs.value))
                if op.op_lvl < 0:
                    fact = current_file.checkFactAlreadyExist(op.rhs.name)
                    fact.value = result
                else:
                    fact = Fact("",FACT_ID, 0)
                    fact.value = result
                    self.replaceAllOp(op, fact)
                addFactId()
                # self.display()
                if not self.checkIfSolved():
                    self.makeItSolvable()

def factValue(factornot):
    if type(factornot) is Fact:
        return str(factornot.value)
    else :
        return 'operationid : ' + str(factornot.id)
class Fact:
    def __init__(self, name, id, is_not):
        self.name = name
        self.value = 0
        self.id = id
        self.is_not = is_not


class Operation:
    def __init__(self, op, id, op_lvl):
        self.op = op
        self.id = id
        self.op_lvl = op_lvl
        self.lhs = None
        self.rhs = None
        self.result = None
        self.solvable = 0
    
    def ADD(self):
        if self.lhs.value is None and self.rhs.value:
            return self.rhs.value
        if self.rhs.value is None and self.lhs.value:
            return self.lhs.value
        if self.rhs.value is None and self.lhs.value is None:
            return None
        return self.lhs.value & self.rhs.value

    def OR(self):
        if self.lhs.value is None and self.rhs.value:
            return self.rhs.value
        if self.rhs.value is None and self.lhs.value:
            return self.lhs.value
        if self.rhs.value is None and self.lhs.value is None:
            return None
        return self.lhs.value | self.rhs.value
    
    def XOR(self):
        if self.lhs.value is None and self.rhs.value:
            return self.rhs.value
        if self.rhs.value is None and self.lhs.value:
            return self.lhs.value
        if self.rhs.value is None and self.lhs.value is None:
            return None
        return self.lhs.value ^ self.rhs.value

    def IMP(self):
        return self.lhs.value

    def IAOI(self):
        return self.rhs.value and self.lhs.value

    def makeOperation(self):
        name = ""
        if self.op == "+":
            name = "ADD"
        elif self.op == "|":
            name = "OR"
        elif self.op == "^":
            name = "XOR"
        elif self.op == "=>":
            name = "IMP"
        elif self.op == "<=>":
            name = "IAOI"
        method = getattr(self, name, lambda: "Error")
        return method()


def set_values(line):
    for c in line:
        if c != "=" and c.isalpha():
            fact = current_file.checkFactAlreadyExist(c)
            if not fact:
                # Create fact
                print("no fact")
            else : 
                fact.value = 1
                # print(str(fact.name) + "Set to 1")
    print("values to be set" + str(line))

def set_questions(line):
    print("questions to be set" + str(line))


def setFact(fact, f, s):
    if not f:
        f = fact
    else :
        s = fact
    return fact

class dF:
    def __init(self, f_f, s_f):
        self.f_f = f_f
        self.s_f = s_f

def set_rule(line):
    next = 0
    operation_lvl = 0
    fact = None
    p_op = None
    operand = None
    for idx, c in enumerate(line):
        if next:
            next -= 1
        else:
            if c == "(":
                    operation_lvl += 1
            elif c == ")":
                operation_lvl -= 1
            elif c.isalpha():
                print(c)
                fact = current_file.createFact(c, 0)
                
            elif c == "!": 
                if line[idx + 1].isalpha():
                    fact = current_file.createFact(c, 1)
                else :
                    end("Error")
            else :
                if c == '<' or c == '=':
                    if c == '<':
                        next += 1
                        operand = c + line[idx + 1] + line[idx + 2]
                    elif c == '=':
                        operand = c + line[idx + 1]
                    next += 1
                    operation_lvl -= 1
                else:
                    operand = c
        if operand:
            op = current_file.createOperation(operand, operation_lvl)
            if p_op and not fact:
                op.lhs = p_op
            elif operation_lvl > 0 and fact and p_op:
                p_op.rhs = op
                op.lhs = fact
                fact = None
            else :
                op.lhs = fact
                fact = None
            p_op = op
            operand = None
        elif p_op and fact:
            p_op.rhs = fact
            fact = None
        current_file.checkChangeOp(p_op)
        
        
def parse_line(line):
    line = list(re.sub(r'\s+', '', line))
    if line[0] == "=":
        set_values(line)
    elif line[0] == "?":
        set_questions(line)
    else:
        set_rule(line)
        addRuleId()

def check_line(line):
    if line.find("#") >= 0:
        line = line.split("#", 1)[0]
    if not len(line) or not line.strip():
        return
    parse_line(line)

def check_file(s_file):
    try:
        file = open(s_file)
        for line in file:
            check_line(line)
        current_file.orderOperationInRules()
        current_file.makeItSolvable()
        current_file.display()
        current_file.displayFacts()
        file.close()
    except Exception as err:
        end("Give me a real file please." + err)

if __name__ == '__main__':
    arg = sys.argv
    if (len(arg) != 2):
        end("usage: ./expert.py input_file")
    else:
        current_file = File(arg[1])
        check_file(arg[1])



