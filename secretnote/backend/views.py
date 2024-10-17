from django.shortcuts import render, get_object_or_404,get_list_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.urls import reverse
from django.db.models import F,Q
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit
from datetime import datetime
from django.utils import timezone

from .models import Note
import uuid 


@ratelimit(key='ip', rate='100/m')
def signup(request):
    if request.method=="POST":
        username = request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        if username!="" and email!="" and password!="":
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("notes:all"))
        else:
            print("all fields are required")
    return render(request,"backend/signup.html")

@ratelimit(key='ip', rate='100/m')
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username!=""  and password!="":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("notes:all"))
            else:
                raise Http404("unAuthorized user")
        else:
            print("all fields are required")
    return render(request,"backend/signin.html")


def homepage(request):
    return render(request, "backend/homepage.html")



@ratelimit(key='ip', rate='100/m')
def content(request, note_url):
    note = get_object_or_404(Note, url=note_url) 
    if note.views_limit<1:
        note.delete()
        return HttpResponseRedirect(reverse("notes:all"))
    note.views_limit = max(0, note.views_limit - 1)
    note.save()
    return render(request, "backend/note.html", {"note": note})



@login_required
@ratelimit(key='ip', rate='100/m')
@never_cache
def allnotes(request):
    print(request.user)
    outdated_notes = Note.objects.filter(Q(views_limit=0) | Q(expiration__lte=datetime.now()))
    outdated_notes.delete()
    notes=Note.objects.all()
    context={"notes": notes}
    return render(request,"backend/allnotes.html",context)

   
        

@login_required
@ratelimit(key='ip', rate='100/m')
def addnote(request):
    print(request.user)
    if request.method == "POST":
        
        content=request.POST.get('content')
        expiration=request.POST.get('expiration')  
        expiration = datetime.strptime(expiration, '%Y-%m-%dT%H:%M')
        expiration = timezone.make_aware(expiration, timezone.get_current_timezone())
        views_limit = int(request.POST.get('views_limit'))
        
        if content=="": content="No content"
        if views_limit<=0: views_limit=10
        if expiration<=timezone.now(): expiration=timezone.now()+timezone.timedelta(days=1)
        
        n=Note(content=content,expiration=expiration,views_limit=views_limit,url=uuid.uuid4())
        n.save()
        
        # print(n.created_at) #2024-10-09 12:53:10.248280+00:00  datetime
        # print(n.expiration) #2024-10-10T01:01 string
        return HttpResponseRedirect(reverse("notes:all"))
    return render(request,"backend/addnote.html")