from plotter import Plotter
from interpret import interpreter, evaluater, diffeqsolver, gen_code
from PyQt4 import QtGui, QtCore
import sys
from numpy import *


class ApplicationWindow(QtGui.QMainWindow):

    def __init__(self):

        QtGui.QMainWindow.__init__(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Application Main Window")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        self.main_widget = QtGui.QWidget(self)

        self.grid = QtGui.QGridLayout(self.main_widget) #setting layout type
        self.grid.setColumnMinimumWidth(4,200)
        self.grid.setSpacing(10)

        self.graph = Plotter(self.main_widget)

        self.input_box = QtGui.QLineEdit("plot y=exp(-(x)**2) from -4 to 4")
        self.text_box = QtGui.QTextEdit("Code Snippets Here.")

        self.slider_display = QtGui.QLineEdit("")

        self.button_plot = QtGui.QPushButton('Plot')
        self.button_plot.clicked.connect(self.plot_init)

        self.button_save = QtGui.QPushButton('Save')
        self.button_save.clicked.connect(self.save)
        # dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.grid.addWidget(self.graph,1,0,1,3)
        self.grid.addWidget(self.button_plot,0,1)
        self.grid.addWidget(self.button_save,0,2)
        self.grid.addWidget(self.input_box,0,0)
        self.grid.addWidget(self.text_box,1,4,1,2)
        # self.grid.addWidget(self.slider1,0,2,1,1)
        # self.grid.addWidget(self.slider_display,0,3,1,1)
        # l.addWidget(dc)

        # self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

    def save(self):
        print("Save")
        self.plot_init()
        self.graph.save()

    def plot_init(self):
        """
        This function initializes the plot. 
        If sliders need to be created, it happens here. 
        """
        text = str(self.input_box.text())
        self.val_range, self.fn, self.mod_list,self.method = interpreter(text)

        if len(self.mod_list) != 0:
            start = [1 for i in self.mod_list]
            self.grid.setColumnMinimumWidth(2,100)
            self.group_box = QtGui.QGroupBox("Modifiers")
            self.vbox = QtGui.QVBoxLayout()
            self.sliders = []
            for i in xrange(len(self.mod_list)):
                slider1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
                slider1.setRange(1,10)
                slider1.valueChanged.connect(self.plot_w_slider)
                self.sliders.append(slider1)
                self.vbox.addWidget(slider1)
                self.vbox.addStretch(1)
                self.group_box.setLayout(self.vbox)
                self.grid.addWidget(self.group_box, 1,3,1,1)
            if isinstance(self.method,str):
                x, y = evaluater(self.val_range,self.fn,self.mod_list,start)
            elif isinstance(self.method,dict):
                x, y = diffeqsolver(self.val_range,self.fn,self.method['solve'],self.mod_list,start)

            if y == "Error":
                self.text_box.append("Error")
            self.graph.make_graph(x,y)
            self.graph.draw()
            code = gen_code(self.val_range, self.fn, self.mod_list,values)
            self.text_box.append(code)

        elif len(self.mod_list) == 0:
            self.grid.setColumnMinimumWidth(2,10)
            if isinstance(self.method,str):
                x, y = evaluater(self.val_range,self.fn)
            elif isinstance(self.method,dict):
                x, y = diffeqsolver(self.val_range,self.fn,self.method['solve'])
            if y == "Error":
                self.text_box.append("Error")
            self.graph.make_graph(x,y)
            self.graph.draw()      
            code = gen_code(self.val_range,self.fn)
            self.text_box.append(code)

    # @QtCore.pyqtSlot(int)
    def plot_w_slider(self):
        values = [slider.value() for slider in self.sliders]
        # print(values)
        x, y = evaluater(self.val_range,self.fn,self.mod_list,values)
        if y == "Error":
            self.text_box.append("Error")
        self.graph.make_graph(x,y)
        self.graph.draw()

        code = gen_code(self.val_range, self.fn, self.mod_list,values)
        self.text_box.append(code)



    @QtCore.pyqtSlot(int)
    def get_text_plot(self,*args):
        try:
            a = float(args[0])
            print(a)
        except IndexError:
            a = 1.0
        text = str(self.input_box.text())
        x, y = interpreter(text)
        self.graph.make_graph(x,y,a)
        self.graph.draw()


    def closeEvent(self, ce):
        self.fileQuit()


qApp = QtGui.QApplication(sys.argv)
aw = ApplicationWindow()
# aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
