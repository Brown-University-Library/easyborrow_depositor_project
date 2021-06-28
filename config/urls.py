"""easyborrow_depositor_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from easyborrow_depositor_app import views


urlpatterns = [

    ## primary app urls...
    path( 'confirm_request/', views.confirm_request, name='confirm_request_url' ),  # validates and cleans incoming data; presents confirmation-button; triggers call to confirm_handler
    path( 'confirm_handler/', views.confirm_handler, name='confirm_handler_url' ),  # deposits data to db; triggers email to user; redirects to message
    path( 'message/', views.message, name='message_url' ),                          # shows user confirmation-message (or problem message)
    path( 'admin/', admin.site.urls ),

    ## support urls...
    path( 'version/', views.version, name='version_url' ),
    path( 'error_check/', views.error_check, name='error_check_url' ),
    path( 'info/', views.info, name='info_url' ),

]
