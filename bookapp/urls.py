from django.urls import path
from bookapp import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('booklist/',views.booklist,name='booklist'),
    path('details/',views.details,name='details'),
    path('register/',views.register,name='register'),
    path('registerchance/',views.registerchance,name='registerchance'),
    path('register_ok/',views.register_ok,name='register_ok'),
    path('getcapthcha/',views.getcapthcha,name='getcapthcha'),
    path('checkcapthcha/',views.checkcapthcha,name='checkcapthcha'),
    path('checkname/',views.checkname,name='checkname'),
    path('login/',views.login,name='login'),
    path('loginchance/',views.loginchance,name='loginchance'),
    path('logout/',views.logout,name='logout'),
    path('addbook/',views.addbook,name='addbook'),
    path('delcar/',views.delcar,name='delcar'),
    path('delcar2/',views.delcar2,name='delcar2'),
    path('alldelcar/',views.alldelcar,name='alldelcar'),
    path('car/',views.car,name='car'),
    path('updatecar/',views.updatecar,name='updatecar'),
    path('indent/',views.indent,name='indent'),
    path('indent_ok/',views.indent_ok,name='indent_ok'),
    path('indentchance/',views.indentchance,name='indentchance'),
    path('cartoindent/',views.cartoindent,name='cartoindent'),
    path('sendemail/',views.sendemail,name='sendemail'),
    path('deloldcode/',views.deloldcode,name='deloldcode'),
    path('codecheck/',views.codecheck,name='codecheck')
]