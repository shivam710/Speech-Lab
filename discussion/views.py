from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.shortcuts import redirect
from django.urls import reverse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from . import consumers

from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2

from home.authhelper import loginFLOW
from datetime import datetime

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "speechlab-40e3b",
    "private_key_id": "0c72055efb04e25425e2fc454cbacf0d4ec4ff46",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDoPJ6DnatZcx3Y\nCuNBhGFA1pmoRE9hVd5wVvpbEUaDP75PQeWWatb4l5nuEQpg5hgEQfJ6LXjehoZN\n+jGJL51H0mO3YxcFpIq4imSbiEI8/y69hveiJCS12J6SErtzpSkb1z/Hmn/e87FT\naf6rJ6OLNXsA70fWoYovqIaB1rtJAjZIFR3GAoDZ6CVoklCVRvGPUXQZVbsJBfwQ\nY2/gS1Q29Rpa6HUnvquDidIwhPzKS86y+xaD/+yV981JTM8QEzhjKv8Fmwv9pOBw\nSJkwa2GhESvizaeE2yuDm9/ElImykFOP2JtwRjVtra8dWcY3x15LeWaYMi9SudEt\nzX7Qm/iXAgMBAAECggEADaYVEYUrCeHIcjxe6NMqkrtKDT1JMQjxPsb4hcZOekOS\ndWlZC0MSM/VXovSLbfB39DVwARrlDKb5WQyIQW4en0GlLKT9OGQC5x+dvr+pAkQO\nb4McJgJbyfgw3ELk6MIJ2CIJaeYRon0jVyoBQUveF74NPEZ+gVsTGllG4SCeodwL\nvKr+nrAPj8hM7kC6TJUFtaZ5JEi2+kEwBULbmYMXuy2OHr5Lv4xr3RaVmJ6B0zHk\nS//uJQbV6O/5Ukwg2td+zCU1WHE+4I1s1r3YcyhB58AwmM8xA6hYbuYX4njGC+t0\nGiCTjAHcOZUTvsIDg1mc2i+/RLFWjMh4KjNO5ANkYQKBgQD+FBAh+KYzmh5F/pRq\nXExLhijRwshrXmfH6+6e66hNS63zEI3S9TYOZxRal5kAGAVFl5InybyNs1V11tAR\nXgNN5DkEHkK9XSTbUipplG0IzA9dM2ESB4AF3A5NrXlGt0i+nBNtqqq7Vwzw9Y/u\n7NSwdpFNk7WfZi+59pHoQg57JwKBgQDp/kRwM/suIccfVqau2+g37OvVLXbUJ6Y6\nRYqrk+3OS5alzBwfwnZ8WsA3d66+WaFh4MAw7ehXH76/x2CMweExcAjbC8XMMTfQ\nM10BLCchSgXiBsuHise45uc5TNUsYbwo14tJmp80pcuGOalMsIrCUO8t4WACs1WK\n7j7Fuba9EQKBgBEdyuRu+stZI5b1iowLwbwIwrE23QeWqYknVMDyATmL0qEgSV2f\n1U9tFEryEYWXGKvShS8XARPOtAAnQ4cX/UL/D/Q+EaLuJnB7/Y11SU8haBuQPYbY\naIB8jZ4gBJ6F9Gma3Bg0OiI6wA1vjY27+KwWoL1IKSEe4jI18ShjYtRbAoGACj5U\nVqkf5NwbsHaFo4ADAXfAtztfSVhXAZQLxwkZzv8mICn4TTehIj6CzarSnoij9Pn2\nz+2KT04XdqPOyTqvlg92g8hXJ2I8NEQbXTLGn8Fy0ntDq7JanfCVzL9dUa0RpKQS\n9+zp7U8Yws6BZ9cOrAUJA3QrVNLu+r8FRnij1FECgYEApzgWBveYHNn0QzkWRz/B\nldB+I0CoMuNT9w5cVZpwj+s2D5zFl6A/WCn6ZzbcH5ZqA2R/n0YGwlfrQ9nfACxe\nqPoy+Mhnl0wXsMSrjXfE8ZhL3uVRpwIjK8es5ixFh6i+y9C/9ppW2ePYwEd4eNMq\nnqxrE9t50lXmiKRzfNH6tRE=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-2m0dg@speechlab-40e3b.iam.gserviceaccount.com",
    "client_id": "108831226506513377533",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2m0dg%40speechlab-40e3b.iam.gserviceaccount.com"
})
# firebase_admin.initialize_app(cred)
db = firestore.client()


# Calender
flags = tools.argparser.parse_args([])
FLOW = OAuth2WebServerFlow(
    client_id='378262545952-1r36bf3nd2bjad3641sprit3020rcpem.apps.googleusercontent.com',
    client_secret='vMX5C3nvgZ2OKkr1b0aXcZex',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='IITG-Speech-Lab'
    )
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = tools.run_flow(FLOW, storage, flags)

httpObject = httplib2.Http()
httpObject = credentials.authorize(httpObject)
service = discovery.build('calendar', 'v3', http=httpObject)


def course_group(request, CourseID, CourseGroupID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    # context['CourseGroupID_json'] = mark_safe(json.dumps(CourseGroupID))
    # context['CourseID_json'] = mark_safe(json.dumps(CourseID))
    context['CourseGroupID_json'] = CourseGroupID
    context['CourseID_json'] = CourseID
    # return render(request, 'discussion/group.html', {
    #     'CourseGroupID_json' : mark_safe(json.dumps(CourseGroupID)),
    #     'CourseID_json' : mark_safe(json.dumps(CourseID)),
    # })
    return render(request, 'discussion/group.html', context)

# def group(request, CourseID, AssignmentID, GroupID):
#     context = {}
#     context = loginFLOW(request, context)
#     if context['username'] == '':
#         return HttpResponseRedirect(reverse('home:home'))

#     username = context['username']

#     context['GroupID_json'] = mark_safe(json.dumps(GroupID))
#     context['CourseID_json'] = mark_safe(json.dumps(CourseID))
#     context['AssignmentID_json'] = mark_safe(json.dumps(AssignmentID))
#     # return render(request, 'discussion/group.html', {
#     #     'GroupID_json' : mark_safe(json.dumps(GroupID)),
#     #     'CourseID_json' : mark_safe(json.dumps(CourseID)),
#     #     'AssignmentID_json' : mark_safe(json.dumps(AssignmentID)),
#     # })
#     return render(request, 'discussion/group.html', context)



def group(request, CourseID, AssignmentID, GroupID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    context['GroupID_json'] =  GroupID
    context['CourseID_json'] = CourseID
    context['AssignmentID_json'] = AssignmentID
    # return render(request, 'discussion/group.html', {
    #     'GroupID_json' : mark_safe(json.dumps(GroupID)),
    #     'CourseID_json' : mark_safe(json.dumps(CourseID)),
    #     'AssignmentID_json' : mark_safe(json.dumps(AssignmentID)),
    # })
    return render(request, 'discussion/group.html', context)

def notice_board(request,CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    Designation = user_dict['Designation']

    # CourseID = self.scope['url_route']['kwargs']['CourseID']
    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Notices')
    # #
    all_notice=[]
    docs = list(doc_ref.get())
    for i in range(len(docs)):
        id = docs[i].id
        doc = docs[i]
        doc = doc.to_dict()
        temp={
            'NoticeHead' : doc['NoticeHead'],
            'NoticeBody': doc['NoticeBody'],
            'Author': doc['Author'],
            'NoticeTime': doc['NoticeTime'],
        }
        all_notice.append(temp)

    context['all_notice'] = all_notice
    context['title'] = CourseID
    context['Designation'] = Designation
    # context={
    #     "all_notice":all_notice,
    #     "title":CourseID
    # }
    return render(request,'discussion/notice.html',context)

def add_notice(request,CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    NoticeHead = request.POST['NoticeHead']
    if NoticeHead=="":
        NoticeHead="Notice"
    NoticeBody = request.POST['NoticeBody']
    print(NoticeHead)
    print(NoticeBody)
    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Notices').add({'Author' : username,'NoticeHead' : NoticeHead, 'NoticeBody' : NoticeBody, 'NoticeTime':firestore.SERVER_TIMESTAMP})
    return redirect('/discussion/courses/'+CourseID+'/noticeboard')

def view_calendar(request, CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CourseID:
                CalendarID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        context['CourseID'] = CourseID
        context['CalendarID'] = CalendarID
        # return render(request, 'discussion/calendar.html', {'CourseID': CourseID, 'CalendarID': CalendarID})
        return render(request, 'discussion/calendar.html', context)


def add_event(request, CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CourseID:
                CalendarID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    if request.method == 'POST':
        Summary = request.POST['Summary']
        Location = request.POST['Location']
        Description = request.POST['Description']
        StartDate = request.POST['Start']
        EndDate = request.POST['End']

        event = {
            'summary': Summary,
            'location': Location,
            'description': Description,
            'start': {
                'dateTime': StartDate+'T00:00:00+0530',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': EndDate+'T23:59:59+0530',
                'timeZone': 'America/Los_Angeles',
            },
            'visibility': 'public',
        }

        event = service.events().insert(calendarId=CalendarID, body=event).execute()
        return redirect('/discussion/courses/'+CourseID+'/events')

    elif request.method == 'GET':
        events_result = service.events().list(calendarId=CalendarID, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        context['events'] = events
        context['CourseID'] = CourseID
        context['CalendarID'] = CalendarID

        dateToday = datetime.today().strftime('%Y-%m-%d')
        context['dateToday'] = dateToday
        return render(request, 'discussion/add_event.html', context)

def delete_event(request, CourseID, EventID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CourseID:
                CalendarID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    service.events().delete(calendarId=CalendarID, eventId=EventID).execute()
    return redirect('/discussion/courses/'+CourseID+'/events')

def create_calendar(request, CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    calendar = {
    'summary': CourseID,
    'timeZone': 'America/Los_Angeles'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()
    print(created_calendar['id'])
    return redirect('/discussion/courses/'+CourseID+'/')
