#from sys import time
import random as rand
import math 
import statistics as stat

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
        self.high = 6.00

    def get_rand_checkin_time(self):
        time = None
        return self.converter(time)
        
    def converter(self, time):
        if (time == None):
            time = round(rand.uniform(self.low, self.high), 2)
        ad = round(time%1, 2)
        #converting to get format in mm:ss
        if (ad > .59):
            time = math.floor(time)
            time = (time + 1.00) + (ad - .60)
            time = round(time, 2)
        else:
            time = round(time, 2)
        return time
        

class GW(AP):
    def __init__(self):
        super().__init__()
        self.RP_list = []
        
        
    def add_RP(self):
        self.RP_list.append(RP())
        
        
    def pop_RP(self):
        print('todo')
    
    
    def GW_checkin(self):
        if (self.checkin_offset == self.low):
            #get checkin time
            self.checkin_offset = self.get_rand_checkin_time()
            self.current_time += self.checkin_offset
        
        if (self.download_firmware == False):
            #begin download
            self.download_firmware = True
            self.download_time = self.GW_process()
            if (self.download_time >= self.high):
                #download or upgrade exceeds 5 min, wait (or in my case just add 5 min to total
                self.download_time += self.high
                self.download_time = self.converter(self.download_time)
            self.current_time += self.download_time
            
        elif (self.download_complete == False):
            #Must wait for each RP to set 'download_complete' = True
            for rp in self.RP_list:
                rp.RP_checkin(self)
            self.download_complete = True
            self.upgrade_time = self.GW_process()
            if (self.upgrade_time >= self.high):
                #download or upgrade exceeds 5 min, wait (or in my case just add 5 min to total
                self.upgrade_time += self.high
                self.upgrade_time = self.converter(self.upgrade_time)
            self.current_time += self.upgrade_time
        else:
            self.upgrade_complete = True
            for rp in self.RP_list:
                rp.upgrade_complete = True
                rp.RP_checkin(self)
            
            
            
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
    
            if (self.checkin_offset == self.low):
                self.checkin_offset = self.get_rand_checkin_time()
                self.current_time += self.checkin_offset
        
        
            if (self.download_firmware == False):
                #begin download
                self.download_firmware = True
                self.download_time = self.RP_process()
                if (self.download_time >= self.high):
                    #download or upgrade exceeds 5 min, wait (or in my case just add 5 min to total
                    self.download_time += self.high
                    self.download_time = self.converter(self.download_time)
                self.current_time += self.download_time
                
            elif (self.download_complete == False):
                #download complete, update
                self.download_complete = True
                self.upgrade_time = self.RP_process()
                if (self.upgrade_time >= self.high):
                    #download or upgrade exceeds 5 min, wait (or in my case just add 5 min to total
                    self.upgrade_time += self.high
                    self.upgrade_time = self.converter(self.upgrade_time)
                self.current_time += self.upgrade_time
            else:
                self.upgrade_complete = True
    
            
        
    def RP_process(self):
        if (self.download_firmware == True):
            return self.get_rand_checkin_time()
        elif (self.download_complete == True):
            return self.get_rand_checkin_time()
        else:
            
            return 'complete'
    

def run(gw_list, GW_total, RW_total, avg):
    for i in range(GW_total):
        gw_list.append(GW())
        #first GW checkin
        gw_list[i].GW_checkin()
            
        for j in range(RW_total):
            #making sure have RW for each GW
            gw_list[i].add_RP()
            #first RP checkin
            gw_list[i].RP_list[j].RP_checkin(gw_list[i])
            #print(gw_list[i].RP_list[j].checkin_offset)
        
        #contains both 2nd GW and RP checkin
        gw_list[i].GW_checkin()
        
        gw_list[i].GW_checkin()
        
    avg.append(getAvg(gw_list))

def getAvg(gw_list):
    totalAP = []
    upgrade = []
    for gw in gw_list:
        for rw in gw.RP_list:
            upgrade.append(rw.current_time)
        upgrade.append(gw.current_time)
        totalAP.append(max(upgrade))
        upgrade.clear()
    return round(stat.mean(totalAP),2)
    
def getCheckin(gw_list, life, time):
    for gw in gw_list:
        for rp in gw.RP_list:
            if ((rp.checkin_offset + rp.download_time + rp.upgrade_time) < time):
                life.append("complete")
            elif () #need to finish this 
            #offset + download > time its downloading
            #offset + download + upgrade > time it is upgrading idfk


def main():
    #need to get average upgrade time over 10 runs
    #need to get status of all AP at certain time
    #4GW with 3 RP each vs 3 GW with 4 RP each
    #change time to 0.00 to 6.00, how does that effect run - new challenges
    gw_list = []
    avg = []
    life = []
    GW_total = 10 #10 GW total
    RW_total = 2 # 2 per GW
    time = 8 # 8 min mark
    
    
    for i in range(0,10):
        run(gw_list, GW_total, RW_total, avg)
        """for obj in gw_list:
            print("GW: {} {} {} {}".format(obj.checkin_offset, obj.download_time, obj.upgrade_time, obj.converter(obj.current_time)))
            for rp_ob in obj.RP_list:
                print("   RP: {} {} {} {}".format(rp_ob.checkin_offset, rp_ob.download_time, rp_ob.upgrade_time, rp_ob.converter(rp_ob.current_time)))
                """
        getCheckin(gw_list, life, time)
            
        
        for GW in gw_list:
            GW.RP_list.clear()
        gw_list.clear()
        
    
    print("{}".format(round(stat.mean(avg),2)))
    
    
        


if __name__ == "__main__":
    main()