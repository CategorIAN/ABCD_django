from django.shortcuts import render
from .forms import newPersonForm, FormRequestForm, InvitationForm, SimpleEventForm, PersonForm
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from . import sql_scripts
from urllib.parse import urlencode
from datetime import datetime, timedelta
from .sql_scripts import *
from .Person import Person


def index(request):
    return render(request, 'app/index.html')
#=======================================================================================================================
def updatePerson(request):
    return render(request, 'app/updatePerson.html', {'form': newPersonForm()})

def updatePerson_get(request):
    if "add" in request.POST:
        data = newPersonForm(request.POST).data
        executeSQL(addPerson(data["name"]))
        return HttpResponseRedirect("/app/updatePerson")
    if "delete" in request.POST:
        data = newPersonForm(request.POST).data
        executeSQL(*deletePerson(data["name"]))
        return HttpResponseRedirect("/app/updatePerson")
#=======================================================================================================================
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
#=======================================================================================================================
def addInvitation(request):
    event_id = request.GET.get('event_id')
    t = None if event_id is None else (Event.objects.get(pk=event_id).timestamp-timedelta(weeks=1)).strftime('%Y-%m-%d')
    settings = {"classes": 'table table-striped table-hover', 'index': False}
    call_list_html = "" if event_id is None else callListDF(event_id).to_html(**settings)
    meal_stats_html = "" if event_id is None else readSQL(mealStats(event_id)).to_html(**settings)
    context = {
        'event_form': SimpleEventForm(initial={'event': event_id}),
        'invitation_form': InvitationForm(initial={'event': event_id, 'timestamp': t}),
        'current_event_id': event_id,
        'call_list': call_list_html,
        'meal_stats': meal_stats_html,
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
    if "call_list" in request.POST:
        df = callListDF(event)
        checkboxes = df.shape[0] * [{col: False for col in ['Invited', 'Going',
                                                            'Plus One', 'Waiting', 'Declined', 'Flaked']}]
        call_list = pd.concat([df['name'], pd.DataFrame(checkboxes), df.loc[:, df.columns != 'name']], axis=1)
        print(call_list)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="call_list_{event}.csv"'
        call_list.to_csv(path_or_buf=response, index=False)
        return response
#=======================================================================================================================
def personalProfile(request):
    person = request.GET.get('person')
    person_info = Person(person)
    context = {
        'person': person,
        'person_form': PersonForm(initial={'name': person}),
        'data': "\n".join([person_info.readText(), person_info.readLinScale(), person_info.readMultChoice()])
    }
    return render(request, 'app/PersonProfile.html', context)

def personalProfile_get(request, person):
    person_id = PersonForm(request.POST).data['name']
    return HttpResponseRedirect(f"/app/personalProfile?{urlencode({'person': person_id})}")







