from rest_framework import serializers
from .models import *
from policy.models import Policy

MARRY_L2C   = {label: code for code, label in MARRY_CHOICES}
GRAD_L2C    = {label: code for code, label in GRADUATE_CHOICES}
EMP_L2C     = {label: code for code, label in EMPLOYMENT_CHOICES}
MAJOR_L2C   = {label: code for code, label in MAJOR_CHOICES}
SPECIAL_L2C = {label: code for code, label in SBIZ_CHOICES}

class EnrollSerializer(serializers.ModelSerializer):
    major_code = serializers.SlugRelatedField(
        many = True,
        slug_field = 'code',
        queryset=Major.objects.all()
    )

    special_code = serializers.SlugRelatedField(
        many=True,
        slug_field="code",
        queryset=Special.objects.all()
    )

    class Meta:
        model = Profile
        fields = ["id", "age", "region", "min_income", "max_income",
            "marry_code", "graduate_code", "employment_code", "major_code", "special_code", "goal"
        ]
        
    def to_internal_value(self, data):
        data = data.copy()

        # 단일 choices
        for key, data_key, table in (
            ("marry_code", "marry", MARRY_L2C),
            ("graduate_code", "graduate", GRAD_L2C),
            ("employment_code", "employment", EMP_L2C),
        ):
            val = data.get(data_key, None)
            if isinstance(val, str):
                data[key] = table.get(val, val)  # 라벨이면 코드로 치환, 코드면 그대로

        # M2M
        majors = data.pop("major", None)
        if isinstance(majors, list):
            data["major_code"] = [MAJOR_L2C.get(v, v) for v in majors]
        specials = data.pop("special", None)
        if isinstance(specials, list):
            data["special_code"] = [SPECIAL_L2C.get(v, v) for v in specials]

        return super().to_internal_value(data)
        
class ProfileSerializer(serializers.ModelSerializer):
    major = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()

    marry = serializers.SerializerMethodField()
    graduate = serializers.SerializerMethodField()
    employment = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "age", "region", "min_income", "max_income",
            "marry", "graduate", "employment", "major", "special", "goal"
        ]
    
    def get_marry(self, obj): return obj.get_marry_code_display()
    def get_graduate(self, obj): return obj.get_graduate_code_display()
    def get_employment(self, obj): return obj.get_employment_code_display()
    def get_major(self, obj):
        return [m.get_code_display() for m in obj.major_code.all()]

    def get_special(self, obj):
        return [s.get_code_display() for s in obj.special_code.all()]