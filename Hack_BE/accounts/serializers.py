from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class CustomRegisterSerializer(RegisterSerializer):
    _has_phone_field = False
    email = None

    username = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
        data = super(CustomRegisterSerializer, self).get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        return data
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.username = self.cleaned_data.get('username')
        user.save()
        adapter.save_user(request, user, self)
        return user
    

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname']


# #마이페이지 전용 - password 
# class MyPageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id','username','nickname','age','location']
#         read_only_fields = fields 

class CustomLoginSerializer(LoginSerializer):
    email = None

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError('로그인 정보가 일치하지 않습니다.', code='authorization')

        else:
            raise serializers.ValidationError('아이디와 비밀번호를 모두 입력해주세요.', code='authorization')

        attrs['user'] = user
        return attrs