from django.db import models
from django.db import connections
import datetime
from django import forms
class ORDERS(models.Model):
    USERNAME=models.CharField(max_length = 100)
    ORDER_ID=models.CharField(max_length = 200)
    STATUS=models.CharField(max_length = 20)
    FAIL_REASON=models.CharField(max_length = 100)
    RETURN_STATUS=models.CharField(max_length = 10)
    CUSTOMER_ID=models.CharField(max_length = 50)
    EFFDT=models.DateTimeField(auto_now=True)
    PRODUCT_GROSS=models.FloatField(default=0)
    CUSTOMER_SHIP_FEE=models.FloatField(default=0)
    SHOPEE_SHIP_FEE=models.FloatField(default=0)
    RETURN_SHIP_FEE=models.FloatField(default=0)
    TOTAL_PAID=models.FloatField(default=0)
    SHOPEE_SUBSIDY=models.FloatField(default=0)
    SHOPEE_REDEEM=models.FloatField(default=0)
    CREDIT_DISCOUNT=models.FloatField(default=0)
    DISCOUNT_CODE=models.CharField(max_length = 50)
    CUSTOMER_COUPON=models.FloatField(default=0)
    CUSTOMER_GIVEBACK=models.FloatField(default=0)
    SHOPEE_COUPON=models.FloatField(default=0)
    TRANSCATION_FEE=models.FloatField(default=0)
    SERVICE_FEE=models.FloatField(default=0)
    CASHFLOW_FEE=models.FloatField(default=0)
    INSTALLMENTS=models.IntegerField(default=0)
    CREDIT_CHARGE=models.CharField(max_length = 20)
    MAIN_COMMODITY_NM=models.CharField(max_length = 100)
    SUB_COMMODITY_NM=models.CharField(max_length = 100)
    ORG_PRICE=models.FloatField(default=0)
    DIS_PRICE=models.FloatField(default=0)
    MAIN_COMMODITY_ID=models.CharField(max_length = 50)
    SUB_COMMODITY_ID=models.CharField(max_length = 50)
    COUNT=models.IntegerField(default=0)
    PROMOTION_METRIC=models.CharField(max_length = 10)
    SHOPEE_PROMOTION=models.CharField(max_length = 50)
    RECIPIENT_ADDR=models.CharField(max_length = 100)
    RECIPIENT_PHONE=models.CharField(max_length = 20)
    PICKUP_STORE_ID=models.CharField(max_length = 20)
    CITY=models.CharField(max_length = 50)
    DISTRICT=models.CharField(max_length = 50)
    POSTAL=models.CharField(max_length = 10)
    RECIPIENT_NAME=models.CharField(max_length = 50)
    SHIPPING_TYPE=models.CharField(max_length = 20)
    DELIVER_TYPE=models.CharField(max_length = 20)
    PREPARE_TIME=models.CharField(max_length = 100)
    PAYMENT_TYPE=models.CharField(max_length = 20)
    LAST_SHIP_TIME=models.DateTimeField(auto_now=True)
    SHIIPPING_CODE=models.CharField(max_length = 30)
    CUSTOMER_PAID_TIME=models.DateTimeField(auto_now=True)
    ACTUAL_SHIP_TIME=models.DateTimeField(auto_now=True)
    ORDER_COMPLETE_TIME=models.DateTimeField(auto_now=True)
    CUSTOMER_COMMENT=models.TextField ()
    COMMENT=models.TextField()
    class Meta:
        db_table='orders'
        unique_together = (('USERNAME','ORDER_ID', 'STATUS', 'FAIL_REASON', 'RETURN_STATUS', 'CUSTOMER_ID', 'EFFDT', 'MAIN_COMMODITY_NM', 'SUB_COMMODITY_NM' ))

class COST_DETAIL(models.Model):
    TAOBAO = 1
    SHIPPING = 2
    TAX = 3
    OTHERS=4
    COST_TYPE = (
        (TAOBAO, 'TAOBAO'),
        (SHIPPING, 'SHIPPING'),
        (TAX, 'TAX'),
        (OTHERS, 'OTHERS'),
    )
    USERNAME = models.CharField(max_length=50)
    YYYYMM = models.CharField(max_length=10)
    COST_TYPE = models.PositiveSmallIntegerField(choices=COST_TYPE)
    EFFDT = models.DateField(null=True)
    AMOUNT = models.IntegerField(null=True)
    ADDDATETIME = models.DateField( auto_now=True)
    COMMENT= models.CharField(max_length=200,blank=True)
    class meta:
        managed = True
        db_table='cost_detail'


class COST_SUM(models.Model):
    USERNAME=models.CharField(max_length = 100,primary_key=True)
    YYYYMM=models.CharField(max_length = 10)
    TAOBAO= models.IntegerField(default=0)
    SHIP= models.IntegerField(default=0)
    TAX= models.IntegerField(default=0)
    OTHER= models.IntegerField(default=0)
    COST= models.IntegerField(default=0)
   
    class Meta:
        managed = False
        db_table='cost_sum'

class HotSales(models.Model):
    MAIN_COMMODITY_NM = models.CharField(max_length = 200,primary_key=True)
    SUMP = models.IntegerField(default=0)
    SUMC = models.IntegerField(default=0)
    PERCENT=models.FloatField(default=0)
    class Meta:
        managed = False

class ACTUAL_PROFIT(models.Model):
    USERNAME=models.CharField(max_length = 100,primary_key=True)
    ORDER_ID= models.CharField(max_length = 200)
    STATUS= models.CharField(max_length = 20)
    EFFDT= models.DateTimeField(auto_now=True)
    YYYYMM=models.CharField(max_length = 10)
    PRODUCT_GROSS= models.IntegerField(default=0)
    ACTUAL_PROFIT= models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table='actual_profit'

class MONTH_REVENUE(models.Model):

    USERNAME=models.CharField(max_length = 100,primary_key=True)
    YYYYMM=models.CharField(max_length = 10)
    NUMYYYYMM= models.IntegerField(default=0)
    MONTH_REVENUE= models.IntegerField(default=0)
    
    class Meta:
        managed = False
        db_table='month_revenue'

class ALL_PROFIT_VW(models.Model):

    USERNAME=models.CharField(max_length = 100,primary_key=True)
    YYYYMM=models.CharField(max_length = 10)
    NUMYYYYMM= models.IntegerField(default=0)
    COST= models.IntegerField(default=0)
    MONTH_REVENUE= models.IntegerField(default=0)
    PROFIT= models.IntegerField(default=0)
    
    class Meta:
        managed = False
        db_table='all_profit_vw'

class GETYYYYMM(models.Model):
    YYYYMM= models.IntegerField(default=0,primary_key=True)
    class Meta:
        managed = False
    
class GETYYYYMMDD(models.Model):
       
    YYYYMMDD=models.CharField(max_length = 10,primary_key=True)
    class Meta:
        managed = False

class ALLORDERS(models.Model):
    USERNAME=models.CharField(max_length = 100)
    ORDER_ID= models.CharField(max_length = 200,primary_key=True)
    EFFDT= models.DateTimeField(auto_now=True)
    STATUS= models.CharField(max_length = 20)
    MAIN_COMMODITY_NM= models.CharField(max_length = 512)
    SUB_COMMODITY_NM= models.CharField(max_length = 512)
    SHIIPPING_CODE=models.CharField(max_length = 30)
    SHIPPING_TYPE= models.CharField(max_length = 20)
    RECIPIENT_NAME= models.CharField(max_length = 20)
    PRODUCT_GROSS= models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table='allorders'

class TODO(models.Model):
    USERNAME=models.CharField(max_length = 100)
    ORDER_ID= models.CharField(max_length = 200,primary_key=True)
    EFFDT= models.DateTimeField(auto_now=True)
    STATUS= models.CharField(max_length = 20)
    MAIN_COMMODITY_NM= models.CharField(max_length = 512)
    SUB_COMMODITY_NM= models.CharField(max_length = 512)
    SHIIPPING_CODE=models.CharField(max_length = 30)
    SHIPPING_TYPE= models.CharField(max_length = 20)
    RECIPIENT_NAME= models.CharField(max_length = 20)
    PRODUCT_GROSS= models.IntegerField(default=0)
    CALLITEM= models.BooleanField(default=False)
    SHIPTAOBAO= models.BooleanField(default=False)
    ITEMARRIVED= models.BooleanField(default=False)
    DONE= models.BooleanField(default=False)
    COMMENT= models.CharField(max_length = 20)
    class Meta:
        managed = True
        db_table='todo'




   

 
   
