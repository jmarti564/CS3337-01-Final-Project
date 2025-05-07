# 5/4
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from bookMng import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', include('bookMng.urls')), path('postbook', views.postbook, name='postbook'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('search/', views.search_books, name='search_books'),
    path('admin/', admin.site.urls),
    path('', include('bookMng.urls')),
    # Authentication
    path('register/', views.Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Favorites
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/toggle/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),

    #displaybooks search
    path('books/', views.displaybooks, name='displaybooks'),  # Changed: displaybooks URL (5/3)
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
