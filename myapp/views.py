from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'myapp/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_message': room_messages, 'participants': participants}
    return render(request, 'myapp/room.html', context)

def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'myapp/profile.html', context)


@login_required(login_url='loginpage')
def createroom(request):
    topics =Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user, topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'myapp/room_form.html', context)

@login_required(login_url='loginpage')
def updateroom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not Allowed here..')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'myapp/room_form.html', context)

@login_required(login_url='loginpage')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not Allowed here..')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'myapp/deleteroom.html', {'obj': room})

def Loginpage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
             user = User.objects.get(username=username)
             user = authenticate(request, username=username, password=password)
             if user is not None:
                login(request, user)
                if request.user.is_authenticated:
                    return redirect('home')

             else:
                messages.error(request, 'Username or Password Does not match')

        except:
            messages.error(request, 'User does not exist')


    context = {'page':page}
    return render(request, 'myapp/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def Registerpage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error occured during registration! Please try Again... ')
    context = {'page': page, 'form': form}
    return render(request, 'myapp/login_register.html', context)


def deletemessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not Allowed here..')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'myapp/deleteroom.html', {'obj': message})

@login_required()
def Update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'myapp/update_user.html', {'form':form})


def topic_page(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'myapp/topics.html', {'topics': topics})