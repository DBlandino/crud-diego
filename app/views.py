from django.shortcuts import render, redirect
from app.forms import CarrosForm, UsuariosForm
from app.models import Carros, Usuarios



# Create your views here.
def form(request):
    data = {}
    data['form'] = CarrosForm()
    return render(request, 'form.html', data)


def create(request):
    form = CarrosForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')


def view(request, pk):
    data = {}
    data['db'] = Carros.objects.get(pk=pk)
    return render(request, 'view.html', data)


def edit(request, pk):
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
    logado = request.session.get('logado')
    if (logado != 1):
        return render(request, 'index.html', { 'error': "Voce precisa logar primeiro" })
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
            return render(request, 'index.html', { 'logado': 1 })
    else:
        data['form'] = UsuariosForm()

    return render(request, 'login.html', data)
