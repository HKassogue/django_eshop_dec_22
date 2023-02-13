from django.shortcuts import render, redirect
from .forms import LoginForm

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        from django.contrib.auth import authenticate, login
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
           context['errors'] = True
    return render(request, 'myauth/login.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    from django.contrib.auth.forms import UserCreationForm
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        from eshop.models import Customer
        Customer(user=user).save()
        from django.contrib.auth import authenticate, login
        login(request, 
            authenticate(username=user.username, password=form.cleaned_data['password1']))
        return redirect('home')
    return render(request, 'myauth/register.html', {'form': form})