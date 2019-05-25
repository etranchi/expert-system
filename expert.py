#!/usr/local/bin/python3
import sys
import re
def end(reason): #coucou toi
    print(reason)
    exit()

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
        self.rule_id = 0
        self.path = path
        self.facts = []
        self.rules = []

    def addRule(self, operation, id, operation_lvl):
        if self.checkRule(operation):
            if len(self.rules) == self.rule_id:
                self.rules.append([])
            self.rules[self.rule_id].append(Operation(operation, id, operation_lvl))
        # else:
        #     print("Operation not added")

    def addFact(self, name, id, is_not):
        if not self.checkFactAlreadyExist(name):
            self.facts.append(Fact(name, id, is_not))
        # else: 
        #     print("Fact not added")

    def checkRule(self, operation):
        return next((x for x in RULE_LIST if x == operation), None)

    def checkFactAlreadyExist(self, name):
        return next((x for x in self.facts if x.name == name), None)
    
    def display(self):
        print(self.rules)
        for  id in self.rules:
            print("Rule numero :" + str(id))
            for op in id:
                print( str(op.id)+ "Operation : " + str(op.op) + ", left : " +  str(op.lhs_id) + ", right : " + str(op.rhs_id))
    

class Fact:
    def __init__(self, name, id, is_not):
        self.name = name
        self.value = 0
        self.id = id
        self.is_not = is_not


class Operation:
    def __init__(self, op, id, op_lvl):
        self.op = op
        self.op_lvl = op_lvl
        self.id = id
        self.lhs_id = id - 1
        self.rhs_id = id + len(op)


def set_values(line):
    print("values to be set" + str(line))

def set_questions(line):
    print("questions to be set" + str(line))

def set_rule(line):
    next = 0
    operation_lvl = 0
    for idx, c in enumerate(line):
        if next:
            next -= 1
        else:
            if c.isalpha():
                current_file.addFact(c, idx, 0)
            elif c == "(":
                operation_lvl += 1
            elif c == ")":
                operation_lvl -= 1
            elif c == "!": 
                if line[idx + 1].isalpha():
                    current_file.addFact(c, idx, 1)
                else :
                    end("Error")
            else :
                operand = ""
                if c == '<':
                    next = 2
                    operand = c + line[idx + 1] + line[idx + 2] 
                elif c == '=':
                    operand = c + line[idx + 1]
                    next = 1
                else:
                    operand = c
                current_file.addRule(operand, idx, operation_lvl)

def parse_line(line):
    line = list(re.sub(r'\s+', '', line))
    if line[0] == "=":
        set_values(line)
    elif line[0] == "?":
        set_questions(line)
    else:
        set_rule(line)
        current_file.rule_id += 1

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



