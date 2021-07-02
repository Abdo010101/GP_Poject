
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('predict/' ,views.predict , name='predict'),
    path('login/',views.loginPage , name='loginPage'),
    path('logout/',views.logoutPage,name='logoutPage'),
    path('register/',views.registerPage,name='registerPage'),
]
