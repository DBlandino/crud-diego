from django.shortcuts import render, redirect
from django.core import serializers
from django.core.files import File
import zipfile as zip
import json
from app.forms import CarrosForm, UsuariosForm, SobreForm
from app.models import Carros, Usuarios, Sobre



# Create your views here.
def form(request):
    if request.method == 'GET':
        isLogged = request.session.get('isLogged')
        if isLogged != True:
            return redirect('login')

        data = {}
        data['form'] = CarrosForm()
        return render(request, 'form.html', data)


def create(request):
    form = CarrosForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')


def view(request, pk):
    if request.method == 'GET':
        isLogged = request.session.get('isLogged')
        if isLogged != True:
            return redirect('login')

        data = {}
        data['db'] = Carros.objects.get(pk=pk)
        return render(request, 'view.html', data)


def edit(request, pk):
    if request.method == 'GET':
        isLogged = request.session.get('isLogged')
        if isLogged != True:
            return redirect('login')

        data = {}
        data['db'] = Carros.objects.get(pk=pk)
        data['form'] = CarrosForm(instance=data['db'])
        return render(request, 'form.html', data)


def update(request, pk):
    data = {}
    data['db'] = Carros.objects.get(pk=pk)
    form = CarrosForm(request.POST or None, instance=data['db'])
    if form.is_valid():
        form.save()
        return redirect('home')



def delete(request, pk):
    db = Carros.objects.get(pk=pk)
    db.delete()
    return redirect('home')


def home(request):
    if request.method == 'GET':
        isLogged = request.session.get('isLogged')
        if isLogged != True:
            return redirect('login')
        
        data = {}
        search = request.GET.get('search')
        if search:
            data['db'] = Carros.objects.filter(modelo__icontains=search)
        else:
            data['db'] = Carros.objects.all()
        return render(request, 'index.html', data)



## login
def login(request):
    data = {}
    if request.method == 'POST':
        data['form'] = UsuariosForm(request.POST)
        if data['form'].is_valid():
            userEmail = data['form'].cleaned_data['email']
            usuarios = Usuarios.objects.filter(email=userEmail)
            if usuarios.count() > 0:
                request.session['isLogged'] = True
                return redirect('home')
    else:
        data['form'] = UsuariosForm()

    return render(request, 'login.html', data)

def formUser(request):
    if request.method == 'GET':
        isLogged = request.session.get('isLogged')
        if isLogged != True:
            return redirect('login')

        data = {}
        data['form'] = UsuariosForm()
        return render(request, 'cadastro.html', data)


def createUser(request):
    form = UsuariosForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')

def updateUser(request, pk):
    data = {}
    data['db'] = Usuarios.objects.get(pk=pk)
    form = UsuariosForm(request.POST or None, instance=data['db'])
    if form.is_valid():
        form.save()
        return redirect('home')


def users(request):
    if request.method == 'GET':
        isLogged = request.session.get('isLogged')
        if isLogged != True:
            return redirect('login')
        
        data = {}
        search = request.GET.get('search')
        if search:
            data['db'] = Usuarios.objects.filter(email__icontains=search)
        else:
            data['db'] = Usuarios.objects.all()
        return render(request, 'users.html', data)

def deleteUser(request, pk):
    db = Usuarios.objects.get(pk=pk)
    db.delete()
    return redirect('users')

def sobre(request):
    data = {}
    data['db'] = Sobre.objects.filter(pk=1)

    if data['db'].count() <= 0:
        s = Sobre(id=1, texto="")
        s.save()
        data['db'] = s
        data['form'] = SobreForm(instance=data['db'])
    else:
        data['form'] = SobreForm(instance=data['db'].get())

    return render(request, 'sobre.html', data)

def updateSobre(request):
    data = {}
    data['db'] = Sobre.objects.get(pk=1)
    form = SobreForm(request.POST or None, instance=data['db'])
    if form.is_valid():
        form.save()
        return redirect('home')

def logout(request):
    request.session['isLogged'] = None
    return redirect('login')

def exportAll(request):
    usuarios = list(Usuarios.objects.all())
    usuarios_list = serializers.serialize('json', usuarios)

    carros = list(Carros.objects.all())
    carros_list = serializers.serialize('json', carros)

    sobre = list(Sobre.objects.all())
    sobre_list = serializers.serialize('json', sobre)

    with open('./usuarios.json', 'w') as f:
        fUser = File(f)
        fUser.write(usuarios_list)

    with open('./carros.json', 'w') as f:
        fCar = File(f)
        fCar.write(carros_list)

    with open('./sobre.json', 'w') as f:
        fSobre = File(f)
        fSobre.write(sobre_list)

    zf = zip.ZipFile('./export.zip', 'w')
    zf.write('./usuarios.json')
    zf.write('./carros.json')
    zf.write('./sobre.json')
    zf.close()

    return redirect('sobre')
