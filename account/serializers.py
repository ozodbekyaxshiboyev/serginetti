from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, max_length=20, write_only=True)
    password2 = serializers.CharField(min_length=4, max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'email','phone_number', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'message': 'Parollarni bir xil kiriting'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, write_only=True)
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def validate(self, attrs):
        authenticate_kwargs = {
            'full_name': attrs['full_name'],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)
        print(1111, user)
        if not user:
            raise AuthenticationFailed({
                'message': 'Fullname or password is not correct'
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'message': 'Account is not active'
            })
        refresh = self.get_token(user)

        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        attrs['user_id'] = user.id

        del attrs['full_name'], attrs['password']

        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1000)

    class Meta:
        model = User
        fields = ('token',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'email',
            'phone_number',
            'role',
            'image',
                  )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'email',
            'phone_number',
            'role',
            'image',
            'country',
            'city',
            'street',
            'name_cc',
            'floor',
            'inn',
            'company_name',
            'company_address',
            'mail_address',
            'contract1',
            'contract2',
            'bank',
            'account1',
            'account2',
                  )


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {'success': False, 'message': 'Parol avalgisi bilan bir xil bo`lmasligi kerak'})

        if password != password2:
            raise serializers.ValidationError(
                {'success': False, 'message': 'Yangi paroller bir xil kiritilmadi!'})

        user.set_password(password)
        user.save()
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = RefreshToken(attrs['refresh'])
        try:
            token.blacklist()
        except AttributeError:
            pass
        return {}

