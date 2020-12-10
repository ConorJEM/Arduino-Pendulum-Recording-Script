# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 03:33:35 2019

@author: cmcgale
"""

import serial #Package for serial communications
import time #Used for delays and to assign time codes to data readings
import numpy as np #Used for creating vectors, etc. 
import matplotlib.pyplot as plt #For plotting
import math
import os, sys

arduino = serial.Serial('/dev/tty.usbmodem14101', 115200, timeout=.1) #Open connection to Arduino
samples = 300 #We will take this many readings
angle_data = np.zeros(samples) #Creates a vector for our angle data
time_data = np.zeros(samples) #Creates a vector of same length for time
i = 1;
timeinit = time.clock()
print(timeinit)
calibrate = 125 #Value to zero potentiometer reading when pendulum is motionless, read from Arduino
with open("//Users/cmcgale/Desktop/output.csv",'w') as out:
    while i!=samples:
        data = arduino.readline()[0:-2].decode('utf-8')
        if data:
            angle_data[i] = float(data)
            time_data[i] = (time.clock()-timeinit)*10
            out.write("{0},{1}\n".format(angle_data[i],time_data[i]))
            i = i + 1
            plt.plot(time_data,angle_data-calibrate,'k.')
            plt.axis([0,15,0,200])

plt.show()
arduino.close()
#Hard to fit to the oscillotory data as our time step is large
#Coding a peak finding algorithm so we can fit the decay more accurately
x = time_data
y = angle_data
peaksx = []
peaksy =[]
avg = y.mean()
y = y - avg
plt.figure()
plt.subplot(1,2,1)
peaksx.append(x[0])
peaksy.append(y[0])
plt.plot(x[0],y[0],'r.')
for i in range(len(x)):
    if i == 0 or i == len(x)-1:
        continue
    if y[i] <= y[i-1]:
        if y[i] <= y[i+1]:
            if -y[i] == peaksy[-1]:
                plt.plot(x[i],y[i],'k.')
                continue
            plt.plot(x[i],y[i],'r.')
            peaksx.append(x[i])
            peaksy.append(-y[i])
            continue
    else:
        if y[i] >= y[i+1]:
            if y[i] == peaksy[-1]:
                plt.plot(x[i],y[i],'k.')
                continue
            plt.plot(x[i],y[i],'r.')
            peaksx.append(x[i])
            peaksy.append(y[i])
            continue
    plt.plot(x[i],y[i],'k.')

plt.subplot(1,2,2)
fitx = []
fity = []

for j in range(len(peaksx)):
    if peaksy[j] > 0 and j < 14:
        fitx.append(peaksx[j])
        fity.append(peaksy[j])
        plt.plot(peaksx[j],peaksy[j],'b.')

tofitx = np.array(fitx)
tofity = np.array(fity)
line = np.polyfit(np.exp(tofitx), (tofity), 1, w=(tofity)**2)
print(line)
tempx = np.linspace(0,5,100)
plt.plot(tempx,line[1]*np.exp(line[0]*tempx))
plt.show()

with open("//Users/cmcgale/Desktop/output_peaks.csv",'w') as out:
    for i in range(len(tofitx)):
        out.write("{0},{1}\n".format(tofitx[i],tofity[i]))