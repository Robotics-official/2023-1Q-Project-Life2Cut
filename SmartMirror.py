import hashlib

import os, sys
from os import remove
import time
from picamera import PiCamera
import cv2
from PIL import Image, ImageDraw, ImageEnhance
import qrcode
from io import StringIO

import tkinter as tk
import requests
from datetime import datetime


def return_print(*message):
        io = StringIO()
        print(*message, file=io, end="")
        return io.getvalue()

def on_click(event):
    for i in range (2) :
            for i in range(1, 6+1):
                    cv2.namedWindow("Window_name", cv2. WINDOW_NORMAL)
                    cv2.setWindowProperty("Window_name", cv2. WND_PROP_FULLSCREEN, cv2. WINDOW_FULLSCREEN)
                    cv2.moveWindow("Window_name", x=0, y=0)
                    img = cv2.imread(f'./images/countdown/{i}.jpg', cv2.IMREAD_COLOR)
                    cv2.imshow("Window_name", img)
                    cv2.waitKey(1000)
                    time.sleep(0.5)
                    cv2.destroyAllWindows()

            os.system("./camera.sh")

    path = os.path.normpath("./images/temp")
    file_list = os.listdir(path)
    file_list.sort(reverse=True)
    size = len(file_list)

    global first, second
    new = Image.new("RGBA", (800, 400))

    cnt = 0
    for filename in file_list:
            img = return_print("./images/temp"+f"{os.path.splitext(filename)[0]}")
            cnt += 1
            if cnt == 1:
                    second = Image.open(f"{img}.jpg")
                    new.paste(second, (400,0))
                    remove(f"{img}.jpg")
                    print("first image removed")
            if cnt == 2:
                    first = Image.open(f"{img}.jpg")
                    new.paste(first, (0,0))
                    remove(f"{img}.jpg")
                    print("second image removed")
                    break
                    
    now = datetime.now()
    nowDateTime = now.strftime('%Y-%m-%d_%H%M%S')
    # HASH
    hash_object = hashlib.sha256(nowDateTime.encode())
    filename_hash = hash_object.hexdigest()[:10]
    # IMAGE SAVE
    new.save("./images/"+f"{filename_hash}.PNG")
    new.show()
    # READY URL
    host_url = "http://host"
    image_url = host_url+'/images/'+f"{filename_hash}"
    # QR CREATE
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(image_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # QR SAVE
    img.save('./qr/'+f"{filename_hash}.png")
    # QR SHOW
    img.show()

def get_latest_news():
    # NEWS API
    url = f'https://newsapi.org/v2/top-headlines?country=kr&apiKey=48ae3c0708b74cf298f8664d1499df6d'

    # API REQUEST
    response = requests.get(url)

    # GET LATEST NEWS
    articles = response.json().get('articles', [])
    latest_news = []
    for article in articles:
        title = article.get('title')
        source = article.get('source', {}).get('name')
        latest_news.append(f'{title} ({source})')
        break

    return latest_news

def get_weather():
    # OPENWEATHER API
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=38200acbfebee11d606c8944e6904527&units=metric' # YOUR_APPID에는 실제 APPID를 입력해주세요
    res = requests.get(url)
    data = res.json()

    # GET WEATHER
    temp = data['main']['temp']
    weather = data['weather'][0]['description']

    return f'Temperature: {temp}°C\nWeather: {weather}'

# TK SETTING
root = tk.Tk()

root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.configure(bg='black')

root.bind('<Button-1>', on_click)

# TK NAME
root.title('Digital Clock & Weather')

# CLOCK LABEL
clock_label = tk.Label(root, font=('Arial', 80, 'bold'), bg='black', fg='white')
clock_label.pack()

# WEATHER LABEL
weather_label = tk.Label(root, font=('Arial', 20, 'bold'), bg='black', fg='white')
weather_label.pack()

# NEWS LABEL
news_label = tk.Label(root, font=('Monospace Regular', 10, 'bold'), bg='black', fg='white')
news_label.pack()

def update():
    # REALTIME UPDATE
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    # UPDATE 1S
    clock_label.after(1000, update)

    # WEATHER UPDATE
    weather_info = get_weather()
    weather_label.config(text=weather_info)

    # NEWS UPDATE
    latest_news = get_latest_news()
    news_label.config(text='\n'.join(latest_news))

# LABEL LAYOUT
clock_label.pack(pady=50)
weather_label.pack()

# SMARTMIRROR UPDATE
update()

# TK START
root.mainloop()
