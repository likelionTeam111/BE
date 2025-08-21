from rest_framework import serializers
from accounts.models import CustomUser
from policy.models import Policy
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ("code", "label")

class SpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Special
        fields = ("code", "label")


class ProfileSerializer(serializers.ModelSerializer):
    major = serializers.SlugRelatedField(
        many = True,
        slug_field = 'code',
        queryset=Major.objects.all()
    )

    special = serializers.SlugRelatedField(
        many=True,
        slug_field="code",
        queryset=Special.objects.all()
    )

    class Meta:
        model = Profile
        fields = ["id", "age", "min_income", "max_income",
            "marry", "graduate", "employment", "major", "special",
        ]

    # def create(self, validated_data):
    #     major_data = validated_data.pop('major', [])
    #     special_data = validated_data.pop('special', [])
        
    #     profile = Profile.objects.create(**validated_data)
        
    #     profile.major.set(major_data)
    #     profile.special.set(special_data)
        
    #     return profile

    # def update(self, instance, validated_data):
    #     major_data = validated_data.pop('major', [])
    #     special_data = validated_data.pop('special', [])

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
        
    #     instance.major.set(major_data)
    #     instance.special.set(special_data)

    #     instance.save()
    #     return instance

# class ProfileSerializer(serializers.ModelSerializer):
#     marry_display = serializers.SerializerMethodField()
#     graduate_display = serializers.SerializerMethodField()
#     employment_display = serializers.SerializerMethodField()

#     majors = serializers.SlugRelatedField(
#         many = True,
#         write_only=True,
#         slug_field = 'code',
#         queryset=Major.objects.all()
#     )

#     specials = serializers.SlugRelatedField(
#         many=True,
#         write_only=True,
#         slug_field="code",
#         queryset=Special.objects.all()
#     )

#     majors_display = serializers.SerializerMethodField()
#     special_display = serializers.SerializerMethodField()

#     class Meta:
#         model = Profile
#         fields = [
#         'age', 'region', 'marry', 'marry_display',
#         'min_income', 'max_income', 'graduate', 'graduate_display',
#         'employment', 'employment_display', 'goal',
#         'majors', 'majors_display', 'specials', 'special_display',
#     ]
    
#     def get_marry_display(self,obj):return obj.get_marry_display()
#     def get_graduate_display(self, obj):return obj.get_graduate_display()
#     def get_employment_display(self, obj):return obj.get_employment_display()

#     def get_special_display(self, obj):return [special.label for special in obj.special.all()]
#     def get_majors_display(self,obj):return [major.label for major in obj.majors.all()]

class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'plcyNm', 'plcyKywdNm', 'lclsfNm', 'mclsfNm']