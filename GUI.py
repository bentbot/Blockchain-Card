#!/usr/bin/env python3

import tkinter as tk
import sys, time, cardReaderExceptions, cardReader
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
import sqlite3
SERIAL_PORT = '/dev/cu.usbserial-142430'

class GUI(Frame):    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.__coercivityRadioBtnValue = StringVar()
        self.__coercivityRadioBtnValue.set('hi')
        
        self.__autoSaveDatabase = BooleanVar()
        self.__autoSaveDatabase.set(False)
        
        self.__enableDuplicates = BooleanVar()
        self.__enableDuplicates.set(False)
        
        self.__connected = False        
        self.__connectedLabelIndicator = None
        
        self.__blockchain_label = None
        self.__public_key = None
        self.__private_key = None
        self.__pubKeyEntry = None
        self.__privKeyEntry = None

        self.__tracks = ['', '', '']
        self.__trackOneEntry = None
        self.__trackTwoEntry = None
        self.__trackThreeEntry = None        
        
        self.__msr = None
        
        self.build_main_window()

    def octal_to_str(self,octal_str):
        str_converted = ""
        for octal_char in octal_str.split(" "):
            str_converted += chr(int(octal_char, 8))
        return str_converted

    def encode_public(self,alpha):
        i = 0
        a = ''
        
        # TODO

        # for a in alpha:
            # print (oct(a))
        # exit();

        # b = ''
        # for x in alpha:
        #     if i < 80:
        #         a = a+x
        #     else:
        #         b = b+x
        #     i=i+1
        # print (a)

        # ab = [oct(a),oct(b)]
        # print (ab)
        # return ab

    def convert_pub(self,alpha,beta):
        gamma = alpha+beta
        os = "".join(char for char in gamma if char.isdigit())
        os = ' '.join([os[i:i+3] for i in range(0, len(os), 3)])
        self.__public_key = self.octal_to_str(os)
        return self.__public_key

    def encode_private(self,alpha):
        key = ''
        for x in alpha:
            if x.islower():
                key = key+'*'+x.upper()
            else:
                key = key+x
        return key
        
    def convert_priv(self,alpha):
        key = ''
        cap = False
        for x in alpha:
            if x=='?' or x=='%':
                cap = False
            elif x=='*':
                cap = True
            elif cap == True:
                key = key + x.lower()
                cap = False
            else:
                key = key + x
        self.__private_key = key;
        return self.__private_key

    def main_window_menu(self):
           
        m = Menu(root)
    
        fileMenu = Menu(m, tearoff=0)
        fileMenu.add("command", label="New File", command = self.on_exit)
        fileMenu.add("command", label="Open...", command = self.on_exit)
        fileMenu.add("command", label="Save", command = self.on_exit)
        fileMenu.add("command", label="Save As...", command = self.on_exit)
        fileMenu.add("separator")
        fileMenu.add("command", label="Quit", command = self.on_exit)
 
        m.add("cascade", menu=fileMenu, label="File")
        
        readermenu = Menu(m, tearoff=0)
        readermenu.add("command", label="Connect to MSR605", command = self.connect_to_msr605)
        readermenu.add("command", label="Close connection to MSR605", command = self.close_connection)
        readermenu.add("command", label="Reset MSR605 Card Reader", command = self.reset)
        readermenu.add("separator")
        readermenu.add("command", label="Test Communication", command = self.communication_test)
        readermenu.add("command", label="Test Sensors", command = self.sensor_test)
        readermenu.add("command", label="Test RAM", command = self.ram_test)
        readermenu.add("separator")
        readermenu.add("radiobutton", label="High Coercivity", value="hi", variable=self.__coercivityRadioBtnValue, command = self.coercivity_change)
        readermenu.add("radiobutton", label="Low Coercivity", value="low", variable=self.__coercivityRadioBtnValue, command = self.coercivity_change)

        m.add("cascade", menu=readermenu, label="Card Reader")

        databaseMenu = Menu(m, tearoff=0)
        databaseMenu.add("checkbutton", label="Autosave Cards", onvalue=True, offvalue=False, variable=self.__autoSaveDatabase)
        databaseMenu.add("command", label="View Saved Cards", command = self.view_database)
        databaseMenu.add("separator")
        databaseMenu.add("checkbutton", label="Save Duplicate Cards", onvalue=True, offvalue=False, variable=self.__enableDuplicates)

        m.add("cascade", menu=databaseMenu, label="Database")
        
        root.configure(menu=m)
        
    def build_main_window(self):
           
        #Calls main Window Menu along with a .configure -> Shows the menu
        m = self.main_window_menu()
        
        tracks = Frame(root)     
        tracks.pack(side = LEFT)

        blockchainLabelFrame = Frame(tracks, padx = 10, pady = 0)     
        blockchainLabelFrame.grid(row = 0, column = 0)       
        Label(blockchainLabelFrame, text="Blockchain Magnetic Card Wallet Creation Tool", padx = 10, pady = 0, font=('system', 16)).pack(side = LEFT)    
        blockchainLabelFrame2 = Frame(tracks, padx = 10, pady = 0)     
        blockchainLabelFrame2.grid(row = 1, column = 0)  
        Label(blockchainLabelFrame2, text="Read and Write blockchain keys to magnetic stripe cards: V0.1", padx = 10, pady = 0, font=('system', 13)).pack(side = LEFT)    
        
        #Public Key
        pubKeyFrame = Frame(tracks, padx = 10, pady = 8)     
        pubKeyFrame.grid(row = 3, column = 0)       
        Label(pubKeyFrame, text="Public Key:", padx = 10, pady = 8).pack(side = LEFT)    
        self.__pubKeyEntry = Text(pubKeyFrame, bd = 1, width = 70, height = 3)
        self.__pubKeyEntry.pack(side = RIGHT)
        
        #Private Key
        privKeyFrame = Frame(tracks, padx = 10, pady = 8)     
        privKeyFrame.grid(row = 4, column = 0)       
        Label(privKeyFrame, text="Private Key:", padx = 10, pady = 8).pack(side = LEFT)    
        self.__privKeyEntry = Text(privKeyFrame, bd = 1, width = 70, height = 3)
        self.__privKeyEntry.pack(side = RIGHT)
        
        #Track One
        # trackOneFrame = Frame(tracks, padx = 10, pady = 8)     
        # trackOneFrame.grid(row = 2, column = 0)       
        # Label(trackOneFrame, text="Track 1:", padx = 10, pady = 8).pack(side = LEFT)    
        # self.__trackOneEntry = Text(trackOneFrame, bd = 1, width = 70, height = 3)
        # self.__trackOneEntry.pack(side = RIGHT)
        
        # #Track Two
        # trackTwoFrame = Frame(tracks, padx = 10, pady = 8)     
        # trackTwoFrame.grid(row = 3, column = 0)       
        # Label(trackTwoFrame, text="Track 2:", padx = 10, pady = 8).pack(side = LEFT)    
        # self.__trackTwoEntry = Text(trackTwoFrame, bd = 1, width = 70, height = 3)
        # self.__trackTwoEntry.pack(side = RIGHT)
        
        # #Track Three
        # trackThreeFrame = Frame(tracks, padx = 10, pady = 8)   
        # trackThreeFrame.grid(row = 4, column = 0)     
        # Label(trackThreeFrame, text="Track 3:", padx = 10, pady = 8).pack(side = LEFT)    
        # self.__trackThreeEntry = Text(trackThreeFrame, bd = 1, width = 70, height = 3)
        # self.__trackThreeEntry.pack(side = RIGHT)
        
        
        
        #Displays if you're connected to the MSR605
        self.__connectedLabelIndicator = Label(tracks, text = "MSR605 is not connected.", fg = 'black', padx = 0, pady = 10, font=('system', 13))
        self.__connectedLabelIndicator.grid(row = 5, column = 0) 
        
        # Button(tracks, text="Connect to MSR605", command = self.connect_to_msr605).grid(row = 4, column = 0)
        # Button(tracks, text="Close connection to MSR605", command = self.close_connection).grid(row = 5, column = 0)
        # Button(tracks, text="Reset MSR605", command = self.reset).grid(row = 6, column = 0)  
        
        
        buttons = Frame(root)     
        buttons.pack(side = RIGHT)
        
        
        #Coercivity Radio Buttons
        # coercivityRadioButtons = Frame(buttons, padx = 10, pady = 10)
        # coercivityRadioButtons.pack(side = TOP, padx = 20)
        # Label(coercivityRadioButtons, text="SET COERCIVITY", padx = 10, pady = 10, font=('Helvetica', 10, 'underline')).pack(side = TOP)    
        # Radiobutton(coercivityRadioButtons, text="HI-CO", variable=self.__coercivityRadioBtnValue, value="hi", command = self.coercivity_change).pack(side=TOP)
        # Radiobutton(coercivityRadioButtons, text="LOW-CO", variable=self.__coercivityRadioBtnValue, value="low", command = self.coercivity_change).pack(side=TOP)
        
        #Read-Write-Erase Buttons
        readWriteEraseButtons = Frame(buttons, padx = 0, pady = 0)
        readWriteEraseButtons.pack(side = TOP, padx = 10)
        Label(readWriteEraseButtons, text="Card Controls", padx = 10, pady = 10).pack(side = TOP)    
        Button(readWriteEraseButtons, text="READ", command = self.read_card).pack(side=TOP)
        Button(readWriteEraseButtons, text="WRITE", command = self.write_card).pack(side=TOP)
        Button(readWriteEraseButtons, text="ERASE", command = self.erase_card).pack(side=TOP)

        # ledButtons = Frame(buttons, padx = 10, pady = 10)
        # ledButtons.pack(side = TOP, padx = 20)
        # Label(ledButtons, text="LED OPTIONS", padx = 10, pady = 10, font=('Helvetica', 10, 'underline')).pack(side = TOP)    
        # Button(ledButtons, text="ALL ON", command = lambda: self.led_change("on")).pack(side=TOP)
        # Button(ledButtons, text="ALL OFF", command = lambda: self.led_change("off")).pack(side=TOP)
        # Button(ledButtons, text="GREEN ON", command = lambda: self.led_change("green")).pack(side=TOP)
        # Button(ledButtons, text="YELLOW ON", command = lambda: self.led_change("yellow")).pack(side=TOP)
        # Button(ledButtons, text="RED ON", command = lambda: self.led_change("red")).pack(side=TOP)
        
        # testButtons = Frame(buttons, padx = 10, pady = 10)
        # testButtons.pack(side = TOP, padx = 20)
        # Label(testButtons, text="MSR605 TESTS", padx = 10, pady = 10, font=('Helvetica', 10, 'underline')).pack(side = TOP)    
        # Button(testButtons, text="COMMUNICATION TEST", command = self.communication_test).pack(side=TOP)
        # Button(testButtons, text="SENSOR TEST", command = self.sensor_test).pack(side=TOP)
        # Button(testButtons, text="RAM TEST", command = self.ram_test).pack(side=TOP)

    
           
    def connect_to_msr605(self):        
        if (self.__connected == True or self.__msr != None):
            self.__connectedLabelIndicator.config(text = "Reconnecting to MSR605.", fg = 'black')
            self.close_connection()
        
        try:
            self.__msr = cardReader.CardReader(SERIAL_PORT)
        
        except cardReaderExceptions.MSR605ConnectError as e:
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "MSR605 Card Reader is Offline.", fg = 'black')
            showerror("Connect Error", e)
            print (e)
        
        except cardReaderExceptions.CommunicationTestError as e:
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "MSR605 Card Reader is Offline.", fg = 'black')
            showerror("Communication Error", e)            
            print (e)
        
        else:
            self.__connected = True
            self.__connectedLabelIndicator.config(text = "MSR605 Card Reader is Online.", fg = 'black')
    
    def close_connection(self):
        if (self.__connected == True or self.__msr != None):
            self.__msr.close_serial_connection()
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "MSR605 Card Reader is Offline.", fg = 'black')
            self.__msr = None
        
        else:
            self.__connectedLabelIndicator.config(text = "MSR605 Card Reader is Offline.", fg = 'black')
    
    def exception_error_reset(self, title, text):
        showerror(title, text)
        self.__connectedLabelIndicator.config(text = "Resetting the MSR605...", fg = 'black')
        self.reset()
        
        
    def coercivity_change(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is Offline.", fg = 'black')
            return None
        
        rdbSelection = self.__coercivityRadioBtnValue.get()        
        
        try:
            if (rdbSelection == 'hi'):            
                self.__msr.set_hi_co()
            elif (rdbSelection == 'low'):
                self.__msr.set_low_co()
                
        except cardReaderExceptions.SetCoercivityError as e :
            self.__connectedLabelIndicator.config(text = "Issue setting the Coercivity.", fg = 'red')
            print (e)            
        
        else:
            try:
                coercivity = self.__msr.get_hi_or_low_co()
            except cardReaderExceptions.GetCoercivityError as e :
                self.__connectedLabelIndicator.config(text = "Issue getting the Coercivity.", fg = 'red')
                print (e)
            
            
    def read_card(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is offline.", fg = 'black')
            return None

        self.__connectedLabelIndicator.config(text = "Please swipe card...", fg = 'black')

        try:
            self.__tracks = self.__msr.read_card()
        except cardReaderExceptions.CardReadError as e :
            self.__connectedLabelIndicator.config(text = "Card read error. Try again?", fg = 'red')
            print (e)
            
            self.__pubKeyEntry.delete(1.0, END)
            self.__privKeyEntry.delete(1.0, END)

            # self.__trackOneEntry.delete(1.0, END)
            # self.__trackTwoEntry.delete(1.0, END)
            # self.__trackThreeEntry.delete(1.0, END)
            
            self.__pubKeyEntry.insert(END, self.convert_pub(e.tracks[1],e.tracks[2]))
            self.__privKeyEntry.insert(END,  self.convert_priv(e.tracks[0]))

            # self.__trackOneEntry.insert(END, e.tracks[0])
            # self.__trackTwoEntry.insert(END, e.tracks[1])
            # self.__trackThreeEntry.insert(END, e.tracks[2])
            
            if (self.__autoSaveDatabase.get() == True):
                
                if (self.__enableDuplicates == False):
                    
                    cursor.execute("""SELECT * FROM Cards WHERE trackOne=? AND trackTwo=? AND trackThree=?""", (self.__tracks))
                
                    conn.commit()
                    result = cursor.fetchone()

                    # if (result != None):
                    #     showinfo("Duplicate", "This card already exists in the Database, please enable Duplicates in the Database dropdown to add it")
                    # else:
                    if (result == None):
                        cursor.execute("""INSERT INTO Cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks))                    
                        conn.commit()                
                else:                
                    cursor.execute("""INSERT INTO Cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks))                    
                    conn.commit()
            
            
            # else:
                # showinfo("Autosave to Database","Autosave is turned off in the Database menu dropdown, please \nselect it if you wish to store the cards that are read in")
            
            
            return None
    
        except cardReaderExceptions.StatusError as e :
            self.__connectedLabelIndicator.config(text = "Connection Error.", fg = 'red')
            print (e)
            return None
        
        else:

            self.__pubKeyEntry.delete(1.0, END)
            self.__privKeyEntry.delete(1.0, END)

            # self.__trackOneEntry.delete(1.0, END)
            # self.__trackTwoEntry.delete(1.0, END)
            # self.__trackThreeEntry.delete(1.0, END)
            
            self.__pubKeyEntry.insert(END, self.convert_pub(self.__tracks[1],self.__tracks[2]))
            self.__privKeyEntry.insert(END,  self.convert_priv(self.__tracks[0]))

            # self.__trackOneEntry.insert(END, self.__tracks[0])
            # self.__trackTwoEntry.insert(END, self.__tracks[1])
            # self.__trackThreeEntry.insert(END, self.__tracks[2])

            self.__connectedLabelIndicator.config(text = "Card read successfully.", fg = 'black')

            if (self.__autoSaveDatabase.get() == True):
                
                if (self.__enableDuplicates.get() == False):
                    
                    cursor.execute("""SELECT * FROM Cards WHERE trackOne=? AND trackTwo=? AND trackThree=?""", (self.__tracks))
                
                    conn.commit()
                    result = cursor.fetchone()
                    
                    # if (result != None):
                        # showinfo("Duplicate", "This card already exists in the Database, please enable Duplicates in the Database dropdown to add it")
                    #else:
                    if (result == None):
                        cursor.execute("""INSERT INTO Cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks))                    
                        conn.commit()                
                else:                
                    cursor.execute("""INSERT INTO Cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks))                    
                    conn.commit()
            # else:
                # showinfo("Autosave to Database","Autosave is turned off in the Database menu dropdown, please \nselect it if you wish to store the cards that are read in")
            
                
    def write_card(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is not connected.", fg = 'black')
            return None
        
        # tracks = [self.__trackOneEntry.get(1.0, END)[:-1], self.__trackTwoEntry.get(1.0, END)[:-1], self.__trackThreeEntry.get(1.0, END)[:-1]]
        # public = self.encode_public(self.__pubKeyEntry.get(1.0, END)[:-1])
        private = self.encode_private(self.__privKeyEntry.get(1.0, END)[:-1])

        tracks = [ private, public[0], public[1]  ]

        self.__connectedLabelIndicator.config(text = "Please swipe card...", fg = 'black')
        
        try:        
            self.__tracks = self.__msr.write_card(tracks, False)
        
        except cardReaderExceptions.CardWriteError as  e :
            self.exception_error_reset("Write Error", e)
            print(e)
            return None
        
        except cardReaderExceptions.StatusError as e :
            self.exception_error_reset("Write Error", e)
            print(e)
            return None
        
        else:

            self.__connectedLabelIndicator.config(text = "Written to card successfully.", fg = 'green')
        
    def erase_card(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is not connected.", fg = 'red')
            return None
        self.__connectedLabelIndicator.config(text = "Swipe card...", fg = 'black')
        
        #
        #
        #CHECK THIS************
        #
        #
        try:
            self.__msr.erase_card(7) #all tracks are erased
        
        except cardReaderExceptions.EraseCardError as e :
            self.exception_error_reset("Erase Error", e)
            print (e)
            return None
        
        else:
            self.__connectedLabelIndicator.config(text = "Successfully erased card.", fg = 'black')
            
            
    def led_change(self, whichLeds):
        if (self.__connected == False or self.__msr == None):
            return None
        if (whichLeds == "on"):
            self.__msr.led_on()
            return None
        elif (whichLeds == "off"):
            self.__msr.led_off()
            return None
        elif (whichLeds == "green"):
            self.__msr.green_led_on()
            return None
        elif (whichLeds == "yellow"):
            self.__msr.yellow_led_on()
            return None
        elif (whichLeds == "red"):
            self.__msr.red_led_on()
            return None
            
    def reset(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is not connected.", fg = 'black')
            return None
        
        self.__msr.reset()
        self.__connectedLabelIndicator.config(text = "The MSR605 has been reset.", fg = 'black')
    
    def communication_test(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is not connected.", fg = 'black')
            return None
        
        try:
            self.__msr.communication_test()
        
        except cardReaderExceptions.CommunicationTestError as e :
            self.exception_error_reset("Communication Test Error", e)
            print (e)
            return None
        
        else:
            self.__connectedLabelIndicator.config(text = "Communications Test Passed.", fg = 'green')
        
    def ram_test(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is not connected.", fg = 'black')
            return None
        
        try:
            self.__msr.ram_test()
        
        except cardReaderExceptions.RamTestError as e :
            self.exception_error_reset("Ram Test Error", e)
            print (e)
            return None
        
        else:
            self.__connectedLabelIndicator.config(text = "RAM Check Passed.", fg = 'green')
            
    def sensor_test(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The MSR605 is not connected.", fg = 'black')
            return None
        
            self.__connectedLabelIndicator.config(text = "Please swipe a card...", fg = 'black')
        
        try:
            self.__msr.sensor_test()
        
        except cardReaderExceptions.SensorTestError as e :
            self.exception_error_reset("Sensor Test Error", e)
            self.__connectedLabelIndicator.config(text = "Sensor Check Error.", fg = 'red')
            print (e)
            return None
        
        else:
            self.__connectedLabelIndicator.config(text = "Sensor Check Passed.", fg = 'green')
    

    def view_database(self):
        dbView = tk.Toplevel(self)
        dbView.title("Historical Logs")
        dbView.minsize(500,200)
        
        dbTree = ttk.Treeview(dbView)
        dbTree.pack(side = TOP)
        
        dbTree['columns'] = ('Public')
        
        dbTree.column('Public', width=500)
        dbTree.heading('Public', text='Public Key')
        
        # dbTree.column('Private', width=100)
        # dbTree.heading('Private', text='Private')
        
        # dbTree.column('Track 1', width=100)
        # dbTree.heading('Track 1', text='Track 1')
        
        # dbTree.column('Track 2', width=100)
        # dbTree.heading('Track 2', text='Track 2')
        
        # dbTree.column('Track 3', width=100)
        # dbTree.heading('Track 3', text='Track 2')
        
        cursor.execute("""SELECT * FROM Cards""")
        conn.commit()
        tracks = cursor.fetchall()
        
        i=1
        for track in tracks:            
            # dbTree.insert("" , END,    text=i, values=(self.convert_pub(track[1],track[2]), self.convert_priv(track[0]), track[0], track[1], track[2]))
            dbTree.insert("" , END,    text=i, values=(self.convert_pub(track[1],track[2])))
            i += 1


    def on_exit(self):        
        conn.close()
        
        if (self.__connected == True or self.__msr != None):
            self.close_connection()
        
        root.destroy()
        
        
root = tk.Tk()
root.title("Blockchain Cards")
root.minsize(790,240)
gui = GUI(root)


conn = sqlite3.connect("cardDatabase.db") 
 
cursor = conn.cursor()
gui.connect_to_msr605();
 
# create a table
cursor.execute("""CREATE TABLE if not exists Cards
                  (trackOne text, trackTwo text, trackThree text) 
               """)
conn.commit()

root.pack_propagate(0) # don't shrink

root.protocol("WM_DELETE_WINDOW", lambda: gui.on_exit())
root.mainloop() 


# Launch the status message after 1 millisecond (when the window is loaded)
#root.after(1, update_status)