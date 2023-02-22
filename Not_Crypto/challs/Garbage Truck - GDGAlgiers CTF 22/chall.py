import gc
import re
import os
os.chdir("/home/ctf")
os.system('rm chall.py')
del os
print("""
  ____            _                       ______               __
 / ___| __ _ _ __| |__   __ _  __ _  ___  |_   _| __ _   _  ___| | __
| |  _ / _` | '__| '_ \ / _` |/ _` |/ _ \   | || '__| | | |/ __| |/ /
| |_| | (_| | |  | |_) | (_| | (_| |  __/   | || |  | |_| | (__|   <
 \____|\__,_|_|  |_.__/ \__,_|\__, |\___|   |_||_|   \__,_|\___|_|\_\\
                              |___/
      ______________
     '-------------.`-.
        /..---..--.\\  `._________________________________________
       //||   ||   \\\   `-\\-----\\-----\\-----\\-----\\-----\\--\\
   __.'/ ||   ||    \\\     \\     \\     \\     \\     \\     \\  \\
  /   /__||___||___.' \\     \\     \\     \\     \\     \\     \\ |
  |       |  -|        \\     \\     \\     \\     \\     \\     \\/
  |       |___|________ \\     \\     \\     \\     \\     \\_.-'
  [ ____ /.-----------.\ \\     \\     \\     \\     \\   .'
 | |____|/ .-'''''''-. \\ \\     \\     \\ .-'''''''-.\\_/
 | |____|.'           '.\\ \\____....----.'           '.
 | |___ /    .-----.    \\\______....---/    .-----.    \\
 | |___|    / o o o \    \|============|    / o o o \    \\
 | |__ |   | o     o |   ||____________|   | o     o |   |
[_.|___\    \ o o o /    |             \    \ o o o /    |
  .  .  \    '-----'    /  .   ..  . .  \    '-----'    /  . .
 .  .  . '.           .'   .  .   .   .  '.           .' .  .
 ..  .   . '-._ _ _.-'   .  .   .   .   .  '-._ _ _.-' . .
 Hi there, can you help me find the keys in the garbage!!!
""")

"CyberErudites{cl34N1N9_7H3_94r8493_W17h_gC}"

def garbage_truck():
    return "empty garbage truck"


del vars()['gc']
while True:
    text = input('>>> ').lower()
    check = (lambda word: re.compile(r"\b({0})\b".format(word), flags=re.IGNORECASE).search)("print|def|import|chr|map|os|system|builtin|exec|eval|subprocess|pty|popen|read|get_data|open|\+")(''.join(text.split("__")))
    if check :
        print('you cannot get rid of the garbage like this')
    else:
        try:
            exec(text)
            print(garbage_truck())
        except:
            print('No.no.no you will break my truck with that!!!')
