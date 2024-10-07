from django.urls import path

from . import views

app_name = "notes"
urlpatterns=[
    path('',views.index),
    path('all/',views.allnotes),
    path("<str:note_url>/",views.content,name="url"),
]