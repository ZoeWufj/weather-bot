import requests
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# 設置 Line Notify 的 URL 和權杖
url = 'https://notify-api.line.me/api/notify'
token = os.environ['LINE_NOTIFY_TOKEN']
headers = {
    'Authorization': 'Bearer ' + token    # 設定權杖
}

# 取得天氣資訊
weather_url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization=CWA-A12B3F3C-FA33-4056-8A96-786BD044C45F&downloadType=WEB&format=JSON'
weather_data = requests.get(weather_url)
weather_data_json = weather_data.json()
location = weather_data_json['cwaopendata']['dataset']['Station']

# 初始化訊息
msg = ""

for i in location:
    name = i['StationName']            # 測站地點
    city = i['GeoInfo']['CountyName']  # 城市
    area = i['GeoInfo']['TownName']    # 行政區
    temp = i['WeatherElement']['AirTemperature']     # 氣溫
    humd = i['WeatherElement']['RelativeHumidity']   # 相對濕度
    weather = i['WeatherElement']['Weather']         # 天氣狀況
    wind_dir = i['WeatherElement']['WindDirection']  # 風向
    wind_speed = i['WeatherElement']['WindSpeed']    # 風速
    air_pressure = i['WeatherElement']['AirPressure'] # 氣壓
    precipitation = i['WeatherElement']['Now']['Precipitation'] # 降雨量

    daily_high_temp = i['WeatherElement']['DailyExtreme']['DailyHigh']['TemperatureInfo']['AirTemperature']
    daily_high_time = i['WeatherElement']['DailyExtreme']['DailyHigh']['TemperatureInfo']['Occurred_at']['DateTime']
    daily_low_temp = i['WeatherElement']['DailyExtreme']['DailyLow']['TemperatureInfo']['AirTemperature']
    daily_low_time = i['WeatherElement']['DailyExtreme']['DailyLow']['TemperatureInfo']['Occurred_at']['DateTime']

    if city == "臺北市" and area == "內湖區" and name == "內湖":
        msg = (
            f"{city} {area} {name}觀測站\n"
            f"氣溫: {temp} 度\n"
            f"相對濕度: {humd} %\n"
            f"天氣: {weather}\n"
            f"風向: {wind_dir} 度\n"
            f"風速: {wind_speed} m/s\n"
            f"氣壓: {air_pressure} hPa\n"
            f"降雨量: {precipitation} mm\n"
            f"今日最高氣溫: {daily_high_temp} 度 (時間: {daily_high_time})\n"
            f"今日最低氣溫: {daily_low_temp} 度 (時間: {daily_low_time})"
        )
        break

# 發送訊息到 Line Notify
if msg:
    data = {
        'message': msg    # 設定要發送的訊息
    }
    response = requests.post(url, headers=headers, data=data)

    # 檢查回應狀態
    if response.status_code == 200:
        print("訊息已成功發送到 Line Notify")
    else:
        print("發送失敗，狀態碼：", response.status_code)
else:
    print("找不到符合條件的天氣資訊")

    
