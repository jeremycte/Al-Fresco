import requests, json
from apikey import weather_key
from bs4 import BeautifulSoup

API_KEY = weather_key

def get_weather(location):

    # creating url and requests instance
    url = "https://www.google.com/search?q="+"weather"+location
    html = requests.get(url).content
 
    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    string = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    data = string.split('\n')
    time = data[0]
    sky = data[1]
    sky = sky.lower()

    # getting all div tag
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text

    # conditions
    if sky == "thunderstorm":
        chance_of_rain = "70 - 90%"
    elif sky == "scattered thunderstorms":
        chance_of_rain = "50 - 70%"
    elif sky == "partly cloudly":
        chance_of_rain = "30 - 50%"
    elif sky == "sunny":
        chance_of_rain = "10 - 30%"
    elif sky == "clear":
        chance_of_rain = "10 - 30%"
    elif sky == "showers":
        chance_of_rain = "80 - 90%"
    elif sky == "rain":
        chance_of_rain = "80 - 90%"
    elif sky == "mostly cloudy":
        chance_of_rain = "50 - 70%"
    else:
        chance_of_rain = "40 - 60%"  
 
    # printing all data
    # print("Temperature is", temp)
    return "3 Hour Weather Forecast: " + '\n' + "Temperature: " + temp + '\n' + "Time: " + time + '\n' + "Sky Description: " + sky + '\n' + "Chance of Rain: " + chance_of_rain

# def get_time(location):
    
#     # creating url and requests instance
#     url = "https://www.google.com/search?q="+"weather"+location
#     html = requests.get(url).content
 
#     # getting raw data
#     soup = BeautifulSoup(html, 'html.parser')
#     string = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
 
#     # formatting data
#     data = string.split('\n')
#     time = data[0]

#     # getting all div tag
#     listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
#     strd = listdiv[5].text
 
#     # printing all data
#     print("Time: ", time)
#     return "Time: " + time

# def get_sky(location):
    
#     # creating url and requests instance
#     url = "https://www.google.com/search?q="+"weather"+location
#     html = requests.get(url).content
    
#     # getting raw data
#     soup = BeautifulSoup(html, 'html.parser')
#     str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    
#     # formatting data
#     data = str.split('\n')
#     sky = data[1]
    
#     # getting all div tag
#     listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
#     strd = listdiv[5].text
    
#     # printing all data
#     print("Sky Description: ", sky)
#     return "Sky Description: " + sky

# def rain_chances(location):
    
#     # creating url and requests instance
#     url = "https://www.google.com/search?q="+"weather"+location
#     html = requests.get(url).content
    
#     # getting raw data
#     soup = BeautifulSoup(html, 'html.parser')
#     str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    
#     # formatting data
#     data = str.split('\n')
#     sky = data[1]
    
#     # getting all div tag
#     listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
#     strd = listdiv[5].text

#     # conditions
#     if sky == "Thunderstorm":
#         chance_of_rain = "70 - 90%"
#     elif sky == "Scattered thunderstorms":
#         chance_of_rain = "50 - 70%"
#     elif sky == "partly cloudly":
#         chance_of_rain = "30 - 50%"
#     elif sky == "sunny":
#         chance_of_rain = "10 - 30%"
#     elif sky == "clear":
#         chance_of_rain = "10 - 30%"
#     elif sky == "showers":
#         chance_of_rain = "80 - 90%"
#     elif sky == "rain":
#         chance_of_rain = "80 - 90%"
#     else:
#         chance_of_rain = "40 - 60%"  

#     print("Chance of Rain: ", chance_of_rain)
#     return "Chance of Rain: " + chance_of_rain