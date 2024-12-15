from django.shortcuts import render
from .forms import newPersonForm, FormRequestForm
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

def addRequest(request):
    query = "SELECT * FROM person_general_due"
    df = sql_scripts.readSQL(query)
    context = {
        'form': FormRequestForm(),
        'df_html': df.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'app/addRequest.html', context)

def addRequest_get(request):
    data = FormRequestForm(request.POST).data
    sql_scripts.executeSQL([sql_scripts.request(data["person"], data["form"], data["timestamp"])])
    return HttpResponseRedirect("/app/addRequest")







