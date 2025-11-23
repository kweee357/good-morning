import requests
from datetime import date, datetime

# --- 配置区 ---
APP_ID = 'wx310604ee84d9f81d'
APP_SECRET = '170b1b95b54785c47516968cb4ba1047'
USER_ID = 'ocOX52KPEzIU77LyVSnTp0PQQJgQ'
TEMPLATE_ID = 'YitsRcwPwFVqEwO9d8ox-mPU2w51VYN3s2a8nPBgOAI'  # 需要创建新模板

START_DATE = "2024-12-05"
BIRTHDAY = "02-23"
CITY_CODE = "101030100"
TO_NICKNAME = "宝宝"
FROM_NICKNAME = "爱你的郭浩"

def get_weather():
    try:
        url = f"http://t.weather.sojson.com/api/weather/city/{CITY_CODE}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        weather_data = resp.json()
        
        if weather_data.get('status') == 200:
            data = weather_data['data']
            forecast = data['forecast'][0]
            weather = forecast['type']
            low_temp = forecast['low'].replace('低温', '').replace('℃', '').strip()
            high_temp = forecast['high'].replace('高温', '').replace('℃', '').strip()
            temp_range = f"{low_temp}~{high_temp}"
            current_temp = f"{data['wendu']}°C"
            
            if '雨' in weather:
                tip = "今天有雨，记得带伞☔️"
            elif '晴' in weather:
                tip = "天气晴朗🌞，记得防晒"
            elif '云' in weather:
                tip = "多云天气⛅，温度适宜"
            elif '雪' in weather:
                tip = "下雪啦⛄，注意保暖"
            elif '霾' in weather:
                tip = "今天有雾霾，注意安全哦"
            else:
                tip = "注意天气变化"
                
            return weather, temp_range, current_temp, tip
    except Exception as e:
        print(f"天气获取失败: {e}")
    
    return "未知", "未知", "未知", "出门记得看天气"

def calculate_dates():
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    love_days = (date.today() - start_date).days
    
    today = datetime.now()
    birthday_this_year = datetime.strptime(f"{today.year}-{BIRTHDAY}", "%Y-%m-%d").date()
    if birthday_this_year < today.date():
        birthday_next_year = birthday_this_year.replace(year=today.year + 1)
        birth_days = (birthday_next_year - today.date()).days
    else:
        birth_days = (birthday_this_year - today.date()).days
        
    return love_days, birth_days

def send_wechat_message():
    print("🚀 开始发送微信消息...")
    
    # 获取token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        resp = requests.get(token_url)
        token_data = resp.json()
        
        if 'access_token' in token_data:
            token = token_data['access_token']
            print("✅ Token获取成功")
        else:
            print(f"❌ 获取token失败: {token_data}")
            return False
    except Exception as e:
        print(f"❌ Token请求失败: {e}")
        return False

    # 获取数据
    weather, temp_range, current_temp, tip = get_weather()
    love_days, birth_days = calculate_dates()
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[datetime.now().weekday()]
    
    print("📦 准备发送的数据:")
    print(f"  日期: {current_date}")
    print(f"  星期: {weekday}")
    print(f"  天气: {weather}")
    print(f"  温度: {temp_range}")
    print(f"  当前温度: {current_temp}")
    print(f"  提示: {tip}")
    print(f"  恋爱天数: {love_days}天")
    print(f"  生日倒计时: {birth_days}天")
    print(f"  昵称: {TO_NICKNAME}")
    print(f"  发送者: {FROM_NICKNAME}")
    
    # 构建发送数据
    data = {
        "touser": USER_ID,
        "template_id": TEMPLATE_ID,
        "data": {
            "date": {"value": current_date},
            "weekday": {"value": weekday},
            "weather": {"value": weather},
            "temperature": {"value": temp_range},
            "currentTemp": {"value": current_temp},
            "tip": {"value": tip},
            "loveDays": {"value": f"{love_days}天"},
            "birthdayCountdown": {"value": f"{birth_days}天"},
            "toNickname": {"value": TO_NICKNAME},
            "fromNickname": {"value": FROM_NICKNAME}
        }
    }
    
    # 发送消息
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    try:
        print("📤 正在发送消息...")
        res = requests.post(send_url, json=data)
        result = res.json()
        
        print(f"📨 微信API响应: {result}")
        
        if result.get('errcode') == 0:
            print("✅ 消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 发送请求失败: {e}")
        return False

if __name__ == '__main__':
    send_wechat_message()
