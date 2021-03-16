#!/usr/bin/python3

import requests
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
from math import floor
from PIL import ImageTk, Image
import cv2

url = 'http://10.41.50.65'
timeout = 0.5

def main():
    global cameraEnabled,cap
    global status
    global printer_status, window, lbVideo, cameraButton

    cameraEnabled = False
    cap = 0
    

    window = tk.Tk(className="3D45 Control Tool")
    
    frame1 = tk.Frame(master=window)
    frame1.place(x=5,y=5,width=500,height=580)

    frame2 = tk.Frame(master=window)
    frame2.place(x=510,y=5,width=640,height=480)

    greeting = tk.Label(master=frame1,text="Do something?")
    ulButton = tk.Button(master=frame1,text="Print file",command=print_file)
    pauseButton = tk.Button(master=frame1,text="Pause Print",command=pause_print)
    resumeButton = tk.Button(master=frame1,text="Resume Print",command=resume_print)
    cancelButton = tk.Button(master=frame1,text="Cancel Print",command=cancel_print)
    cameraButton = tk.Button(master=frame1,text="Show Camera",command=switch_camera)
    lbVideo      = tk.Label(master=frame2)

    status = tk.Label(master=frame1,text="Status",wraplength=380,anchor="e", justify='left',font='TkFixedFont')
    printer_status = tk.Label(master=frame1,text="printer_status",wraplength=380,anchor="e", justify='left',font='TkFixedFont')

    greeting.pack()
    ulButton.pack()
    pauseButton.pack()
    resumeButton.pack()
    cancelButton.pack()
    status.pack()
    printer_status.pack()
    cameraButton.pack()
    lbVideo.pack()

    window.resizable(width=False, height=False)
    window.geometry('1200x600')

    window.after(1, get_status)   # the delay is in milliseconds
    video_stream()
    window.mainloop()





# function for video streaming
def video_stream():
    if cameraEnabled:
        try:
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lbVideo.imgtk = imgtk
            lbVideo.configure(image=imgtk)
            lbVideo.after(10, video_stream) 
        except:
            lbVideo["text"] = "couldn't get video"
            switch_camera()
    


def switch_camera():
    global cameraEnabled, cap
    if cameraEnabled: # disable
        cameraEnabled = False
        cameraButton["text"] = "Enable Camera"
        lbVideo.pack_forget()
    else: # enable camera now
        cap = cv2.VideoCapture(url + ':10123/?action=stream')
        if not cap.isOpened():
            status["text"] = "Couldn't enable camera"
            return
        cameraEnabled = True
        cameraButton["text"] = "Disable Camera"
        lbVideo.pack()
        lbVideo.after(10, video_stream) 

def print_file():
    filename = askopenfilename(initialdir='/z/3d',filetypes=[("G-Code","*.gcode")]) # show an "Open" dialog box and return the path to the selected file
    print(filename)
    fp,fn = os.path.split(filename)

    files = {'print_file': (fn,open(filename, 'rb'))}

    status["text"] = "Sending file to printer..."
    try:
        r = requests.post(url + '/print_file_uploads', files=files,timeout=20.00)
    except:
        status["text"] = "PRINT_FILE: timeout"
        return

    if(eval(r.text)["error_code"] == 200):
        data = {'PRINT':fn}
        r2 = requests.post(url + '/command', data=data,timeout=timeout)
        if(eval(r2.text)["error_code"] == 200):
            status["text"] = "Printing file " + fn + " success!"
        else:
            status["text"] = "error: " + r2.text
        
    else:
        status["text"] = "error: " + r.text
        exit()


def pause_print():
    data = {'PAUSE':''}
    try:
        r = requests.post(url + '/command', data=data,timeout=timeout)
    except:
        status["text"] = "PAUSE: timeout"
        return

    if(eval(r.text)["error_code"] == 200):
            status["text"] = "Pause success!"
    else:
        status["text"] = "error: " + r.text

def resume_print():
    data = {'RESUME':''}
    try:
        r = requests.post(url + '/command', data=data,timeout=timeout)
    except:
        status["text"] = ",RESUME: timeout"
        return

    if(eval(r.text)["error_code"] == 200):
            status["text"] = "Resume success!"
    else:
        status["text"] = "error: " + r.text

def cancel_print():

    MsgBox = tk.messagebox.askquestion ('Cancel current print','Are you sure you want to cancel the current print?',icon = 'warning')
    if MsgBox != 'yes':
       return
    
    data = {'CANCEL':''}
    
    try:
        r = requests.post(url + '/command', data=data,timeout=timeout)
    except:
        status["text"] = "CANCEL: timeout"
        return

    if(eval(r.text)["error_code"] == 200):
            status["text"] = "Cancelling print success!"
    else:
        status["text"] = "error: " + r.text

def get_status():
    data = {'GETPRINTERSTATUS':''}
    try:
        r = requests.post(url + '/command', data=data,timeout=timeout)
    except:
        printer_status["text"] = "GETPRINTERSTATUS: timeout"
        window.after(1000, get_status)   # the delay is in milliseconds
        cameraButton["state"] = "disabled"
        return
    if(eval(r.text)["error_code"] == 200):
        my_dict = eval(r.text)
        if my_dict["door_open"] == 0:
            door = "No"
        else:
            door = "Yes"

        hr = floor(my_dict["elaspedtime"]/3600)
        mn = floor(my_dict["elaspedtime"]/60) - hr*60
        sc = my_dict["elaspedtime"] - hr*3600 - mn*60
        r_hr = floor(my_dict["remaining"]/3600)
        r_mn = floor(my_dict["remaining"]/60) - r_hr*60
        r_sc = my_dict["remaining"] - r_hr*3600 - r_mn*60
            

        my_text = ""
        my_text = "%s--------------------------------\n" % my_text
        my_text = "%sJob name:  %s\n" % (my_text,my_dict["jobname"])
        my_text = "%sJob status:            %s\n" % (my_text,my_dict["jobstatus"])
        my_text = "%sDoor open:             %s\n" % (my_text,door)
        my_text = "%sFilament Type:         %s\n" % (my_text,my_dict["filament_type "])
        my_text = "%s\n" % (my_text)
        my_text = "%sNozzle temp:           %3d°/%3d°\n" % (my_text,my_dict["temperature"],my_dict["extruder_target_temperature"])
        my_text = "%sBuildplate temp:       %3d°/%3d°\n" % (my_text,my_dict["platform_temperature"],my_dict["buildPlate_target_temperature"])
        my_text = "%sChamber temp:          %3d°\n" % (my_text,my_dict["chamber_temperature"])
        my_text = "%s\n" % (my_text)
        my_text = "%sElapsed time:          %2d:%02d:%02d\n" % (my_text,hr,mn,sc)
        my_text = "%sRemaining time:        %2d:%02d:%02d\n" % (my_text,r_hr,r_mn,r_sc)
        my_text = "%sProgress:              %5.1f%%\n" % (my_text,my_dict["progress"])
        
        my_text = "%s--------------------------------\n" % my_text
        
        printer_status["text"] = my_text

        # enable camera button
        cameraButton["state"] = "active"
    else:
        printer_status["text"] = "error: " + r.text
    window.after(1000, get_status)   # the delay is in milliseconds

if __name__ == '__main__': main()
