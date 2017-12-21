#!/usr/bin/env python

""" A ham radio keyer for raspberry pi"""

import RPi.GPIO as GPIO
import time
from cmd import Cmd

# Set defaults here
CALL = "ww4n"
RST = "r 5nn tu"
default_WPM = 25
BCM_pin = 24


def dit():
    tx(DitLength)
    time.sleep(DitLength)


def dah():
    tx(DahLength)
    time.sleep(DitLength)


def space():
    time.sleep(CharSpaceExtra)


def word():
    time.sleep(WordSpaceExtra)


def tx(keylength):
    """ Keys the TX """
    # set the output to Key Down...
    GPIO.output(BCM_pin, True)
    time.sleep(keylength)
    # clear the output ...
    GPIO.output(BCM_pin, False)
    return


def send(code):
    for element in morse[code]:
        if element == ".":
            dit()
        elif element == "-":
            dah()


def lookup(message):
    sendspace = True
    for char in message:
        if char == "<":
            sendspace = False
            continue
        if char == ">":
            sendspace = True
            continue
        if char == " ":
            sendspace = True
        if char == " ":
            word()
        elif char not in morse.keys():
            print("")
            print("unknown char: %s" % char)
            pass
        else:
            send(char)
            if sendspace:
                space()
    print("sent message: '%s'" % message)


class MyPrompt(Cmd):
    def emptyline(self):
        pass

    def do_PROSIGNS(self, args):
        """Anything enclosed in angle brackets will have no separating space: <bt>"""
        pass

    def do_CALL(self, args):
        """Passing arguments sets the CALL message.
With no arguments, the CALL message is sent.
'CALL ?' displays the current CALL message."""
        global CALL
        if not args:
            lookup(CALL.lower())
        elif args == "?":
            print("current CALL message: '%s'" % CALL)
        else:
            print("Setting CALL to '%s'" % args.lower())
            CALL = args.lower()

    def do_RST(self, args):
        """Passing arguments sets the RST message.
With no arguments, the RST message is sent.
'RST ?' displays the current RST message."""
        global RST
        if not args:
            lookup(RST.lower())
        elif args == "?":
            print("current RST message: '%s'" % RST)
        else:
            print("Setting RST to '%s'" % args.lower())
            RST = args.lower()

    def do_EOF(self, args):
        """Quits the program. Type 'EOF' or press 'Cntrl-D'"""
        print("Quitting.")
        raise SystemExit

    def default(self, line):
        lookup(line.lower())

    def do_WPM(self, args):
        """Sets WPM to argument passed. No argument will set it to the default."""
        global WPM
        global DitLength
        global DahLength
        if not args:
            WPM = default_WPM
        else:
            WPM = int(args)
        prompt.prompt = str(WPM) + ' WPM> '
        DitLength = float(60 / float(WPM * 50))
        DahLength = 3 * DitLength

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BCM_pin, GPIO.OUT)
GPIO.output(BCM_pin, GPIO.LOW)

WPM = default_WPM
DitLength = float(60 / float(WPM * 50))
DahLength = 3 * DitLength
# Dits and Dahs will have one ditlength space after each already
# CharSpace and WordSpace should be 3 and 7, so here is the extra
CharSpaceExtra = 2 * DitLength
WordSpaceExtra = 6 * DitLength

morse = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "y": "-.--",
    "z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "?": "..--..",
    ".": ".-.-.-",
    ",": "--..--",
    "/": "-..-."
}

if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = str(WPM) + ' WPM> '
    prompt.cmdloop('Starting keyer. Type "help" for help...')
