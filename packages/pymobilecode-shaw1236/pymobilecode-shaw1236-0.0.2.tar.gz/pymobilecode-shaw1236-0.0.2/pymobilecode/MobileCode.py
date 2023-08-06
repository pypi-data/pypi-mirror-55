# MobileCode.py - Mobile text code utilities 
# Author: Simon Li
# Date  : Dec 19, 2018
#
# Usage : $haw1236$%
# import MobileCode 
# mobileCode = MobileCode();

''' == Usage ==
import MobileCode
mobileCode = MobileCode(8)

phoneList = ["6172201234", "9051234567", "9087654321"]

# Add the phone list
for phone in phoneList:
    mobileCode.add(phone)

# Show all the codes
print("Here are the code list:")
mobileCode.list()

# Get the code for a phone number 
print("phone: {0}, code: {1}".format(phoneList[1], mobileCode.get(phoneList[1])))

# Remove a code pair 
print("Here are the code list after removal of %s" % phoneList[1])
mobileCode.remove(phoneList[1])
mobileCode.list()
'''
import random

class MobileCode:
    def __init__(self, len = 6): # Create an empty container
        self.__MobileCodes = {}
        self.__length = len
        MobileCode.checkLength(len)

    @staticmethod
    def checkLength(len):
        # range 4 - 100
        lowest = 4
        highest = 100
        if len < lowest or len > highest:
            raise ValueError("Invalid length: {0}, must be between {1} and {2}".format(len, lowest, highest))

    @property
    def length(self):
        return self.__length
 
    @length.setter
    def length(self, len):
        MobileCode.checkLength(len)
        self.__length = len
 
    @property
    def mobileCode(self):
        return self.__MobileCodes

    # Generate a random code 
    def generateMobileCode(self):
        lowest = 10 ** (self.__length - 1)
        highest = 10 ** self.__length - 1
        
        number = random.randint(lowest, highest)
        while number in self.__MobileCodes:
            number = random.randint(lowest, highest)
        return number
 
    # Add a phone into the container 
    def addMobileCode(self, mobile):
        self.__MobileCodes[mobile] = self.generateMobileCode()

    # Add a phone list into the container 
    def addMobileCodes(self, listMobile):
        for mobile in listMobile:   
            self.__MobileCodes[mobile] = self.generateMobileCode()

    # Get the code for this phone
    def getMobileCode(self, mobile):
        return self.__MobileCodes[mobile]

    # Has the container included the phone?
    def hasMobileCode(self, mobile):
        return mobile in self.__MobileCodes

    # Verify the code against the phone stored in the container
    def verifyMobileCode(self, mobile, code):
        if not mobile in self.__MobileCodes:
           print("{0} is not on the list".format(mobile)) 
           return False
        
        return self.__MobileCodes[mobile] == code

    # Remove the phone from the container
    def removeMobileCode(self, mobile):
        del self.__MobileCodes[mobile]
    
    # List all the codes within the container
    def listMobileCodes(self):
        for key in self.__MobileCodes:
            print("{0} -> {1}".format(key, self.__MobileCodes[key]))

    ## Shorten version
    # Add a phone into the container 
    def add(self, mobile):
        self.__MobileCodes[mobile] = self.generateMobileCode()
    
    # Get the code for this phone
    def get(self, mobile):
        return self.__MobileCodes[mobile]
    
    # Remove the phone from the container
    def remove(self, mobile):
        del self.__MobileCodes[mobile]

    # Verify the code against the phone stored in the container
    def verify(self, mobile, code):
        if not mobile in self.__MobileCodes: 
           return False
        else: 
           return self.__MobileCodes[mobile] == code

    # Has the container included the phone?
    def has(self, mobile):
        return mobile in self.__MobileCodes
    
    # List all the codes within the container
    def list(self):
        for key in self.__MobileCodes:
            print("{0} -> {1}".format(key, self.__MobileCodes[key]))

if __name__ == '__main__':
    mobileCode = MobileCode()

    phoneList = ["6172201234", "9051234567", "9087654321"]

    # Add the phone list
    for phone in phoneList:
        mobileCode.add(phone)

    # Show all the codes
    print("Here are the code list:")
    mobileCode.list()

    # Get the code for a phone number 
    print("phone: {0}, code: {1}".format(phoneList[1], mobileCode.get(phoneList[1])))

    # Remove a code pair 
    print("Here are the code list after removal of %s" % phoneList[1])
    if mobileCode.has(phoneList[1]):
        mobileCode.remove(phoneList[1])
        mobileCode.list()
