#from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
# from mainapp.forms import DataForm
from mainapp.models import HotSales
from mainapp.models import ACTUAL_PROFIT

from mainapp.models import COST_SUM
from mainapp.models import COST_DETAIL

from mainapp.models import MONTH_REVENUE
from mainapp.models import ALL_PROFIT_VW

from mainapp.models import GETYYYYMM
from mainapp.models import GETYYYYMMDD
from mainapp.models import ALLORDERS
from mainapp.models import TODO
from django.shortcuts import render

from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.
from django.db.models import Sum
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator,EmptyPage
from django.db import connection
# Create your views here.
from mainapp.serializers import ALLORDERSSerializer
from rest_framework import viewsets

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
from dateutil import relativedelta
from subprocess import run,PIPE

from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.views import generic
from .forms import (
    BookModelForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    #BookFilterForm
)


global mydb 
mydb = mysql.connector.connect(
            host="54.150.254.70",
            user="Eric",
            password="1qaz@WSX",
            database="dev"
            )
# Create your views here.
class ALLORDERSViewSet(viewsets.ModelViewSet):
    queryset = ALLORDERS.objects.all()
    serializer_class = ALLORDERSSerializer

@login_required(redirect_field_name=None,login_url="/login/")
def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        if username=='Demo':
            username='florine__20'
            
    ORDERMNMAXSQLstr="select substring(MAX(EFFDT),1,4)*100+substring(MAX(EFFDT),6,2) as YYYYMM from orders Where USERNAME='"+username+"'"
    COSTMNMAXSQLstr="select substring(MAX(YYYYMM),1,4)*100+substring(MAX(YYYYMM),6,2) as YYYYMM from COST_SUM Where USERNAME='"+username+"'"
    
    ORDERMNMAX=GETYYYYMM.objects.raw(ORDERMNMAXSQLstr)[0].YYYYMM
    COSTMNMAX=GETYYYYMM.objects.raw(COSTMNMAXSQLstr)[0].YYYYMM
    YYYYMM=min(ORDERMNMAX,COSTMNMAX)
    MM=int(YYYYMM%100)
    YYYY=int((YYYYMM-MM)/100)
    
    Today = date.today() 
    if len(str(Today.month))==2:
        Todayyyymm=str(Today.year)+'-'+str(Today.month)
    else:
        Todayyyymm=str(Today.year)+'-0'+str(Today.month)
    
    
    abc = datetime.date(YYYY, MM, 1)
   
    #abc = datetime.date(2022, 10, 31)
    if len(str(abc.month))==2:
        THISYYYYMM=str(abc.year)+'-'+str(abc.month)
    else:
        THISYYYYMM=str(abc.year)+'-0'+str(abc.month)
    THISYYYY=str(abc.year)
    LASTYYYY=str(abc.year-1)
    month, year = (abc.month, abc.year) if abc.month != 1 else (12, abc.year-1)
    month2, year2 = (abc.month-1, abc.year) if abc.month != 1 else (12, abc.year-1)
    
    pre_month = abc.replace(day=1, month=month, year=year)
    pre2_month = abc.replace(day=1, month=month2, year=year2)
    
    pre_month=str(pre_month)[0:7]
    pre2_month=str(pre2_month)[0:7]
    #GET HOTSALES
    #resultdisplay=HotSales.objects.all()
    HOTSALESSQLstr=  "select D.MAIN_COMMODITY_NM,D.SUMP,D.SUMC,(SUMC-SUMP)/SUMP*100 as PERCENT FROM (select AA.MAIN_COMMODITY_NM,IFNULL(BB.SUMP,0) as SUMP,AA.SUMC FROM (select  A.MAIN_COMMODITY_NM as MAIN_COMMODITY_NM,SUM(A.COUNT) as SUMC  FROM ORDERS A where SUBSTRING(CAST(A.EFFDT AS char),1,7)="
    HOTSALESSQLstr+="'"+pre_month+"'" 
    HOTSALESSQLstr+="and A.STATUS<>'不成立' and USERNAME='"+username+"' group by A.MAIN_COMMODITY_NM order by SUM(A.COUNT) desc LIMIT 5) AA left join (select  B.MAIN_COMMODITY_NM as MAIN_COMMODITY_NM,SUM(B.COUNT) as SUMP  FROM ORDERS B where SUBSTRING(CAST(B.EFFDT AS char),1,7)="
    HOTSALESSQLstr+="'"+pre2_month+"'" 
    HOTSALESSQLstr+="and B.STATUS<>'不成立' and USERNAME='"+username+"' group by B.MAIN_COMMODITY_NM) BB on AA.MAIN_COMMODITY_NM=BB.MAIN_COMMODITY_NM) D"
    
    resultdisplay=HotSales.objects.raw(HOTSALESSQLstr)
    #GET PROFIT and Margin 
    preRevenue= ACTUAL_PROFIT.objects.filter(USERNAME=username,YYYYMM=pre_month).aggregate(Sum('ACTUAL_PROFIT'))['ACTUAL_PROFIT__sum']
    pre2Revenue= ACTUAL_PROFIT.objects.filter(USERNAME=username,YYYYMM=pre2_month).aggregate(Sum('ACTUAL_PROFIT'))['ACTUAL_PROFIT__sum']

    preCost= COST_SUM.objects.filter(USERNAME=username,YYYYMM=pre_month)[0].COST
    pre2Cost= COST_SUM.objects.filter(USERNAME=username,YYYYMM=pre2_month)[0].COST

    prePROFIT=int(int(preRevenue)-preCost)
    pre2PROFIT=int(int(pre2Revenue)-pre2Cost)
    MomProfit=int((prePROFIT-pre2PROFIT)/pre2PROFIT*100)
    
    preMargin=round(prePROFIT/preRevenue*100,2)
    pre2Margin=round(pre2PROFIT/pre2Revenue*100,2)
    MomMargin=round(preMargin-pre2Margin,2)


    #GET Total Orders
    preTotalOrders= ACTUAL_PROFIT.objects.filter(USERNAME=username,YYYYMM=pre_month).count()
    pre2TotalOrders= ACTUAL_PROFIT.objects.filter(USERNAME=username,YYYYMM=pre2_month).count()
    DiffTotalOrders=preTotalOrders-pre2TotalOrders
    
    #GET REVENUE
  
    thisREVENUE = MONTH_REVENUE.objects.filter(USERNAME=username,YYYYMM=THISYYYYMM)
    if thisREVENUE.count()==0:
        thisREVENUEresult=0
    else:
        thisREVENUEresult=int(thisREVENUE[0].MONTH_REVENUE)

    #GET CHART DATA1
    numTHISYYYYMM=abc.year*100+abc.month  
    if abc.month>6:
        numSixBFYYYYMM=  numTHISYYYYMM-6
    else:
        numSixBFYYYYMM=(abc.year-1)*100+abc.month-6+12
        

    Chart1Result = MONTH_REVENUE.objects.filter(USERNAME=username,NUMYYYYMM__gt=numSixBFYYYYMM,NUMYYYYMM__lte=numTHISYYYYMM)
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
    if abc.month>6:
        numLASTSixBFYYYYMM=  numLASTYYYYMM-6
    else:
       
        numLASTSixBFYYYYMM=(abc.year-2)*100+abc.month-6+12
  
    Chart2Result_This=ALL_PROFIT_VW.objects.filter(USERNAME=username,NUMYYYYMM__gt=numSixBFYYYYMM,NUMYYYYMM__lte=numTHISYYYYMM)
    Chart2Result_Last = ALL_PROFIT_VW.objects.filter(USERNAME=username,NUMYYYYMM__gt=numLASTSixBFYYYYMM,NUMYYYYMM__lte=numLASTYYYYMM)
    Chart2Data_This=[]
    Chart2Data_Last=[]
  
    for row in Chart2Result_This:
        Chart2Data_This.append(row.PROFIT)
    for row in Chart2Result_Last:
        Chart2Data_Last.append(row.PROFIT)
 
    #GET Profit of The YEAR
    numpre_month=abc.year*100+int(abc.month)
    numlastY_pre_month=(abc.year-1)*100+int(abc.month)
    numpre_month_start=abc.year*100+1
    numlastY_pre_month_start=(abc.year-1)*100+1
    
 
    TotalPROFIT_This_val=int(ALL_PROFIT_VW.objects.filter(USERNAME=username,NUMYYYYMM__gte=numpre_month_start,NUMYYYYMM__lte=numpre_month).aggregate(Sum('PROFIT'))['PROFIT__sum'])
    TotalPROFIT_Last_val=int(ALL_PROFIT_VW.objects.filter(USERNAME=username,NUMYYYYMM__gte=numlastY_pre_month_start,NUMYYYYMM__lte=numlastY_pre_month).aggregate(Sum('PROFIT'))['PROFIT__sum'])
    YOY_TotalPROFIT=round((TotalPROFIT_This_val-TotalPROFIT_Last_val)/TotalPROFIT_Last_val*100,2)


    context = {'segment': 'index','HotSales':resultdisplay,'Title_Pre':pre2_month,'Title_Cur':pre_month,
    'Profit_Cur':prePROFIT,'Profit_Mom':MomProfit,
    'Margin_Cur':preMargin,'Margin_Mom':MomMargin,
    'Total_Orders_Cur':preTotalOrders,'Total_Orders_Dif':DiffTotalOrders,
    'REVENUE_this':thisREVENUEresult,'Chart1Label':Chart1Label,'Chart1Data':Chart1Data,
    'THISYYYY':THISYYYY,'LASTYYYY':LASTYYYY,
    'Chart2Label':Chart2Label,'Chart2Data_This':Chart2Data_This,'Chart2Data_Last':Chart2Data_Last,
    'TotalPROFIT_This_val':TotalPROFIT_This_val,'YOY_TotalPROFIT':YOY_TotalPROFIT,'Todayyyymm':Todayyyymm
    }
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
    

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        """
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        """
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def orders(request):
    username = None
    demo=False
    if request.user.is_authenticated:
        username = request.user.username
        if username=='Demo':
            username='florine__20'
            demo=True

    ALLORDERSDATA=ALLORDERS.objects.filter(USERNAME=username).order_by('-EFFDT')
    for i in range(len(ALLORDERSDATA)):
        ALLORDERSDATA[i].PRODUCT_GROSS=int(ALLORDERSDATA[i].PRODUCT_GROSS)
        ALLORDERSDATA[i].EFFDT=ALLORDERSDATA[i].EFFDT.strftime('%Y-%m-%d %H:%M')
        if demo==True and len(ALLORDERSDATA[i].SHIIPPING_CODE)>0:
            ALLORDERSDATA[i].SHIIPPING_CODE='***' + ALLORDERSDATA[i].SHIIPPING_CODE[3:]
           
    p=Paginator(ALLORDERSDATA,20)
    page_num=request.GET.get('page',1)
    try:
        page=p.page(page_num)
    except EmptyPage:
        page=p.page(1)
    page=p.page(page_num)
    request.session['count'] = 0
    return render(request, 'home/orders.html',{'ALLORDERSDATA':page})

@login_required(login_url="/login/")
def pending(request):
    username = None
    demo=False
    if request.user.is_authenticated:
        username = request.user.username
        if username=='Demo':
            username='florine__20'
            demo=True
    ALLORDERSstr=  "SELECT ORDER_ID,EFFDT,STATUS,MAIN_COMMODITY_NM,SUB_COMMODITY_NM,SHIIPPING_CODE,SHIPPING_TYPE,RECIPIENT_NAME,PRODUCT_GROSS,CALLITEM,SHIPTAOBAO,ITEMARRIVED,DONE,COMMENT FROM TODO Where  STATUS='待出貨' and USERNAME='"+username+"' order by EFFDT asc"
    ALLORDERSDATA=TODO.objects.raw(ALLORDERSstr)
    for i in range(len(ALLORDERSDATA)):
        ALLORDERSDATA[i].PRODUCT_GROSS=int(ALLORDERSDATA[i].PRODUCT_GROSS)
        ALLORDERSDATA[i].EFFDT=ALLORDERSDATA[i].EFFDT.strftime('%Y-%m-%d %H:%M')
        
        if ALLORDERSDATA[i].COMMENT==None:
            ALLORDERSDATA[i].COMMENT=''
        if demo==True and len(ALLORDERSDATA[i].SHIIPPING_CODE)>0:
            ALLORDERSDATA[i].SHIIPPING_CODE='***' + ALLORDERSDATA[i].SHIIPPING_CODE[3:]
           
    # p=Paginator(ALLORDERSDATA,20)
    # page_num=request.GET.get('page',1)
    # try:
    #     page=p.page(page_num)
    # except EmptyPage:
    #     page=p.page(1)
    # page=p.page(page_num)

    if request.method == 'POST':
        
       
        call_list= request.POST.getlist('call')
        ship_list= request.POST.getlist('ship')
        arrive_list= request.POST.getlist('arrive')
        done_list= request.POST.getlist('done')
        comment_list= request.POST.getlist('comment')
      
        TODO.objects.filter(USERNAME=username).update(CALLITEM=False)
        TODO.objects.filter(USERNAME=username).update(SHIPTAOBAO=False)
        TODO.objects.filter(USERNAME=username).update(ITEMARRIVED=False)
        TODO.objects.filter(USERNAME=username).update(DONE=False)
        TODO.objects.filter(USERNAME=username).update(COMMENT='')
        #TODO.objects.filter(USERNAME=username).update(DONE=False)
        for order_id in call_list:
            TODO.objects.filter(USERNAME=username, ORDER_ID=order_id).update(CALLITEM=True)
        for order_id in ship_list:
            TODO.objects.filter(USERNAME=username, ORDER_ID=order_id).update(SHIPTAOBAO=True)
        for order_id in arrive_list:
            TODO.objects.filter(USERNAME=username, ORDER_ID=order_id).update(ITEMARRIVED=True)
        for order_id in done_list:
            # TODO.objects.filter(USERNAME=username, ORDER_ID=order_id).update(DONE=True)
            TODO.objects.filter(USERNAME=username, ORDER_ID=order_id).update(STATUS='已出貨')
        for i in range(len(comment_list)):
            TODO.objects.filter(USERNAME=username, ORDER_ID=ALLORDERSDATA[i].ORDER_ID).update(COMMENT=comment_list[i])
        redirect=1
        return render(request, 'home/pending.html',
        {'ALLORDERSDATA':ALLORDERSDATA,'redirect':redirect,'redirect_url': '/pending'}
        )
    
    return render(request, 'home/pending.html',{'ALLORDERSDATA':ALLORDERSDATA})

@login_required(login_url="/login/")
def shipping(request):
    username = None
    demo=False
    if request.user.is_authenticated:
        username = request.user.username
        if username=='Demo':
            username='florine__20'
            demo=True


    ALLPURCHASESstr=  "SELECT ORDER_ID,EFFDT,MAIN_COMMODITY_NM,SUB_COMMODITY_NM,CALLITEM,SHIPTAOBAO,ITEMARRIVED FROM TODO Where STATUS='已出貨' and USERNAME='"+username+"' order by EFFDT asc"
    ALLPURCHASEDATA=TODO.objects.raw(ALLPURCHASESstr)
    for i in range(len(ALLPURCHASEDATA)):
        
        ALLPURCHASEDATA[i].EFFDT=ALLPURCHASEDATA[i].EFFDT.strftime('%Y-%m-%d %H:%M')

    
    # p=Paginator(ALLPURCHASEDATA,20)
    # page_num=request.GET.get('page',1)
    # try:
    #     page=p.page(page_num)
    # except EmptyPage:
    #     page=p.page(1)
    # page=p.page(page_num)

   
    
    return render(request, 'home/shipping.html',{'ALLORDERSDATA':ALLPURCHASEDATA})

@login_required(login_url="/login/")
def simple_upload(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    
     
    mycursor = mydb.cursor()

    count= request.session.get('count')
  
    if count==0:
    
        #GET UploadFromYYYYMMDD
        UPLYYYYMMDDsql="SELECT substring(MIN(EFFDT),1,10) as YYYYMMDD FROM orders where STATUS not in ('完成','不成立')"
        UPLYYYYMMDD=GETYYYYMMDD.objects.raw(UPLYYYYMMDDsql)[0].YYYYMMDD
        
        if UPLYYYYMMDD==None:
            UPLYYYYMMDDsql="SELECT substring(MAX(EFFDT),1,10) as YYYYMMDD FROM orders"
            UPLYYYYMMDD=GETYYYYMMDD.objects.raw(UPLYYYYMMDDsql)[0].YYYYMMDD
            date_object = datetime.datetime.strptime(UPLYYYYMMDD, '%Y-%m-%d').date()
            UPLYYYYMMDD=date_object+datetime.timedelta(days=1)
            UPLYYYYMMDD=UPLYYYYMMDD.strftime('%Y-%m-%d')
        current_dateTime = datetime.datetime.now()
        current_dateTime=current_dateTime.strftime('%Y-%m-%d')
        end_date=datetime.datetime.strptime(current_dateTime, '%Y-%m-%d').date()
        start_date = datetime.datetime.strptime(UPLYYYYMMDD, '%Y-%m-%d').date()
        task=[]
        row=1
        while start_date<end_date:
            s=start_date
            if start_date.month==end_date.month:
                e=end_date
            else:
                e=(datetime.date((start_date+relativedelta.relativedelta(months=1)).year, (start_date+relativedelta.relativedelta(months=1)).month, 1))-datetime.timedelta(days=1)
            sStr=s.strftime('%Y-%m-%d')
            eStr=e.strftime('%Y-%m-%d')
            fs_Str=s.strftime('%Y%m%d')
            fe_Str=e.strftime('%Y%m%d')
            taskStr='Please upload data from '+sStr+' to '+ eStr
            myfilestr='myfile'+str(row)
            uploadstr='upload'+str(row)
            task.append([taskStr,myfilestr,uploadstr,'未完成',fs_Str,fe_Str])
            start_date=e+datetime.timedelta(days=1)
            row=row+1
    
        request.session['task'] = task
        
        deletesql = "delete from ORDERS_UPD_TMP where USERNAME='"+username+"'"
        mycursor.execute(deletesql)
        mydb.commit()
 
    #if request.method == 'POST' and request.FILES['myfile1']:
    if request.method == 'POST':
        task= request.session.get('task')
        for i in range(len(task)):
            mm=task[i][1]
            if request.FILES.get(str(mm))!=None:
                myfile = request.FILES.get(str(mm))
                break
        #myfile = request.FILES['myfile1']
        
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        myfileName=myfile.name
        
        uploaded_file_url = fs.url(filename)
        
        CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   
        XLSX_DIR=os.path.join(CORE_DIR, "media") 
        xlsx_file_name=filename       
        xlsx_file=os.path.join(XLSX_DIR, xlsx_file_name) 
        file_start_date=xlsx_file_name[10:18]
        file_end_date=xlsx_file_name[19:27]
        legal=False
        for i in range(len(task)):
                                      
            if task[i][4]==file_start_date and task[i][5]==file_end_date:
                legal=True
                task[i][3]='完成'
                break
       
       
        rows=[]
        data = xlrd.open_workbook(xlsx_file).sheet_by_index(0)
        
        found=False
        for r in range(data.nrows):
            if r==0:
                continue
            else:     
                temp=[]
                temp.append(username)
                for i in range(0,len(data.row_values(r))):
                    
                    text=data.cell(rowx=r,colx=i).value
                    text=str(text)
                    
                    if (i==43 or i==45 or i==46 or i==47) and len(text)!=16:
                        text=None
                    temp.append(text)
                    
        
                rows.append(temp)   
               
           
        
        sql = "INSERT INTO ORDERS_UPD_TMP (USERNAME,ORDER_ID,STATUS,FAIL_REASON,RETURN_STATUS,CUSTOMER_ID,EFFDT,PRODUCT_GROSS,CUSTOMER_SHIP_FEE,SHOPEE_SHIP_FEE,RETURN_SHIP_FEE,TOTAL_PAID,SHOPEE_SUBSIDY,SHOPEE_REDEEM,CREDIT_DISCOUNT,DISCOUNT_CODE,CUSTOMER_COUPON,CUSTOMER_GIVEBACK,SHOPEE_COUPON,TRANSCATION_FEE,SERVICE_FEE,CASHFLOW_FEE,INSTALLMENTS,CREDIT_CHARGE,MAIN_COMMODITY_NM,SUB_COMMODITY_NM,ORG_PRICE,DIS_PRICE,MAIN_COMMODITY_ID,SUB_COMMODITY_ID,COUNT,PROMOTION_METRIC,SHOPEE_PROMOTION,RECIPIENT_ADDR,RECIPIENT_PHONE,PICKUP_STORE_ID,CITY,DISTRICT,POSTAL,RECIPIENT_NAME,SHIPPING_TYPE,DELIVER_TYPE,PREPARE_TIME,PAYMENT_TYPE,LAST_SHIP_TIME,SHIIPPING_CODE,CUSTOMER_PAID_TIME,ACTUAL_SHIP_TIME,ORDER_COMPLETE_TIME,CUSTOMER_COMMENT,COMMENT) VALUES (%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s)"
        val = rows
        mycursor.executemany(sql, val)
        mydb.commit()

        mycursor.close()
        #mydb.close()
        os.remove(xlsx_file)
        
        count=count+1
        request.session['count'] = count
        request.session['task'] = task
   
        return render(request, 'home/simple_upload.html', {
            # 'uploaded_file_url': '/orders',
            # 'uploaded_file_name': myfile.name,
            'count':count,
            'task':task,
            'rows':len(task)
        })
        
    return render(request, 'home/simple_upload.html',{'task':task,'count':count,'rows':len(task)})

@login_required(login_url="/login/")
def update_order(request):
    finish=0
    task= request.session.get('task')
    delete_key_str=str(task[0][4])
    delete_key=delete_key_str[0:4]+'-'+delete_key_str[4:6]+'-'+delete_key_str[6:]
    update_date_str=str(task[-1][5])
    update_date=update_date_str[0:4]+'-'+update_date_str[4:6]+'-'+update_date_str[6:]
 
    
    username = None
    if request.user.is_authenticated:
        username = request.user.username

     
    mycursor = mydb.cursor()
    deletesql = "delete from ORDERS where USERNAME='"+username+"'"+" and EFFDT>='"+delete_key+"'"
    mycursor.execute(deletesql)
    mydb.commit()
    
    insertsql = "insert into ORDERS (select * from ORDERS_UPD_TMP)"
    mycursor.execute(insertsql)
    mydb.commit()

    inserttodosql="insert into todo (select *,FALSE,FALSE,FALSE,FALSE,'' from allorders where status='待出貨' and USERNAME='"+username+"'"+" and ORDER_ID not in (select distinct order_id from todo where USERNAME='"+username+"'"+"))"
    mycursor.execute(inserttodosql)
    mydb.commit()

    deletetodosql = "delete from todo where USERNAME='"+username+"'"+" and order_id not in (select distinct order_id from allorders where status='待出貨' and USERNAME='"+username+"'"+")"
    mycursor.execute(deletetodosql)
    mydb.commit()

    mycursor.close()
      
    finish=1
    return render(request, 'home/simple_upload.html',{'redirect':finish,'redirect_url': '/orders','update_date':update_date})

@login_required(login_url="/login/")
def cost(request):
    redirect=0
    username = None
    demo=False
    if request.user.is_authenticated:
        username = request.user.username
        if username=='Demo':
            username='florine__20'
            demo=True
  
    ALLCOSTDATA=COST_SUM.objects.filter(USERNAME=username).order_by('-YYYYMM')
   
    #check if new month
    UPLYYYYMMDD=str(ALLCOSTDATA[0].YYYYMM)+"-01"
    current_dateTime = datetime.datetime.now()
    current_dateTime=current_dateTime.strftime('%Y-%m-%d')
    end_date=datetime.datetime.strptime(current_dateTime, '%Y-%m-%d').date()
    start_date = datetime.datetime.strptime(UPLYYYYMMDD, '%Y-%m-%d').date()
    start_date=(datetime.date((start_date+relativedelta.relativedelta(months=1)).year, (start_date+relativedelta.relativedelta(months=1)).month, 1))
    vals=[]

    while start_date<=end_date:
        print(start_date)
        print(end_date)
        vals.append([username,start_date.strftime('%Y-%m-%d')[:7],1,start_date,0,current_dateTime,""])
        start_date=(datetime.date((start_date+relativedelta.relativedelta(months=1)).year, (start_date+relativedelta.relativedelta(months=1)).month, 1))
    # if len(vals)>0:
   
        sql = "INSERT INTO mainapp_cost_detail (USERNAME,YYYYMM,COST_TYPE,EFFDT,AMOUNT,ADDDATETIME,COMMENT) VALUES (%s,%s, %s,%s,%s, %s,%s)"
        mycursor = mydb.cursor()
        mycursor.executemany(sql, vals)
        mydb.commit()
        mycursor.close()
    
    return render(request, 'home/cost.html',
    {'COST_DATA':ALLCOSTDATA,'redirect':redirect}
    )


@login_required(login_url="/login/")
def cost_detail(request,YYYYMM):
    if request.method == 'GET':
        username = None
        demo=False
        if request.user.is_authenticated:
            username = request.user.username
            if username=='Demo':
                username='florine__20'
                demo=True
        ALLCOSTDETAILSstr=  "SELECT * FROM COST_DETAIL Where USERNAME='"+username+"' and YYYYMM='"+YYYYMM+"' order by EFFDT"
        ALLCOSTDETAILDATA=COST_DETAIL.objects.raw(ALLCOSTDETAILSstr)
        print("GET")
        for i in range(len(ALLCOSTDETAILDATA)):
            
            ALLCOSTDETAILDATA[i].EFFDT=ALLCOSTDETAILDATA[i].EFFDT.strftime('%Y-%m-%d')
            if ALLCOSTDETAILDATA[i].COMMENT==None:
                ALLCOSTDETAILDATA[i].COMMENT=''


        return render(request, 'home/cost_detail.html',
        {'COSTDETAIL_DATA':ALLCOSTDETAILDATA,'YYYYMM':YYYYMM,'demo':demo,'username':username}
        )

# class cost_detail(generic.ListView):
#     model = COST_DETAIL
#     context_object_name = 'costs'
#     template_name = 'home/cost_detail.html'

#     def get_queryset(self):
#         qs = super().get_queryset()
#         qs = qs.filter(USERNAME=self.request.user.username, YYYYMM='2023-03')
#         if 'type' in self.request.GET:
#             qs = qs.filter(book_type=int(self.request.GET['type']))
#         return qs

# def details(request,YYYYMM):
#     data = dict()
#     username = None
#     demo=False
#     if request.user.is_authenticated:
#         username = request.user.username
#         if username=='Demo':
#             username='florine__20'
#             demo=True
#     if request.method == 'GET':
#         costs = COST_DETAIL.objects.filter(USERNAME=username, YYYYMM=YYYYMM)
#         data['table'] = render_to_string(
#             '_costs_table.html',
#             {'costs': costs},
#             request=request
#         )
#         return JsonResponse(data)    


class BookCreateView(BSModalCreateView):
    template_name = 'home/create_cost.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    # success_url = reverse_lazy('cost_detail-202303')
    def get_success_url(self, **kwargs):
        return reverse_lazy('cost_detail', args = (self.object.YYYYMM,))
    # def get(self, request, ):
    #     form = self.form_class(initial=self.initial)
    #     return render(request, self.template_name, {'form': form,})
    # def get_context_data(self, **kwargs):
    # # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in the publisher
    #     context['YYYYMM'] = self.YYYYMM
    #     return context
  




