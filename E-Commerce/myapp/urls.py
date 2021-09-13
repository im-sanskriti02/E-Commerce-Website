from django.contrib import admin
from django.urls import path
from myapp import views
from gurukripa  import settings
from django.conf.urls.static import static
from .views import Index, Cart, Checkout, OrderView, Login
from .middlewares.auth import auth_middleware


app_name = 'myapp' 
urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('item/<int:item_id>/', views.detail, name="detail"),
    path('add_item/', views.add_item, name="add_item"),
    path('cart/', Cart.as_view(), name="cart"),
    path('check-out/', Checkout.as_view(), name="checkout"),
    path('orders/', auth_middleware(OrderView.as_view()), name="orders"),
    path('login/', Login.as_view(), name = "login"),
    path("signup/", views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)