from django.shortcuts import render, get_object_or_404,get_list_or_404

# Create your views here.
from django.http import HttpResponse, Http404

from .models import Note


def index(request):
    return HttpResponse("Hello, world. You're at the backend index")

def content(request, note_url):
    note = get_object_or_404(Note, url=note_url) 
    return HttpResponse(f"You're looking at Note {note.id} with content {note.content}")


def allnotes(request):
    notes=get_list_or_404(Note)
    context={"notes": notes}
    return render(request,"backend/index.html",context)
