Blockchain Magnetic Card Wallet Creation Tool
  ------------------

_Edited: 11  April, 2021_

Authors:
- Liam Hogan - bentbot@outlook.com
- Manwinder Sidhu - manwindersapps@gmail.com

Contact: bentbot@outlook.com
Platform: Windows / Mac
Python: 3.5.2 (I originally wrote this in 2.7 but I think I had issues with Tkinter)
Legal Documentation: LICENSE (file) and also in some of the classes


  Libraries Required
  ------------------
  PySerial for communication between the PC and MSR605 (https://github.com/pyserial/pyserial)
  
  Tkinter for the GUI
  


  Hardware Description
  --------------------
  The MSR605 is a card reader/writer, its writes to the standard magstripe cards
  that most people are used to using (Credit Cards, Debit Cards, pretty much any
  card with a colored stripe on the back, its usually black). I purchased mine
  on ebay. I choose to buy this card reader because it had good documentation
  online



  Project Description
  -------------------
  A simple way to store a block-chain wallet in your actual wallet. Simply put, this application encodes your BitCoin (or alternative crypto's) public and private keys on to magnetic cards for safe storage or alternative uses. Use this to keep a physical copy of your BitCoin wallet backup with you. If you wanted to, you could make additional hardware for accessing or spending the funds by integrating with blockchain-core.

  

  File Description
  ----------------
  GUI.py - the graphical interface that allows you to control the MSR605
  
  MSR605Test.py - this tests the devices different functions, it's pretty much tests all the functions that
                  the device can perform

  cardReader.py - the interface between python and the MSR605, this class sends the command over serial and
                  returns any info requested
                  
  isoStandardDictionary.py - contains 2 dictionaries (track 2 and 3 have the same standard for what characters
                             are allowed) and a function that tells you if a character is valid for a given track
                             
                             
  cardReaderExceptions.py - The MSR605 provides feed back in the case errors arise, this information can be useful
                            and this class contains exceptions for each of the functions the MSR605 can preform




  Bugs
  ----
  April 11, 2021
  Writing cards does not currently work.
  
  
