from django.shortcuts import render
from .forms import newPersonForm, FormRequestForm, InvitationForm, SimpleEventForm
from .models import *
from django.http import HttpResponseRedirect
from . import sql_scripts
from urllib.parse import urlencode
from datetime import datetime, timedelta
from .sql_scripts import *


def index(request):
    return render(request, 'app/index.html')

def addPerson(request):
    return render(request, 'app/addPerson.html', {'form': newPersonForm()})

def addPerson_get(request):
    data = newPersonForm(request.POST).data
    sql_scripts.executeSQL(sql_scripts.addPerson(data["name"]))
    return HttpResponseRedirect("/app/addPerson")

def addRequest(request):
    df = readSQL("SELECT * FROM PERSON_GENERAL_DUE")
    context = {
        'form': FormRequestForm(),
        'df_html': df.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'app/addRequest.html', context)

def addRequest_get(request):
    data = FormRequestForm(request.POST).data
    sql_scripts.executeSQL(sql_scripts.request(data["person"], data["form"], data["timestamp"]))
    return HttpResponseRedirect("/app/addRequest")

def addInvitation(request):
    event_id = request.GET.get('event_id')
    t = None if event_id is None else (Event.objects.get(pk=event_id).timestamp-timedelta(weeks=1)).strftime('%Y-%m-%d')
    settings = {"classes": 'table table-striped table-hover', 'index': False}
    if event_id is None:
        call_list = ""
    else:
        df = readSQL(f"Select event_plan from event where eventid = '{event_id}'")
        event_plan = df['event_plan'].iloc[0]
        if event_plan == "None":
            call_list = readSQL(callList(event_id)).to_html(**settings)
        else:
            call_list = readSQL(plannedCallList(event_id)).to_html(**settings)
    context = {
        'event_form': SimpleEventForm(initial={'event': event_id}),
        'invitation_form': InvitationForm(initial={'event': event_id, 'timestamp': t}),
        'current_event_id': event_id,
        'call_list': call_list
    }
    return render(request, 'app/addInvitation.html', context)

def addInvitation_get(request, event):
    if "get_event" in request.POST:
        event_id = SimpleEventForm(request.POST).data['event']
        return HttpResponseRedirect(f"/app/addInvitation?{urlencode({'event_id': event_id})}")
    if "invite" in request.POST:
        data = InvitationForm(request.POST).data
        input = {x: data[x] for x in ["event", "timestamp", "person", "plus_ones", "result"]}
        executeSQL(invite(**input))
        return HttpResponseRedirect(f"/app/addInvitation?{urlencode({'event_id': event})}")







