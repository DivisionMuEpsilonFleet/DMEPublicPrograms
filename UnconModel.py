import matplotlib.pyplot as plt
test_time = 0
# creating an empty canvas
fig = plt.figure()
 
# defining the axes with the projection
# as 3D so as to plot 3D graphs
ax = plt.axes(projection="3d")

class UnconProc:
    def __init__(self, basecd, globalcd, runtime, name):
        self.CD = basecd
        self.GCD = globalcd
        self.RunT = runtime
        self.Name = name


    def get_GCD(self):
        return self.GCD

    def get_CD(self):
        return self.CD
    
    def get_Name(self):
        return self.Name
    def NaiveUnConProcsInXSec(self, X,reaching_gcd_bool):
       if(reaching_gcd_bool == True):
          return int(X / self.GCD) #int will act as a floor function
       if(reaching_gcd_bool == False):
          return int(X / self.CD) #int will act as a floor function
       

 
class Console:
    def __init__(self, basecd, globalcd, runtime, name):
        self.BaseCD = basecd
        self.GCD = globalcd
        self.RunT = runtime
        self.currentCD = 0
        self.elapsedtime = 0
        self.available = True
        self.Name = name


    def get_GCD(self):
        return self.GCD

    def get_CD(self):
        return self.CD
    
    def get_Name(self):
        return self.Name

    def update_availability(self):
        if(self.currentCD <= 0):
            self.currentCD = 0
            self.available = True
        else:
            self.available = False

    def elapse_time(self):
        self.elapsedtime = self.elapsedtime+1

    def try_trigger_console(self,current_time):
        self.update_availability()
        if(self.available == True):
            self.available = False
            self.currentCD = self.BaseCD
            self.elapsedtime = 0
            print("Triggered: " + self.Name + " at " + str(current_time))
            return self.Name, True
        else:
            return self.Name, False


    def decrement_console_time(self):
        self.currentCD = self.currentCD - 1

    def apply_uncon(self):
        if(self.elapsedtime < self.GCD and self.currentCD < self.GCD):
            self.currentCD = self.GCD - self.elapsedtime

        elif(self.elapsedtime < self.RunT): #If this is true, no uncon proc can be applied
            pass

        elif(self.currentCD < 0):
            self.currentCD = 0
        else:
            self.currentCD = self.currentCD - self.BaseCD*0.075
    
    def apply_SFTF_Reduction(self):
        self.currentCD = self.currentCD - self.BaseCD*0.25

def main(UnCons,Consoles):
    time_stamps_for_procs                        = []
    magnitude_of_uncon_procs                     = []
    magnitude_of_console_activations             = []

    for t in range (0,test_time):
        UnConIterationCounter = 0

        time_stamps_for_procs.append(t)
        magnitude_of_uncon_procs.append(0)
        magnitude_of_console_activations.append(0)  

        for UnCon in UnCons:
            for console in Consoles:
                if(UnConIterationCounter == 0):
                    console.decrement_console_time()
                    console_name, console_was_triggered = console.try_trigger_console(t)
                                  
                    if(console_was_triggered == True):
                        magnitude_of_console_activations[len(magnitude_of_console_activations)-1] = magnitude_of_console_activations[len(magnitude_of_console_activations)-1] + 1
                    
                    if(console_name == "Subspace Fracture Tunneling Field" and console_was_triggered == True): #if SFTF was just activated
                                    for consoles_to_be_reduced_by_SFTF in Consoles:
                                        if (consoles_to_be_reduced_by_SFTF.get_Name() != "Subspace Fracture Tunneling Field"): #Ensure SFTF isn't reducing itself
                                            consoles_to_be_reduced_by_SFTF.apply_SFTF_Reduction()
                                        else: #If the console is SFTF, then just pass to avoid a reduction
                                            pass
                if t % UnCon.get_GCD() == 0: #Then t / GCD has no remainder, ie we get an uncon proc.

                    if(UnConIterationCounter == 0):
                        magnitude_of_uncon_procs[len(magnitude_of_uncon_procs)-1] = magnitude_of_uncon_procs[len(magnitude_of_uncon_procs)-1] + 1
                    #print(UnCon.get_Name() + " Activated at " + str(t))
                    console.apply_uncon()

                console.elapse_time()
            UnConIterationCounter = UnConIterationCounter+1

    return time_stamps_for_procs, magnitude_of_uncon_procs, magnitude_of_console_activations

  
test_time                                = 250
CleanGetaway                             = UnconProc(30, 15, 0,  "Clean Getaway")
GravityWell                              = UnconProc(60, 40, 0,  "Gravity Well")
PhotonicShockwave                        = UnconProc(40, 30, 0,  "Photonic Shockwave")
TractorBeam                              = UnconProc(30, 20, 10, "Tractor Beam")
EjectWarpPlasma                          = UnconProc(45, 20, 10, "Eject Warp Plasma")
HeisenbergAmplifier                      = UnconProc(30,15,0,    "Heisenberg Amplifier")
TractorBeamRepulsors                     = UnconProc(40,20,10,   "Tractor Beam Repulsors")
ViralImpulseBurst                        = UnconProc(45,30,0,    "Viral Impulse Burst")
IonicTurbulence                          = UnconProc(60,30,0,    "Ionic Turbulence")
ChronometricInversionField               = UnconProc(60,30,0,    "Chronometric Inversion Field")
TimelineCollapse                         = UnconProc(40,20,0,    "Timeline Collapse")
EmitUnstableWarpBubble                   = UnconProc(120,60,0,   "Emit Unstable Warp Bubble")
ScrambleSensors                          = UnconProc(60,40,0,    "Scramble Sensors")
JamTargetingSensors                      = UnconProc(60,40,0,    "Jam Targeting Sensors")
ElectromagneticPulseProbe                = UnconProc(60,30,0,    "Electromagnetic Pulse Probe")

Non_Baryonic_Buffer_Field                = Console(120,30,0,     "Non Baryonic Buffer Field")
Adaptive_Emergency_Systems               = Console(120,0,0,      "Adaptive Emergency Systems")
Dynamic_Power_Redistribution_Module      = Console(120,0,20,     "Dynamic Power Redistribution Module")
Subspace_Fracture_Tunneling_Field        = Console(30,0,0,       "Subspace Fracture Tunneling Field")

UnCons_List = [CleanGetaway, TractorBeam, GravityWell, EjectWarpPlasma, PhotonicShockwave]
Console_List = [Subspace_Fracture_Tunneling_Field, Adaptive_Emergency_Systems]
X, Y, Z = main(UnCons_List,Console_List)

ax.set_xlabel("Time")
ax.set_ylabel("Number of Uncon Procs on Tick")
ax.set_zlabel("Number of Consoles Activated")

# plotting a scatter plot with X-coordinate,
# Y-coordinate and Z-coordinate respectively
# and defining the points color as cividis
# and defining c as z which basically is a 
# definition of 2D array in which rows are RGB
#or RGBA



#Generates full data set
ax.scatter3D(X, Y, Z)

# Showing the above plot
plt.show()
