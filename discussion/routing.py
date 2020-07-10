from django.conf.urls import url
from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/discussion/user/<slug:username>/courses/<slug:CourseID>/coursegroup/<slug:CourseGroupID>', consumers.ChatConsumer),
    path('ws/discussion/user/<slug:username>/courses/<slug:CourseID>/assignments/<slug:AssignmentID>/groups/<slug:GroupID>', consumers.ChatConsumer2),
]
