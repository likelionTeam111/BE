from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.response import Response
from .models import *

class DisplayChoiceField(serializers.ChoiceField):

    # DB에 저장된 코드 → 응답 라벨로 변환
    def to_representation(self, value):
        if value in ("", None):
            return None
        return self._choices.get(value, value)
    
    # 입력 라벨 → 코드 변환
    def to_internal_value(self, data):
        for key, val in self._choices.items():
            if val == data:
                return key
        # 라벨이 choices에 없으면 validation error 발생
        self.fail("invalid_choice", input=data)


class LabelManyField(serializers.SlugRelatedField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.queryset.model.__name__ == "Major":
            choices = dict(MAJOR_CHOICES)
        elif self.queryset.model.__name__ == "Special":
            choices = dict(SBIZ_CHOICES)
        else:
            choices = {}

        self.code_to_label = choices
        self.label_to_code = {v: k for k, v in choices.items()}

    def to_internal_value(self, data):
        # 비어있으면 빈 리스트 반환
        if data in (None, "", []):
            return []  
        label = str(data).strip()
        code = self.label_to_code.get(label)
        if not code:
            self.fail("invalid_choice", input=data)
        try:
            return self.get_queryset().get(code=code)
        except self.get_queryset().model.DoesNotExist:
            self.fail("not_found", input=data)

    def to_representation(self, obj):
        return self.code_to_label.get(getattr(obj, "code", None), getattr(obj, "code", None))

    default_error_messages = {
        "invalid_choice": '"{input}"은(는) 허용된 라벨이 아닙니다.',
        "not_found": '"{input}" 라벨에 해당하는 항목을 찾을 수 없습니다.',
    }


class ProfileSerializer(serializers.ModelSerializer):
    # 단일 choice 필드
    marry_code = DisplayChoiceField(choices=MARRY_CHOICES, required=False)
    graduate_code = DisplayChoiceField(choices=GRADUATE_CHOICES, required=False)
    employment_code = DisplayChoiceField(choices=EMPLOYMENT_CHOICES, required=False)
    max_income = serializers.IntegerField(required=False, allow_null=True)
    min_income = serializers.IntegerField(required=False, allow_null=True)

    # M2M 필드: 라벨 입력, 코드 저장
    majors_code = LabelManyField(many=True, slug_field="code",queryset=Major.objects.all(),required=False,allow_empty=True)
    special_code = LabelManyField(many=True, slug_field="code",queryset=Special.objects.all(),required=False,allow_empty=True)

    class Meta:
        model = Profile
        fields = [
            "age",
            "region",
            "marry_code",
            "max_income", 
            "min_income",
            "graduate_code",
            "employment_code",
            "goal",
            "majors_code",
            "special_code",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile_data = []

        for key, value in data.items():
            if isinstance(value, list):
                if value:  # 빈 리스트가 아니면
                    profile_data.append(value)  # flatten 하지 않고 그대로 추가
            elif value not in (None, ""):
                profile_data.append(value)

        return {"profile_data": profile_data}
