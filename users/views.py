import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, QueryDict
from django.contrib.auth.models import User

from oauth2_provider.views import TokenView
from oauth2_provider.models import AccessToken, Application

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .serializers import UserRegistrationSerializer, UserLoginSerializer


class UserCreateApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_summary='List of the users',
        operation_description="This endpoint provides a list of users in the system.",
        tags=["User CRUD"],
        responses={200: UserRegistrationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                user = User.objects.get(pk=pk)
                return Response({'item': UserRegistrationSerializer(user).data})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        users = User.objects.all()
        return Response({'items': UserRegistrationSerializer(users, many=True).data})

    @swagger_auto_schema(
        operation_summary='Create a new user',
        operation_description="This endpoint allows registering a new user by providing user data.",
        request_body=UserRegistrationSerializer,
        tags=["User CRUD"],
        responses={201: UserRegistrationSerializer()}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {"username": user.username, "email": user.email}
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_summary='Update user',
        operation_description="This endpoint allows updating user information.",
        request_body=UserRegistrationSerializer,
        tags=["User CRUD"],
        responses={200: UserRegistrationSerializer()}
    )
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'Method PUT not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"item": serializer.data})

    @swagger_auto_schema(
        operation_summary='Delete user',
        operation_description="This endpoint allows deleting a user by id.",
        tags=["User CRUD"],
        responses={204: 'User deleted successfully'}
    )
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error': 'Method DELETE not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'message': f'Deleted user with ID {pk}'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        operation_summary='OAUTH2 Token obtain',
        operation_description="Get access and refresh tokens by username and password or refresh token.",
        request_body=UserLoginSerializer,
        tags=["User CRUD"],
        responses={200: 'Token response'}
    )
    def post(self, request):
        APPLICATION_NAME = 'okr_november2024'

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")
        app_qs = Application.objects.filter(name=APPLICATION_NAME)
        if not app_qs.exists():
            return Response({"non_field_errors": ["Missing auth Application"]}, status=status.HTTP_400_BAD_REQUEST)
        app = app_qs.first()

        existing_tokens = AccessToken.objects.filter(user=user)

        # Create QueryDict for POST to TokenView
        post_data = QueryDict(mutable=True)

        if serializer.validated_data.get('is_refresh'):
            # Refresh token
            token = existing_tokens.first()
            post_data.update({
                'grant_type': 'refresh_token',
                'client_id': app.client_id,
                'client_secret': app.client_secret,
                'refresh_token': token.refresh_token.token,
            })
        else:
            # If new login by password
            post_data.update({
                'grant_type': 'password',
                'username': serializer.validated_data.get('username'),
                'password': serializer.validated_data.get('password'),
                'client_id': app.client_id,
                'client_secret': app.client_secret,
            })

        # request to TokenView
        token_request = HttpRequest()
        token_request.method = 'POST'
        token_request.POST = post_data

        # Get token
        token_response = TokenView.as_view()(token_request)
        response_status = token_response.status_code
        response_data = json.loads(token_response.content)

        return Response(response_data, status=response_status)
