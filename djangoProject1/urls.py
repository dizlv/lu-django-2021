"""djangoProject1 URL Configuration

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

from salaries import views

# http://<ip>:<port>/ - salaries list
# http://<ip>:<port>/monthly/ - report
# http://<ip>:<port>/add/ - 1. get form 2. save data (GET, POST)

urlpatterns = [
    path('', views.salaries_list, name='salaries-list'),
    path('monthly/', views.salaries_monthly_report),
    path('add/', views.salary_add),
    path('import/', views.import_salary_entries),
    path('js/', views.js_view),
    path('api/salaries/', views.SalariesAPIView.as_view()),

    path('admin/', admin.site.urls),
]
