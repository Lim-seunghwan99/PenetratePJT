from django.shortcuts import render, redirect
from .models import Keyword, Trend
from .forms import KeywordForm
from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Create your views here.
def keyword(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.save()
    keywords = Keyword.objects.all()
    form = KeywordForm()
    context = {
        'keywords': keywords,
        'form': form
    }
    return render(request, 'trends/keyword.html', context)

def delete(request, pk):
    keyword = Keyword.objects.get(pk=pk)
    keyword.delete()
    return redirect('trends:keyword')

def crawling(request):
    def get_google_data(keywords):
        # 가져올 웹 페이지 url
        url = f'https://www.google.com/search?q={keywords}'

        driver = webdriver.Chrome()
        driver.get(url)

        # 열린 페이지 소스를 받아옴
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 검색 결과 가져오기
        # div 태그 안의 id 가 result-stats 라는 요소
        result_stats = soup.select_one("div#result-stats")
        # print(result_stats.text)
        temp = result_stats.text[7:-10].replace(',','')
        return int(temp)
    
    keywords = Keyword.objects.all()
    for keyword in keywords:
        result = get_google_data( keyword.name)
        trend, is_created = Trend.objects.get_or_create(defaults={'result': result},name=keyword.name, search_period='all')
        if is_created:
            trend.result = result
        trend.save()
    trends = Trend.objects.all()
    context = {
        'trends': trends,
    }
    return render(request, 'trends/crawling.html', context)
    

def histogram(request):
    x = []
    y = []
    trends = Trend.objects.all()
    for trend in trends:
        if trend.search_period == 'all':
            x.append(trend.name)
            y.append(trend.result)

    plt.clf()
    plt.bar(range(0, len(x)), y, label='Trends')
    plt.xticks(range(0, len(x)), x, rotation=45)
    plt.grid()
    plt.title('Technology Trend Analysis')
    plt.xlabel('keyword')
    plt.ylabel('result')
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    context = {
        'chart_image': f'data:image/png;base64,{image_base64}'
    }
    return render(request, 'trends/crawling_histogram.html', context)

def acvanced(request):
    def get_google_data(keywords):
        # 가져올 웹 페이지 url
        url = f'https://www.google.com/search?q={keywords}&tbs=qdr:y'

        driver = webdriver.Chrome()
        driver.get(url)

        # 열린 페이지 소스를 받아옴
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 검색 결과 가져오기
        # div 태그 안의 id 가 result-stats 라는 요소
        result_stats = soup.select_one("div#result-stats")
        # print(result_stats.text)
        temp = result_stats.text[7:-10].replace(',','')
        return int(temp)
    
    x = []
    y = []
    
    keywords = Keyword.objects.all()
    for keyword in keywords:
        result = get_google_data(keyword.name)
        trend, is_created = Trend.objects.get_or_create(defaults={'result': result},name=keyword.name, search_period='year')
        if is_created:
            trend.result = result    
        trend.save()
        x.append(trend.name)
        y.append(trend.result)

    plt.clf()
    plt.bar(range(0, len(x)), y, label='Trends')
    plt.xticks(range(0, len(x)), x, rotation=45)
    plt.grid()
    plt.title('Technology Trend Analysis')
    plt.xlabel('keyword')
    plt.ylabel('result')
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    context = {
        'chart_image': f'data:image/png;base64,{image_base64}'
    }
    return render(request, 'trends/crawling_advanced.html', context)
