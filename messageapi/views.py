import json
import io
import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message, Group
from .serializers import MessageSerializer, UserSerializer, GroupDataSerializer
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view

    
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
        json_data = request.body
        token_data = request.headers['Authorization']
        token_data = token_data.split(' ')
        token_data = token_data[1]
        token = Token.objects.get(key=token_data)
        user = token.user
        if user.is_superuser:
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            python_data['is_staff'] = True
            serializer = UserSerializer(data=python_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(json.dumps({'message': 'user created successfully! now you can signin'}))
            else:
                return HttpResponse(json.dumps(serializer.errors))
        
        else:
            return HttpResponse(json.dumps({'message': 'You do not have permission to create a user'}))

@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['PUT'])
def edit_user(request):
    if request.method == 'PUT':
        json_data = request.body
        token_data = request.headers['Authorization']
        token_data = token_data.split(' ')
        token_data = token_data[1]
        token = Token.objects.get(key=token_data)
        user = token.user
        if user.is_superuser:
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            try:
                user = User.objects.get(pk = python_data.get('user_id'))
                user.username = python_data.get('username') if python_data.get('username') else user.username
                user.first_name = python_data.get('first_name') if python_data.get('first_name') else user.first_name
                user.last_name = python_data.get('last_name') if python_data.get('last_name') else user.last_name
                user.save()
                return HttpResponse(json.dumps({'message':"User info updated successfully...."}))
            except:
                return HttpResponseBadRequest(json.dumps({'message':"User not found...."}))
        else:
            return HttpResponse(json.dumps({'message' : "You Don't have permission to edit usre info..."}))

@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['POST'])
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        json_data = request.body
        token_data = request.headers['Authorization']
        token_data = token_data.split(' ')
        token_data = token_data[1]
        token = Token.objects.get(key=token_data)
        user = token.user
        if not user.is_superuser:
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            python_data.update({'created_at': datetime.datetime.now()})
            python_data.update({'created_by': user.id})
            serializer = MessageSerializer(
                data=python_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(json.dumps({'message': 'message sent successfully!'}))
            else:
                return HttpResponse(json.dumps(serializer.errors))
        else:
            return HttpResponse(json.dumps({'message':'You can not send messages'}))
    else:
        return HttpResponse('Only POST method is allowed')


@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['PATCH'])
def like_message(request):
    if request.method == 'PATCH':
        json_data = request.body
        token_data = request.headers['Authorization']
        token_data = token_data.split(' ')
        token_data = token_data[1]
        token = Token.objects.get(key=token_data)
        user = token.user
        if not user.is_superuser:
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            try:
                message = Message.objects.get(pk = python_data.get('id'))
                message.likes += 1
                message.save()
                return HttpResponse(json.dumps({'message':'Message Liked Successfully'}))
            except:
                return HttpResponse(json.dumps({'message':'Message does not exist'}))
        else:
            return HttpResponse(json.dumps({'message':'You can not like messages'}))
            

@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['POST'])
def create_group(request):
    if request.method == 'POST':
        json_data = request.body
        token_data = request.headers['Authorization']
        token_data = token_data.split(' ')
        token_data = token_data[1]
        token = Token.objects.get(key=token_data)
        user = token.user
        if not user.is_superuser:
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            python_data['members'] = [user.id]
            serializer = GroupDataSerializer(data=python_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(json.dumps({'message': 'Group created successfully! now you can signin'}))
            else:
                return HttpResponse(json.dumps(serializer.errors))           
        else:
            return HttpResponse(json.dumps({'message' : 'You can not create a group'}))
        

@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['PATCH'])
def add_member(request):
    if request.method == 'PATCH':
        json_data = request.body
        token_data = request.headers['Authorization']
        token_data = token_data.split(' ')
        token_data = token_data[1]
        token = Token.objects.get(key=token_data)
        user = token.user
        if not user.is_superuser:
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            if python_data.get('group_id') and python_data.get('new_member'):
                try:
                    group_data = Group.objects.get(pk = python_data.get('group_id'))
                except:
                    return HttpResponseBadRequest(json.dumps({'message':"Group not found...."}))
                try:
                    user = User.objects.get(pk = python_data.get('new_member'))
                except:
                    return HttpResponseBadRequest(json.dumps({'message':"User not found...."}))
                if python_data.get('new_member') not in group_data.members:
                    group_data.members.append(python_data.get('new_member'))
                    group_data.save()
                    return HttpResponse(json.dumps({'message' : 'Member Added Successfully'}))
                else:
                    return HttpResponse(json.dumps({'message' : 'Member Already Exists, Please try with any other member '}))   
            else:
                if not python_data.get('group_id'):
                    return HttpResponse(json.dumps({'message' : 'Please provied group_id'}))
                else:
                    return HttpResponse(json.dumps({'message' : 'Please provied new_member'}))
        
        else:
            return HttpResponse(json.dumps({'message' : "You Don't have permission to add members to a Group"}))


@csrf_exempt
@permission_classes((AllowAny,))      
@api_view(['DELETE'])
def delete_group(request):
    if request.method == 'DELETE':
        json_data = request.body
        token_data = request.headers['Authorization']
        token_data = token_data.split(' ')
        token_data = token_data[1]
        token = Token.objects.get(key=token_data)
        user = token.user
        if not user.is_superuser:
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            if python_data.get('group_id'):
                try:
                    group = Group.objects.get(group_id = python_data.get('group_id'))
                    group.delete()
                    return HttpResponse(json.dumps({'message':'Group Deleted Successfully'}))
                except:
                    return HttpResponse(json.dumps({'message':'Group does not exist'}))
        else:
            return HttpResponse(json.dumps({'message':'You do not have permission to Delete a Group'}))

                
                
            