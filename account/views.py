import jwt
from django.conf import settings
from drf_yasg import openapi
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from .models import User
from .permissions import IsOwnUserOrReadOnly
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserDetailSerializer,
    EmailVerificationSerializer,
    ChangePasswordSerializer, LogoutSerializer
)




class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user)

        current_site = 'localhost:8000/'
        relative_link = 'account/verify-email/'
        abs_url = f'http://{current_site}{relative_link}?token={str(token.access_token)}'
        email_body = f'Salom, {user.email} \n Serginetti sayti uchun akkountingizni faollashtirish uchun link \n {abs_url}'
        data = {
            'to_email': user.email,
            'email_subject': 'Serginnetti sayti uchun emailigizni aktivlashtiring',
            'email_body': email_body
        }
        Util.send_email(data)

        return Response({'success': True, 'message': 'Emailingizga akkountingizni faollashtirishga link yuborildi'},
                        status=status.HTTP_201_CREATED)


class EmailVerificationView(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify email',
                                           type=openapi.TYPE_STRING)

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'success': True, 'message': 'Email tasdiqlandi'},
                            status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as e:
            return Response({'success': False, 'message': f'Verification expired | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'success': False, 'message': f'Invalid token | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        count = queryset.count()
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    # permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)

    # def get(self, request, *args, **kwargs):
    #     query = self.get_object()
    #     if query:
    #         serializer = self.get_serializer(query)
    #         return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'success': False, 'message': 'query did not exist'}, status=status.HTTP_404_NOT_FOUND)
    #
    # def patch(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     serializer = self.get_serializer(obj, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'success': True, 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
    #     return Response({'success': False, 'message': 'credentials is invalid'}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)




