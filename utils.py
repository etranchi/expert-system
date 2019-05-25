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