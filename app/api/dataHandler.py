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