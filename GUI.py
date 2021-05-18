#!/usr/bin/env python3

import tkinter as tk
import sys, time, msr
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
import sqlite3

# CHANGE TO YOUR OWN MSR605 CARD READER SERIAL INTERFACE
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

    def encode_public(self,alpha):
        gamma='';
        for a in alpha:
            beta = int(ord(a))
            if ( beta < 100 ) :
                beta = '0'+str(beta);
            gamma=gamma+''+str(beta);
        delta=''; epsilon=''; i=0;
        for g in gamma:
            if i < 70:
                delta=delta+g
            else:
                epsilon=epsilon+g
            i=i+1
        return [delta,epsilon]

    def convert_pub(self,alpha,beta):
        gamma = alpha+beta
        delta = ""
        epsilon = "".join(char for char in gamma if char.isdigit())
        epsilon = " ".join([epsilon[i:i+3] for i in range(0, len(epsilon), 3)])
        for octal_char in epsilon.split(" "):
            delta+=chr(int(octal_char))
        return delta

    def encode_private(self,alpha):
        beta = ''
        for a in alpha:
            if a.islower():
                beta = beta+'*'+a.upper()
            elif a!='*' and a!='%':
                beta = beta+a
        return beta
        
    def convert_priv(self,alpha):
        beta = ''
        theta = False
        for a in alpha:
            if a=='?' or a=='%':
                theta = False
            elif a=='*':
                theta = True
            elif theta == True:
                beta = beta + a.lower()
                theta = False
            else:
                beta = beta + a
        return beta

    def main_window_menu(self):
           
        m = Menu(root)
    
        fileMenu = Menu(m, tearoff=0)
        fileMenu.add("command", label="Read from Card", command = self.read_card)
        fileMenu.add("command", label="Write to Card", command = self.write_card)
        fileMenu.add("command", label="Erase Card", command = self.erase_card)
        # fileMenu.add("command", label="Save As...", command = self.on_exit)
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

        m.add("cascade", menu=readermenu, label="Device")

        databaseMenu = Menu(m, tearoff=0)
        databaseMenu.add("command", label="View Database", command = self.view_database)
        readermenu.add("separator")
        databaseMenu.add("checkbutton", label="Save Cards to Database", onvalue=True, offvalue=False, variable=self.__autoSaveDatabase)
        databaseMenu.add("checkbutton", label="Save Duplicate Cards", onvalue=True, offvalue=False, variable=self.__enableDuplicates)

        m.add("cascade", menu=databaseMenu, label="Database")
        
        root.configure(menu=m)
        
    def build_main_window(self):

        #Calls main Window Menu along with a .configure -> Shows the menu
        m = self.main_window_menu()

        titles = Frame(root)
        titles.pack(fill=BOTH, side=TOP, expand=YES)

        blockchainLabelFrame = Frame(titles, padx = 0, pady = 10)     
        blockchainLabelFrame.grid(row = 0, column = 0)       
        Label(blockchainLabelFrame, text="Blockchain Card Encoder", padx = 220, pady = 0, font=('system', 15)).pack(side = TOP, expand = YES)
        blockchainLabelFrame2 = Frame(titles, padx = 0, pady = 0)
        blockchainLabelFrame2.grid(row = 1, column = 0)  
        Label(blockchainLabelFrame2, text="Scan your card or enter a blockchain address to encode.", padx = 220, pady = 0, font=('system', 13)).pack(side = TOP, expand = YES)

        tracks = Frame(root)     
        tracks.pack(fill=BOTH, side = LEFT, expand=YES)

        #Public Key
        pubKeyFrame = Frame(tracks, padx = 10, pady = 8)     
        pubKeyFrame.grid(row = 3, column = 0)       
        Label(pubKeyFrame, text="Public Key: ", padx = 10, pady = 6).pack(side = LEFT)    
        self.__pubKeyEntry = Text(pubKeyFrame, bd = 1, highlightbackground="gray", highlightcolor="gray", highlightthickness=1, width = 70, height = 3)
        self.__pubKeyEntry.pack(side = RIGHT)

        #Private Key
        privKeyFrame = Frame(tracks, padx = 10, pady = 8)     
        privKeyFrame.grid(row = 4, column = 0)       
        Label(privKeyFrame, text="Private Key:", padx = 10, pady = 8).pack(side = LEFT)    
        self.__privKeyEntry = Text(privKeyFrame, bd = 1, highlightbackground="gray", highlightcolor="gray", highlightthickness=1, width = 70, height = 3)
        self.__privKeyEntry.pack(side = RIGHT)

        #Displays if you're connected to the MSR605
        self.__connectedLabelIndicator = Label(tracks, text = "Card reader is not connected.", fg = 'red', padx = 0, pady = 10, font=('system', 13))
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
        Label(readWriteEraseButtons,  text="Wallet Actions", padx = 10, pady = 0).pack(side = TOP)    
        Button(readWriteEraseButtons, text="Read Card", width = 20, command = self.read_card).pack(side=TOP)
        Button(readWriteEraseButtons, text="Write Card", width = 20, command = self.write_card).pack(side=TOP)
        Button(readWriteEraseButtons, text="Erase Card", width = 20, command = self.erase_card).pack(side=TOP)

           
    def connect_to_msr605(self):        
        if (self.__connected == True or self.__msr != None):
            self.__connectedLabelIndicator.config(text = "Reconnecting to MSR605.", fg = 'black')
            self.close_connection()
        
        try:
            self.__msr = msr.msr(SERIAL_PORT)
        
        except any as e:
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "Card reader is offline.", fg = 'black')
            showerror("Connect Error", e)
            print (e)
        
        except any as e:
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "Card reader is offline.", fg = 'black')
            showerror("Communication Error", e)            
            print (e)
        
        else:
            self.__connected = True
            self.__connectedLabelIndicator.config(text = "Card reader is online.", fg = 'black')
    
    def close_connection(self):
        if (self.__connected == True or self.__msr != None):
            # self.__msr.close_serial_connection()
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "Card reader is offline.", fg = 'black')
            self.__msr = None
        
        else:
            self.__connectedLabelIndicator.config(text = "Card reader is offline.", fg = 'black')
    
    def exception_error_reset(self, title, text):
        showerror(title, text)
        self.__connectedLabelIndicator.config(text = "Resetting the card reader.", fg = 'black')
        self.reset()
        
        
    def coercivity_change(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is offline.", fg = 'black')
            return None
        
        rdbSelection = self.__coercivityRadioBtnValue.get()        
        
        try:
            if (rdbSelection == 'hi'):            
                self.__msr.set_coercivity(True)
            elif (rdbSelection == 'low'):
                self.__msr.set_coercivity(False)
                
        except Exception as e:
            self.__connectedLabelIndicator.config(text = "Issue setting the coercivity.", fg = 'red')
            print (e)            
        
        else:
            try:
                coercivity = self.__msr.get_coercivity()
            except Exception as e:
                self.__connectedLabelIndicator.config(text = "Issue getting the coercivity.", fg = 'red')
                print (e)
            
            
    def read_card(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is offline.", fg = 'black')
            return None
        self.__connectedLabelIndicator.config(text = "Swipe your card now...", fg = 'black')
        self.refresh()
        try:
            self.__tracks = self.__msr.read_tracks()
            # print(self.__tracks)
            if (self.__tracks == "1"):
                self.__connectedLabelIndicator.config(text = "Card was read successfully as a blank.", fg = 'black')
                self.refresh()
                return None;
            if (self.__tracks == "0"):
                self.__connectedLabelIndicator.config(text = "Card read error. Please try again.", fg = 'red')
                self.refresh()
                return None;
            if(self.__tracks[0] and self.__tracks[0]!='%0?'):
                privateKey=self.convert_priv(self.__tracks[0])
                self.__privKeyEntry.delete(1.0, END)
                self.__privKeyEntry.insert(END,privateKey)
            if(self.__tracks[1] and self.__tracks[2]):
                publicKey=self.convert_pub(self.__tracks[2],self.__tracks[1])
                self.__pubKeyEntry.delete(1.0, END)
                self.__pubKeyEntry.insert(END,publicKey)
            if(self.__tracks[0]=='%0?'):
                self.__connectedLabelIndicator.config(text = "Card successfully identified as a blank.", fg = 'darkgreen')
            else:
                self.__connectedLabelIndicator.config(text = "Card read successfully.", fg = 'darkgreen')
            self.refresh()
            if (self.__autoSaveDatabase.get() == True):
                if (self.__enableDuplicates.get() == False):
                    cursor.execute("""SELECT * FROM Cards WHERE publicKey=?""", (publicKey))
                    conn.commit()
                    result = cursor.fetchone()
                    if (result == None):
                        cursor.execute("""INSERT INTO Cards(publicKey) VALUES(?)""", (publicKey))                    
                        conn.commit()                
                else:                
                    cursor.execute("""INSERT INTO Cards(publicKey) VALUES(?)""", (publicKey))                    
                    conn.commit()
        except Exception as e:
            self.__connectedLabelIndicator.config(text = "Card reader timed out.", fg = 'black')
            self.__msr.reset()
            self.refresh()
            print(e)
                
    def write_card(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is not connected.", fg = 'red')
            return None
        # tracks = [self.__trackOneEntry.get(1.0, END)[:-1], self.__trackTwoEntry.get(1.0, END)[:-1], self.__trackThreeEntry.get(1.0, END)[:-1]]
        public = self.encode_public(self.__pubKeyEntry.get(1.0, END)[:-1])
        private = self.encode_private(self.__privKeyEntry.get(1.0, END)[:-1])
        self.__connectedLabelIndicator.config(text = "WARNING: Data on the card will be lost! Swipe card to write...", fg = 'red')
        self.refresh()
        try:
            self.__tracks = self.__msr.write_tracks(private.encode(), public[1].encode(), public[0].encode())
            self.__connectedLabelIndicator.config(text = "Card was successfully created.", fg = 'darkgreen')
            self.refresh()
        except Exception as e:
            self.__connectedLabelIndicator.config(text = "Card reader timed out.", fg = 'black')
            self.__msr.reset()
            self.refresh()
            print(e)


    def erase_card(self):
        self.__privKeyEntry.delete(1.0, END)
        self.__pubKeyEntry.delete(1.0, END)
        self.publicKey=False; self.privateKey=False;
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is not connected.", fg = 'red')
            return None
        self.__connectedLabelIndicator.config(text = "WARNING: Data on the card will be lost! Swipe card to erase...", fg = 'red')
        self.refresh()
        try:
            numb = '0';
            self.__tracks = self.__msr.write_tracks(numb.encode(), numb.encode(), numb.encode())
        except Exception as e:
            self.__connectedLabelIndicator.config(text = "Error erasing card.", fg = 'black')
            self.__msr.reset()
            self.refresh()
            print(e)
        else:
            self.__connectedLabelIndicator.config(text = "Card successfully erased.", fg = 'darkgreen')
            self.refresh()
            
    def reset(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is not connected.", fg = 'red')
            return None
        self.__msr.reset()
        self.__connectedLabelIndicator.config(text = "The card reader has been reset.", fg = 'black')
    
    def communication_test(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is not connected.", fg = 'red')
            return None
        try:
            self.__msr.communication_test()
        except Exception as e:
            self.exception_error_reset("Communication Test Error", e)
            print (e)
            return None
        else:
            self.__connectedLabelIndicator.config(text = "Communications test passed.", fg = 'darkgreen')
        
    def ram_test(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is not connected.", fg = 'red')
            return None
        
        try:
            self.__msr.ram_test()
        
        except Exception as e:
            self.exception_error_reset("Ram Test Error", e)
            print (e)
            return None
        
        else:
            self.__connectedLabelIndicator.config(text = "RAM check passed.", fg = 'darkgreen')
            
    def sensor_test(self):
        if (self.__connected == False or self.__msr == None):
            self.__connectedLabelIndicator.config(text = "The card reader is not connected.", fg = 'red')
            return None
        
            self.__connectedLabelIndicator.config(text = "Please swipe a card...", fg = 'black')
        
        try:
            self.__msr.sensor_test()
        
        except Exception as e:
            self.exception_error_reset("Sensor Test Error", e)
            self.__connectedLabelIndicator.config(text = "Sensor check error.", fg = 'red')
            print (e)
            return None
        
        else:
            self.__connectedLabelIndicator.config(text = "Sensor check passed.", fg = 'darkgreen')
    

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

    def refresh(self):
        root.update()
        root.after(1000,self.refresh)

root = tk.Tk()
root.title("Blockchain Card Encoder")
root.minsize(790,240)
root.resizable(0,0)
gui = GUI(root)

conn = sqlite3.connect("cardDatabase.db") 
 
cursor = conn.cursor()
gui.connect_to_msr605();
 
# create a table
cursor.execute("""CREATE TABLE if not exists Cards
                  (name text, publicKey text) 
               """)
conn.commit()

root.pack_propagate(0) # don't shrink

root.protocol("WM_DELETE_WINDOW", lambda: gui.on_exit())
root.mainloop() 


# Launch the status message after 1 millisecond (when the window is loaded)
# root.after(1, update_status)


