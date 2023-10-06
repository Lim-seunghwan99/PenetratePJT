from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd

# Create your views here.
from io import BytesIO

import base64
plt.switch_backend('Agg')
def index(request):
    x = [1, 2, 3, 4]
    y = [2, 4, 8, 16]

    # 다른 view 함수에서 plt를 이미 그린 상태에서
    # 다시 그리는 경우를 대비하여 초기화를 진행
    plt.clf() # plt를 초기화 하는 함수

    plt.plot(x, y)
    plt.title("Graph")
    plt.ylabel('y label')
    plt.xlabel('x label')

    # plt.savefig('firstgraph.png')
    # 비어있는 버퍼를 생성
    buffer = BytesIO()

    # 버퍼에 그래프를 저장
    plt.savefig(buffer, format="png")

    # 버퍼의 내용을 base64로 인코딩
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')

    # 버퍼를 닫아줌
    buffer.close()

    # 이미지를 웹 페이지에 표시하기 위해
    # URI 형식(주소 형식)으로 만들어진 문자열을 생성
    context = {
        # chart_image: 저장된 이미지의 경로
        'chart_image': f'data:image/png;base64,{image_base64}',
    }

    # return render(request, "index.html", context)
    return render(request, "index.html")


csv_path = 'weathers/data/austin_weather.csv'
# 다운로드 받은 데이터(.csv 출력)를 Pandas DataFrame 형식으로 저장 및 problem1.html 렌더링
def problem1(request):
    df = pd.read_csv(csv_path)
    
    context = {
        'df': df,
    }
    return render(request, 'problem1.html', context)

# # 일 별 온도 비교를 위한 라인 그래프 생성 및 problem2.html 렌더링
def problem2(request):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    x = df['Date']
    y1 = df['TempHighF']
    y2 = df['TempAvgF']
    y3 = df['TempLowF']
    plt.clf() # plt를 초기화 하는 함수
    plt.figure(figsize=(10,6))
    plt.plot(x, y1, label='High Temperature')
    plt.plot(x, y2, label='Average Temperature')
    plt.plot(x, y3, label='Low Temperature')
    plt.title("Temperature Variation")
    plt.ylabel('Temperature (Fahrenheit)')
    plt.xlabel('Date')
    plt.legend(loc='lower center')
    plt.grid(True)
    

    
    buffer = BytesIO()

    # 버퍼에 그래프를 저장
    plt.savefig(buffer, format="png")

    # 버퍼의 내용을 base64로 인코딩
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')

    # 버퍼를 닫아줌
    buffer.close()
    context = {
        # chart_image: 저장된 이미지의 경로
        'chart_image2': f'data:image/png;base64,{image_base64}',
    }
    return render(request, 'problem2.html', context)

# # 월 별 온도 비교를 위한 라인 그래프 생성 및 problem3.html 렌더링
def problem3(request):
    df = pd.read_csv(csv_path, usecols= range(0,4))
    df['Date'] = pd.to_datetime(df['Date'])
    after_2014 = df[df["Date"] >= "2014-01-01"]
    after_2014['Date'] = pd.to_datetime(after_2014['Date'])
    df_m_mean = after_2014.resample('M', on='Date').mean()
    # df['Month'] = df['Date'].dt.month
    x = df_m_mean.index
    y1 = df_m_mean['TempHighF']
    y2 = df_m_mean['TempAvgF']
    y3 = df_m_mean['TempLowF']
    plt.clf() # plt를 초기화 하는 함수
    plt.figure(figsize=(10,6))
    plt.plot(x, y1, label='High Temperature')
    plt.plot(x, y2, label='Average Temperature')
    plt.plot(x, y3, label='Low Temperature')
    plt.title("Temperature Variation")
    plt.ylabel('Temperature (Fahrenheit)')
    plt.xlabel('Date')
    plt.legend(loc='lower right')
    # plt.xticks(df['Month'], ['2014-01', '2014-07', '2015-01', '2015-07', '2016-01', '2016-07', '2017-01', '2017-07'])
    plt.grid(True)
    

    
    buffer = BytesIO()

    # 버퍼에 그래프를 저장
    plt.savefig(buffer, format="png")

    # 버퍼의 내용을 base64로 인코딩
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')

    # 버퍼를 닫아줌
    buffer.close()
    context = {
        # chart_image: 저장된 이미지의 경로
        'chart_image3': f'data:image/png;base64,{image_base64}',
    }
    return render(request, 'problem3.html', context)

# # 기상 현상 발생 횟수 히스토그램 생성 및 problem4.html 렌더링
def problem4(request):
    df = pd.read_csv(csv_path)
    No_Events = 0
    Rain = 0
    Thunderstorm = 0
    Fog =  0
    Snow = 0 
    for i in df['Events']:
        event = i.replace(' ','').split(',')
        if event[0] == '':
            No_Events += 1
        else:
            for ev in event:
                if ev == 'Rain':
                    Rain += 1
                elif ev == 'Thunderstorm':
                    Thunderstorm += 1
                elif ev == 'Fog':
                    Fog += 1
                elif ev == 'Snow':
                    Snow += 1

    column = [No_Events, Rain, Thunderstorm, Fog, Snow]
    row = ['No_Events', 'Rain', 'Thunderstorm', 'Fog', 'Snow']

    plt.clf() # plt를 초기화 하는 함수
    plt.figure(figsize=(10,6))
    plt.bar(row, column)
    plt.title("Event Counts")
    plt.ylabel('Count')
    plt.xlabel('Events')
    plt.grid(True)
    

    
    buffer = BytesIO()

    # 버퍼에 그래프를 저장
    plt.savefig(buffer, format="png")

    # 버퍼의 내용을 base64로 인코딩
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')

    # 버퍼를 닫아줌
    buffer.close()
    context = {
        # chart_image: 저장된 이미지의 경로
        'chart_image4': f'data:image/png;base64,{image_base64}',
    }
    return render(request, 'problem4.html', context)
