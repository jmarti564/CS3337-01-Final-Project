from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_detail/<int:book_id>', views.book_detail , name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('about/', views.about, name='about'),
]




