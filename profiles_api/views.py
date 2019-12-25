from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework import viewsets
from profiles_api import models
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


class HelloApiView(APIView):
    # Test API View

    serializer_class=serializers.HelloSerializer

    def get(self, request, format=None):
        an_apiview = [
            'User HTTP methods as function (get,past,patch,put,delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logig',
            'Is mapped manually to URLs',
        ]

        return Response({'message':'Hello!', 'an_apiview':an_apiview})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message=f'hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self,request, pk=None):
        return Response({'method':'PUT'})

    def patch(self,request,pk=None):
        return Response({'method':'Patch'})

    def delete(self,request,pk=None):
        return Response({'method':'Delete'})

class HelloViewSet(viewsets.ViewSet):

    serializer_class=serializers.HelloSerializer

    def list(self, request):
        a_viewsets=[
            'Uses actions (list, create, retrieve, update, partial_update)',
            'automatically maps to URLs usingg Routers',
            'provides more functionality with less code',
        ]

        return Response({'message':'Hello!', 'a_viewset':a_viewsets})

    def create(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message=f'Hello {name}!'
            return Response({'message':message})
        else:
            return response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self,request, pk=None):
        return Response({'http_method':'GET'})

    def update(self,request,pk=None):
        return Response({'http_method':'put'})

    def partial_update(self,request,pk=None):
        return Response({'Partial_response':'Patch'})

    def destroy(self,request,pk=None):
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.UserProfileSerializer
    queryset=models.UserProfile.objects.all()
    authentication_class=(TokenAuthentication,)
    permissions_class=(permissions.UpdateOwnProfile,)
    filter_backends=(filters.SearchFilter ,)
    search_fields = ('name','email',)


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentiaction_classes=(TokenAuthentication,)
    serializer_class=serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_class=(
        permissions.UpdateOwnStatus,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)


