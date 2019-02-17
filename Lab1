"""
Last modified on 2/13/19

@author: Gerardo Armenta
lab 1
"""
import numpy as np
import matplotlib.pyplot as plt
import math

def square(ax,n,p,w,c):
    if n>0:
        i1 = [1]
        t = (p*w) + p[i1]
        q = (p*w) - 400
        ax.plot(p[:,0],p[:,1],color=c)
        square(ax,n-1,q,w,'b')
        square(ax,n-1,q*-1,w,'r')
        square(ax,n-1,t,w,'y')
        square(ax,n-1,t*-1,w,'g')

plt.close('all') 
orig_size = 400
w = 0.5
p = np.array([[-orig_size,-orig_size],[-orig_size,orig_size],[orig_size,orig_size],[orig_size,-orig_size],[-orig_size,-orig_size]])
fig, ax = plt.subplots()
square(ax,2,p,w,'k')
ax.set_aspect(1.0)
ax.axis('off')
plt.show()

# the properties of a circle 
def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

# Plots n circles
def draw_circles(ax,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        center[0] = center[0]*w
        draw_circles(ax,n-1,center,radius*w,w)
      
fig, ax = plt.subplots() 
# for 2a use draw_circles(ax,10,[100,0],100,.6)
# for 2b use draw_circles(ax,50,[100,0],100,.9)
# for 2c use draw_circles(ax, 110, [100,0], 100,.96)
draw_circles(ax, 10, [100,0], 100,.6)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()

# plots binary tree
def draw_triangle(ax,n,p,w):
        ax.plot(p[:,0],p[:,1],color='k')
        triangles(ax,n,p,w)
        
def triangles(ax,n,q,w):
    if n>0:
        neg = (q - 800)
        ax.plot(neg[:,0],neg[:,1],color='k')
        pos = (q + 800)
        ax.plot(pos[:,0],pos[:,1],color='b')
        triangles(ax,n-1,q,w)

orig_size = 800
p = np.array([[-orig_size,0],[0,orig_size],[orig_size,0],])
fig, ax = plt.subplots()
draw_triangle(ax,1,p,.2)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()

# Plots n circles inside n circles
def draw_circles(ax,n,center,radius,w,c):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color=c)
        draw_circles(ax,n-1,center,radius*w,w,'b')
        center[0] = center[0]*.58
        draw_circles(ax,n-1,center,radius*w,w,'g')  
      
fig, ax = plt.subplots() 
draw_circles(ax, 2, [100,0], 100,.33,'k')
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
