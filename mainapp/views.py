from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
# from mainapp.forms import DataForm
from mainapp.models import HotSales
from mainapp.models import SUM_ACTUAL_PROFIT
from mainapp.models import COST
from mainapp.models import TOTAL_ORDERS
from mainapp.models import MONTH_REVENUE
from mainapp.models import ALL_PROFIT_VW
from mainapp.models import SUM_TOTAL_PROFIT
from django.shortcuts import render

# Create your views here.
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db import connection

import mysql.connector
import pandas as pd
import xlrd
import csv
import re
import sys
import csv
import requests
import random
import time
import os
import datetime
import json
from datetime import date
from subprocess import run,PIPE
#@login_required(login_url="/login/")
def index(request):

    abc = date.today() 
    THISYYYYMM=str(abc.year)+'-'+str(abc.month)
    THISYYYY=str(abc.year)
    LASTYYY=str(abc.year-1)
    month, year = (abc.month-1, abc.year) if abc.month != 1 else (12, abc.year-1)
    month2, year2 = (abc.month-2, abc.year) if abc.month != 1 else (12, abc.year-1)
    pre_month = abc.replace(day=1, month=month, year=year)
    pre2_month = abc.replace(day=1, month=month2, year=year2)
    pre_month=str(pre_month)[0:7]
    pre2_month=str(pre2_month)[0:7]
    #GET HOTSALES
    #resultdisplay=HotSales.objects.all()
    HOTSALESSQLstr=  "select D.MAIN_COMMODITY_NM,D.SUMP,D.SUMC,(SUMC-SUMP)/SUMP*100 as PERCENT FROM (select AA.MAIN_COMMODITY_NM,IFNULL(BB.SUMP,0) as SUMP,AA.SUMC FROM (select  A.MAIN_COMMODITY_NM as MAIN_COMMODITY_NM,SUM(A.COUNT) as SUMC  FROM ORDERS A where SUBSTRING(CAST(A.EFFDT AS char),1,7)="
    HOTSALESSQLstr+="'"+pre_month+"'" 
    HOTSALESSQLstr+="and A.STATUS='完成' group by A.MAIN_COMMODITY_NM order by SUM(A.COUNT) desc LIMIT 5) AA left join (select  B.MAIN_COMMODITY_NM as MAIN_COMMODITY_NM,SUM(B.COUNT) as SUMP  FROM ORDERS B where SUBSTRING(CAST(B.EFFDT AS char),1,7)="
    HOTSALESSQLstr+="'"+pre2_month+"'" 
    HOTSALESSQLstr+="and B.STATUS='完成' group by B.MAIN_COMMODITY_NM) BB on AA.MAIN_COMMODITY_NM=BB.MAIN_COMMODITY_NM) D"
    resultdisplay=HotSales.objects.raw(HOTSALESSQLstr)
    #GET PROFIT and Margin 
    RevenueSQLstr="select SUM(ACTUAL_PROFIT) as SUM_ACTUAL_PROFIT from ACTUAL_PROFIT where YYYYMM="
    preRevenueSQLstr=RevenueSQLstr+"'"+pre_month+"'" 
    pre2RevenueSQLstr=RevenueSQLstr+"'"+pre2_month+"'" 
    preRevenue = SUM_ACTUAL_PROFIT.objects.raw(preRevenueSQLstr)[0]
    pre2Revenue = SUM_ACTUAL_PROFIT.objects.raw(pre2RevenueSQLstr)[0]
    CostSQLstr="select COST from COST where YYYYMM="
    preCostSQLstr=CostSQLstr+"'"+pre_month+"'" 
    pre2CostSQLstr=CostSQLstr+"'"+pre2_month+"'" 
    preCost = COST.objects.raw(preCostSQLstr)[0]
    pre2Cost = COST.objects.raw(pre2CostSQLstr)[0]
    prePROFIT=int(preRevenue.SUM_ACTUAL_PROFIT-preCost.COST)
    pre2PROFIT=int(pre2Revenue.SUM_ACTUAL_PROFIT-pre2Cost.COST)
    MomProfit=int((prePROFIT-pre2PROFIT)/pre2PROFIT*100)
    
    preMargin=round(prePROFIT/preRevenue.SUM_ACTUAL_PROFIT*100,2)
    pre2Margin=round(pre2PROFIT/pre2Revenue.SUM_ACTUAL_PROFIT*100,2)
    MomMargin=round(preMargin-pre2Margin,2)

    #GET Total Orders
    TotalOrdersSQLstr="select COUNT(1) as COUNT from ACTUAL_PROFIT where YYYYMM="
    preTotalOrdersSQLstr=TotalOrdersSQLstr+"'"+pre_month+"'" 
    pre2TotalOrdersSQLstr=TotalOrdersSQLstr+"'"+pre2_month+"'" 
    preTotalOrders = TOTAL_ORDERS.objects.raw(preTotalOrdersSQLstr)[0].COUNT
    pre2TotalOrders = TOTAL_ORDERS.objects.raw(pre2TotalOrdersSQLstr)[0].COUNT
    DiffTotalOrders=preTotalOrders-pre2TotalOrders

    #GET REVENUE
    REVENUESQLstr="select YYYYMM,NUMYYYYMM,MONTH_REVENUE from MONTH_REVENUE where YYYYMM="
    thisREVENUESQLstr=REVENUESQLstr+"'"+THISYYYYMM+"'" 
    thisREVENUE = MONTH_REVENUE.objects.raw(thisREVENUESQLstr)
    if len(list(thisREVENUE))==0:
        thisREVENUEresult=0
    else:
        thisREVENUEresult=int(thisREVENUE[0].MONTH_REVENUE)

    #GET CHART DATA1

 
    numTHISYYYYMM=abc.year*100+abc.month  
    numSixBFYYYYMM=  numTHISYYYYMM-6
    chartREVENUESQLstr="select YYYYMM,NUMYYYYMM,MONTH_REVENUE from MONTH_REVENUE where NUMYYYYMM>="
    SixBFREVENUESQLstr=chartREVENUESQLstr+str(numSixBFYYYYMM) 
    Chart1Result = MONTH_REVENUE.objects.raw(SixBFREVENUESQLstr)

    Chart1Label=[]
    Chart1Data=[]
    Chart2Label=[]
    Month_dict={'01':'JAN','02': 'FEB' ,'03':'MAR' ,'04':'APR' ,'05':'MAY' ,'06':'JUN' ,'07':'JUL','08': 'AUG' ,'09':'SEP','10': 'OCT','11': 'NOV' ,'12':'DEC'}
    for row in Chart1Result:
        YY=row.YYYYMM[2:4]
        MM=row.YYYYMM[5:]
        MN=row.YYYYMM[2:4]+"'"+Month_dict[MM]
        Chart2Label.append(Month_dict[MM])
        Chart1Label.append(MN)
        Chart1Data.append(row.MONTH_REVENUE)

    #GET CHART DATA2

    numLASTYYYYMM=(abc.year-1)*100+abc.month  
    numLASTSixBFYYYYMM=  numLASTYYYYMM-6
    chart2PROFITSQLstr="select YYYYMM,NUMYYYYMM,PROFIT from ALL_PROFIT_VW where NUMYYYYMM>="


    ThisSixBFPROFITSQLstr=chart2PROFITSQLstr+str(numSixBFYYYYMM)
    LastSixBFPROFITSQLstr=chart2PROFITSQLstr+str(numLASTSixBFYYYYMM) +" and NUMYYYYMM<"+str(numLASTYYYYMM)
    Chart2Result_This = ALL_PROFIT_VW.objects.raw(ThisSixBFPROFITSQLstr)
    Chart2Result_Last = ALL_PROFIT_VW.objects.raw(LastSixBFPROFITSQLstr)


    Chart2Data_This=[]
    Chart2Data_Last=[]

    for row in Chart2Result_This:
        Chart2Data_This.append(row.PROFIT)
    for row in Chart2Result_Last:
        Chart2Data_Last.append(row.PROFIT)

    #GET Profit of The YEAR
    numpre_month=abc.year*100+int(month)
    numlastY_pre_month=(abc.year-1)*100+int(month)
    numpre_month_start=abc.year*100+1
    numlastY_pre_month_start=(abc.year-1)*100+1
    
    ThisTotalPROFITSQLstr="select SUM(PROFIT) as SUM_TOTAL_PROFIT from ALL_PROFIT_VW where NUMYYYYMM>="
    ThisTotalPROFITSQLstr=ThisTotalPROFITSQLstr+str(numpre_month_start)+" and NUMYYYYMM<="+str(numpre_month)
    TotalPROFIT_This = SUM_TOTAL_PROFIT.objects.raw(ThisTotalPROFITSQLstr)[0]
    TotalPROFIT_This_val=int(TotalPROFIT_This.SUM_TOTAL_PROFIT)

    LastTotalPROFITSQLstr="select SUM(PROFIT) as SUM_TOTAL_PROFIT from ALL_PROFIT_VW where NUMYYYYMM>="
    LastTotalPROFITSQLstr=LastTotalPROFITSQLstr+str(numlastY_pre_month_start)+" and NUMYYYYMM<="+str(numlastY_pre_month)
    TotalPROFIT_Last = SUM_TOTAL_PROFIT.objects.raw(LastTotalPROFITSQLstr)[0]
    TotalPROFIT_Last_val=int(TotalPROFIT_Last.SUM_TOTAL_PROFIT)
    YOY_TotalPROFIT=round((TotalPROFIT_This_val-TotalPROFIT_Last_val)/TotalPROFIT_Last_val*100,2)


    context = {'segment': 'index','HotSales':resultdisplay,'Title_Pre':pre2_month,'Title_Cur':pre_month,
    'Profit_Cur':prePROFIT,'Profit_Mom':MomProfit,
    'Margin_Cur':preMargin,'Margin_Mom':MomMargin,
    'Total_Orders_Cur':preTotalOrders,'Total_Orders_Dif':DiffTotalOrders,
    'REVENUE_this':thisREVENUEresult,'Chart1Label':Chart1Label,'Chart1Data':Chart1Data,
    'THISYYYY':THISYYYY,'LASTYYY':LASTYYY,
    'Chart2Label':Chart2Label,'Chart2Data_This':Chart2Data_This,'Chart2Data_Last':Chart2Data_Last,
    'TotalPROFIT_This_val':TotalPROFIT_This_val,'YOY_TotalPROFIT':YOY_TotalPROFIT}
    
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))
    #return render(request,'home/dashboard.html',{'HotSales':resultdisplay})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



   

@login_required(login_url="/login/")
def simple_upload(request):
    
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
       
        CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   
        XLSX_DIR=os.path.join(CORE_DIR, "media") 
        xlsx_file_name=filename       
        xlsx_file=os.path.join(XLSX_DIR, xlsx_file_name) 
      
        
        count=0
        rows=[]
        mydb = mysql.connector.connect(
        host="ec2-54-64-213-252.ap-northeast-1.compute.amazonaws.com",
        user="Eric",
        password="1qaz@WSX",
        database="DEV"
        )
        mycursor = mydb.cursor()
        
        data = xlrd.open_workbook(xlsx_file).sheet_by_index(0)
        

        for r in range(data.nrows):
            if r==0:
                continue
            else:     
                temp=[]
                for i in range(0,len(data.row_values(r))):
                    
                    text=data.cell(rowx=r,colx=i).value
                    text=str(text)
                    
                    if (i==43 or i==45 or i==46 or i==47) and len(text)!=16:
                        text=NULL
                    temp.append(text)
                    
        
                rows.append(temp)   
                count+=1
        sql = "INSERT INTO ORDERS (ORDER_ID,STATUS,FAIL_REASON,RETURN_STATUS,CUSTOMER_ID,EFFDT,PRODUCT_GROSS,CUSTOMER_SHIP_FEE,SHOPEE_SHIP_FEE,RETURN_SHIP_FEE,TOTAL_PAID,SHOPEE_SUBSIDY,SHOPEE_REDEEM,CREDIT_DISCOUNT,DISCOUNT_CODE,CUSTOMER_COUPON,CUSTOMER_GIVEBACK,SHOPEE_COUPON,TRANSCATION_FEE,SERVICE_FEE,CASHFLOW_FEE,INSTALLMENTS,CREDIT_CHARGE,MAIN_COMMODITY_NM,SUB_COMMODITY_NM,ORG_PRICE,DIS_PRICE,MAIN_COMMODITY_ID,SUB_COMMODITY_ID,COUNT,PROMOTION_METRIC,SHOPEE_PROMOTION,RECIPIENT_ADDR,RECIPIENT_PHONE,PICKUP_STORE_ID,CITY,DISTRICT,POSTAL,RECIPIENT_NAME,SHIPPING_TYPE,DELIVER_TYPE,PREPARE_TIME,PAYMENT_TYPE,LAST_SHIP_TIME,SHIIPPING_CODE,CUSTOMER_PAID_TIME,ACTUAL_SHIP_TIME,ORDER_COMPLETE_TIME,CUSTOMER_COMMENT,COMMENT) VALUES (%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s)"
        val = rows
        mycursor.executemany(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        os.remove(xlsx_file)
        
 
        
        return render(request, 'home/simple_upload.html', {
            'uploaded_file_url': 'home/orders.html',
            'count':count
        })
        
    return render(request, 'home/simple_upload.html')



#@login_required(login_url="/login/")
# def button_call(request):
    
#     emoji_pattern = re.compile("["
#                             u"\u2728"
#                             u"\uff5e"
#                             u"\u2763"
#                             u"\ufe0f"
#                             u"\U0001f9f6"
#                             u"\u2661"
#                             u"\U0001f49e"
#                             u"\U0001f60d"
#                             u"\u2764"
#                             u"\U0001f499"
#                             u"\U0001f497"
#                             u"\U0001f970"
#                             u"\U0001f90e"
#                             u"\U0001f90d"
#                             u"\U0001f496"
#                             u"\U0001f929"
#                             u"\U0001f97a"
#                             u"\u9834"
#                             u"\U0001f495"
#                             u"\U0001f493"
#                             u"\U0001f64f"
#                             u"\U0001f3fb"
#                             u"\u51c3"
#                             u"\u5afa"
#                             u"\U0001f49d"
#                             u"\U0001f4e6"
#                             u"\u4f03"
#                             "]+", flags=re.UNICODE)
   

    
#     CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   
#     XLSX_DIR=os.path.join(CORE_DIR, "xlsx") 
#     xlsx_file_name="Order.all.20220701_20220731.xlsx"
#     csv_file_name=xlsx_file_name[:-5]+'.csv'
#     xlsx_file=os.path.join(XLSX_DIR, xlsx_file_name) 
#     csv_file=os.path.join(XLSX_DIR, csv_file_name) 
#     with open(csv_file,'w', newline = "", encoding="big5") as f:
    
#         ob = csv.writer(f)
#         data = xlrd.open_workbook(xlsx_file).sheet_by_index(0)


#         for r in range(data.nrows):
#             if r==0:
#                 HEADER=['ORDER_ID','STATUS','FAIL_REASON','RETURN_STATUS','CUSTOMER_ID','EFFDT','PRODUCT_GROSS','CUSTOMER_SHIP_FEE','SHOPEE_SHIP_FEE','RETURN_SHIP_FEE','TOTAL_PAID','SHOPEE_SUBSIDY','SHOPEE_REDEEM','CREDIT_DISCOUNT','DISCOUNT_CODE','CUSTOMER_COUPON','CUSTOMER_GIVEBACK','SHOPEE_COUPON','TRANSCATION_FEE','SERVICE_FEE','CASHFLOW_FEE','INSTALLMENTS','CREDIT_CHARGE','MAIN_COMMODITY_NM','SUB_COMMODITY_NM','ORG_PRICE','DIS_PRICE','MAIN_COMMODITY_ID','SUB_COMMODITY_ID','COUNT','PROMOTION_METRIC','SHOPEE_PROMOTION','RECIPIENT_ADDR','RECIPIENT_PHONE','PICKUP_STORE_ID','CITY','DISTRICT','POSTAL','RECIPIENT_NAME','SHIPPING_TYPE','DELIVER_TYPE','PREPARE_TIME','PAYMENT_TYPE','LAST_SHIP_TIME','SHIIPPING_CODE','CUSTOMER_PAID_TIME','ACTUAL_SHIP_TIME','ORDER_COMPLETE_TIME','CUSTOMER_COMMENT','COMMENT']
#                 ob.writerow(HEADER)
#             else:     
#                 temp=[]
#                 for i in range(0,len(data.row_values(r))):

#                     text=data.cell(rowx=r,colx=i).value
#                     text=str(text)
#                     text= emoji_pattern.sub(r'', text)
#                     temp.append(text)
#                 ob.writerow(temp)   
    
#     #print("Hello World!")
#     #context = {'segment': 'index'}

#     #html_template = loader.get_template('home/dashboard.html')
#     #return HttpResponse(html_template.render(context, request))
#     #out=run(sys.executable,['D:\\Eric\\AWS\\AWS_FLORINE\\AWS_FLORINE_DJ\\apps\home\\function.py'],shell=False,stdout=PIPE)
#     #out="HI"
#     #print(out)

#     return render(request,'home/dashboard.html')

"""
def index(request):
    form = DataForm()
    queryset = models.Data.objects.all()
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'title': 'Simple App', 'form': form, 'posts': queryset}
    return render(request, 'mainapp/index.html', context=context)


from openpyxl import Workbook
from django.http import HttpResponse
from openpyxl.styles import Font

def export_data(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Data.xlsx"'

    # create workbook
    wb = Workbook()
    sheet = wb.active

    # stylize header row
    # 'id','title', 'quantity','pub_date'
      
    c1 = sheet.cell(row = 1, column = 1) 
    c1.value = "id"
    c1.font = Font(bold=True)
    
    c2 = sheet.cell(row= 1 , column = 2) 
    c2.value = "title"
    c2.font = Font(bold=True)

    c3 = sheet.cell(row= 1 , column = 3) 
    c3.value = "quantity"
    c3.font = Font(bold=True)

    c4 = sheet.cell(row= 1 , column = 4) 
    c4.value = "pub_date"
    c4.font = Font(bold=True)
    
    # export data to Excel
    rows = models.Data.objects.all().values_list('id','category', 'quantity','pub_date',)
    for row_num, row in enumerate(rows, 1):
        # row is just a tuple
        for col_num, value in enumerate(row):
            c5 = sheet.cell(row=row_num+1, column=col_num+1) 
            c5.value = value

    wb.save(response)

    return response
"""