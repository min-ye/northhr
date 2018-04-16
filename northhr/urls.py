"""northhr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from archive import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.person_search, name='person_search'),
    path('login/', views.login, name='login'),
    #path('account/password/', views.login, name='password'),
    path('logout/', views.logout, name='logout'),
    path('password/', views.change_password, name='change_password'),
    #path('category/', views.category, name='category'),
    path('layout/', views.layout, name='layout'),
    path('person/log/<int:person_id>', views.log, name='log'),
    path('person/personlog/<int:person_id>', views.personlog, name='personlog'),
    #path('form_template_1/', views.form_template_1, name='form_template_1'),
    path('person/detail/<int:id>', views.person_detail, name='person_detail'),
    path('person/search/', views.person_search, name='person_search'),
    path('person/edit/', views.person_new, name='person_new'),
    path('person/new/', views.person_new, name='person_new'),
    path('person/edit/<int:id>', views.person_edit, name='person_edit'),
    path('person/unknown/', views.person_unknown, name='person_unknown'),
    path('register/<int:person_id>', views.register, name='register'),
    path('person/excel/<int:person_id>', views.excel, name='excel'),
]