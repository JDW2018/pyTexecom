# pytexecom

This project is an attempt to create a python libary for communicating with Texecom Premier Elite Alarms Panels. The plugin is designed to be connected to COM port 2 on the panel with the following configuration

Mode: Crestron 
Speed: 19200
Data Bits: 8 
Stop Bits: 1
Parity: None

The alarm panel communicates with the libary on every state change. The libary implements a callback for devices so they can be notifed of changes.  
