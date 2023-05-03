from django.db import models

# Create your models here.

class hhrawInfo(models.Model):
    date = models.DateField(primary_key=True,verbose_name='日期')
    runoff = models.FloatField(null=False,verbose_name='径流量')
    precipitation = models.FloatField(null=False,verbose_name='降雨量')
    evaporation = models.FloatField(null=False,verbose_name='蒸发量')
    temperature = models.FloatField(null=False,verbose_name='温度')