"""
URL configuration for poll_project project.

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
from django.urls import path, include
from poll import views
app_name = 'poll'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('votes/', views.view_votes, name='view_votes'),
    path('create/', views.create_poll, name='create_poll'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("signup/", views.signup_view, name="signup"),
    path('category/<int:category_id>/', views.category_polls, name='category_polls'),

    path('create_survey/', views.create_survey, name='create_survey'),
    path('select_survey_questions/', views.select_survey_questions, name='select_survey_questions'),
    path('view_surveys/', views.view_surveys, name='view_surveys'),
    path('survey/<int:survey_id>/take/', views.take_survey, name='take_survey'),
    path('survey/<int:survey_id>/', views.view_survey, name='view_survey'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('view_survey_list/', views.view_survey_list, name='view_survey_list'),
]

