print("Publishing!")
import os
import random
try:
    os.system("git add .")
    os.system(f'git commit -m "{random.random()}"')
    os.system("git push")
except:
    print("An error occured.")