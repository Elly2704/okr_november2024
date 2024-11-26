import json
from django.conf import settings
from .serializers import UserLoginSerializer
from oauth2_provider.views import TokenView
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer


class UserCreateApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @extend_schema(summary='List of the users',
                   description="This endpoint provide list of users in system.",
                   request=UserRegistrationSerializer,
                   tags=["User CRUD"]
                   )
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if pk:
            try:
                user = User.objects.get(pk=pk)
                return Response(
                    {'item': UserRegistrationSerializer(user).data})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        users = User.objects.all()
        return Response({'items': UserRegistrationSerializer(users, many=True).data})  # Сериализуем и возвращаем

    @extend_schema(summary='Create a new user',
                   description="This endpoint allows to register a new user by providing a user data.",
                   request=UserRegistrationSerializer,
                   tags=["User CRUD"]
                   )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateDeleteApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @extend_schema(summary='Update a new user',
                   description="This endpoint allows to update the user information.",
                   request=UserRegistrationSerializer,
                   tags=["User CRUD"]
                   )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegistrationSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"item": serializer.data})

    @extend_schema(summary='Delete a new user',
                   description="This endpoint allows to delete the user by id.",
                   request=UserRegistrationSerializer,
                   tags=["User CRUD"]
                   )
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method DELETE not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=pk)
            user.delete()
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': f'Deleted user with ID {pk}'}, status=status.HTTP_204_NO_CONTENT)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    @extend_schema(summary='OAUTH2',
                   description="This endpoint provide access_token and refresh_token.",
                   request=UserLoginSerializer,
                   tags=["User CRUD"]
                   )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        #user = serializer.validated_data['user']

        data = {
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': settings.OAUTH2_CLIENT_ID,
            'client_secret': settings.OAUTH2_CLIENT_SECRET,
        }

        # create TokenView
        token_view = TokenView.as_view()
        request._request.POST = data
        request._request.method = 'POST'

        # get Token
        response = token_view(request._request)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = json.loads(response.content)
            return Response(response_data, status=response.status_code)
