# Dremel 3D45 Undocumented
This repo lists features and information about the Dremel 3D45 3D-Printer which are not part of the official manual.
Everything listed here comes with out any warranty, usage of that information is at your own risk!

## General information
**Firmware Version**: v3.0_R02.10.09

## Command API
The printer provides a command API on port 80.
It can be accessed using *curl* like so:
```
curl 192.168.0.123/command -X POST -H "Content-Type: application/x-form-urlencoded" -d "GETPRINTERSTATUS"
```

The following commands are known, more might be available:

**command**         | **description**
--------------------+----------------
GETPRINTERSTATUS    | returns a JSON object with lots of information about the current status
GETPRINTERINFO      | Info such as firmware version, IP address etc
PAUSE               | pauses the current print
RESUME              | resumes the current print, if paused
PRINT               | takes unknown 2nd parameter, presumably prints
GETJOBSTATUS        |

## Dremel Dashboard
A web interface can be reached via
https://192.168.0.123:11134

This is quite useful and provides lots of real-time information. A print can be started from it, but it cannot be stopped or paused.