from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Runoff_Visualization import models
import json
from django.db.models import Avg, Sum, Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


# Create your views here.
def reg(request):
    res = models.hhrawInfo.objects.filter(date='2001-06-22').values('date', 'runoff', 'precipitation', 'evaporation',
                                                                    'temperature')
    return HttpResponse(res)


def left_1(request):
    result = models.hhrawInfo.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').order_by('month').annotate(
        avg_precipitation=Sum('precipitation') / 16,
        avg_evaporation=Sum('evaporation') / 16,
        avg_temperature=Avg('temperature')
    )

    p_list = []
    e_list = []
    t_list = []
    for i in result:
        p_list.append(int(i['avg_precipitation']))
        e_list.append(int(i['avg_evaporation']))
        t_list.append(int(i['avg_temperature']))
    data = {'p_list': p_list, 'e_list': e_list, 't_list': t_list}

    return HttpResponse(json.dumps(data), content_type='application/json')  # 返回JSON格式的数据，其中data字段存储转化后的列表数据


def left_2(request):
    # 获取大于2200的年份列表
    year = ExtractYear('date')
    result = models.hhrawInfo.objects.annotate(name=ExtractYear('date')).values('name').filter(
        runoff__gt=1000).annotate(
        value=Count('date'))
    # return JsonResponse([result])
    return HttpResponse(json.dumps(list(result)), content_type='application/json')


from datetime import date


def date_handler(obj):
    return obj.isoformat() if isinstance(obj, date) else None


def right_1(request):
    runoff_list = []
    date_list = []
    all_value = models.hhrawInfo.objects.all().values('date', 'runoff')

    for i in list(all_value):
        runoff_list.append(i['runoff'])
        date_list.append(i['date'])
    data = [runoff_list, date_list]
    return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')


def left_3(request):
    runoff_list = []
    date_list = []
    p_list = []
    all_value = models.hhrawInfo.objects.all().values('date', 'runoff', 'precipitation')

    for i in list(all_value):
        runoff_list.append(i['runoff'])
        date_list.append(i['date'])
        p_list.append(i['precipitation'])
    data = [runoff_list, date_list, p_list]
    return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')


def right_3(request):
    data = models.hhrawInfo.objects.annotate(year=ExtractYear('date')).values('year').filter(
        evaporation__gt=8).annotate(value=Count('date')).order_by('year')
    data = list(data)
    e_list = []
    year_list = []
    for i in data:
        e_list.append(i['value'])
        year_list.append(i['year'])
    data = [e_list, year_list]
    return HttpResponse(json.dumps(data), content_type='application/json')


class weatherAPI(APIView):
    def get(self, request):
        date_list = []
        low_list = []
        high_list = []
        key = "1888c42a580fb5345dd1305bb40ff78c"
        url = "https://restapi.amap.com/v3/weather/weatherInfo?city=110101&key=1888c42a580fb5345dd1305bb40ff78c&extensions=all&output=json"
        response = requests.get(url)
        data = response.json()
        for i in data['forecasts'][0]['casts']:
            date_list.append(i['date'])
            low_list.append(i['nighttemp'])
            high_list.append(i['daytemp'])

        data = [date_list, low_list, high_list]
        return HttpResponse(json.dumps(data), content_type='application/json')
