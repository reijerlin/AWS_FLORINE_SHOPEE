from django.db import models
from django.db import connections


class Data(models.Model):
    category = models.CharField(max_length = 10, 
        choices = [('A', 'A'), ('B', 'B'), ('C', 'C')])
    quantity = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now=True)

class HotSales(models.Model):
    MAIN_COMMODITY_NM = models.CharField(max_length = 200,primary_key=True)
    SUMP = models.IntegerField(default=0)
    SUMC = models.IntegerField(default=0)
    PERCENT=models.FloatField(default=0)
    class Meta:
        db_table='test'
class ACTUAL_PROFIT(models.Model):

    ORDER_ID= models.CharField(max_length = 200,primary_key=True)
    STATUS= models.CharField(max_length = 20)
    EFFDT= models.DateTimeField(auto_now=True)
    YYYYMM=models.CharField(max_length = 10)
    PRODUCT_GROSS= models.IntegerField(default=0)
    ACTUAL_PROFIT= models.IntegerField(default=0)
    class Meta:
        db_table='ACTUAL_PROFIT'
class SUM_ACTUAL_PROFIT(models.Model):

    
    SUM_ACTUAL_PROFIT= models.IntegerField(default=0,primary_key=True)
    
class COST(models.Model):

    COST= models.IntegerField(default=0,primary_key=True)

    class Meta:
        db_table='COST'

class TOTAL_ORDERS(models.Model):

    COUNT= models.IntegerField(default=0,primary_key=True)

class MONTH_REVENUE(models.Model):


    YYYYMM=models.CharField(max_length = 10,primary_key=True)
    NUMYYYYMM= models.IntegerField(default=0)
    MONTH_REVENUE= models.IntegerField(default=0)
    
    class Meta:
        db_table='MONTH_REVENUE'

class ALL_PROFIT_VW(models.Model):


    YYYYMM=models.CharField(max_length = 10,primary_key=True)
    NUMYYYYMM= models.IntegerField(default=0)
    PROFIT= models.IntegerField(default=0)
    
    class Meta:
        db_table='ALL_PROFIT_VW'

class SUM_TOTAL_PROFIT(models.Model):

    
    SUM_TOTAL_PROFIT= models.IntegerField(default=0,primary_key=True)

    