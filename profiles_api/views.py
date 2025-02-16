from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404



from profiles_api.serializers import ( UserProfileSerializer, RegistrationSerializer )
#from profiles_api import serializers
from profiles_api.models import UserProfile

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from profiles_api.permissions import UpdateOwnProfile

from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from rest_framework.decorators import api_view

#from profiles_project import models



# Create your views here.
class HelloAPIView(APIView):
    
    serializer_Class = UserProfileSerializer
    #serializer_Class = serializers.HelloSerializer
    
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
    
    
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, UpdateOwnProfile,) #isAuthenticated  # Only authenticated users can update their own profile, other users can only view their profiles.
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)
      
    
class UserLoginAPIView(ObtainAuthToken):
    """ Handle creating user authentication tokens. """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class UserProfileDetailView(APIView):
    """Retrieve the authenticated user's profile"""
    authentication_classes = [TokenAuthentication]  # Token authentication
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        """Return authenticated user's data"""
        user = request.user  # Get the authenticated user
        serializer = UserProfileSerializer(user)  # Serialize user data
        return Response(serializer.data)  # Return the user data


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['name'] = account.name
            data['email'] = account.email

            token = Token.objects.get(user=account).key
            data['token'] = token

            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }
       
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)
    

@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
    

class HelloViewSet(viewsets.ViewSet):
    
    serializer_class = UserProfileSerializer
    
    def list(self, request):
         queryset = UserProfile.objects.all()
         serializer = UserProfileSerializer(queryset, many=True)
         return Response(serializer.data)
     
     
    def create(self, request):
         serializer = self.serializer_class(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
     
    def retrieve(self, request, pk=None):
         user = get_object_or_404(UserProfile, pk=pk)  # ✅ Safe lookup
         serializer = self.serializer_class(user)
         return Response(serializer.data)
        #  pk = request.parser_context.get('kwargs').get('pk')
        #  user = UserProfile.objects.get(pk=pk)
        #  serializer = self.serializer_class(user)
        #  return Response(serializer.data)
     
            
    def update(self, request, pk=None):  # ✅ Full update (PUT)
        user = get_object_or_404(UserProfile, pk=pk)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):  # ✅ Partial update (PATCH)
        user = get_object_or_404(UserProfile, pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):  # ✅ Delete user
        user = get_object_or_404(UserProfile, pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    