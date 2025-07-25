
import os
import random
from time import sleep
sleep(1)
try:
    os.system("git add .")
    print("git add .")
    sleep(1)
    os.system(f'git commit -m "{random.random()}"')
    print("Created a commit")
    os.system("git push")
    print("Pushed")
except:
    sleep(1)
    print("An error occured.")
    input("Press enter to exit")