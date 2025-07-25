
import os
import random
import platform
import b
from time import sleep
import datetime

now = datetime.datetime.now()

print(now)

sleep(1)
try:
    os.system("git add .")
    print("git add .")
    sleep(1)
    b.cls
    os.system(f'git commit -m "{now}"')
    print("Created a commit")
    sleep(1)
    b.cls
    os.system("git push")
    print("Pushed")
    sleep(1)
except:
    sleep(1)
    print("An error occured.")
    input("Press enter to exit")