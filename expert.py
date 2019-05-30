#!/usr/local/bin/python3
import sys
import re

RULE_ID = 0
FACT_ID = 0
OPERATION_ID = 0
R_S = "RIGHT"
M_S = "MIDDLE"
L_S = "LEFT"

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


OP_LIST = [
    "+",
    "|",
    "^",
]

class File:
    def __init__(self, path):
        self.path = path
        self.facts = []
        self.rules = []
        self.operations = []
        self.maxLvl = 0
        self.minLvl = -1

    def displayRules(self):
        print("Rules :")
        for r in self.rules:
            if len(r.hash) > 0:
                print(r.hash + " : " + str(r.solved))
    
    def displayOp(self):
        print("Operations:")
        for o in self.operations:
            if type(o) is Operation and len(o.hash) > 0:
                print(o.hash + " : " + str(o.solved) + str(o.result))
            if type(o) is Fact and len(o.name) > 0:
                print(o.name + " : " + str(o.solved)  + str(o.value))

    def displayFacts(self):
        print("Facts:")
        for f in self.facts:
            if len(f.name) > 0:
                print(f.name + " : " + str(f.value))

    def find_operation_same_same(self, hash):
        return next((x for x in self.operations if x.hash == hash), None)
    
    def find_fact_same_same(self, name, is_not):
        return next((x for x in self.facts if x.name == name), None)

    def replace_op_by_fact(self, op):
        i = -1
        fact = Fact(op.hash, 0)
        fact.value = op.result
        fact.solved = 1
        for _ in self.operations:
            i += 1
            if type(_) is Operation and fact.name == _.hash: 
                self.operations[i] = fact
                print("fact added" + fact.name)
    
    def set_value_to_op_and_fact(self,lhs, rhs):
        rhs.solved = 1
        if type(rhs) is Fact:
            fact = self.find_fact_same_same(rhs.name, None)
            if fact:
                if type(lhs) is Fact:
                    fact.value = lhs.get_v()
                    print(fact.name + "set to " + str(lhs.value))
                else :
                    fact.value = lhs.result
                    print(fact.name + "set to " + str(lhs.result))
                fact.solved = 1
                
        else :
            self.set_value_to_op_and_fact(lhs, rhs.rhs)
            self.set_value_to_op_and_fact(lhs, rhs.lhs)
        

class Fact:
    def __init__(self, name, is_not):
        self.name = name
        self.value = 0
        self.is_not = is_not
        self.solved = None
        
    def get_v(self):
        if self.is_not:
            return int(not self.value)
        return self.value


class Operation:
    def __init__(self, op, op_side, strings, hash):
        self.op = op
        self.id = id
        self.op_type = op_side
        self.hash = hash
        self.lhs_s = strings[0]
        self.rhs_s = strings[1]
        self.rhs = None
        self.lhs = None
        self.result = None
        self.solved = 0
        self.removed = 0

    
    def get_op_value(self, str):
        for op in OP_LIST:
            if str.find(op) > 0:
                return str[str.find(op)]
        end("Error on parsing.")

    def create_operations(self, str, side):
        if len(str) > 2:
            operation = current_file.find_operation_same_same(str)
            if not operation :
                operand = self.get_op_value(str)
                sides = str.split(operand)            
                operation = Operation(operand, side, sides, str)
                current_file.operations.append(operation)
                operation.parse_each_side()
            return operation
        else:
            is_not = 0
            print("STR",str, len(str))
            if len(str) == 2:
                is_not = 1
                str = str[1]
            fact = current_file.find_fact_same_same(str, is_not)
            if not fact:
                fact = Fact(str , is_not)
                current_file.facts.append(fact)
            return fact

    def parse_each_side(self):
        self.lhs = self.create_operations(self.lhs_s, L_S)
        self.rhs = self.create_operations(self.rhs_s, R_S)
    
    def removeMe(self):
        if not self.removed:
            self.removeFromOpMe()
            self.removeFromRulesMe()
            self.removed = 1

    def removeFromOpMe(self):
        try:
            index = current_file.operations.index(self)
            if index >= 0:
                current_file.operations.pop(index)
        except ValueError:
            return
        
    
    def removeFromRulesMe(self):
        try:
            index = current_file.rules.index(self)
            if index >= 0:
                current_file.rules.pop(index)
        except ValueError:
            return

    
    def make_my_operation(self):
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
        self.result = method()
        self.solved = 1 
        if (name != "IMP" and name != "IAOI"):
            current_file.replace_op_by_fact(self)

    def ADD(self):
        return self.lhs.get_v() and self.rhs.get_v()

    def OR(self):
        if self.lhs.get_v() is None and self.rhs.get_v():
            return self.rhs.get_v()
        if self.rhs.get_v() is None and self.lhs.get_v():
            return self.lhs.get_v()
        if self.rhs.get_v() is None and self.lhs.get_v() is None:
            return None
        return self.lhs.get_v() | self.rhs.get_v()
    
    def XOR(self):
        if self.lhs.get_v() is None and self.rhs.get_v():
            return self.rhs.get_v()
        if self.rhs.get_v() is None and self.lhs.get_v():
            return self.lhs.get_v()
        if self.rhs.get_v() is None and self.lhs.get_v() is None:
            return None
        return self.lhs.get_v() ^ self.rhs.get_v()

    def IMP(self):
        self.solved = 1
        if type(self.rhs) is Fact:
            fact = current_file.find_fact_same_same(self.rhs.name, None)
            if fact:
                if type(self.lhs) is Fact: 
                    fact.value = self.lhs.get_v()
                    print(fact.name + " v set to : " + str(fact.value))
                else :
                    if not self.lhs.solved:
                        self.lhs.make_my_operation()
                    fact.value = self.lhs.result
                fact.solved = 1
                return fact.get_v()
        else :
            current_file.set_value_to_op_and_fact(self.lhs, self.rhs)
            if type(self.lhs) is Fact:
                return self.lhs.get_v()
            else :
                return self.lhs.result
        
        

    def IAOI(self):
        return self.rhs.get_v() and self.lhs.get_v()




def make_easy_op():
    easy_op = []
    for op in current_file.operations:
        if type(op) is Operation:
            # print("j'ai une op : "+ op.hash)
            # print(type(op.lhs), type(op.rhs))
            # print(op.lhs.solved, op.rhs.solved)
            if (type(op.lhs) is Fact) and (op.lhs.solved == 1 or op.rhs.solved == 1):
                print("lhs is fact !")
                op.make_my_operation()
                op.removeMe()
                print("Operation done op: " + op.hash + "=" + str(op.result))
                current_file.displayFacts()
                return
def make_easy_rule():
    i = -1
    
    for op in current_file.rules:
        if op.solved == 0:
            print("jai une op")
            print(op.hash)
            if op.lhs.solved == 1 or len(current_file.rules) == 1:
                op.make_my_operation()
                print("Operation done ru: " + op.hash + "=" + str(op.result))
                op.removeMe()
                current_file.displayFacts()
                make_easy_rule()
                return


def check_if_solved():
    for op in current_file.rules:
        if op.solved == 0:
            return False
    return True

def makeMagic(rec):
    make_easy_op()
    make_easy_rule()
    if not check_if_solved() and rec < 10:
        makeMagic(rec + 1)
    else:
        current_file.displayFacts()
        current_file.displayOp()
        current_file.displayRules()

def set_rule(line):
    operand = None
    strings = line.split("<=>")
    if len(strings) == 1: 
        operand = "=>"
        strings = line.split("=>")
    else :
        operand = "<=>"
        strings = line.split("<=>")
    middle_op = Operation(operand, M_S, strings, line)
    middle_op.parse_each_side()
    print(format(middle_op.hash, "30") + "Added")
    current_file.rules.append(middle_op)
        
def set_init_values(line):
    for i in range(1, len(line)):
        fact = current_file.find_fact_same_same(line[i], None)
        if fact:
            fact.value = 1
            fact.solved = 1
            print("Fact " + fact.name + " set to 1")

def parse_line(line):
    line = re.sub(r'\s+', '', line)
    if line[0] == "=":
        set_init_values(line)
    elif line[0] == "?":
        # set_questions(line)
        print("questions..")
    else:
        set_rule(line)

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
        print("I got everything needed.")
        makeMagic(0)
        #current_file.orderOperationInRules()
        
        # current_file.makeItSolvable(current_file.maxLvl)
        # current_file.display()
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



