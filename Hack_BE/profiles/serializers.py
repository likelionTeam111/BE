from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.response import Response
from .models import *


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ("code", "label")

class SpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Special
        fields = ("code","label")


class ProfileSerializer(serializers.ModelSerializer):
    marry_display = serializers.SerializerMethodField()
    graduate_display = serializers.SerializerMethodField()
    employment_display = serializers.SerializerMethodField()

    majors = serializers.SlugRelatedField(
        many = True,
        write_only=True,
        slug_field = 'code',
        queryset=Major.objects.all()
    )

    specials = serializers.SlugRelatedField(
        many=True,
        write_only=True,
        slug_field="code",
        queryset=Special.objects.all()
    )

    majors_display = serializers.SerializerMethodField()
    special_display = serializers.SerializerMethodField()

    class Meta:
        model = Profile
    fields = [
        'age', 'region', 'marry', 'marry_display',
        'min_income', 'max_income', 'graduate', 'graduate_display',
        'employment', 'employment_display', 'goal',
        'majors', 'majors_display', 'specials', 'special_display',
    ]
    
    def get_marry_display(self,obj):return obj.get_marry_display()
    def get_graduate_display(self, obj):return obj.get_graduate_display()
    def get_employment_display(self, obj):return obj.get_employment_display()

    def get_special_display(self, obj):return [special.label for special in obj.special.all()]
    def get_majors_display(self,obj):return [major.label for major in obj.majors.all()]