"""
URL configuration for electiononline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from electiononlineapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home , name='home'),
    path('signup/', views.signup , name='signup'),
    path('login/', views.login_user , name='login'),
    path('logout/',views.logoutpage, name= 'logout'),
    path('adminadd/',views.add_position, name= 'adminadd'),
    path('update/<int:pk>',views.update_position, name='update'),
    path('delete/<int:pk>',views.delete_position, name='delete'),
    path('vote/<int:position_id>/', views.vote, name='vote'),
    path('submit_vote/', views.submit_vote, name='submit_vote'),
]
