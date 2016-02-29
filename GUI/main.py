from PyQt4 import QtCore, QtGui, uic

from PyQt4.QtCore import QTimer
import sys

import time
from Engine.SerialPort import SerialPort


from matplotlibwidget import MatplotlibWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


import random

mainGUI = uic.loadUiType("CarGUI.ui")[0] # load ui Copyright Jérome Mallet 2015
 
class MyWindowClass(QtGui.QMainWindow, mainGUI):
	def __init__(self, parent=None):
	
		self.lap = 0
		QtGui.QMainWindow.__init__(self,parent)
		self.setupUi(self)
		self.listPlot = []
		self.lapTable.setColumnWidth(1,  140);
		self.lapTable.setRowCount(0)
        #engine: 
		self.serialthread = SerialPort()	
		self.serialthread.start()
		self.refresh_COM_Ports()

		#Timer 
		self.timer_chrono = QTimer(self)
		self.connect(self.timer_chrono, QtCore.SIGNAL("timeout()"), self.update_chrono)
		
		self.start_time = 0;
        #var:
		self.connected = False        
		self.variables = dict()
		self.selected_var_id = None
       # self.listPorts=[]
       # self.listPorts_desc=[]
        
        #signals:
		
		self.btn_refresh.clicked.connect(self.refresh_COM_Ports)
		self.btn_connect.clicked.connect(self.start_COM)
		self.btn_disconnect.clicked.connect(self.serialthread.disconnect)

		self.btn_clear.clicked.connect(self.clearData)
		
		#Matplotlib
		# a figure instance to plot on
		self.figure = self.mpl_w.figure

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
		self.canvas = FigureCanvas(self.figure)
		
		self.results = []
		self.prev = 0
        # create an axis
		self.ax = self.figure.add_subplot(111)
        # discards the old graph
		self.ax.hold(False)

		self.ax.plot([1,2,3,4,5,6,7,8], '-')

        # refresh canvas
		self.canvas.draw()
		
        
		
		
		#Connexion :
		
		
		self.connect( self.serialthread, QtCore.SIGNAL("com_connected(QString)"), self.com_connected )
		self.connect( self.serialthread, QtCore.SIGNAL("com_disconnected(QString)"), self.com_disconnected )
		self.connect( self.serialthread, QtCore.SIGNAL("refresh_results(QString)"), self.refresh_results )
	
	
	def clearData(self) : 
		self.results = []
		
		for i in range(0,self.lapTable.rowCount()) :
			self.lapTable.removeRow(0)
		self.ax.clear()
		self.mpl_w.draw()
		
	def get_time_ms(self) :
		return  int(round(time.time() *1000))
		
	def update_chrono(self) :
		delta = (self.get_time_ms()-self.start_time)/10 #Time in ms 		
		self.labelChrono.setText("%02d:%02d" %((int(delta/100)),(int(delta%100))))
		self.labelChrono.setStyleSheet('color: black')
		self.timer_chrono.start(50)
		
	def refresh_results(self, readline) :
	
		#Append result 
		self.results.append(int(readline))
		
		readline = str(int(int(readline)/1000)) +" s " + str(int(readline)%1000) + " ms"
		row=self.lapTable.rowCount()
		self.lapTable.insertRow(row)
		self.lapTable.setItem(row,0,QtGui.QTableWidgetItem(str(row)))
		self.lapTable.item(row,0).setTextAlignment(QtCore.Qt.AlignCenter)
		
		self.lapTable.setItem(row,1,QtGui.QTableWidgetItem(readline)) 
		self.lapTable.item(row,1).setTextAlignment(QtCore.Qt.AlignCenter)
		
		self.lapTable.setItem(row,2,QtGui.QTableWidgetItem(str(self.results[-1] - self.prev) + " ms")) 
		self.lapTable.item(row,2).setTextAlignment(QtCore.Qt.AlignCenter)
		
		self.prev = self.results[-1]
		
		#Chrono color style :
		self.labelChrono.setStyleSheet('color: green')
		
		
		
		
		
		#Stop the timer 
		self.timer_chrono.stop()
		
		#Update graph :
		
		# plot data
		
		self.ax = self.figure.add_subplot(111)
        # discards the old graph
		self.ax.hold(False)

		self.ax.plot(self.results, '*-')

        # refresh cplt		
		self.mpl_w.draw()
		
		#Timer visible for 2s
		self.timer_chrono.start(2000)
		self.start_time = self.get_time_ms()  #Start time for chrono
	def closeEvent(self, event):
		self.listPlot.clear()
		self.serialthread.stop()
		event.accept()

        
        
    # ------------- COM FRAME -----------------    
	def refresh_COM_Ports(self):
		Ports = self.serialthread.get_ports()
		self.listPorts=[]
		self.listPorts_desc=[]
		print('COM ports list :') 
		for p, desc, hwid in sorted(Ports):
			print('--- %s %s %s\n' % (p, desc, hwid))
			self.listPorts.append(p)
			self.listPorts_desc.append(desc)
		self.comboBox.clear()
		self.comboBox.addItems(self.listPorts_desc)
    
	def start_COM(self):
		if self.connected:
			return
        
		self.text_connected.setText("<font color='orange'>CONNECTING</font>")
		if self.comboBox.currentText()=="":
			print("No port selected, aborting.")
			self.text_connected.setText("<font color='red'>NO CONNECT</font>")
			return
        
		port=self.listPorts[self.comboBox.currentIndex()]
		self.serialthread.connect(port,9600)
	def com_connected(self,text):
		self.connected=True
		self.text_connected.setText("<font color='green'>CONNECTED</font>")
    
	def com_disconnected(self):
		self.connected=False
		self.text_connected.setText("<font color='red'>NO CONNECT</font>")
    #---------------------------------------------
	
	


	
# création fenetre/class 
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
