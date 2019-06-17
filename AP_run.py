import random as rand
import math 
import statistics as stat

"""
# Datto Assignment by Benjamin Huddle
# 6/16/2019
# AP = access point
# GW = gateway
# RP = repeater
"""

#AP Class that is a parent of both RP and GW (since both are AP)
class AP:

    # Initialize all flags and variables used by both classes
    def __init__(self):
        self.download_firmware = False
        self.download_complete = False
        self.upgrade_complete = False
        
        self.checkin_offset = 0.00
        self.download_time = 0.00
        self.upgrade_time = 0.00
        self.current_time = 0.00
        
        self.low = 0.00
        self.high = 6.00


    # Function that produces the random checkin times for each 
    # RP and GW
    def get_rand_checkin_time(self):
        time = None
        return self.converter(time)
        
    
    # Function that converts any time greater .59 to the next
    # minute.  For instance, 4.71 becomes 5.21
    # Additional rounding to keep the precision to 2 decimals
    def converter(self, time):
        if (time == None):
            time = round(rand.uniform(self.low, self.high), 2)
        ad = round(time%1, 2)
        
        if (ad > .59):
            time = math.floor(time)
            time = (time + 1.00) + (ad - .60)
            time = round(time, 2)
        else:
            time = round(time, 2)
            
        return time
        

# Inherited class of AP, Gateway class has functions
# with logic based towards assessment guidelines
class GW(AP):

    #initialize the list of RP each GW has
    def __init__(self):
        super().__init__()
        self.RP_list = []
        
        
    # Adds the RP to the list of RP's
    def add_RP(self):
        self.RP_list.append(RP())
        
    
    # GW specific checkin. Gets initial checkin time offset, then
    # proceeds to iterate through each checkin in order
    # download, download complete, then upgrade complete
    def GW_checkin(self):
        if (self.checkin_offset == self.low):
            self.checkin_offset = self.get_rand_checkin_time()
            self.current_time += self.checkin_offset
        
        if (self.download_firmware == False):
            self.download_firmware = True
            self.download_time = self.GW_process()
            if (self.download_time >= self.high):
                self.download_time += self.high
                self.download_time = self.converter(self.download_time)
            self.current_time += self.download_time    
        elif (self.download_complete == False):
            for rp in self.RP_list:
                rp.RP_checkin(self)
            self.download_complete = True
            self.upgrade_time = self.GW_process()
            if (self.upgrade_time >= self.high):
                self.upgrade_time += self.high
                self.upgrade_time = self.converter(self.upgrade_time)
            self.current_time += self.upgrade_time
        else:
            self.upgrade_complete = True
            for rp in self.RP_list:
                rp.upgrade_complete = True
                rp.RP_checkin(self)
            
            
    # Returns the checkin time / download time / upgrade time
    def GW_process(self):
        if (self.download_firmware == True):
            return self.get_rand_checkin_time()
        elif (self.download_complete == True):
            return self.get_rand_checkin_time()
        else:
            return 'complete'
    

# RP class that inherits from AP class.  Same methods as GW
# but instead the logic is geared for RP's
class RP(AP):

    # Checkin only if certain flags are set true.
    # takes GW as object to verify flags
    def RP_checkin(self, gw):
        if ((self.download_complete != True and gw.download_complete != True)
                or (self.upgrade_complete == True and gw.upgrade_complete == True)):
            if (self.checkin_offset == self.low):
                self.checkin_offset = self.get_rand_checkin_time()
                self.current_time += self.checkin_offset
        
            if (self.download_firmware == False):
                self.download_firmware = True
                self.download_time = self.RP_process()
                if (self.download_time >= self.high):
                    self.download_time += self.high
                    self.download_time = self.converter(self.download_time)
                self.current_time += self.download_time
            elif (self.download_complete == False):
                self.download_complete = True
                self.upgrade_time = self.RP_process()
                if (self.upgrade_time >= self.high):
                    self.upgrade_time += self.high
                    self.upgrade_time = self.converter(self.upgrade_time)
                self.current_time += self.upgrade_time
            else:
                self.upgrade_complete = True
    
            
    # RP process returns update / download time
    def RP_process(self):
        if (self.download_firmware == True):
            return self.get_rand_checkin_time()
        elif (self.download_complete == True):
            return self.get_rand_checkin_time()
        else:
            return 'complete'
    

# Function to simplify running multiple runs
# gw_list is the list of GW
# GW_total is the total number of GW's
# RW_total is the total number of RW's
# avg is the mean or average of run
def run(gw_list, GW_total, RW_total, avg):
    for i in range(GW_total):
        gw_list.append(GW())
        gw_list[i].GW_checkin()
            
        for j in range(RW_total):
            gw_list[i].add_RP()
            gw_list[i].RP_list[j].RP_checkin(gw_list[i])
        
        gw_list[i].GW_checkin()
        gw_list[i].GW_checkin()
        
    avg.append(getAvg(gw_list))


# Function to calculate the average of list of gateways
# GW_list is the list of GW objects
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
    
    
# Function for checking status of specific checkin time
# GW_list is the list of GW objects 
# life is the list of status's such as downloading, upgrading
# and complete
# time is the time in which user wants to check 
def getCheckin(gw_list, life, time):
    for gw in gw_list:
        for rp in gw.RP_list:
            if ((rp.checkin_offset + rp.download_time + rp.upgrade_time) < time):
                life.append("complete")
            elif ((rp.checkin_offset + rp.download_time) > time):
                life.append("downloading")
            elif ((rp.checkin_offset + rp.download_time) < time):
                life.append("upgrading")
        if ((gw.checkin_offset + gw.download_time + gw.upgrade_time) < time):
            life.append("complete")
        elif ((gw.checkin_offset + gw.download_time) > time):
            life.append("downloading")
        elif ((gw.checkin_offset + gw.download_time) < time):
            life.append("upgrading")
            
    d = {x:life.count(x) for x in life}
    return d


# main loop of program
def main():
    gw_list = [] # list of GW objects
    avg = [] # list of averages
    life = [] # lifecycle checkin data, later for calc totals
    life2 = {} # dict of count of below, per run
    lifecycle = {'complete':0, 'upgrading':0, 'downloading':0} #totals
    GW_total = 10 #10 GW total
    RW_total = 2 # 2 per GW
    time = 8 # 8 min mark
    
    
    for i in range(0,10):
        run(gw_list, GW_total, RW_total, avg)
        life2 = getCheckin(gw_list, life, time)
        lifecycle['complete'] += life2['complete']
        lifecycle['upgrading'] += life2['upgrading']
        lifecycle['downloading'] += life2['downloading']
        
        for GW in gw_list:
            GW.RP_list.clear()
        gw_list.clear()
        life.clear()
        
    
    print("Mean of {} runs: {}".format(10, round(stat.mean(avg),2)))
    print("Upgrade point lifecycle: {}".format(lifecycle))
    
        
if __name__ == "__main__":
    main()