#!/usr/bin/env python3 

import ldap3
import os
import subprocess
import pyautogui as pag
from termcolor import colored
import argparse
import time


# This function will output the credits of the code
def Credits():
    toBePrinted =  "#####################################################################\n"
    toBePrinted += "#       Python3 code to check for LDAP base misconfiguration        #\n"
    toBePrinted += "#          Implemented by Marco Dal Broi @ Studio Consi             #\n"
    toBePrinted += "#                   https://studioconsi.com                         #\n"
    toBePrinted += "#####################################################################\n"
    print(colored(toBePrinted,"green"))


# This function will get the user's input file (string) and will return to the main loop.
def getArgs():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="File IPs")
    
    args = vars(ap.parse_args())
    fileIP = args["file"]
    
    return fileIP;


# This function will beep and alert the user if it finds a misconfiguration in the LDAP configuration
def Success(info):

    duration = 1  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

    toDisplay = f"LDAP information got: {info}"
    subprocess.run(["/usr/bin/notify-send", "--icon=alert", f"{toDisplay}"])
    pag.alert(text=f"LDAP information got: {info}!", title="VULNERABILITY FOUND")  


if __name__ == "__main__":
    Credits()
    fileIP = getArgs()
    
    totIP = 0
    with open(fileIP,"r") as fIPs:
        for ip in fIPs:
            totIP += 1

    counter = 1
    with open(fileIP,"r") as fIPs:
        start = time.perf_counter()
        for ip in fIPs:
            print(f"Checking the ip n°{counter} out of {totIP}")
            ip = str(ip).replace("\n","")

            print(f"Try to connect to: {ip}")
            try:
                server = ldap3.Server(ip, get_info=ldap3.ALL, port=636,use_ssl=True)
                connection = ldap3.Connection(server)
                tocheck = connection.bind()
                print(f"Connection result: {connection}")

                if tocheck == True:
                    info = server.info
                    Success(info)
                    print(colored(info,"red"))
            except:
                pass
            finally:
                counter += 1

        end = time.perf_counter()
        print(f"Actual time used: {round(end-start,2)}")