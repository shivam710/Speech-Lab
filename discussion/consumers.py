from course import views

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import ntplib

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

import hashlib
import time

# cred = credentials.Certificate("iitg-speech-lab-firebase-adminsdk-ggn1f-2f757184a1.json")
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

# -------------------------------------------------------------------------------------------------------------------------------
#Receive and sending messages
class ChatConsumer(WebsocketConsumer):
    print("con1")


    def connect(self):
        print("Connected")
        curAuthor = self.scope['url_route']['kwargs']['username']
        print(curAuthor+"bakchodi")
        self.room_name = self.scope['url_route']['kwargs']['CourseID']
        print(self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        print('channel')
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print("Connected1")
        

        #Retrieve messages from Firebase
        CourseID = self.scope['url_route']['kwargs']['CourseID']
        CourseGroupID = self.scope['url_route']['kwargs']['CourseGroupID']
        print(CourseID)
        print(CourseGroupID)
        doc_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').order_by(u'PostTime')

        docs = list(doc_ref.get())

        self.accept()
        print("Connected2")

        for i in range(len(docs)):
            id = docs[i].id
            doc = docs[i]
            doc = doc.to_dict()
            if (doc['IsPoll'] == False):
                self.send(text_data=json.dumps({
                    'IsPoll': doc['IsPoll'],
                    'messageHead' : doc['MessageHead'],
                    'message': doc['MessageBody'],
                    'Author':doc['Author'],
                    'MessageID': id,
                    'IsReply': False,
                    'ShowReply': False,
                }))
            else:
                self.send(text_data=json.dumps({
                    'IsPoll': doc['IsPoll'],
                    'PollQues': doc['PollQues'],
                    'Author':doc['Author'],
                    'MessageID': id,
                    'IsReply': False,
                    'ShowReply': False,
                }))
        print("Connected3")


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        curAuthor = self.scope['url_route']['kwargs']['username']
        print(curAuthor)
        text_data_json = json.loads(text_data)
        IsPoll = text_data_json['IsPoll']
        CourseID = text_data_json['CourseID']
        CourseGroupID = text_data_json['CourseGroupID']
        MessageID = ''
        # IsReply = ''
        # message = ''
        # messageHead = ''
        # ReplyBody = ''
        print(text_data_json)
        if (IsPoll == False):
            # hash = hashlib.sha1()
            # hash.update(str(time.time()))
            # print(hash.hexdigest())
            # MessageID = hash.hexdigest()[:20]

            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org')
            # MessageID = str(response.tx_time)
            MessageID = 'a' + hashlib.sha224(str(response.tx_time).encode()).hexdigest()[:25]

            ShowReply = text_data_json['ShowReply']
            if (ShowReply == False):
                IsReply = text_data_json['IsReply']
                message = text_data_json['message']
                messageHead = text_data_json['messageHead']
                ReplyBody = text_data_json['ReplyBody']
                if not IsReply:
                    # hash = hashlib.sha1()
                    # hash.update(str(time.time()))
                    # print(hash.hexdigest())
                    # MessageID = hash.hexdigest()[:20]
                    client = ntplib.NTPClient()
                    response = client.request('pool.ntp.org')
                    # MessageID = str(response.tx_time)
                    MessageID = 'a' + hashlib.sha224(str(response.tx_time).encode()).hexdigest()[:25]

                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').document(MessageID).set({'Author' : curAuthor,'MessageHead' : messageHead, 'MessageBody' : message,'IsPoll': False,'PostTime':firestore.SERVER_TIMESTAMP})

                else:
                    MessageID = text_data_json['MessageID']
                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').document(MessageID).collection(u'Replies').add({'Author' : curAuthor,'MessageID' : MessageID, 'PostTime' : firestore.SERVER_TIMESTAMP, 'ReplyBody': ReplyBody})

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'ShowReply': False,
                        'Author': curAuthor,
                        'IsReply': IsReply,
                        'messageHead' : messageHead,
                        'message': message,
                        'ReplyBody': ReplyBody,
                        'MessageID': MessageID,
                    }
                )
            else:
                MessageID = text_data_json['MessageID']
                doc_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').document(MessageID).collection(u'Replies').order_by(u'PostTime')
                replies = list(doc_ref.get())
                for i in range(len(replies)):
                    replies[i] = replies[i].to_dict()
                    replies[i]['PostTime']=str(replies[i]['PostTime'])
                    print(replies[i])
                # Send reply to user in group
                text_data=json.dumps({
                    'IsPoll': False,
                    'ShowReply': True,
                    'IsReply': True,
                    'Replies': replies,
                    'MessageID' : MessageID,
                })
                # print(text_data)
                self.send(text_data)
        else:
            ShowReply = text_data_json['ShowReply']
            if (ShowReply == False):
                IsReply = text_data_json['IsReply']
                if (IsReply == False):
                    PollQues = text_data_json['PollQues']
                    # PollOptNum = text_data_json['PollOptNum']
                    PollOpt = []
                    for i in range(len(text_data_json['PollOptions'])):
                        PollOpt.append(text_data_json['PollOptions'][i])
                    DBPoll = {
                        'Author': curAuthor,
                        'PollQues': PollQues,
                        'PollOpt': PollOpt,
                        'IsPoll': True,
                        'PostTime':firestore.SERVER_TIMESTAMP,
                    }
                    client = ntplib.NTPClient()
                    response = client.request('pool.ntp.org')
                    # MessageID = str(response.tx_time)
                    MessageID = 'a' + hashlib.sha224(str(response.tx_time).encode()).hexdigest()[:25]

                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').document(MessageID).set(DBPoll)

                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'poll_message',
                        'Author': curAuthor,
                        'PollQues': PollQues,
                        'PollOpt': PollOpt,
                        'IsReply': IsReply,
                        'MessageID': MessageID,
                    })
                else:
                    UserOpt = int(text_data_json['UserOpt'])
                    MessageID = text_data_json['MessageID']
                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').document(MessageID).collection(u'Replies').document(curAuthor)
                    # print(UserOpt)
                    DBPollUpdate = {
                        'MessageID': MessageID,
                        'ReplyBody': UserOpt,
                        'PostTime':firestore.SERVER_TIMESTAMP,
                        'Author': curAuthor,
                    }
                    doc_ref.set(DBPollUpdate)

            else:
                MessageID = text_data_json['MessageID']
                doc_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').document(MessageID)
                Poll = doc_ref.get().to_dict()
                PollOpt = Poll['PollOpt']
                PollCnt = []
                for i in range(len(PollOpt)):
                    PollCnt.append(0);

                rep_ref = db.collection(u'Courses').document(CourseID).collection(u'CourseGroup').document(CourseGroupID).collection(u'Messages').document(MessageID).collection(u'Replies')
                replies = list(rep_ref.get())

                userOpt = -1
                for i in range(len(replies)):
                    replies[i] = replies[i].to_dict()
                    PollCnt[replies[i]['ReplyBody']] = PollCnt[replies[i]['ReplyBody']] + 1
                    if (replies[i]['Author'] == curAuthor):
                        userOpt = replies[i]['ReplyBody']

                text_data=json.dumps({
                    'IsPoll': True,
                    'ShowReply': True,
                    'IsReply': True,
                    'PollOpt': PollOpt,
                    'PollCnt': PollCnt,
                    'UserOpt': userOpt,
                    'MessageID': MessageID,
                })
                self.send(text_data)


    # Receive poll from room group
    def poll_message(self, event):

        Author=event['Author']
        PollQues = event['PollQues']
        PollOpt = event['PollOpt']
        IsReply = event['IsReply']
        MessageID = event['MessageID']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'ShowReply': False,
            'Author':Author,
            'IsReply': IsReply,
            'IsPoll': True,
            'PollQues': PollQues,
            'PollOpt': PollOpt,
            'MessageID': MessageID,
        }))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        messageHead = event['messageHead']
        IsReply = event['IsReply']
        ReplyBody = event['ReplyBody']
        MessageID = event['MessageID']
        Author=event['Author']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'ShowReply': False,
            'Author':Author,
            'IsReply': IsReply,
            'IsPoll': False,
            'messageHead' : messageHead,
            'message': message,
            'ReplyBody': ReplyBody,
            'MessageID': MessageID,
        }))

#-----------------------------------------------------------------------------------------------------------------
class ChatConsumer2(WebsocketConsumer):
    curAuthor = 'Utkarsh'

    def connect(self):
        curAuthor = self.scope['url_route']['kwargs']['username']
        # print('Not yet opened', open)
        self.room_name = self.scope['url_route']['kwargs']['CourseID']+self.scope['url_route']['kwargs']['AssignmentID']+self.scope['url_route']['kwargs']['GroupID']
        # print(self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.channel_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        #Retrieve messages from Firebase
        CourseID = self.scope['url_route']['kwargs']['CourseID']
        GroupID = self.scope['url_route']['kwargs']['GroupID']
        AssignmentID=self.scope['url_route']['kwargs']['AssignmentID']
        doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').order_by(u'PostTime')

        docs = list(doc_ref.get())

        self.accept()

        for i in range(len(docs)):
            id = docs[i].id
            doc = docs[i]
            doc = doc.to_dict()
            if (doc['IsPoll'] == False):
                self.send(text_data=json.dumps({
                    'IsPoll': doc['IsPoll'],
                    'messageHead' : doc['MessageHead'],
                    'message': doc['MessageBody'],
                    'Author':doc['Author'],
                    'MessageID': id,
                    'IsReply': False,
                    'ShowReply': False,
                }))
            else:
                self.send(text_data=json.dumps({
                    'IsPoll': doc['IsPoll'],
                    'PollQues': doc['PollQues'],
                    'Author':doc['Author'],
                    'MessageID': id,
                    'IsReply': False,
                    'ShowReply': False,
                }))


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # print("Jeronemo")
        curAuthor = self.scope['url_route']['kwargs']['username']
        text_data_json = json.loads(text_data)
        IsPoll = text_data_json['IsPoll']
        CourseID = self.scope['url_route']['kwargs']['CourseID']
        GroupID = self.scope['url_route']['kwargs']['GroupID']
        AssignmentID=self.scope['url_route']['kwargs']['AssignmentID']
        MessageID = ''
        # IsReply = ''
        # message = ''
        # messageHead = ''
        # ReplyBody = ''
        if (IsPoll == False):
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org')
            # MessageID = str(response.tx_time)
            MessageID = 'a' + hashlib.sha224(str(response.tx_time).encode()).hexdigest()[:25]

            # hash = hashlib.sha1()
            # hash.update(str(time.time()))
            # print(hash.hexdigest())
            # MessageID = hash.hexdigest()[:20]
            ShowReply = text_data_json['ShowReply']
            if (ShowReply == False):
                IsReply = text_data_json['IsReply']
                message = text_data_json['message']
                messageHead = text_data_json['messageHead']
                ReplyBody = text_data_json['ReplyBody']
                if not IsReply:
                    client = ntplib.NTPClient()
                    response = client.request('pool.ntp.org')
                    # MessageID = str(response.tx_time)
                    MessageID = 'a' + hashlib.sha224(str(response.tx_time).encode()).hexdigest()[:25]

                    # hash = hashlib.sha1()
                    # hash.update(str(time.time()))
                    # print(hash.hexdigest())
                    # MessageID = hash.hexdigest()[:20]
                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').document(MessageID).set({'Author' : curAuthor,'MessageHead' : messageHead, 'MessageBody' : message,'IsPoll': False,'PostTime':firestore.SERVER_TIMESTAMP})

                else:
                    MessageID = text_data_json['MessageID']
                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').document(MessageID).collection(u'Replies').add({'Author' : curAuthor,'MessageID' : MessageID, 'PostTime' : firestore.SERVER_TIMESTAMP, 'ReplyBody': ReplyBody})

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'ShowReply': False,
                        'Author': curAuthor,
                        'IsReply': IsReply,
                        'messageHead' : messageHead,
                        'message': message,
                        'ReplyBody': ReplyBody,
                        'MessageID': MessageID,
                    }
                )
            else:
                MessageID = text_data_json['MessageID']
                doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').document(MessageID).collection(u'Replies').order_by(u'PostTime')
                replies = list(doc_ref.get())
                for i in range(len(replies)):
                    replies[i] = replies[i].to_dict()
                    replies[i]['PostTime']=str(replies[i]['PostTime'])
                    print(replies[i])
                # Send reply to user in group
                text_data=json.dumps({
                    'IsPoll': False,
                    'ShowReply': True,
                    'IsReply': True,
                    'Replies': replies,
                    'MessageID':MessageID
                })
                # print(text_data)
                self.send(text_data)
        else:
            ShowReply = text_data_json['ShowReply']
            if (ShowReply == False):
                IsReply = text_data_json['IsReply']
                if (IsReply == False):
                    PollQues = text_data_json['PollQues']
                    # PollOptNum = text_data_json['PollOptNum']
                    PollOpt = []
                    for i in range(len(text_data_json['PollOptions'])):
                        PollOpt.append(text_data_json['PollOptions'][i])
                    DBPoll = {
                        'Author': curAuthor,
                        'PollQues': PollQues,
                        'PollOpt': PollOpt,
                        'IsPoll': True,
                        'PostTime':firestore.SERVER_TIMESTAMP,
                    }
                    client = ntplib.NTPClient()
                    response = client.request('pool.ntp.org')
                    # MessageID = str(response.tx_time)
                    MessageID = 'a' + hashlib.sha224(str(response.tx_time).encode()).hexdigest()[:25]

                    # hash = hashlib.sha1()
                    # hash.update(str(time.time()))
                    # print(hash.hexdigest())
                    # MessageID = hash.hexdigest()[:20]
                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').document(MessageID).set(DBPoll)

                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'poll_message',
                        'Author': curAuthor,
                        'PollQues': PollQues,
                        'PollOpt': PollOpt,
                        'IsReply': IsReply,
                        'MessageID': MessageID,
                    })
                else:
                    UserOpt = int(text_data_json['UserOpt'])
                    MessageID = text_data_json['MessageID']
                    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').document(MessageID).collection(u'Replies').document(curAuthor)
                    # print(UserOpt)
                    DBPollUpdate = {
                        'MessageID': MessageID,
                        'ReplyBody': UserOpt,
                        'PostTime':firestore.SERVER_TIMESTAMP,
                        'Author': curAuthor,
                    }
                    doc_ref.set(DBPollUpdate)

            else:
                MessageID = text_data_json['MessageID']
                doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').document(MessageID)
                Poll = doc_ref.get().to_dict()
                PollOpt = Poll['PollOpt']
                PollCnt = []
                for i in range(len(PollOpt)):
                    PollCnt.append(0);

                rep_ref = db.collection(u'Courses').document(CourseID).collection(u'Assignments').document(AssignmentID).collection(u'Groups').document(GroupID).collection(u'Messages').document(MessageID).collection(u'Replies')
                replies = list(rep_ref.get())

                userOpt = -1
                for i in range(len(replies)):
                    replies[i] = replies[i].to_dict()
                    PollCnt[replies[i]['ReplyBody']] = PollCnt[replies[i]['ReplyBody']] + 1
                    if (replies[i]['Author'] == curAuthor):
                        userOpt = replies[i]['ReplyBody']

                text_data=json.dumps({
                    'IsPoll': True,
                    'ShowReply': True,
                    'IsReply': True,
                    'PollOpt': PollOpt,
                    'PollCnt': PollCnt,
                    'UserOpt': userOpt,
                    'MessageID': MessageID,
                })
                self.send(text_data)


    # Receive poll from room group
    def poll_message(self, event):

        Author=event['Author']
        PollQues = event['PollQues']
        PollOpt = event['PollOpt']
        IsReply = event['IsReply']
        MessageID = event['MessageID']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'ShowReply': False,
            'Author':Author,
            'IsReply': IsReply,
            'IsPoll': True,
            'PollQues': PollQues,
            'PollOpt': PollOpt,
            'MessageID': MessageID,
        }))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        messageHead = event['messageHead']
        IsReply = event['IsReply']
        ReplyBody = event['ReplyBody']
        MessageID = event['MessageID']
        Author=event['Author']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'ShowReply': False,
            'Author':Author,
            'IsReply': IsReply,
            'IsPoll': False,
            'messageHead' : messageHead,
            'message': message,
            'ReplyBody': ReplyBody,
            'MessageID': MessageID,
        }))
