# Check if the arguments are empty
def checkIfEmpty(args):
    for x in args:
        if args[x] is not None:
            print(args[x])
            return False
    return True

# Removes whitespaces and lowercases the arguments from clients
def cleanData(args):
    for x in args:
        if isinstance(args[x], str):
            args[x] = str(args[x]).lower().strip()

# Removes whitespaces from the arguments provided by the clients
def removeSpace(args):
    for x in args:
        if isinstance(args[x], str):
            args[x] = str(args[x]).strip()

# Lowercases the arguments from clients
def removeUpper(args):
    for x in args:
        if isinstance(args[x], str):
            args[x] = str(args[x]).lower()