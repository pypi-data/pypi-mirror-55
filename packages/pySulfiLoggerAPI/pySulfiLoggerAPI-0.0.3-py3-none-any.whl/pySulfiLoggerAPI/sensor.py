import sys
import serial
import serial.tools.list_ports
import time

import tkinter as tk
from tkinter import Label, Entry, StringVar, OptionMenu, simpledialog

global baudrate_
global debug_

def findCom(debug = 0, useAnyDriver = True, driver = ['FTDI','Moxa Inc.'], pickFirst = False ):
    global debug_
    global baudrate_
    ports = serial.tools.list_ports.comports()
    sensorList = []
    for p in ports:
        if useAnyDriver or p.manufacturer in driver:
            baudrate_ = 38400
            debug_ = debug
            try:
                with serial.Serial(p.device, baudrate_, timeout=1) as ser:
                        writeAndRead(ser, "PING", maxattemps=1)
                        if(pickFirst):
                            return p.device
                        else:
                            sensorList.append(p.device)
            except:
                pass

    if(sensorList == []):
        return None
    elif(len(sensorList) == 1):
        return sensorList[0]
    else:
        root=tk.Tk()
        root.withdraw()
        d = SelectFromList(root, sensorList, inputType = 'COM port',title='Select COM port')
        return d.result

#simple get telegrams
def getData(port):
    global baudrate_
    with serial.Serial(port, baudrate_, timeout=1) as ser:
        line = writeAndRead(ser, "GETDATA") 
        stringList = line.decode('latin-1').split(":")
        return stringList[:-1]

def writeAndRead(ser, command, maxattemps = 20, ignoreError = 0):
    command = command + "\n"
    command = command.encode()
    global debug_
    if debug_ == 1:
        print("{:<6} {:<6} {:}".format(ser.name, "Write", command))
    resend = 0
    while resend<2:
        resend = resend + 1    
        ser.write(command)
        attempts = 0
        val = b''
        while attempts < maxattemps+1:
            attempts = attempts + 1
            line = ser.readline()
            val = val + line
            if val[-2:] == b'#\n':
                if debug_ == 1:
                    print("{:<6} {:<6} {:}".format(ser.name, "Read", val))
                return val[:-3]
            if val[-2:] == b'!\n':
                if val[-3:] == b'^!\n':
                    print('Recieved ^!-reply from device -> Resend:{:}'.format(command))
                    resend = 0
                    break
                if (resend<1):
                    #debug_ = 1
                    print('Recieved !-reply from device. Resend initiated.')
                    continue
                if ignoreError == 0:
                    raise RuntimeError('Recieved !-reply from device.')
                return val[:-3]    
            if val[-2:] == b'^':
                print('Recieved ^-reply from device -> Resend:{:}'.format(command))
                resend = 0
                break

        if (maxattemps>1 and resend>0):
            time.sleep(8)
    if ignoreError == 0:
        raise RuntimeError('No response from device, ' + command.decode(), ', resend = {:}'.format(resend))

class SelectFromList(simpledialog.Dialog):
    comport = ''
    optionList = None
    row = 0
    element = []

    def __init__(self, parent, inputList, inputType = '...', title = None):
        self.inputList = inputList
        self.inputType = inputType
        super(SelectFromList, self).__init__(parent, title)

    def body(self, master):
        self.master = master

        # set initial values
        self.dropVar = StringVar()

        self.dropVar.set(f'{self.inputType}') # set the default option
        self.comport = self.inputList[0]

        # add widgets
        self.addOptionMenu(f'Select {self.inputType}: ',self.dropVar,*self.inputList , command = self.change_dropdown)

        # initial focus
        return self.element[0] 

    def addOptionMenu(self, labelText, variable, *values, command):
        Label(self.master, text=labelText).grid(row=self.row, column=0, sticky='W')
        self.element.append( OptionMenu(self.master, variable, *values ,command = command))
        self.element[self.row].grid(row=self.row, column=1)
        self.row += 1

    def addEntry(self, labelText):
        Label(self.master, text=labelText).grid(row=self.row, column=0, sticky='W')
        self.element.append( Entry(self.master))
        self.element[self.row].grid(row=self.row, column=1)
        self.row += 1

    def change_dropdown(self, value):
        self.comport = value

    def apply(self):
        self.result = self.comport

if __name__ == '__main__':
    port = findCom()
    print(port)