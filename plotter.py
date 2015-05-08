import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib import rcParams
from matplotlib.backends import qt4_compat
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
rcParams['legend.fontsize'] = 14
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True
rcParams['figure.figsize'] = 16, 9
rcParams['grid.alpha'] = 0.7
rcParams['patch.facecolor'] = 'white'
rcParams['patch.edgecolor'] = 'white'
rcParams['axes.titlesize'] = 24
rcParams['axes.labelsize'] = 18
# rcParams['patch.edgecolor'] = 'FFFFFF'


class Plotter(FigureCanvas):

    def __init__(self, parent=None):
        dpi = 100
        self.plot_options = {"linewidth":3,"color":"k"}
        self.plot_options_axes = {"linewidth":2, "color":'0.7'} #,'alpha':0.7}
        self.fig = Figure(figsize=(16,9), dpi=dpi)
        
        # x=np.arange(-10,10,0.1)
        # y=np.sin(x)
        # self.make_graph(x,y)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def save(self):
        self.fig.savefig('plot.png')    

    def make_graph(self, x, y,*args):
        """
        This just makes a very simple plot.
        """
        # try:
        #     a = args[0]
        # except IndexError:
        #     a = 1.0
        # y = a*y
        self.fig.clf()
        ax1 = self.fig.add_subplot(111)
        # ax1.hold(False)
        x_space = np.absolute(x[0] - x[1])
        y_max, y_min = np.amax(y), np.amin(y)
        y_space = np.absolute(y_max - y_min)
        ax1.set_xlim((x[0]-5.0*x_space,x[-1]+5.0*x_space))
        ax1.set_ylim([y_min-0.25*y_space, y_max+0.25*y_space])
        ax1.grid()
        ax1.set_xlabel(r"$x$")
        ax1.set_ylabel(r"$f(x)$")
        # ax1.set_title(r"Graph of $f(x)$")
        x_axis = np.linspace(x[0]-5.0*x_space,x[-1]+5.0*x_space,x.size)
        ax1.plot(x_axis, np.zeros(x.size), **self.plot_options_axes)
        ax1.plot(np.zeros(x.size), np.linspace(y_min-0.25*y_space, y_max+0.25*y_space,x.size),**self.plot_options_axes)
        ax1.plot(x, y, **self.plot_options)
        # return ax1

# x=np.arange(-10,10,0.1)
# y=np.sin(x)
# graph = Plotter()
# ax = graph.make_graph(x,y)
# plt.show()


