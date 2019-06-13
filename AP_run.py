#from sys import time
import random as rand

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
        #Set flags to false
        self.download_firmware = False
        self.download_complete = False
        self.upgrade_complete = False
        
        #Set offset and times to 0
        self.checkin_offset = 0.00
        self.download_time = 0.00
        self.upgrade_time = 0.00
        
        #Set lower and upper ranges for random times
        self.low = 0.00
        self.high = 5.00

    def get_rand_checkin_time(self):
        print(round(rand.uniform(self.low, self.high), 2))
        

class GW(AP):
    def __init__(self):
        super().__init__()
        self.RP_list = []
        
        
    def add_RP(self):
        print('todo')
        
        
    def pop_RP(self):
        print('todo')
    
    
    def GW_checkin(self):
        if (self.download_firmware == False):
            #begin download
            self.download_firmware = True
        elif (self.download_complete == False):
            #download complete, check states of RP - wait 5 min if not complete
            self.download_complete = True
        else:
            self.upgrade_complete = True
            
            
    def GW_process(self):
        if (self.download_firmware == True):
            return self.get_rand_checkin_time()
        elif (self.download_complete == True):
            #Must wait for each RP to set 'download_complete' = True
            return self.get_rand_checkin_time()
        else:
            #complete at this point
            return 'complete'
    

class RP(AP):
    def RP_checkin(self, gw):
        if ((self.download_complete != True and gw.download_complete != True)
                or (self.upgrade_complete == True and gw.upgrade_complete == True)):
            if (self.download_firmware == False):
                #begin download
                self.download_firmware = True
            elif (self.download_complete == False):
                #download complete, update
                self.download_complete = True
            else:
                self.upgrade_complete = True
            
        
    def RP_process(self):
        print('todo')
    

def main():
    gw_list = []
    for i in range(10):
        gw_list.append(GW())
        
    for obj in gw_list:
        print(obj.RP_list)


if __name__ == "__main__":
    main()