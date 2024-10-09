from django.urls import path

from . import views

app_name = "notes"
urlpatterns=[
    path('',views.index),
    path('all/',views.allnotes, name="all"),
    path('add/', views.addnote,name="add"),
    path("<str:note_url>/",views.content,name="url"),
]