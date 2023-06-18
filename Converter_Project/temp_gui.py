"""
Kimberly Stochaj
IE 4515
seperate file for developing the GUI
15 June 2023
temp_gui.py
"""

import PySimpleGUI as psg


def main():
    l1 = psg.Text("The treatment you selected is not binary - is there a value that you would like to use to split the treatment and control groups?")
    l2 = psg.Text("please input your answer as only a number e.g. 21.45")
    t3 = psg.Input(key = "split_val")
    b4 = psg.Button("OK")
    
    layout = [[l1], [l2], [t3], [b4]]
    window = psg.Window("USER SELECTION", layout)
    
    while True:
        event, values = window.read()
        if event in (psg.WINDOW_CLOSED, "OK"):
            break
        
    
    window.close()
    print(values["split_val"].isnumeric())
    
main()
