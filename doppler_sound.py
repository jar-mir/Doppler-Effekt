from matplotlib import pyplot as plt
import numpy as np
from IPython.display import Audio
from scipy.io import wavfile


class simulation:
    def __init__(self, sound_speed, sim_frequency):
        self.c = sound_speed
        self.f = sim_frequency

    def setup_source(self, x, y, velocity):
        self.source_StartPos = (x,y)
        self.source_velocity = velocity      
    def setup_observer(self, x, y, velocity):
        self.observer_StartPos = (x,y)
        self.observer_velocity = velocity   
    def source_position(self, time_intervall, accuracy):
        pos = [(self.source_StartPos[0]+t*accuracy*self.source_velocity[0], self.source_StartPos[1]+t*accuracy*self.source_velocity[1])
               for t in range(int(time_intervall[0]*(1/accuracy)),int(time_intervall[1]*(1/accuracy)))]
        return np.array(pos)    
    def observer_position(self, time_intervall, accuracy):
        pos = [(self.observer_StartPos[0]+t*accuracy*self.observer_velocity[0], self.observer_StartPos[1]+t*accuracy*self.observer_velocity[1])
               for t in range(int(time_intervall[0]*(1/accuracy)),int(time_intervall[1]*(1/accuracy)))]
        return np.array(pos)    
    def calc_xDistance(self, time_intervall, accuracy):
        pos_source = self.source_position(time_intervall, accuracy)
        pos_oberserver = self.observer_position(time_intervall, accuracy)

        xdist = [pos_oberserver[t][0]-pos_source[t][0]
                for t in range(0,int(time_intervall[1]*(1/accuracy))-int(time_intervall[0]*(1/accuracy)))]
        return np.array(xdist)
    def calc_yDistance(self, time_intervall, accuracy):
        pos_source = self.source_position(time_intervall, accuracy)
        pos_oberserver = self.observer_position(time_intervall, accuracy)

        ydist = [pos_oberserver[t][1]-pos_source[t][1]
                for t in range(0,int(time_intervall[1]*(1/accuracy))-int(time_intervall[0]*(1/accuracy)))]
        return np.array(ydist)
    def calc_totalDistance(self, time_intervall, accuracy):
        x_dist = self.calc_xDistance(time_intervall, accuracy)
        y_dist = self.calc_yDistance(time_intervall, accuracy)

        total_dist = [np.sqrt(x_dist[t]**2+y_dist[t]**2)
                      for t in range(0,int(time_intervall[1]*(1/accuracy))-int(time_intervall[0]*(1/accuracy)))]
        return np.array(total_dist)
    def calc_frqCurve(self, time_intervall, accuracy):
        x_dist = self.calc_xDistance(time_intervall, accuracy) 
        y_dist = self.calc_yDistance(time_intervall, accuracy) 
        f_curve = []
        for i in range(0,int(time_intervall[1]*(1/accuracy))-int(time_intervall[0]*(1/accuracy))):
            total_dist = np.sqrt(x_dist[i]**2 + y_dist[i]**2)
            if total_dist == 0:
                e = (  0 , 0  )
            else:
                e = (  x_dist[i]/total_dist , y_dist[i]/total_dist  )

            v_o = (self.observer_velocity[0]*e[0]+self.observer_velocity[1]*e[1])
            v_s = (self.source_velocity[0]*e[0]+self.source_velocity[1]*e[1])
            if self.c-v_s <= 0:
                f_curve.append(0)
            else:
                f_curve.append( self.f * (self.c-v_o)/(self.c-v_s))

        return np.array(f_curve)
    def calc_Error(self, time_intervall, accuracy):
        f = self.calc_frqCurve((time_intervall[0],time_intervall[1]), accuracy)
        error = [np.abs(f[i]-f[i-1]) for i in range(1,len(f))]
        error.append(0)
        return np.array(error)
    def calc_FrequencyShift(self, time_intervall, accuracy):
        f = self.calc_frqCurve(time_intervall, accuracy)
        shift = [f[0]*accuracy*2*np.pi]
        for i in range(1,len(f)):
            shift.append(f[i]*accuracy*2*np.pi+shift[i-1])
        return np.array(shift)
    def calc_Amplitude(self, time_intervall, accuracy): #approximation with  constant speed
        x_dist = self.calc_xDistance(time_intervall, accuracy)
        y_dist = self.calc_yDistance(time_intervall, accuracy)
        amp = [0 for t in range(0,int(time_intervall[1]*(1/accuracy))-int(time_intervall[0]*(1/accuracy)))]

        for t in range(0,int(time_intervall[1]*(1/accuracy))-int(time_intervall[0]*(1/accuracy))):  

            xdist_t = x_dist[t]
            xdist_total =  (xdist_t*self.c)/(self.c-self.source_velocity[0])
            ydist_t = y_dist[t]
            ydist_total =  (ydist_t*self.c)/(self.c-self.source_velocity[1])

            total_dist = np.sqrt(xdist_total**2+ydist_total**2)

            if total_dist == 0:
                amp[t] = 1
            else: 
                amp[t] = (1/(total_dist**2))

        return np.array(amp)
        #return 3**-(total_dist**2/1000) + 0.2 * 3**-(total_dist**2/10000000) 
    def calc_Amplitude2(self, time_intervall, accuracy): #approximation with  constant speed
        total_dist = self.calc_totalDistance(time_intervall, accuracy)
        amp = []
        for t in range(len(total_dist)):  
            if total_dist[t] == 0:
                amp.append(1)
            else: 
                amp.append(1/(total_dist[t]**2))

        return np.array(amp)
        #return 3**-(total_dist**2/1000) + 0.2 * 3**-(total_dist**2/10000000)  
    def plot(self, data, label, time_intervall, accuracy, size = (4,4)):
        x = [i*accuracy for i in range(int(time_intervall[0]*(1/accuracy)),int(time_intervall[1]*(1/accuracy)))]
        fig, ax = plt.subplots(figsize=(size[0],size[1]))
        ax.plot(x,data)
        ax.set_title(label)
        plt.show()
    def plot_(self, plots,label, time_intervall, accuracy):
        x = [i*accuracy for i in range(int(time_intervall[0]*(1/accuracy)),int(time_intervall[1]*(1/accuracy)))]
        fig, ax = plt.subplots(1,len(plots), figsize=(4*len(plots),4))
        for i in range(len(plots)):
            ax[i].plot(x,plots[i])
            ax[i].set_title(label[i])
        plt.show()
    def plot_Scene(self, time_intervall = (0,20), accuracy = 1):
        fig, ax = plt.subplots(1,2,figsize=(8, 4))

        
        # plot the source and observer
        ax[0].plot(self.source_StartPos[0], self.source_StartPos[1], "o", color="blue")
        ax[0].plot(self.observer_StartPos[0],self.observer_StartPos[1], "o", color="red")
        if self.observer_velocity[0] != 0 or self.observer_velocity[1] != 0:
            ax[0].arrow(self.observer_StartPos[0],self.observer_StartPos[1], self.observer_velocity[0], self.observer_velocity[1], head_width=2, head_length=2, fc='k', ec='k')
        if self.source_velocity[0] != 0 or self.source_velocity[1] != 0:
            ax[0].arrow(self.source_StartPos[0], self.source_StartPos[1], self.source_velocity[0], self.source_velocity[1], head_width=2, head_length=2, fc='k', ec='k')
        ax[0].axis('equal')
        ax[0].set_title("Startposition")
        #plt.show()


        source = self.source_position(time_intervall, accuracy)
        observer = self.observer_position(time_intervall, accuracy)

        #fig, ax = plt.subplots(figsize=(4, 4))
        ax[1].plot([elem[0] for elem in source],[elem[1] for elem in source], color = "blue", label = "source")
        ax[1].plot([elem[0] for elem in observer],[elem[1] for elem in observer], color = "red", label = "observer") 
        ax[1].axis('equal')
        ax[1].set_title("Bewegungsverlauf")
        plt.show()

    
    
    

if __name__ == "main":
    print("Test Simulation")
    my_sim = simulation(340, 440)

    my_sim.setup_observer(0,0,(0,0))
    my_sim.setup_source(-100,10,(10,0))
    shift = my_sim.calc_FrequencyShift((0,20), 0.0001)
    Audio(np.sin(shift), rate = int(1/0.0001))