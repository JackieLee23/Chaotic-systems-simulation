import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
from random import randint
from scipy.integrate import odeint
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.colors as mcolors
plt.style.use('dark_background')



fig = plt.figure() 
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')
ax.set_xlim((-50, 50))
ax.set_ylim((-50, 50))
ax.set_zlim((-50, 50))



#initial paths
lines = []
markers = []
t = np.arange(0.0, 100.0, 0.01)
initial = [0.0, 0.0, 0.0]
paths = []

#Initial lorenz constants
rh = 28.0
sig = 10.0
beta = 8.0 / 3.0


#Initial cluster settings
clusterSize = 10
clusterRad = 1.0

#Initial animation settings
clicked = True
cluster = False
iteration = 1




#Create paths for a new animation
def diff(state, t):
    return sig * (state[1] - state[0]), state[0] * (rh - state[2]) - state[1], state[0] * state[1] - beta * state[2]

def makePaths():
    global paths, initial, lines, markers
    lines = []
    markers = []
    
    for i in range(clusterSize):
        col = '#%06X' % randint(0x777777, 0xFFFFFF)
        line, = ax.plot([], [], [], lw = 0.5, c= col)
        marker, = ax.plot([], [], [], 'o', c='red')
        markers.append(marker,)
        lines.append(line,)
        
    inits = initial - np.full((3), clusterRad) + 2 * clusterRad * np.random.rand(clusterSize, 3)
    paths = [odeint(diff, init, t) for init in inits]



#animation frame
def newframe(i):
    global iteration
    if clicked:
        return lines + markers
    
    for x in range(len(lines)):
        lines[x].set_data(paths[x][:iteration,0] , paths[x][:iteration,1])
        lines[x].set_3d_properties(paths[x][:iteration,2])
        
        markers[x].set_data(paths[x][iteration-1,0] , paths[x][iteration - 1,1])
        markers[x].set_3d_properties(paths[x][iteration - 1,2])

    iteration += 1
    return lines + markers

# call the animator
makePaths()
anim = animation.FuncAnimation(fig, newframe, frames = 10000, interval=1, blit=True)







#buttons and slider functions
def pause(event):
    global clicked
    clicked = True

def resume(event):
    global clicked
    clicked = False

def clear(event):
    anim.event_source.stop()

def startNew(event):
    global iteration, clicked, cluster
    clicked = False
    iteration = 1
    makePaths()
    anim.event_source.stop()
    
    anim.event_source.start()


def updateSlider(value):
    global initial, rh, sig, beta, clusterSize, clusterRad
    
    initial[0] = sliders[0].val
    initial[1] = sliders[1].val
    initial[2] = sliders[2].val

    rh = sliders[3].val
    sig = sliders[4].val
    beta = sliders[5].val

    clusterSize = sliders[6].val
    clusterRad = sliders[7].val
    


#Make buttons and sliders

#buttons
axcolor = 'lightgoldenrodyellow'

axcluster = plt.axes([0.1, 0.9, 0.1, 0.05])
bcluster = Button(axcluster, 'New', color="red")
bcluster.on_clicked(startNew)

axpause = plt.axes([0.3, 0.9, 0.1, 0.05])
bpause = Button(axpause, 'Pause', color="red")
bpause.on_clicked(pause)

axstart = plt.axes([0.5, 0.9, 0.1, 0.05])
bstart = Button(axstart, 'Resume', color="red")
bstart.on_clicked(resume)

axclear = plt.axes([0.7, 0.9, 0.1, 0.05])
bclear = Button(axclear, 'Clear', color="red")
bclear.on_clicked(clear)


#sliders
sliders = []
slidernames = ["Initial x", "Initial y", "Initial z", "Rho", "Sigma", "Beta", "Number points", "Cluster Radius"]
sliderinitials = [1.0, 1.0, 1.0, 28.0, 10.0, 8.0 / 3.0, 10, 1.0]

slidersteps = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1, 0.01]
sliderrange = [[-50.0, 50.0], [-50.0, 50.0], [-50.0, 50.0], [-60.0, 60.0], [-60.0, 60.0], [-60.0, 60.0], [1, 25], [0.0, 50.0]]

for i in range(8):
    
    ainitx = plt.axes([0.1, 0.7 - 0.08 * i, 0.15, 0.02], facecolor=axcolor)
        
    sinitx = Slider(ainitx, slidernames[i], sliderrange[i][0], sliderrange[i][1], valinit = sliderinitials[i], valstep=slidersteps[i])
    sinitx.on_changed(updateSlider)
    sliders.append(sinitx)



plt.show()
 
