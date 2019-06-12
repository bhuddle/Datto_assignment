#from sys import time

# Python 3.7 for Datto assigmnet
# AP = access point
# GW = gateway
# RP = repeater
"""
 Create a list of gateway, router
 
"""

total_time = 0.00

class AP:
    def __init__(self):
        self.download_firmware = False
        self.download_complete = False
        self.upgrade_complete = False
        
        self.checkin_offset = 0.00
        self.download_time = 0.00
        self.upgrade_time = 0.00
    

class GW(AP):
    def __init__(self):
        self.RP_list = []
        
        
    def add_RP(self):
        print('todo')
        
        
    def pop_RP(self):
        print('todo')
    

class RP(AP):
    pass
    

def main():
    print('todo')


if __name__ == "__main__":
    main()