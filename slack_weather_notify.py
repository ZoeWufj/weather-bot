import json
import slack
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
slackMsg = ''

# 取得天氣資訊
weather_url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-D0047-061?Authorization=CWA-A12B3F3C-FA33-4056-8A96-786BD044C45F&downloadType=WEB&format=JSON'
weather_data = requests.get(weather_url)
weather_data_json = weather_data.json()

# 取得當前時間
now = datetime.now()

# 計算當前時間所屬的三小時區間
hour = (now.hour // 3) * 3
start_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
end_time = start_time + timedelta(hours=3)

# 將時間格式化為所需的字串格式
start_time_str = start_time.strftime('%Y-%m-%dT%H:00:00+08:00')
end_time_str = end_time.strftime('%Y-%m-%dT%H:00:00+08:00')

# 查找臺北市的資料
locations = weather_data_json["cwaopendata"]["dataset"]["locations"]

if locations["locationsName"] == "臺北市":
    # 查找內湖區天氣描述
    for location in locations["location"]:
        if location["locationName"] == "內湖區":
            for weather_element in location["weatherElement"]:
                if weather_element["elementName"] == "WeatherDescription":
                    for weather in weather_element["time"]:
                        if weather["startTime"] == start_time_str and weather["endTime"] == end_time_str:
                            # print(weather["elementValue"]["value"])
                            weather_value = weather["elementValue"]["value"]
                            
                            # 將天氣資訊字串轉換為易讀格式，並去除不需要的資訊
                            weather_parts = weather_value.split("。")
                            filtered_parts = [part for part in weather_parts if not any(word in part for word in ["風", "濕度"])]
                            formatted_weather = "\n".join(filtered_parts)

                            slackMsg = f"""
未來3小時天氣預報：
{formatted_weather}
                            """
                            break
                    break
            break

# print(slackMsg)

client.chat_postMessage(channel='#chit-chat', text=slackMsg)
