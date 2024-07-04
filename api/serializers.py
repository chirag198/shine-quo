from rest_framework import serializers
from .models import User, StudentProfile, MentorProfile
from .models import UserMentorMatch


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_student', 'is_mentor']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_student=validated_data['is_student'],
            is_mentor=validated_data['is_mentor']
        )
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'


class MentorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProfile
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserMentorMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMentorMatch
        fields = '__all__'
