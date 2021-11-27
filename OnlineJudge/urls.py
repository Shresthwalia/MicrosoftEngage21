"""OnlineJudge URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from OnlineJudge import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', csrf_exempt(views.display_home_page)),
    url(r'^createproblem/', csrf_exempt(views.create_problem)),
    url(r'^createassignment/', csrf_exempt(views.create_assignment)),
    url(r'^getproblem/', csrf_exempt(views.get_problem)),
    url(r'^displayproblem/', csrf_exempt(views.display_problem)),
    url(r'^getresults/', csrf_exempt(views.get_results)),
    path(r'^addproblem/', csrf_exempt(views.show_add_problem_page)),
    url(r'^addassignment/', csrf_exempt(views.add_assignment)),
    url(r'^attemptproblem/', csrf_exempt(views.attempt_problem)),
    url(r'^displayassignment/', csrf_exempt(views.attempt_problem)),
    url(r'^attemptassignment/',csrf_exempt(views.attempt_assignment))
]
