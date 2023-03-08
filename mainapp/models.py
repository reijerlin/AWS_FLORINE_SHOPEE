from django.db import models
from django.db import connections




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
    USERNAME=models.CharField(max_length = 100,primary_key=True)
    YYYYMM=models.CharField(max_length = 10)
    TAOBAO= models.IntegerField(default=0)
    SHIP= models.IntegerField(default=0)
    TAX= models.IntegerField(default=0)
    OTHER= models.IntegerField(default=0)
    COST= models.IntegerField(default=0)
    COMMENT=models.CharField(max_length = 50,default="")

    class Meta:
        db_table='COST'
    # class Meta:
    #     managed = False
    #     db_table = 'COST'

    # def __repr__(self):
    #     return f'<COST: COST object ({self.USERNAME}, {self.YYYYMM}, {self.COST})>'

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
class GETYYYYMM(models.Model):
    YYYYMM= models.IntegerField(default=0,primary_key=True)
    
    
class GETYYYYMMDD(models.Model):
    
    YYYYMMDD=models.CharField(max_length = 10,primary_key=True)

class ALLORDERS(models.Model):
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
        db_table='ALLORDERS'

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
    ARGENT= models.BooleanField(default=False)
    CALLITEM= models.BooleanField(default=False)
    SHIPTAOBAO= models.BooleanField(default=False)

    class Meta:
        db_table='TODO'
 
   