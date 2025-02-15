from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#from profiles_api.serializer import ( HelloSerializer )
from profiles_api import serializer

# Create your views here.
class HelloAPIView(APIView):
    
    #serializer_Class = HelloSerializer
    serializer_Class = serializer.HelloSerializer
    
    def get(self, request, format=None):
        
        an_apiview = [
            'Users HTTP Methos as (get, post, put, delete)',
            'Views are the endpoint that receives a request',
            'They handle the request and return a response',
            'APIView is a subclass of View',
            'APIView automatically handles JSON data and provides methods for different HTTP methods',
            'APIView automatically handles authentication and authorization',
            'Is similar to a trandiation Django View',
            'Is mapped manually to our URLs'
        ]
        
         # Extract request data safely
        request_data = {
            "method": request.method,
            "user_agent": request.META.get('HTTP_USER_AGENT', 'Unknown'),
            "remote_addr": request.META.get('REMOTE_ADDR', 'Unknown'),
            "query_params": request.query_params,  # For GET requests
            "data": request.data,  # For POST, PUT, DELETE requests
        }
        
        return Response({"message": "Hello, World!", 'an_apiview': an_apiview, 'request': request_data})
    
    
    def post(self, request):
        serializer = self.serializer_Class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello, {name}!'
            return Response({'message': message, 'data' : request.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    
    def put(self, request, pk=None):
        # Implement PUT method logic here, handle updating objects
        return Response({'method': 'PUT'})
    
    
    def patch(self, request, pk=None):
        # Handle PATCH method logic here, handle updating objects
        return Response({'method': 'PATCH'})
    
    
    def delete(self, request, pk=None):
        # For deleting object
        return Response({'method': 'DELETE'})