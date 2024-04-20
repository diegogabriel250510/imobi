from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
# Create your views here.
def cadastro(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'preencha todos os campos')
            return redirect('/auth/cadastro')
        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, 'usuario já existe')
            return redirect('/auth/cadastro')
        try:
            user = User.objects.create_user(username=username,email=email,password=senha)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'usuario cadastrado com sucesso')
            return redirect('/auth/logar')
        except:
            messages.add_message(request, constants.ERROR, 'erro interno do sistema')
            return redirect('/auth/cadastro')

def logar(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, "logar.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username,password=senha)
        if not usuario:
            messages.add_message(request, constants.ERROR, 'usuario ou senha invalidos')
        else:
            auth.login(request, usuario)
            return redirect('/')
        
def sair(request):
    auth.logout(request)
    return redirect("/auth/logar")