from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
# add this for authentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from .models import Task
from .serializers import TaskSerializer, UserSerializer
# Import the user model
from django.contrib.auth.models import User

class TaskView(APIView):
 
    permission_classes = [IsAuthenticated] # 
    def get(self, request: Request) -> Response:
        '''get all tasks'''
        user = request.user
        # Check if the user exists

       
        tasks = Task.objects.filter(student=user)
     
        serializer = TaskSerializer(tasks, many=True)
        data = serializer.data
        return Response(data)
    
    def post(self, request: Request) -> Response:
        '''add task'''
        data = request.data
  
        user = request.user
        data['student'] = user.id
        print(data)
        
        serialzer = TaskSerializer(data=data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data)
        
        return Response(serialzer.errors)
    
    def put(self, request: Request, pk: int) -> Response:
        '''uodate task'''
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'does not exist'})
        
        data = request.data
        serializer = TaskSerializer(task, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
# Get all users
class UserView(APIView):
    def get(self, request: Request,user:str) -> Response:
        '''Get all user's tasks'''
        user = User.objects.get(username=user)
        serializer = UserSerializer(user)
        data = serializer.data
        return Response(data)
    

class CreateUserView(APIView):
    def post(self, request: Request) -> Response:
        '''create user'''
        data = request.data
        username = data['username']
        # Check if the user exists
        user = User.objects.filter(username=username)
        if user:
            return Response({'error': 'user already exists'})
        password = data['password']
        user = User.objects.create_user(username=username, password=password)
        print(user)
        return Response(data)
     
  