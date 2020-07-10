from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from home.authhelper import get_signin_url, get_token_from_code, get_access_token
from home.outlookservice import get_me
import time
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from course import views
from django.contrib import auth
from urllib.parse import quote, urlencode
from home.authhelper import loginFLOW
import datetime
# from django.auth import logout
import os

#cred = credentials.Certificate('./iitg-speech-lab-firebase-adminsdk-ggn1f-2f757184a1.json')
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

# Create your views here.


# Create your views here.


def home(request):
    redirect_uri = 'http://localhost:8001/home/gettoken/'
    
    sign_in_url = get_signin_url(redirect_uri)
    data = db.collection(u'Homepage').document("homepage").get().to_dict()
    pics = db.collection(u'Homepage').document("HomeImages").get().to_dict()
    pics_list = [i for i in enumerate(pics['Image'])]
    context = {'sign_in_url': sign_in_url,
                'data' : data,
                'pics' : pics_list}
    context = loginFLOW(request, context)
    return render(request, 'home/home.html', context)

def faq(request):
    data = db.collection(u'Homepage').document("faq").get().to_dict()
    temp = [item for item in enumerate(data['qa'])]
    context = {'stuff' : temp}
    context = loginFLOW(request, context)
    return render(request, 'home/faq.html', context)

def contactus(request):
    data = db.collection(u'Homepage').document("contactUs").get().to_dict()
    context = loginFLOW(request, data)
    return render(request, 'home/contactus.html', context)

def addProject(request, uinfo):
    context = {}
    context = loginFLOW(request, context)

    if context['username'] == '':
        return HttpResponse('You are not authorized.')
    elif context['username'] != uinfo:
        return HttpResponse('You are not authorized.')

    user_dict = db.collection(u'Users').document(uinfo).get().to_dict()
    if 'isAdmin' in user_dict:
        context["isAdmin"] = "True"
    else:
        context["isAdmin"] = "False"
    context["Designation"] = user_dict['Designation']

    return render(request, 'home/addproject.html', context)

def projectDelete(request, pinfo):
    context = {}
    context = loginFLOW(request, context)

    if context['username'] == '':
        return HttpResponse("You are not logged in")

    project_dict = db.collection(u'Projects').document(pinfo).get().to_dict()
    user = project_dict['Creator'].get()

    if context['username'] != user.id:
        return HttpResponse("You are not authorized.")

    db.collection(u'Projects').document(pinfo).delete()
    return HttpResponseRedirect("/users/" + user.id + "/")

def projectEdit(request, pinfo):
    context = {}
    context = loginFLOW(request, context)

    if context['username'] == '':
        return HttpResponse("You are not logged in")

    project_dict = db.collection(u'Projects').document(pinfo).get().to_dict()
    user = project_dict['Creator'].get()

    if context['username'] != user.id:
        return HttpResponse("You are not authorized.")

    context['project'] = project_dict

    return render(request, "home/editproject.html", context)

def projectUpdate(request, pinfo):
    context = {}
    if request.method == 'POST':
        context = loginFLOW(request, context)

        if context['username'] == '':
            return HttpResponse("You are not logged in")

        project_dict = db.collection(u'Projects').document(pinfo).get().to_dict()
        creator = project_dict['Creator'].get().id

        if context['username'] != creator:
            return HttpResponse("You are not authorized")

        updated_project = {}
        updated_project['Title'] = request.POST.get('title')
        updated_project['AboutProject'] = request.POST.get('about')
        if request.POST.get('cmurl') != '':
            updated_project["Media"] = request.POST.get('cmurl')
        updated_project['Mentor'] = request.POST.get('mentors')
        updated_project['People'] = request.POST.get('people')
        updated_project['Achievements'] = request.POST.get('achievements')

        db.collection(u'Projects').document(pinfo).update(updated_project)

        return HttpResponseRedirect("/home/projects/" + pinfo)
    return HttpResponseRedirect(reverse('home:home'))


def add(request, uinfo):
    context = {}
    if request.method == 'POST':
        context = loginFLOW(request, context)
        if context['username'] != uinfo:
            return HttpResponse("You are not authorized")

        username = context['username']
        project = {}
        project['Title'] = request.POST.get('title')
        project['AboutProject'] = request.POST.get('about')
        project['Creator'] = db.collection(u'Users').document(username)
        project["Media"] = request.POST.get('cmurl')
        project['Mentor'] = request.POST.get('mentors')
        project['People'] = request.POST.get('people')
        project['Achievements'] = request.POST.get('achievements')

        db.collection(u'Projects').add(project)

        return HttpResponseRedirect("/users/" + username)
    return HttpResponseRedirect(reverse('home:home'))


def gettoken(request):
    # return HttpResponse('gettoken view')
    try:
        auth_code = request.GET['code']
    except:
        return HttpResponseRedirect(reverse('home:home'))
    redirect_uri = 'http://localhost:8001/home/gettoken/'
    print(redirect_uri)
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user = get_me(access_token)
    refresh_token = token['refresh_token']
    expires_in = token['expires_in']
    print(user)

    username = user['userPrincipalName']
    print(user)
    username = username.replace("@outlook.com", "")
    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()

    if user_dict is None:
        if username!='abcdsh3':
            des = "Student"
            print('username\n')
            data = {
                u'Username': username,
                u'FullName': user['displayName'],
                u'Program': user['jobTitle'],
                u'Designation': des,
                u'About': "",
                u'Contact': "",
                u'Department': "CSE",
                u'ProfilePic': "https://firebasestorage.googleapis.com/v0/b/speechlab-40e3b.appspot.com/o/pp.png?alt=media&token=52bae678-5e47-4fc8-a736-084dbafbefcf",
                u'RollNumber': user["surname"],
                u'URL': {
                    'Github': '',
                    'Homepage': '',
                    'Linkedin': ''
                },
                u'Email': user['mail']
            }
            db.collection(u'Users').document(username).set(data)
        else:
            des = "Faculty"
            data = {
                u'Username': username,
                u'FullName': user['displayName'],
                u'CollegeDesignation': user['jobTitle'],
                u'Designation': des,
                u'About': "",
                u'Contact': "",
                u'Department': "CSE",
                u'ProfilePic': "https://firebasestorage.googleapis.com/v0/b/speechlab-40e3b.appspot.com/o/pp.png?alt=media&token=52bae678-5e47-4fc8-a736-084dbafbefcf",
                u'RoomNumber': "",
                u'URL': {
                    'Github': '',
                    'Homepage': '',
                    'Linkedin': ''
                },
                u'Email': user['mail'],
                u'ProfCourseList':[]
            }
            db.collection(u'Users').document(username).set(data)



    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + expires_in - 300


    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    request.session['token_expires'] = expiration
    # request.session.flush()
    # auth.logout(request)
    # logout(request)

    # return HttpResponseRedirect("https://login.microsoftonline.com/common/oauth2/logout?post_logout_redirect_uri =http://localhost:8000/home/")
    # return HttpResponse('Roll {0}'.format(user['jobTitle']))
    return HttpResponseRedirect("/users/" + username)



def logout(request):
    request.session['access_token'] = None
    return HttpResponseRedirect(reverse('home:home'))


def ViewUser(request, uinfo):
    # db.collection(u'Courses').document('Webd 223_abcdsh3_2020').delete()
    context = {}
    context = loginFLOW(request, context)

    if context['username'] != uinfo:
        return HttpResponse("You are not authorized")

    profile = db.collection(u'Users').document(context['username'])
    profile_dict = profile.get().to_dict()

    context['profile'] = profile_dict


    all_projects = db.collection(u'Projects').where(u'Creator', u'==', profile).get()
    project_list = []
    for x in all_projects:
        project = x.to_dict()
        project['id'] = x.id
        project_list.append(project)
    if 'isAdmin' in profile_dict:
        context["isAdmin"] = "True"
    else:
        context["isAdmin"] = "False"

    context['Designation'] = profile_dict['Designation']
    context['projects'] = project_list
    
    if not project_list:
        context['isProjects'] = "False"
    else:
        context['isProjects'] = "True"

    return render(request, 'home/profile.html', context)


def student(request):
    user_ref = db.collection(u'Users').get()
    user_list = []
    count = 0
    counter_list = []
    for user in user_ref:
        user_dict = user.to_dict()
        # print(user_dict["Designation"])
        if user_dict["Designation"] == 'Student':
            user_list.append(user_dict)

            counter_list.append(count % 3)
            count += 1
    uc_list = zip(user_list, counter_list)
    context = {'uc_list': uc_list}
    context = loginFLOW(request, context)
    return render(request, 'home/people.html', context)


def faculty(request):
    user_ref = db.collection(u'Users').get()
    user_list = []
    count = 0
    counter_list = []
    for user in user_ref:
        user_dict = user.to_dict()
        if user_dict["Designation"] == 'Faculty':
            user_list.append(user.to_dict())
            counter_list.append(count % 3)
            count += 1
    uc_list = zip(user_list, counter_list)
    context = {'uc_list': uc_list}
    context = loginFLOW(request, context)

    return render(request, 'home/people.html', context)


def projects(request):
    context = {}
    projects = db.collection(u'Projects').get()
    project_list = []
    for x in projects:
        project = x.to_dict()
        project['id'] = x.id
        project_list.append(project)

    context['projects'] = project_list
    context = loginFLOW(request, context)
    return render(request, 'home/projects.html', context)


def projectView(request, pinfo):
    project_ref = db.collection(u'Projects').document(pinfo).get()
    project_dict = project_ref.to_dict()

    context = {'Project': project_dict}
    context = loginFLOW(request, context)
    context['CreatorName'] = project_dict['Creator'].get().to_dict()['FullName']
    return render(request, 'home/viewProject.html', context)


def editProfile(request, uinfo):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('home:gettoken')))
    if not access_token:
        return HttpResponse("You are not logged in")
    user = get_me(access_token)
    username = user['userPrincipalName'].replace("@outlook.com", "")
    if username != uinfo:
        return HttpResponse("You are not authorized")
    user = db.collection(u'Users').document(username).get()
    user_dict = user.to_dict()
    user_dict["id"] = user.id
    t = 0
    if user_dict["Designation"] == "Student":
        t = 1
    if user_dict["Designation"] == "Faculty":
        t = 0
    context = {'isStudent': t, 'user': user_dict}
    context = loginFLOW(request, context)
    if 'isAdmin' in user_dict:
        context["isAdmin"] = "True"
    else:
        context["isAdmin"] = "False"
    context['Designation'] = user_dict['Designation']
    return render(request, 'home/editProfile.html', context)

def editContact(request, uinfo):
    context = {}
    loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(context['sign_in_url'])
    elif context['username'] != uinfo:
        return HttpResponse('You are not authorized')

    user_dict = db.collection(u'Users').document(context['username']).get().to_dict()
    contact_dict = db.collection(u'Homepage').document(u'contactUs').get().to_dict()

    if 'isAdmin' in user_dict:
        context["isAdmin"] = "True"
    else:
        context["isAdmin"] = "False"
    context["Designation"] = user_dict['Designation']


    if context['isAdmin'] == "False":
        return HttpResponse('Sorry, you do not have authorization rights')

    context['Contact'] = contact_dict
    return render(request, "home/editcontact.html", context)

def saveContact(request, uinfo):
    if request.method == 'POST':
        access_token = get_access_token(request, request.build_absolute_uri(reverse('home:gettoken')))
        if not access_token:
            return HttpResponse("You are not logged in")
        user = get_me(access_token)
        username = user['mail'].replace("@iitg.ac.in", "")
        if username != uinfo:
            return HttpResponse("You are not authorized")

        contact = db.collection(u'Homepage').document(u'contactUs').get()
        contact_dict = contact.to_dict()

        contact_dict["Email"] = request.POST.get('email')
        contact_dict["Location"] = request.POST.get('address')
        contact_dict["PhoneNumber"] = request.POST.get('phone')

        db.collection(u'Homepage').document(u'contactUs').set(contact_dict)
        return HttpResponseRedirect("/users/" + username)
    return HttpResponseRedirect(reverse('home:home'))

def editHome(request, uinfo):
    context = {}
    loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(context['sign_in_url'])
    elif context['username'] != uinfo:
        return HttpResponse('You are not authorized')

    user_dict = db.collection(u'Users').document(context['username']).get().to_dict()
    home_dict = db.collection(u'Homepage').document(u'homepage').get().to_dict()

    if 'isAdmin' in user_dict:
        context["isAdmin"] = "True"
    else:
        context["isAdmin"] = "False"
    context["Designation"] = user_dict['Designation']


    if context['isAdmin'] == "False":
        return HttpResponse('Sorry, you do not have authorization rights')

    home_list = home_dict['paragraphs']
    count = []
    counter = 0
    for item in home_dict['paragraphs']:
        counter += 1
        count.append(counter)

    final_list = zip(count, home_list)
    context['home_list'] = final_list
    context['section_no'] = counter

    return render(request, "home/edithome.html", context)

def saveHome(request, uinfo):
    if request.method == 'POST':
        access_token = get_access_token(request, request.build_absolute_uri(reverse('home:gettoken')))
        if not access_token:
            return HttpResponse("You are not logged in")
        user = get_me(access_token)
        username = user['mail'].replace("@iitg.ac.in", "")
        if username != uinfo:
            return HttpResponse("You are not authorized")

        home_list = []
        if request.POST.get('newT') != '' and request.POST.get('newC') != '':
            home_list.append({'title' : request.POST.get('newT'), 'text' : request.POST.get('newC')})
        for i in range(int(request.POST.get('section_no'))):
            if request.POST.get('t'+str(i+1)) != '' and request.POST.get('c'+str(i+1)) != '':
                home_list.append({'title' : request.POST.get('t'+str(i+1)), 'text' : request.POST.get('c'+str(i+1))})

        home_dict = {'paragraphs' : home_list}
        db.collection(u'Homepage').document(u'homepage').set(home_dict)

        return HttpResponseRedirect("/users/" + username + "/editHome/")
    return HttpResponseRedirect(reverse('home:home'))

def editFaq(request, uinfo):
    context = {}
    loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(context['sign_in_url'])
    elif context['username'] != uinfo:
        return HttpResponse('You are not authorized')

    user_dict = db.collection(u'Users').document(context['username']).get().to_dict()
    faq_dict = db.collection(u'Homepage').document(u'faq').get().to_dict()

    if 'isAdmin' in user_dict:
        context["isAdmin"] = "True"
    else:
        context["isAdmin"] = "False"
    context["Designation"] = user_dict['Designation']

    if context['isAdmin'] == "False":
        return HttpResponse('Sorry, you do not have authorization rights')

    faq_list = faq_dict['qa']
    count = []
    counter = 0
    for item in faq_dict['qa']:
        counter += 1
        count.append(counter)

    final_list = zip(count, faq_list)
    context['faq_list'] = final_list
    context['numberOfFAQ'] = counter

    return render(request, "home/editfaq.html", context)

def saveFaq(request, uinfo):
    if request.method == 'POST':
        access_token = get_access_token(request, request.build_absolute_uri(reverse('home:gettoken')))
        if not access_token:
            return HttpResponse("You are not logged in")
        user = get_me(access_token)
        username = user['mail'].replace("@iitg.ac.in", "")
        if username != uinfo:
            return HttpResponse("You are not authorized")

        faq_list = []
        if request.POST.get('newQ') != '' and request.POST.get('newA') != '':
            faq_list.append({'q' : request.POST.get('newQ'), 'a' : request.POST.get('newA')})
        for i in range(int(request.POST.get('numberOfFAQ'))):
            if request.POST.get('q'+str(i+1)) != '' and request.POST.get('a'+str(i+1)) != '':
                faq_list.append({'q' : request.POST.get('q'+str(i+1)), 'a' : request.POST.get('a'+str(i+1))})

        faq_dict = {'qa' : faq_list}
        db.collection(u'Homepage').document(u'faq').set(faq_dict)

        return HttpResponseRedirect("/users/" + username + "/editFaq/")
    return HttpResponseRedirect(reverse('home:home'))



def edit(request, uinfo):
    if request.method == 'POST':
        access_token = get_access_token(request, request.build_absolute_uri(reverse('home:gettoken')))
        if not access_token:
            return HttpResponse("You are not logged in")
        user = get_me(access_token)
        username = user['userPrincipalName'].replace("@outlook.com", "")
        if username != uinfo:
            return HttpResponse("You are not authorized")
        user = db.collection(u'Users').document(username).get()
        user_dict = user.to_dict()
        if request.POST.get('filename') != '':
            user_dict["ProfilePic"] = request.POST.get('cmurl')
        user_dict["About"] = request.POST.get('about_me')
        user_dict["Contact"] = request.POST.get('contact')
        user_dict["URL"]["Github"] = request.POST.get('github')
        user_dict["URL"]["Linkedin"] = request.POST.get('linkedin')
        user_dict["URL"]["Homepage"] = request.POST.get('homepage')
        db.collection(u'Users').document(username).set(user_dict)
        return HttpResponseRedirect("/users/" + username)
    return HttpResponseRedirect(reverse('home:home'))

def redirect_user(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('home:gettoken')))
    if not access_token:
        return HttpResponse("You are not logged in")
    user = get_me(access_token)
    username = user['userPrincipalName'].replace("@outlook.com", "")
    return HttpResponseRedirect("/users/" + username)
    

def noticeboard(request):
    data = db.collection(u'Homepage').document("NoticeBoard").get().to_dict()
    temp = [item for item in enumerate(data['AllNotices'])]
    context = {'stuff' : temp}
    context = loginFLOW(request, context)
    return render(request, 'home/noticeboard.html', context)

def addNotice(request, uinfo):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] != uinfo:
        return HttpResponse("You are not authorized")
    
    user_dict = db.collection(u'Users').document(uinfo).get().to_dict()
    if 'isAdmin' in user_dict:
        context['isAdmin'] = "True"
    else:
        context['isAdmin'] = "False"
    context['Designation'] = user_dict['Designation']
    return render(request, 'home/addnotice.html', context)

def saveNotice(request,uinfo):
    context = {}
    if request.method == 'POST':
        context = loginFLOW(request, context)

        if context['username'] != uinfo:
            return HttpResponse("You are not authorized")

        user_dict = db.collection(u'Users').document(uinfo).get().to_dict()
        
        if user_dict['Designation'] != 'Faculty' and 'isAdmin' not in user_dict:
            return HttpResponse("You are not authorized")
        
        new_notice = {  'title' : request.POST.get('title'),
                        'text' : request.POST.get('text'),
                        'author' : user_dict['FullName'],
                        'created' : datetime.datetime.now(),}

        notices_dict = db.collection(u'Homepage').document(u'NoticeBoard').get().to_dict()
        notices_dict['AllNotices'].append(new_notice)

        print(notices_dict)

        db.collection(u'Homepage').document(u'NoticeBoard').set(notices_dict)

        return HttpResponseRedirect("/home/noticeboard/")
    return HttpResponseRedirect(reverse('home:home'))