
from django.urls import path, re_path,include
from mainapp import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from mainapp import views

router = DefaultRouter()
router.register('ALLORDERS', views.ALLORDERSViewSet)

urlpatterns = [

    # The home page
    
    path('', views.index, name='home'),
    #path('admin/', admin.site.urls),
    
    path("", include("authentication.urls")), # Auth routes - login / register
    path('simple_upload',views.simple_upload,name='simple_upload'),
    path('orders',views.orders,name='orders'),
    path('pending',views.pending,name='pending'),
    path('shipping',views.shipping,name='shipping'),
    path('update_order',views.update_order,name='update_order'),
    path('cost',views.cost,name='cost'),
    path('api/',include(router.urls))
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

