print("Loaded definitions! 'b.py'")
import os
import time
from time import sleep
import platform
import random

def cls():
    if platform == "darwin":
        os.system("clear")
    else:
        os.system("cls")