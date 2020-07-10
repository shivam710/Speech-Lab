from home.authhelper import loginFLOW
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound

from django.urls import reverse
from django.contrib import messages

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import random

from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2

from home.authhelper import loginFLOW
from datetime import datetime

# cred = credentials.Certificate('./iitg-speech-lab-firebase-adminsdk-ggn1f-2f757184a1.json')
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
firebase_admin.initialize_app(cred)
db = firestore.client()

# Calendar
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

def dashboard(request):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    Designation = user_dict['Designation']

    if Designation == "Faculty":
        ProfCourseList = user_dict['ProfCourseList']
        CourseDetails = []
        for course in ProfCourseList:
            CourseDetails.append(course.get().to_dict())
            print(course.get())

        context['CourseDetails'] = CourseDetails

        return render(request, 'course/main_page.html', context)

    elif Designation == "Student":
        if not 'CourseList' in user_dict:
            StudCourseList = []
        else:
            StudCourseList = user_dict['CourseList']

        # print(StudCourseList)
        RegisteredCourses = []
        TotalCourses = []
        TotalCourses1 = []
        for course in StudCourseList:
            RegisteredCourses.append(course['CourseID'].get().to_dict())

        Courses = db.collection(u'Courses').get()
        for course in Courses:
            TotalCourses1.append(course.to_dict())
        TACoursesL = []

        try:
            TACoursesList = db.collection(u'Users').document(username).get().to_dict()['CoursesListAsTA']
            for TA in TACoursesList:
                TACoursesL.append( TA.get().to_dict() )
        except:
            pass
    
        for course in TotalCourses1:
            if course not in RegisteredCourses and course not in TACoursesL:
                TotalCourses.append(course)

        context['RegisteredCourses'] = RegisteredCourses
        context['TotalCourses'] = TotalCourses
        context['TACoursesList'] = TACoursesL

        return render(request,'course/main_page_stud.html',context)


def getDesig(request, cinfo):
    context = {}
    context = loginFLOW(request, context)
    username = context['username']
    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    Designation = user_dict['Designation']
    if Designation == "Faculty":
        return "Faculty"

    CourseDict = db.collection("Courses").document(
        cinfo).get().to_dict()

    try:
        TAListref = CourseDict["TAList"]
        for TA in TAListref:
            if username == TA.get().to_dict()["Username"]:
                return "Faculty"
    except:
        pass

    try:
        StuRef = db.collection("Courses").document(
            cinfo).get().to_dict()["StudentList"]

        for Stu in StuRef:
            if username == Stu["StudentID"].get().to_dict()["Username"]:
                return "Student"
    except:
        pass

    return "UnRegStu"


def Enroll_CoursePage(request, cinfo):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    # user_ref = db.collection(u'Users').document(username).get()
    # user_dict = user_ref.to_dict()
    Designation = getDesig(request, cinfo)
    print(Designation)
    if Designation != "UnRegStu":
        return HttpResponse(status=511)
    print(Designation)
    context['CourseInfo'] = cinfo

    if request.method == 'POST':
        postdata = request.POST.get("Enrollment")
        main = db.collection(u'Courses').document(cinfo).get().to_dict()

        try:
            copydata = db.collection(u'Users').document(
                username).get().to_dict()['CourseList']
        except:
            copydata = []

        datay = {
            u'CourseID':  db.collection(u'Courses').document(cinfo)
        }
        copydata.append(datay)

        atndata = {
            u'StudentID': db.collection(u'Users').document(username),
            u'TotalAttendance': 0
        }

        try:
            attendance_list = db.collection(u'Courses').document(
                cinfo).get().to_dict()['AttendanceList']
        except:
            attendance_list = []

        attendance_list.append(atndata)

        dbdata = main['EnrollmentKey']
        # dbdata = postdata

        try:
            stn_list = db.collection(u'Courses').document(
                cinfo).get().to_dict()['StudentList']
        except:
            stn_list = []

        pushdata = {
            u'StudentID': db.collection(u'Users').document(username),
            u'Grade': 0
        }
        stn_list.append(pushdata)

        if dbdata == postdata:
            data = {
                u'CourseList': copydata
            }
            attndata = {
                u'AttendanceList': attendance_list
            }
            StnList = {
                u'StudentList': stn_list
            }
            print('hello shivam\n')
            db.collection(u'Users').document(username).update(data)
            db.collection(u'Courses').document(cinfo).update(attndata)
            db.collection(u'Courses').document(cinfo).update(StnList)
        return HttpResponseRedirect(reverse('course:dashboard'))
    else:
        return render(request, 'course/enrollcourse.html', context)


def Update_Attendance(request, cinfo, aid, gid):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty" and Designation != "TA":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    context['Designation']=Designation

    if request.method == 'POST':
        checkedstudent = request.POST.getlist('checks[]')
        for student in checkedstudent:
            userref = db.collection(u'Users').document(student)
            courseref = db.collection(u'Courses').document(cinfo).get()
            attendance_list = courseref.to_dict()['AttendanceList']
            index = 0
            check = 0
            while (check == 0):
                try:
                    stud_username = attendance_list[index]['StudentID'].get().to_dict()[
                        'Username']
                    if stud_username == student:
                        attendance_list[index]['TotalAttendance'] = attendance_list[index]['TotalAttendance'] + 1
                        data = {
                            u'AttendanceList': attendance_list
                        }
                        db.collection(u'Courses').document(cinfo).update(data)
                        check = 1
                    index = index + 1
                except:
                    check = 1

        return HttpResponseRedirect(reverse('course:dashboard'))
    else:
        group_ref = db.collection(u'Courses').document(cinfo).collection(
            u'Assignments').document(aid).collection(u'Groups').document(gid).get()
        try:
            studentlist = group_ref.to_dict()['StudentList']
        except:
            studentlist = ""
        index = 0
        studentinfo = []
        check = 0
        while(check == 0):
            try:
                studentinfo.append(
                    studentlist[index]['StudentID'].get().to_dict())
                index = index + 1
            except:
                check = 1

        print(studentinfo)
        context['cinfo'] = cinfo
        context['aid'] = aid
        context['gid'] = gid
        context['studentinfo'] = studentinfo
        # {
        #     'cinfo': cinfo,
        #     'aid': aid,
        #     'gid': gid,
        #     'studentinfo': studentinfo,
        # }
        return render(request, 'course/updateattendance.html', context)


def Show_Attendance(request, cinfo):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    Designation = getDesig(request, cinfo)

    context['Designation'] = Designation

    course_ref = db.collection(u'Courses').document(cinfo).get()
    print(course_ref)
    print('course\n\n')
    course_arr = course_ref.to_dict()['AttendanceList']
    list = []
    for user in course_arr:
        grade = 0
        for users in course_ref.to_dict()['StudentList']:
            if users['StudentID'] == user['StudentID']:
                grade = users['Grade']

        temp_dict = {
            "StudentName": user['StudentID'].get().to_dict()['FullName'],
            "Attendance": user['TotalAttendance'],
            "grade": grade,
            "Image": user['StudentID'].get().to_dict()['ProfilePic']
        }
        list.append(temp_dict)

    context['list'] = list
    context['CourseInfo'] = cinfo
    # {
    #     'list': list,
    #     'CourseInfo': cinfo,
    # }

    return render(request, 'course/show_attendance.html', context)


def Add_Grade(request, cinfo, aid, gid):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty" and Designation != "TA":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    context['Designation'] = Designation

    group_ref = db.collection(u'Courses').document(cinfo).collection(
        u'Assignments').document(aid).collection(u'Groups').document(gid)
    group_data = group_ref.get().to_dict()['StudentList']
    if request.method == "POST":
        for user in group_data:
            Igrade = user['Grade']
            user['Grade'] = int(request.POST.get(
                user['StudentID'].get().to_dict()['username']))
            user_ref = user['StudentID']
            Course_Data = db.collection(u'Courses').document(
                cinfo).get().to_dict()['StudentList']
            for users in Course_Data:
                if users['StudentID'] == user['StudentID']:
                    users['Grade'] = users['Grade'] + user['Grade'] - Igrade
            data = {
                u'StudentList': Course_Data
            }
            db.collection(u'Courses').document(cinfo).update(data)
        data_main = {
            u'StudentList': group_data
        }
        db.collection(u'Courses').document(cinfo).collection(u'Assignments').document(
            aid).collection(u'Groups').document(gid).update(data_main)
        return HttpResponseRedirect(reverse('course:dashboard'))

    else:
        user_list = []
        for user in group_data:
            user_list.append(user['StudentID'].get().to_dict())

        context['user_list'] = user_list
        context['cinfo'] = cinfo
        context['aid'] = aid
        context['gid'] = gid
        # {
        #     'user_list': user_list,
        #     'cinfo': cinfo,
        #     'aid': aid,
        #     'gid': gid
        # }
        return render(request, 'course/addgrade.html', context)


def AddCourse(request):


    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    Designation = user_dict['Designation']
    if Designation != "Faculty":
        return HttpResponse(status=511)

    if request.method == 'POST':
        CourseID = request.POST.get("CourseID", "")

        ref_prof = db.collection(u'Users').document(username)
        data = {
            u'AboutCourse': request.POST.get("AboutCourse", ""),
            u'CourseID': request.POST.get("CourseID", ""),
            u'CourseName': request.POST.get("CourseName", ""),
            u'Weightage': int(request.POST.get("Weightage", "")),
            u'EnrollmentKey': request.POST.get("EnrollmentKey", ""),
            u'EndSemester': {
                u'SemesterType':  request.POST.get("EndSemesterType", ""),
                u'Session': int(request.POST.get("EndSemesterSession", ""))
            },
            u'StartSemester': {
                u'SemesterType':  request.POST.get("StartSemesterType", ""),
                u'Session': int(request.POST.get("StartSemesterSession", ""))
            },
            u'FacultyList': [ref_prof],
            u'CourseInfo': request.POST.get("CourseID", "") + "_" + username + "_" + request.POST.get("StartSemesterSession", ""),
            u'AttendanceList':[],
            u'StudentList':[]

        }
        cid = request.POST.get("CourseID", "")

        cinfo = cid + "_" + username + "_" + \
            request.POST.get("StartSemesterSession", "")

        db.collection(u'Courses').document(cinfo).set(data)

        course_ref = db.collection(u'Courses').document(cinfo)

        prof_data = db.collection(u'Users').document(username).get().to_dict()
        print(prof_data)
        CoursesList = prof_data['ProfCourseList']
        CoursesList.append(course_ref)

        db.collection(u'Users').document(username).update({
            u'ProfCourseList': CoursesList
        })

        calendar = {
        'summary': cinfo,
        'timeZone': 'America/Los_Angeles'
        }

        created_calendar = service.calendars().insert(body=calendar).execute()
        print(created_calendar['id'])

        # return render(request,'course/main_page.html')
        return HttpResponseRedirect(reverse('course:dashboard'))

    return render(request, 'course/addcourseform.html')


def ViewCourse(request, cinfo):
    Designation = getDesig(request, cinfo)
    if Designation == "UnRegStu":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    # cid += "_" + username + " _" + cyear
    assgn_ref = db.collection(u'Courses').document(
        cinfo).collection(u'Assignments').get()
    AssgnDetails = []
    for assgn in assgn_ref:
        AssgnDetails.append(assgn.to_dict())
    context['AssgnDetails'] = AssgnDetails
    context['CourseInfo'] = cinfo
    context['Designation'] = Designation
    # {
    #     'AssgnDetails': AssgnDetails,
    #     'CourseInfo': cinfo
    # }
    return render(request, 'course/viewcourse.html', context)


def AddAssgn(request, cinfo):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty" and Designation != "TA":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    context['CourseInfo'] = cinfo

    if request.method == 'POST':
        ref_prof = db.collection(u'Users').document(username)
        nxtID = len(list(db.collection(u'Courses').document(
            cinfo).collection(u'Assignments').get()))+1
        nextAssID = "AS{}".format(nxtID)
        data = {
            u'About': request.POST.get("About", ""),
            u'AssignmentID': nextAssID,
            u'Deadline': request.POST.get("Deadline", ""),
            u'Name': request.POST.get("Name", ""),
        }
        # aid = request.POST.get("AssignmentID", "")
        db.collection(u'Courses').document(cinfo).collection(
            u'Assignments').document(nextAssID).set(data)

        return HttpResponseRedirect(reverse('course:view_course', kwargs={'cinfo': cinfo}))

    return render(request, 'course/addassgnform.html',context)


def UpAssgn(request, cinfo, aid):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty" and Designation != "TA":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    AssgnDetails = db.collection(u'Courses').document(cinfo).collection(
        u'Assignments').document(aid).get().to_dict()
    context = {
        'CourseInfo': cinfo,
        'AssgnDetails': AssgnDetails,
    }

    if request.method == 'POST':
        ref_prof = db.collection(u'Users').document(username)
        data = {
            u'About': request.POST.get("About", ""),
            u'AssignmentID': aid,
            u'Deadline': request.POST.get("Deadline", ""),
            u'Name': request.POST.get("Name", ""),
        }
        # aid = request.POST.get("AssignmentID", "")
        db.collection(u'Courses').document(cinfo).collection(
            u'Assignments').document(aid).set(data)

        return HttpResponseRedirect(reverse('course:view_course', kwargs={'cinfo': cinfo}))

    else:
        return render(request, 'course/upassgn.html', context)


def viewTA(request, cinfo):
    Designation = getDesig(request, cinfo)
    if Designation == "UnRegStu":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()

    try:
        TAList = db.collection(u'Courses').document(
            cinfo).get().to_dict()["TAList"]
    except:
        TAList = ""

    talist = list()

    for TA in TAList:
        talist.append(TA.get().to_dict())

    context['TA'] = talist
    context['CourseInfo'] = cinfo
    context['Designation'] = Designation
    # {
    #     'TA': talist,
    #     'CourseInfo': cinfo
    # }

    return render(request, 'course/viewTA.html', context)


def ViewAssgn(request, cinfo, aid):
    Designation = getDesig(request, cinfo)
    print(Designation)
    if Designation == "UnRegStu":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()

    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    # Designation = user_dict['Designation']

    group_ref = db.collection(u'Courses').document(cinfo).collection(
        u'Assignments').document(aid).collection(u'Groups').get()
    GroupDetails = []
    for group in group_ref:
        GroupDetails.append(group.to_dict())

    context['GroupDetails'] = GroupDetails
    context['cinfo'] = cinfo
    context['aid'] = aid
    context['Designation'] = Designation
    # {
    #     'GroupDetails': GroupDetails,
    #     'cinfo': cinfo,
    #     'aid': aid,
    # }
    MyGroupList = []

    if Designation == 'Student':
        for group in GroupDetails:
            studs = group['StudentList']
            for stud in studs:
                if stud['StudentID'] == db.collection(u'Users').document(username):
                    MyGroupList.append(group)
    else:
        MyGroupList = GroupDetails

    context['MyGroupList'] = MyGroupList
    return render(request, 'course/viewassgn.html', context)


def AddTA(request, cinfo):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    BTech, MTech, Phd = getStudents()
    context['BTech'] = BTech
    context['MTech'] = MTech
    context['Phd'] = Phd
    context['CourseInfo'] = cinfo
    # {
    #     'BTech': BTech,
    #     'MTech': MTech,
    #     'Phd': Phd,
    #
    # }

    if request.method == 'POST':
        ref_course = db.collection(u'Courses').document(cinfo)
        stuType = request.POST.get("TA_BRANCH", "")
        stuID = request.POST.get(stuType+"TA", "")
        stuID = stuID.split('-')[1]
        ref_TA = db.collection(u'Users').document(stuID)

        if 'TAList' not in ref_course.get().to_dict():
            currTA = []
        else:
            currTA = ref_course.get().to_dict()['TAList']

        if ref_TA not in currTA:
            currTA.append(ref_TA)
        else:
            # show error message or resolve before hand
            pass

        # aid = request.POST.get("AssignmentID", "")
        data = {
            u'TAList': currTA
        }
        db.collection(u'Courses').document(cinfo).update(data)

        if not 'CoursesListAsTA' in ref_TA.get().to_dict():
            coursesAsTA = []
        else:
            coursesAsTA = ref_TA.get().to_dict()['CoursesListAsTA']

        if not ref_course in coursesAsTA:
            coursesAsTA.append(ref_course)
        else:
            pass

        ref_TA.update({
            u'CoursesListAsTA': coursesAsTA
        })

        return HttpResponseRedirect(reverse('course:view_course', kwargs={'cinfo': cinfo}))

    return render(request, 'course/AddTA.html', context)


def getStudents():

    users_ref = db.collection(u'Users').get()
    BTech = []
    MTech = []
    Phd = []

    for user in users_ref:
        userdict = user.to_dict()

        # Remove the first if condition
        if "Designation" in userdict.keys() and userdict["Designation"] == "Student":

            # if userdict["Program"].upper() == "BTECH":
            #     BTech.append(userdict)

            # if userdict["Program"].upper() == "MTECH":
            #     MTech.append(userdict)

            # if userdict["Program"].upper() == "PHD":
            #     Phd.append(userdict)
            BTech.append(userdict)

    return BTech, MTech, Phd


def AddCourseMaterial(request, cinfo):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty" and Designation != "TA":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    context = {
        'CourseInfo': cinfo,
    }
    return render(request, 'course/addcoursematerial.html', context)


def ViewCourseMaterial(request, cinfo):
    Designation = getDesig(request, cinfo)
    if Designation == "UnRegStu":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    # Designation = user_dict['Designation']

    course_data = db.collection(u'Courses').document(cinfo).get().to_dict()

    course_data = db.collection(u'Courses').document(cinfo).get().to_dict()
    if not 'CourseMaterial' in course_data:
        CMaterials = []
    else:
        CMaterials = course_data['CourseMaterial']

    context['CMaterials'] = CMaterials
    context['CourseInfo'] = cinfo
    context['Designation'] = Designation
    # {
    #     'CMaterials': CMaterials,
    #     'CourseInfo': cinfo
    # }
    return render(request, 'course/viewcoursematerial.html', context)


def StoreCMinDb(request, cinfo):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    if request.method == 'POST':
        course_data = db.collection(u'Courses').document(cinfo).get().to_dict()
        newcm = {}
        newcm['Name'] = request.POST.get('filename')
        newcm['Url'] = request.POST.get('cmurl')

        if not 'CourseMaterial' in course_data:
            cm_array = [newcm]
            db.collection(u'Courses').document(cinfo).update({
                u'CourseMaterial': cm_array
            })
        else:
            cm_array = course_data['CourseMaterial']
            cm_array.append(newcm)
            db.collection(u'Courses').document(cinfo).update({
                u'CourseMaterial': cm_array
            })
        # print(newcm)
        # print(cm_array)

        return HttpResponseRedirect(reverse('course:view_course_material', kwargs={'cinfo': cinfo}))
    else:
        return HttpResponseRedirect(reverse('course:view_course_material', kwargs={'cinfo': cinfo}))


def Update_Submission(request, cinfo, aid, gid):
    Designation = getDesig(request, cinfo)
    if Designation == "UnRegStu":
        return HttpResponse(status=511)

    StudentList = db.collection('Courses').document(cinfo).collection("Assignments").document(
        aid).collection("Groups").document(gid).get().to_dict()["StudentList"]

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    context['sub'] = ''
    context['cinfo'] = cinfo
    context['aid'] = aid
    context['gid'] = gid
    context['Designation'] = Designation

    updPer = False
    for stu in StudentList:
        if username == stu["StudentID"].get().to_dict()["Username"]:
            updPer = True
            break
    else:
        if Designation != "Faculty" and Designation != "TA":
            return HttpResponse(status=511)


    group = db.collection(u'Courses').document(cinfo).collection(
        u'Assignments').document(aid).collection(u'Groups').document(gid)

    print(group.get().to_dict())

    
    # {
    #     'sub': '',
    #     'CourseInfo': cinfo,
    #     'aid': aid,
    #     'gid': gid
    # }

    if request.method == 'POST':
        # get submission file from the request and store it in the database
        newcm = {
            'Name': request.POST.get('filename'),
            'Url': request.POST.get('cmurl')
        }
        print(context)
        group.update({u'SubmissionFile': newcm})

        return HttpResponseRedirect(reverse('course:up_submission', kwargs={
            'cinfo': cinfo,
            'aid': aid,
            'gid': gid
        }))

    else:
        # display submission file to the users
        try:
            context['sub'] = group.get().to_dict()['SubmissionFile']
        except:
            pass
        return render(request, 'course/addSubmission.html', context)


def ViewGroup(request, cinfo, aid, gid):
    Designation = getDesig(request, cinfo)
    if Designation == "UnRegStu":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    # cid += "_" + username + " _" + cyear

    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    # Designation = user_dict['Designation']
    context['Designation'] = Designation

    group_ref = db.collection(u'Courses').document(cinfo).collection(
        u'Assignments').document(aid).collection(u'Groups').document(gid).get()
    GroupDetails = group_ref.to_dict()
    studs = GroupDetails['StudentList']
    StudentDetails = []
    for stud in studs:
        StudentDetails.append(stud['StudentID'].get().to_dict())
    context['cinfo'] = cinfo
    context['aid'] = aid
    context['GroupDetails'] = GroupDetails
    context['StudentDetails'] = StudentDetails
    # {
    #     'cinfo' : cinfo,
    #     'aid' : aid,
    #     'GroupDetails' : GroupDetails,
    #     'StudentDetails' : StudentDetails,
    # }
    print(Designation)
    return render(request, 'course/viewgroup.html', context)


def UpdateGroup(request, cinfo, aid, gid):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    context['cinfo'] = cinfo
    context['aid'] = aid
    context['gid'] = gid
    context['Designation'] = Designation

    username = context['username']

    if request.method == 'POST':
        # ref_prof = db.collection(u'Users').document(username)
        data = {
            u'ProjectTitle': request.POST.get("ProjectTitle", ""),
            u'ProblemStatement': request.POST.get("ProblemStatement", "")
        }
        print(data)
        db.collection(u'Courses').document(cinfo).collection(u'Assignments').document(
            aid).collection(u'Groups').document(gid).update(data)
        group_ref = db.collection(u'Courses').document(cinfo).collection(
            u'Assignments').document(aid).collection(u'Groups').document(gid).get()
        GroupDetails = group_ref.to_dict()
        studs = GroupDetails['StudentList']
        StudentDetails = []
        for stud in studs:
            StudentDetails.append(stud['StudentID'].get().to_dict())
        context['cinfo'] = cinfo
        context['aid'] = aid
        context['gid'] = gid
        context['GroupDetails'] = GroupDetails
        context['StudentDetails'] = StudentDetails
        # {
        #     'cinfo' : cinfo,
        #     'aid' : aid,
        #     'GroupDetails' : GroupDetails,
        #     'StudentDetails' : StudentDetails,
        # }

        return render(request, 'course/viewgroup.html', context)

    return render(request, 'course/updategroupform.html',context)


def RandomGroups(request, cinfo, aid):
    Designation = getDesig(request, cinfo)
    if Designation != "Faculty" and Designation != "TA":
        return HttpResponse(status=511)

    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']
    context['Designation'] = Designation
    context['aid'] = aid

    if request.method == 'GET':
        context['cinfo'] = cinfo
        return render(request, 'course/random_groups.html', context)
    elif request.method == 'POST':
        NumGroups = request.POST['NumGroups']
        NumGroups = int(NumGroups)

        StudList = db.collection(u'Courses').document(
            cinfo).get().to_dict()['StudentList']
        random.shuffle(StudList)

        GroupList = []
        for i in range(NumGroups):
            GroupList.append([])
        for i in range(len(StudList)):
            GroupList[i % NumGroups].append(StudList[i])

        print(GroupList)

        for i in range(len(GroupList)):
            if len(GroupList[i]) > 0:
                data = {
                    u'GroupID': 'GID_'+str(i+1),
                    u'ProblemStatement': '',
                    u'ProjectTitle': '',
                    u'StudentList': GroupList[i],
                }

                db.collection(u'Courses').document(cinfo).collection(u'Assignments').document(
                    aid).collection(u'Groups').document('GID_'+str(i+1)).set(data)

        return redirect('/courses/'+cinfo+'/assignments/'+aid)
