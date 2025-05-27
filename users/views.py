import json
import urllib.parse

from django.conf import settings
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserLoginSerializer
from oauth2_provider.views import TokenView
from oauth2_provider.models import AccessToken, Application
# from oauth2_provider.mo
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from django.http import QueryDict

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
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]

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



# @method_decorator(csrf_exempt, name='dispatch')
# class UserLoginView(APIView):
#     serializer_class = UserLoginSerializer
#     permission_classes = [AllowAny]
#
#     @extend_schema(summary='OAUTH2',
#                    description="This endpoint provide access_token and refresh_token.",
#                    request=UserLoginSerializer,
#                    tags=["User CRUD"]
#                    )
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         #user = serializer.validated_data['user']
#
#         data = {
#             'grant_type': 'password',
#             'username': request.data['username'],
#             'password': request.data['password'],
#             'client_id': settings.OAUTH2_CLIENT_ID,
#             'client_secret': settings.OAUTH2_CLIENT_SECRET,
#         }
#
#         # create TokenView
#         token_view = TokenView.as_view()
#         request._request.POST = data
#         request._request.method = 'POST'
#
#         # get Token
#         response = token_view(request._request)
#
#         if response.status_code == 200:
#             response_data = json.loads(response.content)
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             response_data = json.loads(response.content)
#             return Response(response_data, status=response.status_code)
#


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @extend_schema(summary='OAUTH2',
                   description="This endpoint provide access_token and refresh_token.",
                   request=UserLoginSerializer,
                   tags=["User CRUD"]
                   )
    def post(self, request):
        print('1')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('2')

        data = QueryDict('', mutable=True)
        data.update({
            'grant_type': 'password',
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'client_id': settings.OAUTH2_CLIENT_ID,
            'client_secret': settings.OAUTH2_CLIENT_SECRET,
        })
        print('3')

        token_view = TokenView.as_view()
        print('4')
        request._request.POST = data
        request._request.META['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
        request._request.method = 'POST'
        print('5')

        response = token_view(request._request)
        print('6')

        if response.status_code == 200:
            response_data = json.loads(response.content)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = json.loads(response.content)
            return Response(response_data, status=response.status_code)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @extend_schema(summary='OAUTH2',
                   description="This endpoint provide access_token and refresh_token.",
                   request=UserLoginSerializer,
                   tags=["User CRUD"]
                   )
    def post(self, request):
        """
        Application should already exist. Track application via it's name

        app = Application.objects.create(
            name="MyFrontend",
            user=admin,  # the owner of the application
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        Application = okr_november2024_1

        kkBgdQwu9bruSaXp5tpDFwzGvUCYgD1p8xWS4XdaVeaZOccXuHquixo7w3IuqK0duP1FRnY59cGWAYAKdoFuD13E57MeKKfWYz3XIa4ouZjsmSFuWSWXXBDk6Bsbhc6o
        :param request:
        :return:
        """
        from django.contrib.auth import authenticate
        from django.http import HttpRequest
        import base64
        from django.test import RequestFactory

        APPLICATION_NAME: str = 'okr_november2024'

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")
        # user = authenticate(username=serializer.validated_data.get('username'), password=serializer.validated_data.get('password'))

        # Get authenticated user from existing serializer
        print("serializer user", serializer.validated_data.get("user"))

        app = Application.objects.filter(name=APPLICATION_NAME)
        if app.exists() is False:
            return Response(data={"non_field_errors": ["Missing auth Application"]}, status=400)
        app = app.first()

        token = AccessToken.objects.filter(user=user)
        if token.exists() is False:

            data = {
                'grant_type': 'password',
                'username': serializer.validated_data.get('username'),
                'password': serializer.validated_data.get('password'),
                'client_id': app.client_id,
                'client_secret': app.client_secret,
            }

            mock_request = HttpRequest()
            mock_request.user = user
            mock_request.method = 'POST'
            mock_request.POST = data
            request.session.user = user
            # mock_request.session = request.session

            # base64_credentials = base64.b64encode(f"{app.client_id}:{app.client_secret}".encode()).decode()
            # mock_request.META['HTTP_AUTHORIZATION'] = f'Basic {base64_credentials}'

            # mock_request.META = {
            #     'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            # }

            token_view_response = TokenView.as_view()(mock_request)

            # fac = RequestFactory()
            # token_request = fac.post('/o/token/', data, user=user)
            # token_request.user = user
            # print(token_request)
            # token_view_response = TokenView.as_view()(token_request)


        else:
            token_view_response = Response({
                'token': token.first().token,
                'refresh_token': token.first().refresh_token.token,
            })

            if serializer.validated_data.get('is_refresh') is True:
                data = {
                    'grant_type': 'refresh_token',
                    'client_id': app.client_id,
                    'client_secret': app.client_secret,
                    'refresh_token': token.first().refresh_token.token
                }

                mock_request = HttpRequest()
                mock_request.user = user
                mock_request.method = 'POST'
                mock_request.POST = data
                request.session.user = user

                token_view_response = TokenView.as_view()(mock_request)

        return token_view_response