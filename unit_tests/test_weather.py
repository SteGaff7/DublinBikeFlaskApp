import unittest
import json
import urllib.request

class weather_today_array():
    def weatherToday(self):
        weather_array = []
        '''
        Get weather forecast for right now and the next 3 forecasts for the day. Return this as a list with lists within
        '''
        #Current Weather this instant
        with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
            data = json.loads(url.read().decode())

            weather = data["weather"][0]["main"]
            icon = data["weather"][0]["icon"]
            temp = str(round(int(data["main"]["temp"])-273.15)) + "°C"

            weather_array = [["Now", weather, temp, icon],[],[],[]]

        #Next 3 weather forecasts
        with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
            data = json.loads(url.read().decode())

            for i in range(1, 4, +1):
                #print(data["list"][i]["dt_txt"])
                forecast_date_time = data["list"][i]["dt_txt"]
                forecast_date = forecast_date_time.split()[0]
                forecast_time = forecast_date_time.split()[1]
                forecast_time_slice = forecast_time[0:5]

                icon = data["list"][i]["weather"][0]["icon"]
                weather = data["list"][i]["weather"][0]["main"]
                temp = str(round(int(data["list"][i]["main"]["temp"])-273.15)) + "°C"

                weather_array[i] = [forecast_time_slice, weather, temp, icon]

        return weather_array

class Testweather_today_array(unittest.TestCase):

    def test1(self):
        x = weather_today_array().weatherToday()
        self.assertTrue(len(x) == 4)

unittest.main(argv=[''], verbosity=2, exit=False)
