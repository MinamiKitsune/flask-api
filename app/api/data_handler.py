# Check if the arguments are empty
def check_if_empty(args):
    for x in args:
        if args[x] is not None:
            print(args[x])
            return False
    return True


# Removes whitespaces and lowercase the arguments from clients
def clean_data(args):
    for x in args:
        if isinstance(args[x], str):
            args[x] = str(args[x]).lower().strip()


# Removes whitespaces from the arguments provided by the clients
def remove_space(args):
    for x in args:
        if isinstance(args[x], str):
            args[x] = str(args[x]).strip()


# Lowercase the arguments from clients
def remove_upper(args):
    for x in args:
        if isinstance(args[x], str):
            args[x] = str(args[x]).lower()
