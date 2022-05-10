
from django.urls import path
from . import views
from .views import *
app_name='userurl'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signupView, name='signup'),
    path('login/', views.loginView, name='login'),
    path('profit-history', views.profit, name="profit"),
    path('logout/', views.logout_view, name='logout'),
    path('plan/', views.plan, name='plan'),
    path('my-investments/', views.myinvest, name='my_invest'),
    path('my-referals',views.refer, name='refer'),
    path('connect-api/', views.mywallet, name='con'),
    path('connect-api/<slug>/',  views.mycon ,name='connect'),
    # path('settings/', views.edit, name='settings'),
    path('withdraw/', views.withdraw, name='with'),
    path('withdrawal/', views.withdrawal, name='withal'),
    path('deposit/', views.fund, name='depo'),
    path('payments/<slug>/', views.myfund, name='payment'),
    path('change_password/', views.change_password, name='change_password'),
	path('change_password_confirm/', views.change_password_confirm, name='change_password_confirm'),
	path('<slug:pk>', views.change_password_code, name='change_password_code'),
	path('change_password_success/', views.change_password_success, name='change_password_success'),
   

    
]