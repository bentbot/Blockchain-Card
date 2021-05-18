Blockchain Magnetic Card Wallet Creation Tool
  ------------------

_Edited: 18  May, 2021_

  Project Description
  -------------------
  Encode an entire public & private keyset to a magnetic card.
  A simple way to store a blockchain wallet data in magnetic cards (like the ones in your real wallet). This is an application that encodes your BitCoin (or orther crypto-coin) public and private keys onto a magnetic card for safe keeping or for use by vendors. You can use this application with an MSR605 card reader to read and write blockchain encoded cards. Legal Documentation: ./LICENSE

  Requirements
  ------------------
  A MSR605 magnetic card reader / writer (or an equivilent device with a complete python library).
  One or more standard 3-Stripe magnetic cards.
  Python 3+
  
  Authors
  ------------------
  - Liam Hogan - bentbot@outlook.com
  - Damien Bobillot - damien.bobillot.2002+msr@m4x.org
  - Manwinder Sidhu - manwindersapps@gmail.com

  Installation & Run
  ------------------
  - Platform: Windows / Mac
  - Python: 3.5.2

      # Clone
      git clone https://github.com/bentbot/Blockchain-Card.git
      cd Blockchain-Card

      # Start the GUI
      python ./GUI.py

      # Install serial if needed
      pip install serial
 
      # Update the serial port line in ./GUI.py:12
      SERIAL_PORT = '/dev/cu.usbserial-142430'

![Blockchain Card screenshot | May 18, 2021](https://github.com/bentbot/Blockchain-Card/blob/master/screenshot.png?raw=true)

  Hardware Description
  --------------------
  The MSR605 is a card reader/writer, it writes to the standard magstripe cards
  that most people are used to using (Credit Cards, Debit Cards, pretty much any
  card with a colored stripe on the back). I purchased mine on ebay. I choose to 
  buy this card reader because it had good documentation and drivers online.
  
  In this project I use the magcard to store address data in raw encoded form. 
  Magcards can only accept a specific number of bytes on each stripe. Each stripe 
  is different. Some stripes only accept numerals while others accept all alphanumeric characters.
  This application converts the two provided keys into data formatted to fit on a magcard. 
  
  REMEMBER: In no way is this method secure. Anyone that scans your magcard can read your private key.

  File Description
  ----------------
  GUI.py - the graphical interface that allows you to control the MSR605
  msr.py - the library that connects to the card reader (mine is MSR605)  

  Using Alternative Card Readers
  ---------------
  Replace the connection line, "msr.msr(SERIAL_PORT)" in GUI.py line ~197, with your new library. 
  Update each function to with equivalent function in your new library. Important references:
  - read_tracks 	GUI.py:263
  - write_tracks 	GUI.py:313,334
