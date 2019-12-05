import telegram
from tokenSetting import APIBot
import requests
import json


RJAPI = "https://api-rj-app.com/api2/mp3?id="
userLink = "https://www.radiojavan.com/mp3s/mp3/Satin-Toonesti-Eshgham"

finalLink = userLink.split('https://www.radiojavan.com/mp3s/mp3/')[1]

URL = RJAPI + finalLink
data = requests.get(URL).text
data = json.loads(data)

title = data["title"]
link = data["link"]
print(title, link)

# bot = telegram.Bot(token=APIBot)
# print(bot.get_me())