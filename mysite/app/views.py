from django.shortcuts import render
from .forms import newPersonForm
from django.http import HttpResponseRedirect
from . import sql_scripts


def index(request):
    return render(request, 'app/index.html')

def addPerson(request):
    return render(request, 'app/addPerson.html', {'form': newPersonForm()})

def addPerson_get(request):
    data = newPersonForm(request.POST).data
    sql_scripts.executeSQL([sql_scripts.addPerson(data["name"])])
    return HttpResponseRedirect("/app/addPerson")







