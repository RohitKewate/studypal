from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Room,Topic,Message,User
from .forms import RoomForm , UserForm, MyUserCreationForm
from django.db.models import Q

# Create your views here.

#Authentication 
def loginPage(request):
   #login logic
   page='login-page'
   if request.user.is_authenticated:
      return redirect('home-page')


   if request.method == 'POST':
      email= request.POST.get('email')
      password= request.POST.get('password')

      try:
         user = User.objects.get(email=email)
      except:
         messages.error(request,'User does not exist.')

      user = authenticate(request,email=email, password=password)

      if user is not None:
         login(request,user)
         messages.success(request, "LogIn Successfull!")
         return redirect('home-page')
      else:
         messages.error(request, 'Invalid Credentials.')

   context = {'page':page,}
   return render(request, 'base/login_register.html' ,context)

#logout Logic
def logoutPage(request):
   logout(request)
   messages.success(request, "LogOut Successfull!")
   return redirect('home-page')


def registerPage(request):
   form =MyUserCreationForm()

   if request.method == "POST":
      form = MyUserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('home-page')
         
      else:
         messages.error(request, 'An error occured during registration!')


   return render(request, 'base/login_register.html',{"form":form} )
   
def home(request):
    #search function
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
       
       Q(topic__name__icontains=q) |
       Q(name__icontains=q) |
       Q(description__icontains=q)
       
       
       )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context={'rooms': rooms,'topics':topics,'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request,pk):
   room = Room.objects.get(id=pk)
   room_messages = room.message_set.all()
   participants = room.participants.all()
   if request.method == "POST":
      message = Message.objects.create(
         user = request.user,
         room = room,
         body = request.POST.get('body')

      )
      room.participants.add(request.user)
      return redirect('room-page',pk = room.id)
    
   context = {'room': room, 'room_messages': room_messages,'participants':participants}
   return render(request, 'base/room.html',context)


def userProfile(request,pk):
   user= User.objects.get(id=pk)
   rooms = user.room_set.all()
   room_messages = user.message_set.all()
   topics = Topic.objects.all()
   context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
   return render(request,'base/profile.html',context)

@login_required(login_url='login-page')
def createRoom(request):
   form = RoomForm()
   topics = Topic.objects.all()
   if request.method == 'POST':
      topic_name = request.POST.get('topic')
      topic, created = Topic.objects.get_or_create(name=topic_name)
      
      Room.objects.create(
         host=request.user,
         topic=topic,
         name=request.POST.get('name'),
         description=request.POST.get('description'),
      )
      
      return redirect('home-page')

   context = {'form': form , 'topics': topics}
   return render(request, 'base/room_form.html',context)

@login_required(login_url='login-page')
def updateRoom(request,pk):
   room = Room.objects.get(id=pk)
   form = RoomForm(instance=room)
   topics = Topic.objects.all()
   if request.user != room.host:
      return HttpResponse("You are not allowed to do that.")


   if request.method == 'POST':
      topic_name = request.POST.get('topic')
      topic, created = Topic.objects.get_or_create(name=topic_name)
      room.name = request.POST.get('name')
      room.topic = topic
      room.description = request.POST.get('description')
      room.save()
      return redirect('home-page')
         

   context = {'form': form, 'topics': topics, 'room': room }
   return render(request, 'base/room_form.html',context)

@login_required(login_url='login-page')
def deleteRoom(request,pk):
   room = Room.objects.get(id=pk)
   if request.method == 'POST':
      room.delete()
      return redirect('home-page')
   

   return render(request,"base/delete.html", {'obj':room})


@login_required(login_url='login-page')
def deleteMessage(request,pk):
   message = Message.objects.get(id=pk)
   if request.user != message.user:
      return HttpResponse('You are not allowed here!')
   

   if request.method == 'POST':
      message.delete()
      return redirect('home-page')
   

   return render(request,"base/delete.html", {'obj':message})


@login_required(login_url='login-page')
def updateUser(request):
   user = request.user
   form = UserForm(request.POST, request.FILES ,instance=user)
   if request.method == 'POST':
      form = UserForm(request.POST, instance=user)
      if form.is_valid():
         form.save()
         return redirect('user-profile-page', pk = user.id )


   return render(request,'base/update-user.html',{ 'form':form })

#Mobile View
def topicsPage(request):
   q = request.GET.get('q') if request.GET.get('q') != None else ''
   topics = Topic.objects.filter(name__icontains=q)
   context={'topics':topics}
   return render(request, 'base/topics.html',context)

def activityPage(request):
   room_messages = Message.objects.all()
   context={'room_messages':room_messages}
   return render(request, 'base/activity.html',context)