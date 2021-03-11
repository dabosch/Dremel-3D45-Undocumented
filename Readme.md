# Dremel 3D45 Undocumented
This repo lists features and information about the Dremel 3D45 3D-Printer which are not part of the official manual.
Everything listed here comes with out any warranty, usage of that information is at your own risk!

All examples below assume the IP address of the 3D45 is `10.41.50.65`. So you have to supplement this with your IP address.

## General information
**Firmware Version**: v3.0_R02.10.09

## Command API
The printer provides a command API on port 80.
It can be accessed using *curl* like so:
```
curl 10.41.50.65/command -X POST -H "Content-Type: application/x-form-urlencoded" -d "GETPRINTERSTATUS"
```

The following commands are known, more might be available:

**command**         | **description**
------------------- | ---------------
GETPRINTERSTATUS    | returns a JSON object with lots of information about the current status
GETPRINTERINFO      | Info such as firmware version, IP address etc
PAUSE               | pauses the current print
RESUME              | resumes the current print, if paused
PRINT               | takes unknown 2nd parameter, presumably prints
GETJOBSTATUS        | gets job status

## Dremel Dashboard
A web interface can be reached via
https://10.41.50.65:11134

This is quite useful and provides lots of real-time information. A print can be started from it, but it cannot be stopped or paused.

The dashboard includes a simple admin interface. Here the network configuration can be changed.
Default credentials are:

Username: `admin`
Password: `password`

## Simple control interface
A simple control interface for the 3D45 (written in python) is defined in the file Control_3D45.py
