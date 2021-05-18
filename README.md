Blockchain Magnetic Card Wallet Creation Tool
  ------------------

_Edited: 18  May, 2021_

![Blockchain Card screenshot | May 18, 2021](https://github.com/bentbot/Blockchain-Card/blob/master/screenshot.png?raw=true)

Authors:
- Liam Hogan - bentbot@outlook.com
- Manwinder Sidhu - manwindersapps@gmail.com

Platform: Windows / Mac
Python: 3.5.2 (I originally wrote this in 2.7 but I think I had issues with Tkinter)
Legal Documentation: LICENSE (file) and also in some of the classes

  Project Description
  -------------------
  A simple way to store a blockchain wallet data in magnetic cards (like the ones in your real wallet). This is an application that encodes your BitCoin (or orther crypto-coin) public and private keys onto a magnetic card for safe keeping or for use by vendors. You can use this application with an MSR605 card reader to read and write blockchain encoded cards.

  Requirements
  ------------------
  A MSR605 magnetic card reader / writer (or an equivilent device with a complete python library).
  One or more standard 3-Stripe magnetic cards.
  Python 3+
  
  Libraries Required
  ------------------
  MSR Library [Damien Bobillot - damien.bobillot.2002+msr@m4x.org]
  Tkinter for the GUI [Manwinder Sidhu - manwindersapps@gmail.com]

  Installation & Run
  ------------------
      # Start the GUI
      python ./GUI.py

      # Install serial if needed
      pip install serial
 
      # Update the serial port line in ./GUI.py:12
      SERIAL_PORT = '/dev/cu.usbserial-142430'

  Hardware Description
  --------------------
  The MSR605 is a card reader/writer, its writes to the standard magstripe cards
  that most people are used to using (Credit Cards, Debit Cards, pretty much any
  card with a colored stripe on the back, its usually black). I purchased mine
  on ebay. I choose to buy this card reader because it had good documentation
  online

  File Description
  ----------------
  GUI.py - the graphical interface that allows you to control the MSR605
  msr.py - the library that connects to the card reader (MSR605)  

  Alternative Card Readers
  ---------------
  Replace the connection line, "msr.msr(SERIAL_PORT)" in GUI.py line ~197, with your new library. 
  Update each function to with equivalent function in your new library. Important references:
  - read_tracks 	GUI.py:263
  - write_tracks 	GUI.py:313,334
