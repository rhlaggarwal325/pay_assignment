from django.contrib.auth import login
from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'transact1', views.TransactionViewset)

urlpatterns = [
    path('',include(router.urls)),
    path('transact_add/<int:wallet_id>/', views.transact_add_view),
    path('transact_paid/<int:wallet_id>/', views.transact_paid_view),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('balance/', views.current_balance, name='balance'),
    path('register/', views.register_view, name='register'),
    path('add_money/', views.add_money, name="add_money"),
    path('pay_money/', views.pay_money, name="pay_money"),
    path('transaction/', views.transaction_log, name='transaction'),
]
