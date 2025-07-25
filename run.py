print("Publishing!")
import os
try:
    os.system("git add .")
    os.system('git commit -m "hi"')
    os.system("git push")
except:
    print("An error occured.")