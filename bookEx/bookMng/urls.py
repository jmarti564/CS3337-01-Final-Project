# 5/4
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'bookMng'  # <- You MUST have this line to use {% url 'bookMng:something' %}

urlpatterns = [
    path('', views.index, name='index'),
    path('postbook/', views.postbook, name='postbook'),
    path('displaybooks/', views.displaybooks, name='displaybooks'),
    path('mybooks/', views.mybooks, name='mybooks'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/delete/<int:book_id>/', views.book_delete, name='book_delete'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('search/', views.search_books, name='search_books'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.login_view, name='login'),  # <-- You need a login view
    path('logout/', views.logout_view, name='logout'),  # <-- You need a logout view
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/toggle/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('add_comment/<int:book_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
