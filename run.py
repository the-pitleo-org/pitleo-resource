print("Publishing!")
import os
try:
    os.system("git add .")
    os.system("git commit -m 'New Update.'")
    os.system("git push")
except:
    print("An error occured.")