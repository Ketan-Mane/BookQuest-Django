from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import UserForm,ProfileForm
from django.contrib import messages
from payment.models import MemberShip
from BookQuestApp.views import updateMemberShip

User = get_user_model()

# Create your views here.

def register(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Successfull..!')
            return redirect("/accounts/login")
        else:
            return render(request,'register.html',{'form':form})
    else:
        form = UserForm()
        return render(request,'register.html',{'form':form})
    

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username,password=password)
            
            if user is not None:
                auth.login(request,user)
                next_url = request.GET.get('next')
                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect("/") 
            else:
                messages.error(request,"Invalid Username & Password")
            return redirect("/accounts/login")
        else:
            return render(request,'login.html')


@login_required(login_url="/accounts/login")
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url="/accounts/login")
def profile(request):
    updateMemberShip()
    membership = MemberShip.objects.filter(user=request.user).exists()
    if membership:
        membership = MemberShip.objects.get(user=request.user)
    if request.method=="POST":
        form = ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated..!")
            return redirect("/accounts/profile")
        else:
            return render(request,'profile.html',{'form':form,'membership':membership})
    else:
        form = ProfileForm(instance=request.user)
        return render(request,'profile.html',{'form':form,'membership':membership})