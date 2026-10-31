from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/<int:pk>/rename/', views.subject_rename, name='subject_rename'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    # Topics
    path('subjects/<int:subject_id>/topics/', views.topic_list, name='topic_list'),
    path('subjects/<int:subject_id>/topics/add/', views.topic_add, name='topic_add'),
    path('topics/<int:pk>/rename/', views.topic_rename, name='topic_rename'),
    path('topics/<int:pk>/delete/', views.topic_delete, name='topic_delete'),

    # Notes
    path('topics/<int:topic_id>/note/', views.note_view, name='note_view'),
    path('topics/<int:topic_id>/note/delete/', views.note_delete, name='note_delete'),

    # AI Features
    path('ai/doubt/', views.ai_doubt, name='ai_doubt'),
    path('ai/quiz/', views.ai_quiz, name='ai_quiz'),
    path('ai/summarize/', views.ai_summarize, name='ai_summarize'),
    path('ai/study-plan/', views.ai_study_plan, name='ai_study_plan'),

    # Study Sessions
    path('sessions/', views.session_start, name='session_start'),

    # Search
    path('search/', views.search_view, name='search'),

    # Reports
    path('reports/', views.reports_view, name='reports'),

    # Quiz Integrity
    path('integrity/', views.quiz_integrity, name='quiz_integrity'),

    # AJAX
    path('ajax/topics/<int:subject_id>/', views.ajax_topics, name='ajax_topics'),
]
