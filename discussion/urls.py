from django.contrib import admin
from django.urls import path
from . import views

app_name = 'discussion'

urlpatterns = [
    # CourseGroup Discussion Room
    path('courses/<slug:CourseID>/coursegroup/<slug:CourseGroupID>', views.course_group, name='course_group'),
    # Course individual groups
    path('courses/<slug:CourseID>/assignments/<slug:AssignmentID>/groups/<slug:GroupID>', views.group, name='group'),
    #Course Notice Board
    path('courses/<slug:CourseID>/noticeboard', views.notice_board, name='notice_board'),
    #Add Notice
    path('courses/<slug:CourseID>/noticeboard/addnotice', views.add_notice, name='add_notice'),
    # Calender
    path('courses/<slug:CourseID>/calendar', views.view_calendar, name='view_calendar'),
    # Add Event
    path('courses/<slug:CourseID>/events', views.add_event, name='events'),
    # Delete Event
    path('courses/<slug:CourseID>/delete_event/<slug:EventID>', views.delete_event, name='delete_event'),
    # Create Calendar (testing only)
    path('courses/<slug:CourseID>/create_calendar', views.create_calendar, name='create_calendar'),
]
