# Prints a message to the console to emulate the SMS message that will be sent
def sendMockSms(message, number):
    print(message + " to the number: " + number)

# Prints a message to the console to emulate a vaccination SMS that will be sent
def sendMockVacinationSms(message, number, uniqueID):
    print(message + " to the number: " + number + " and their unique ID is: " + uniqueID)
