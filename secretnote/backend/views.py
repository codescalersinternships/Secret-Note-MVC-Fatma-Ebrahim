from django.shortcuts import render, get_object_or_404,get_list_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Note
import uuid 


def index(request):
    return HttpResponse("Hello, world. You're at the backend index")

def content(request, note_url):
    note = get_object_or_404(Note, url=note_url) 
    return HttpResponse(f"You're looking at Note {note.id} with content {note.content}")


def allnotes(request):
    notes=get_list_or_404(Note)
    context={"notes": notes}
    return render(request,"backend/allnotes.html",context)

def addnote(request):
    if request.method == "POST":
        content=request.POST.get('content')
        expiration=request.POST.get('expiration')  
        views_limit=request.POST.get('views_limit')
        n=Note(content=content,expiration=expiration,views_limit=views_limit,url=uuid.uuid4())
        n.save()
        print(n.created_at) #2024-10-09 12:53:10.248280+00:00  datetime
        print(n.expiration) #2024-10-10T01:01 string
        return HttpResponseRedirect(reverse("notes:all"))
    return render(request,"backend/addnote.html")