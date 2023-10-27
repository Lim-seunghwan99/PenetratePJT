from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from rest_framework import status


# Create your views here.
@api_view(['GET'])
def index(request):
    api_key = settings.API_KEY
    # 외부에 노출되지 않도록 내 pc에만 관리하는 변수 : 환경 변수
    # url = "정기예금 API"
    
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()

    return Response(response)


BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
API_KEY = settings.API_KEY

@api_view(['GET'])
def index(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo' : 1
    }
    response = requests.get(URL, params=params).json()['result']
    return Response({'response' : response})

@api_view(['GET'])
def save_deposit_products(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo' : 1
    }
    response = requests.get(URL, params=params).json()['result']

    # baseList
    for item in response.get('baseList'):
        save_data = {
            'fin_prdt_cd': item.get('fin_prdt_cd'),
            'kor_co_nm': item.get('kor_co_nm'),
            'fin_prdt_nm': item.get('fin_prdt_nm'),
            'etc_note': item.get('etc_note'),
            'join_deny': item.get('join_deny'),
            'join_member': item.get('join_member'),
            'join_way': item.get('join_way'),
            'spcl_cnd': item.get('spcl_cnd'),
        }
        serializer = DepositProductsSerializer(data = save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # optionList
    for item in response.get('optionList'):
        save_data = {
            'fin_prdt_cd': item.get('fin_prdt_cd'),
            'intr_rate_type_nm': item.get('intr_rate_type_nm'),
            'intr_rate': item.get('intr_rate'),
            'intr_rate2': item.get('intr_rate2'),
            'save_trm': item.get('save_trm'),
        }
        for elem in save_data:
            if not save_data[elem]:
                save_data[elem] = -1

        serializer = DepositOptionsSerializer(data = save_data)
        product =  DepositProducts.objects.get(fin_prdt_cd = save_data['fin_prdt_cd'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)

    return Response({'response' : response})



@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = {
            "message" : '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'
        }
        return Response(message, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    # 특정 상품의 옵션 리스트 반환
    # D : 옵션 리스트 출력 B의 상품리스트의 가장 첫번째
    fin_prdt_cd = DepositOptions.objects.filter(fin_prdt_cd = fin_prdt_cd)
    serializer = DepositOptionsSerializer(fin_prdt_cd, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_rate(request):
    option = DepositOptions.objects.all().order_by('intr_rate2')[0]
    prdt = DepositProducts.objects.get(pk=option.product.pk)
    options = DepositOptions.objects.filter(product=prdt.pk)
    serializer = DepositOptionsSerializer(options, many=True)
    serializer1 = DepositProductsSerializer(prdt)
    d = {}
    d['deposit_product'] = serializer1.data
    d['options'] = serializer.data
    return Response(d, status=status.HTTP_200_OK)
    



