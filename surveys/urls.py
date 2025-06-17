from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('create/', views.create_survey, name='create_survey'),
    path('success/<int:survey_id>/', views.survey_success, name='survey_success'),
    path('edit-success/<int:survey_id>/', views.survey_edit_success, name='survey_edit_success'),
    path('survey/<int:survey_id>/edit/', views.edit_survey, name='edit_survey'),
    path('list/', views.list_surveys, name='list_surveys'),
    path('survey/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),
    path('survey/<int:survey_id>/view/', views.view_survey, name='view_survey'),
    path('submit/<int:survey_id>/', views.submit_survey, name='submit_survey'),
    path('info/', views.info_view, name='info'),
    path('survey/delete/<int:survey_id>/', views.delete_survey, name='delete_survey'),
    path('view/<int:survey_id>/', views.ADview_survey, name='1view_survey'),

    




]
