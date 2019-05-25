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

    def createOperation(self, operation, operation_lvl):
        if self.checkRule(operation):
            if len(self.rules) == RULE_ID:
                self.rules.append([])
            op = Operation(operation, OPERATION_ID, operation_lvl)
            self.rules[RULE_ID].append(op)
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
        i = 0
        for ru in self.rules:
            self.rules[i] = sorted(ru, key=lambda operation: operation.op_lvl, reverse=True)
            i += 1

    def display(self):
        i = 0
        for  id in self.rules:
            print("Rule numero :" + str(i))
            for op in id:
                print(str(i) + "Operation : " + str(op.op) + ", left : " +  str(op.lhs) + ", right : " + str(op.rhs) + ", level : " + str(op.op_lvl))
            i += 1
    

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
                if c == '<':
                    next = 2
                    operand = c + line[idx + 1] + line[idx + 2] 
                elif c == '=':
                    operand = c + line[idx + 1]
                    next = 1
                else:
                    operand = c
        if operand:
            op = current_file.createOperation(operand, operation_lvl)
            if p_op and not fact:
                op.lhs = p_op
            elif operation_lvl > 0 and fact:
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
        current_file.display()
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



