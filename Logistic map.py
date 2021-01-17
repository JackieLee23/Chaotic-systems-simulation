import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
from random import randint
from scipy.integrate import odeint
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.colors as mcolors
plt.style.use('dark_background')

fig = plt.figure()
ax = fig.add_subplot(111)

initpop = 0.5
r = 2.0
steps = 50

ax.set_ylim(-0.1, 1.1)
ax.set_position([0.1, 0.2, 0.8, 0.7])

l, = ax.plot([], [])
x = np.arange(0)
y = []

#draw new set
def newSet():
    global x, y
    ax.set_xlim(-1, steps)
    x = np.arange(steps + 1)
    y = [initpop]
    for i in range(steps):
        newpop = r * y[i] * (1 - y[i])
        y.append(newpop)

    l.set_xdata(x)
    l.set_ydata(y)
    




#make options sliders
#on update, redraw

def update(val):
    global initpop, r, steps
    steps = sliders[0].val
    initpop = sliders[1].val
    r = sliders[2].val
    
    newSet()

    




sliders = []
slidernames = ["Iteration num", "Initial pop", "r"]
sliderinitials = [50, 0.5, 2]
sliderrange = [[1, 200], [0, 1.0], [0, 4.0]]
slidersteps = [1, 0.01, 0.01]
axcolor = 'lightgoldenrodyellow'

for i in range(3):
    newax = plt.axes([0.1 + i * 0.3, 0.05, 0.15, 0.02], facecolor = axcolor)
    snew = Slider(newax, slidernames[i], sliderrange[i][0], sliderrange[i][1], valinit = sliderinitials[i], valstep=slidersteps[i])
    snew.on_changed(update)
    sliders.append(snew)



newSet();

plt.show()
    
