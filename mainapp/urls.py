
from django.urls import path, re_path,include
from mainapp import views
from django.contrib import admin


urlpatterns = [

    # The home page
    
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")), # Auth routes - login / register
    #path('button_call',views.button_call,name='button_call'),
    path('simple_upload',views.simple_upload,name='simple_upload'),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    
    
]

