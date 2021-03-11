#!/usr/bin/python3

import requests
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename

url = 'http://10.41.50.65'

def main():
    global status

    window = tk.Tk()
    
    frame1 = tk.Frame(master=window, width=400, height=400)
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    greeting = tk.Label(master=frame1,text="Do something?")
    ulButton = tk.Button(master=frame1,text="Print file",command=print_file)
    pauseButton = tk.Button(master=frame1,text="Pause Print",command=pause_print)
    resumeButton = tk.Button(master=frame1,text="Resume Print",command=resume_print)
    cancelButton = tk.Button(master=frame1,text="Cancel Print",command=cancel_print)

    status = tk.Label(master=frame1,text="Status",wraplength=350)

    greeting.pack()
    ulButton.pack()
    pauseButton.pack()
    resumeButton.pack()
    cancelButton.pack()
    status.pack()
    window.resizable(width=False, height=False)
    window.geometry('400x400')
    window.mainloop()


def print_file():
    filename = askopenfilename(initialdir='/z/3d',filetypes=[("G-Code","*.gcode")]) # show an "Open" dialog box and return the path to the selected file
    print(filename)
    fp,fn = os.path.split(filename)

    files = {'print_file': (fn,open(filename, 'rb'))}

    r = requests.post(url + '/print_file_uploads', files=files)

    status["text"] = r.text
    if(eval(r.text)["error_code"] == 200):
        data = {'PRINT':fn}
        r2 = requests.post(url + '/command', data=data)
        if(eval(r2.text)["error_code"] == 200):
            status["text"] = "Printing file " + fn + " success!"
        else:
            status["text"] = "error: " + r2.text
        
    else:
        status["text"] = "error: " + r.text
        exit()


def pause_print():
    data = {'PAUSE':''}
    r = requests.post(url + '/command', data=data)
    if(eval(r.text)["error_code"] == 200):
            status["text"] = "Pause success!"
    else:
        status["text"] = "error: " + r.text

def resume_print():
    data = {'RESUME':''}
    r = requests.post(url + '/command', data=data)
    if(eval(r.text)["error_code"] == 200):
            status["text"] = "Resume success!"
    else:
        status["text"] = "error: " + r.text

def cancel_print():
    data = {'CANCEL':''}
    r = requests.post(url + '/command', data=data)
    if(eval(r.text)["error_code"] == 200):
            status["text"] = "Cancelling print success!"
    else:
        status["text"] = "error: " + r.text


if __name__ == '__main__': main()