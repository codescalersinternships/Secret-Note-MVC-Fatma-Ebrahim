from django.urls import path

from . import views

app_name = "notes"
urlpatterns=[
    path('',views.index),
   
    path('add/', views.addnote,name="add"),
    path('all/',views.allnotes, name="all"),
    path("signup/",views.signup, name="signup"),
    path("signin/",views.signin,name="signin"),
    path("<str:note_url>/",views.content,name="url"),
 
]