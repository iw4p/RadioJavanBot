import telegram
from tokenSetting import APIBot
import urllib, json
import requests


RJAPI = "https://api-rj-app.com/api2/mp3?id="
testLink = "Khashayar-SR-Ki-Chi-Dare-(Ft-Arma)"

# json_url = urlopen(RJAPI + testLink)

# data = json.loads(json_url.read())

r = requests.get(RJAPI + testLink)

print(r.json())

# print(data)

bot = telegram.Bot(token=APIBot)
print(bot.get_me())