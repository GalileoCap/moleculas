#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:34:09 2019

@author: ep-m2-07
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 09:44:26 2019

@author: Galileo Cappella
"""

import random
import numpy as np

def random_start(n, x_size, y_size, z_size): #U: Creates random positions for each molecule #A: Stolen from my Prey vs Predator simmulator
    r= np.repeat(" ", x_size*y_size*z_size).reshape(x_size, y_size, z_size)
    x_pos= []
    y_pos= []
    z_pos= []
    
    i= 0
    while i < n:
        pos= (random.randint(0, x_size-1), random.randint(0, y_size-1), random.randint(0, z_size-1))
        if r[pos] == " ":
            r[pos]= "P"
            x_pos.append(pos[0])
            y_pos.append(pos[1])
            z_pos.append(pos[2])
            i+= 1

    print('Posiciones iniciales = \n', r)
    return x_pos, y_pos, z_pos

def random_vel(n, vmin, vmax): #U: Crea n velocidades al azar (la velocidad en xyz es la misma)
    r= []
    for i in range(n):
        r.append(random.randint(vmin, vmax)**(1./3.))
        
    return r, r, r

def random_mass(n, which): #U: Elije al azar entre las masas qe hayas elegido
    r= []
    for i in range(n):
        r.append(which[random.randint(0, len(which)-1)])

    return r
    
def calc_force(i, pos_x, pos_y, pos_z, K): #U: Calculates the force "felt" by this molecule
    Fx, Fy, Fz= [0] * 3 #A: Each force starts with a value of zero
    for j in range(len(pos_x)):
        if j != i:
            distance= (pos_x[i]-pos_x[j])**2 + (pos_y[i]-pos_y[j])**2 + (pos_z[i]-pos_z[j])**2 #A: Sacada de la consigna
            Fx+= (pos_x[i]-pos_x[j])/(distance**3) #A: Sacada de la consigna
            Fy+= (pos_y[i]-pos_y[j])/(distance**3)
            Fz+= (pos_z[i]-pos_z[j])/(distance**3)
    Fx= 4*K*Fx #A: Terminando la formula
    Fy= 4*K*Fy
    Fz= 4*K*Fz
    
    return Fx, Fy, Fz

def check_sides(pos, v, side): #U: Checks if the molecule bounced with a side
    if pos > side:
        v= -v
        pos-= 2*(pos-side)
    if pos < side:
        v= -v
        pos-= 2*pos

    return pos, v
def simmulate(n=20, r=1, dt=1, which=[1], vol= 50, vmin=0, vmax=0): 
    #A: n=cantidad de particulas; r= cantidad de frames; dt= dela tiempo en segundos; m= masa de las particulas; which= masas posibles; vol= volumen en cm3; vmin/vmax= rango para las velocidades iniciales
    K= 1E-1 #A: I use this value because it works for me, but the actual constant K = 1.38064852E-23
    
    pos_x, pos_y, pos_z= random_start(n, vol, vol, vol)
    vx, vy, vz= random_vel(n, vmin, vmax)
    m= random_mass(n, which)
    
    salida= open("salida.xyz", "w")

    for l in range(r):
        print(n, file=salida) #A: For making the ".xyz" file and storing the coordinates
        print(" ", file=salida)
        for jj in range(n):
            print("6", pos_x[jj], pos_y[jj], pos_z[jj], "0", file=salida)
        
        paso_x= [] #A: Para guardar las posiciones y despues reemplazar las pos
        paso_y= []
        paso_z= []
        
        for i in range(n):
            Fx, Fy, Fz= calc_force(i, pos_x, pos_y, pos_z, K)
            
            vx[i]+= (Fx/m)*dt #A: See README
            vy[i]+= (Fy/m)*dt
            vz[i]+= (Fz/m)*dt
            
            esta_x= pos_x[i]+vx[i]*dt
            esta_y= pos_y[i]+vy[i]*dt
            esta_z= pos_z[i]+vz[i]*dt
            
            esta_x, vx[i]= check_sides(esta_x, vx[i], vol)
            esta_y, vy[i]= check_sides(esta_y, vy[i], vol)
            esta_z, vz[i]= check_sides(esta_z, vz[i], vol)
                
            paso_x.append(esta_x)
            paso_y.append(esta_y)
            paso_z.append(esta_z)

        #print('PASO Nº', l, '\n', paso_x, '\n', paso_y)
        pos_x= paso_x.copy() #A: Actualizo las posiciones
        pos_y= paso_y.copy()
        pos_z= paso_z.copy()
        
    print("END")
#simmulate(250, 1000)
#simmulate(30, 100, x_size=100, y_size=100)