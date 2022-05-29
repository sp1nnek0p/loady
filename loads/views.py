from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import LoadForm, EditProfileForm
from .models import *

# Create your views here.
# When adding Views add the 'document_title' to the context dictionary

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def delete_room_view(request, id):
    obj = Load.objects.get(id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')

    context = {
        'object': obj,
    }
    return render(request, 'loads/delete_obj.jhtml', context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, f'Succesfully logged in @{user}')
            return redirect('editprofile', id=user.id) # Might want to send them straight to the Profile edit page
        else:
            messages.error(request, 'Something went wrong with Signup')
    
    form = UserCreationForm()
    context = {
        'document_title': 'Register',
        'form': form,
    }
    return render(request, 'loads/register.jhtml', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist or is invalid")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"@{username} logged in succesfully")
            return redirect('home')

    context = {
        'document_title': 'Login',
    }
    return render(request, 'loads/login.jhtml', context)


@login_required(login_url='login')
def edit_load_view(request, id):
    load = Load.objects.get(id=id)
    loadform = LoadForm(instance=load)

    if request.user != load.user:
        messages.error(request, 'You can not edit this room')
        return redirect('home')

    if request.method == 'POST':
        loadform = LoadForm(request.POST, instance=load)
        if loadform.is_valid():
            load = loadform.save(commit=False)
            load.user = request.user
            load.save()
            return redirect('home')

    context = {
        'document_title': 'Edit Load',
        'load_form': loadform,
    }
    return render(request, 'loads/createeditload.jhtml', context)


@login_required(login_url='login')
def create_load_view(request):
    loadform = LoadForm()

    if request.method == 'POST':
        loadform = LoadForm(request.POST)
        if loadform.is_valid():
            load = loadform.save(commit=False)
            load.user = request.user
            load.save()
            messages.success(request, f"@{request.user} posted a new load" )
            return redirect('home')

    context = {
        'document_title': 'Create Load',
        'load_form': loadform,
    }
    return render(request, 'loads/createeditload.jhtml', context)


def home_view(request):
    
    if request.GET.get('q') != None:
        query = request.GET.get('q')
    else:
        query = ''

    loads = Load.objects.filter(
        Q(title__icontains=query)|
        Q(description__icontains=query)|
        Q(pickup__icontains=query)|
        Q(dropoff__icontains=query)|
        Q(vehicleType__type__icontains=query)|
        Q(product__icontains=query)
    )

    paginator = Paginator(loads, 8)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'document_title': 'Home',
        'loads': page_obj,

    }
    return render(request, 'loads/home.jhtml', context)


@login_required(login_url='login')
def load_view(request, id):
    load = Load.objects.get(id=id)
    loads = Load.objects.all()
    try:
        detail = DetailUser.objects.get(user=load.user)
        company = detail.companyName
    except:
        company = ''

    paginator = Paginator(loads, 5)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'document_title': 'Load Detail -' + load.title,
        'load': load,
        'company': company,
        'loads': page_obj,

    }
    return render(request, 'loads/loadview.jhtml', context)


@login_required(login_url='login')
def profile_view(request, id):
    user = User.objects.get(id=id)

    loads = user.load_set.all()

    try:
        detailuser = DetailUser.objects.get(user=user)
    except:
        detailuser = ''

    paginator = Paginator(loads, 4)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'document_title': 'Profile',
        'user': user,
        'detailuser': detailuser,
        'loads': page_obj,
    }
    return render(request, 'loads/profile.jhtml', context)


@login_required(login_url='login')
def edit_profile_view(request, id):
    user = User.objects.get(id=id)
    isInstance = False

    try:
        detail = DetailUser.objects.get(user=user)
        detail_form = EditProfileForm(instance=detail)
        isInstance = True
    except:
        messages.warning(request, "Please complete your profile to take full advantage of our site")
        detail_form = EditProfileForm() # Update the ID when saving
        isInstance = False
    
    if isInstance:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=detail)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect('home')
    else:
        if request.method == 'POST':
            form = EditProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect('home')

    context = {
        'document_title': 'Edit Profile',
        'user': user,
        'detail': detail_form,
    }   
    return render(request, 'loads/editprofile.jhtml', context)


@login_required(login_url='login')
def messages_view(request, id):
    user = User.objects.get(id=id)
    msg = DirectMessage.objects.all()
    
    msg_lst = [m for m in msg if m.toUser == user]
    
    if len(msg_lst) > 0:
        last_msg = msg_lst[0]

    context = {
        'document_title': 'Messages',
        'msg_lst': msg_lst,
        'msg': last_msg,
    }
    return render(request, 'loads/messages.jhtml', context)


@login_required(login_url='login')
def message_view(request, id):
    msg = DirectMessage.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    msgs = DirectMessage.objects.all()

    msg_lst = [m for m in msgs if m.toUser == user]

    if request.method == 'POST':
        DirectMessage.objects.create(
            toUser = msg.user,
            user = request.user,
            title = request.POST.get('title'),
            body = request.POST.get('message'),
            replyto = msg.id,
        )
        return redirect('messages', id=request.user.id)

    msg.read = True
    msg.save()

    context = {
        'document_title': 'Messages',
        'msg_lst': msg_lst,
        'msg': msg,
    }
    return render(request, 'loads/message.jhtml', context)


@login_required(login_url='login')
def send_message_view(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        DirectMessage.objects.create(
            toUser = user,
            user = request.user,
            title = request.POST.get('title'),
            body = request.POST.get('message'),
        )
        return redirect('messages', id=request.user.id)

    context = {
        'document_title': 'Message',
        'user': user,
    }
    return render(request, 'loads/message_send.jhtml', context)