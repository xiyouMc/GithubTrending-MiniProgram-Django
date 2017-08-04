import requests
import os
import time

login_api = 'https://python.0x2048.com/v1/login?username=%s&password=%s'
dir = '/Users/xiyouMc/dev/Trending/'
count = 0
for i in os.listdir(dir):
    time.sleep(1)
    if i.endswith('.txt'):
        count = count + 1
        print i
        filepath = dir + i
        with open(filepath, 'r') as file:
            c = file.readline()
            username, password = c.split(',')
            print username, password
            s = requests.get(login_api % (username, password))
            print s.text
print count