# Prints a message to the console to emulate the SMS message that will be sent
def send_mock_sms(message, number):
    print(message + " to the number: " + number)


# Prints a message to the console to emulate a vaccination SMS that will be sent
def send_mock_vaccination_sms(message, number, unique_id):
    print(message + " to the number: " + number + " and their unique ID is: " + unique_id)
