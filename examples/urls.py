from django.urls import path

from . import views


urlpatterns = [
    path('cost/<str:YYYYMM>', views.BooksIndex.as_view(), name='booksindex'),
    #path('booksindex', views.BooksIndex.as_view(), name='booksindex'),
    path('filter/', views.BookFilterView.as_view(), name='filter_book'),
    path('create/', views.BookCreateView.as_view(), name='create_book'),
    #path('create/<str:YYYYMM>', views.BookCreateView.as_view(), name='create_book'),
    path('update/<int:pk>/<str:YYYYMM>', views.BookUpdateView.as_view(), name='update_book'),
    path('read/<int:pk>', views.BookReadView.as_view(), name='read_book'),
    path('delete/<int:pk>/<str:YYYYMM>', views.BookDeleteView.as_view(), name='delete_book'),
    path('cost/books/<str:YYYYMM>', views.books, name='books'),
   
   
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]
