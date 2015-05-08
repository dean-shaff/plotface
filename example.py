

from numpy import *
import matplotlib.pyplot as plt

def f(x,*args):
	return exp(-(x)**2) 

x = arange(-4.0,4.0,0.1)
y = f(x,)

fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(111)
ax.plot(x,y)
plt.show()