#from sys import time
import random as rand
import math 

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
        self.current_time = 0.00
        
        #Set lower and upper ranges for random times
        self.low = 0.00
        self.high = 5.00

    def get_rand_checkin_time(self):
        t = round(rand.uniform(self.low, self.high), 2)
        ad = round(t%1, 2)
        #converting to get format in mm:ss
        if (ad > .59):
            t = math.floor(t)
            t = (t + 1.00) + (ad - .60)
            t = round(t, 2)
        return t
        

class GW(AP):
    def __init__(self):
        super().__init__()
        self.RP_list = []
        
        
    def add_RP(self):
        self.RP_list.append(RP())
        
        
    def pop_RP(self):
        print('todo')
    
    
    def GW_checkin(self):
        if (self.checkin_offset == 0.00):
            #get checkin time
            self.checkin_offset = self.get_rand_checkin_time()
            self.current_time += self.checkin_offset
        
        if (self.download_firmware == False):
            #begin download
            self.download_firmware = True
            self.download_time = self.GW_process()
            self.current_time += self.download_time
            
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
    
            if (self.checkin_offset == 0.00):
                self.checkin_offset = self.get_rand_checkin_time()
                self.current_time += self.checkin_offset
        
        
            if (self.download_firmware == False):
                #begin download
                self.download_firmware = True
                self.download_time = self.RP_process()
                self.current_time += self.download_time
            elif (self.download_complete == False):
                #download complete, update
                self.download_complete = True
            else:
                self.upgrade_complete = True
    
            
        
    def RP_process(self):
        if (self.download_firmware == True):
            return self.get_rand_checkin_time()
        elif (self.download_complete == True):
            
            return self.get_rand_checkin_time()
        else:
            
            return 'complete'
    

def main():
    #need to get average upgrade time over 10 runs
    #need to get status of all AP at certain time
    #4GW with 3 RP each vs 3 GW with 4 RP each
    #change time to 0.00 to 6.00, how does that effect run - new challenges
    gw_list = []
    GW_total = 10 #10 GW total
    RW_total = 2 # 2 per GW
    
    
    for i in range(GW_total):
        gw_list.append(GW())
        gw_list[i].GW_checkin()
        if (gw_list[i].download_time > 5.00):
            #download or upgrade exceeds 5 min, wait (or in my case just add 5 min to total
            gw_list[i].download_time += 5.00
            gw_list[i].current_time += 5.00
            
        for j in range(RW_total):
            #making sure have RW for each GW
            gw_list[i].add_RP()
            gw_list[i].RP_list[j].RP_checkin(gw_list[i])
            #print(gw_list[i].RP_list[j].checkin_offset)
        
    for obj in gw_list:
        print(obj.checkin_offset, obj.download_time, obj.upgrade_time, round(obj.current_time, 2))
        for rp_ob in obj.RP_list:
            print(" ", rp_ob.checkin_offset, rp_ob.download_time, rp_ob.upgrade_time, round(rp_ob.current_time,2))

if __name__ == "__main__":
    main()