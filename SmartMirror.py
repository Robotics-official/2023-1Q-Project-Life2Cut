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


# CLOCK GUI Part

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
                    #dst = cv2.resize(img, dsize=(800, 480), interpolation=cv2.INTER_AREA)
                    cv2.imshow("Window_name", img)
                    #cv2.imshow("dst", dst)
                    cv2.waitKey(1000)
                    time.sleep(0.5)
                    cv2.destroyAllWindows()

            os.system("./camera.sh")

    path = os.path.normpath("/home/pi/camera")
    file_list = os.listdir(path) # path 하위의 모든 파일 및 디렉토리를 리스트로 가져옴
    file_list.sort(reverse=True)
    size = len(file_list) # 해당 디렉토리의 바로 아래에 있는 파일/디렉토리 개수만 계산

    global first, second
    new = Image.new("RGBA", (800, 400))

    cnt = 0
    for filename in file_list:
            img = return_print("/home/pi/camera/"+f"{os.path.splitext(filename)[0]}")
            cnt += 1

            if cnt == 1:
                    second = Image.open(f"{img}.jpg")
                    new.paste(second, (400,0))
                    remove(f"{img}.jpg")
                    print("cnt = 1 success!")
            if cnt == 2:
                    first = Image.open(f"{img}.jpg")
                    new.paste(first, (0,0))
                    remove(f"{img}.jpg")
                    print("cnt = 2 success!")
            if cnt == 3:
                    print("cnt = 3, break!")
                    break
                    
    now = datetime.now()
    nowDateTime = now.strftime('%Y-%m-%d_%H%M%S')
    ### HASH
    hash_object = hashlib.sha256(nowDateTime.encode())
    filename_hash = hash_object.hexdigest()
    ### IMAGE SAVE
    new.save("./images/"+f"{filename_hash[:10]}.PNG")
    new.show()
    ### READY URL
    image_url = 'http://220.149.85.12/images/'+f"{filename_hash[:10]}"
    ### QR CREATE
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(image_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    ### QR SAVE
    img.save('./qr/'+f"{filename_hash[:10]}.png")
    ### QR SHOW
    img.show()

def get_latest_news():
    # News API endpoint
    url = f'https://newsapi.org/v2/top-headlines?country=kr&apiKey=48ae3c0708b74cf298f8664d1499df6d'

    # API 요청
    response = requests.get(url)

    # 응답 데이터에서 최신 뉴스 기사 추출
    articles = response.json().get('articles', [])
    latest_news = []
    for article in articles:
        title = article.get('title')
        source = article.get('source', {}).get('name')
        latest_news.append(f'{title} ({source})')
        break

    return latest_news

def get_weather():
    # OpenWeather API를 사용하여 날씨 정보 가져오기
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=38200acbfebee11d606c8944e6904527&units=metric' # YOUR_APPID에는 실제 APPID를 입력해주세요
    res = requests.get(url)
    data = res.json()

    # 날씨 정보 추출하기
    temp = data['main']['temp']
    weather = data['weather'][0]['description']

    # 날씨 정보 반환하기
    return f'Temperature: {temp}°C\nWeather: {weather}'

# tk 객체 생성
root = tk.Tk()

root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen",
                                    not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

root.configure(bg='black')

root.bind('<Button-1>', on_click)

# 윈도우 제목 설정
root.title('Digital Clock & Weather')

# 시계 라벨 생성
clock_label = tk.Label(root, font=('Arial', 80, 'bold'), bg='black', fg='white')
clock_label.pack()

# 날씨 라벨 생성
weather_label = tk.Label(root, font=('Arial', 20, 'bold'), bg='black', fg='white')
weather_label.pack()

# 뉴스 라벨 생성
news_label = tk.Label(root, font=('Monospace Regular', 10, 'bold'), bg='black', fg='white')
news_label.pack()

# 시계 및 날씨 정보 업데이트 함수
def update():
    # 현재 시간 표시
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update) # 1초마다 업데이트

    # 날씨 정보 표시
    weather_info = get_weather()
    weather_label.config(text=weather_info)

    # 최신 뉴스 업데이트
    latest_news = get_latest_news()
    news_label.config(text='\n'.join(latest_news))

# 라벨 배치
clock_label.pack(pady=50)
weather_label.pack()

# 시계 업데이트 시작
update()

# tk 객체 실행
root.mainloop()
