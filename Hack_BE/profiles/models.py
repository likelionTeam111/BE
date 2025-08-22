from django.db import models
from accounts.models import CustomUser
# Create your models here.
MARRY_CHOICES = [
    ("0055001", "기혼"),
    ("0055002", "미혼"),
    ("0055003", "제한없음"),
]

GRADUATE_CHOICES =[
    ("0049001","고졸 미만"),
    ("0049002","고교 재학"),
    ("0049003","고졸예정"),
    ("0049004","고교 졸업"),
    ("0049005","대학 재학"),
    ("0049006","대졸 예정"),
    ("0049007", "대학 졸업"),
    ("0049008", "석·박사"),
    ("0049009", "기타"),
    ("0049010", "제한없음"),
]

EMPLOYMENT_CHOICES = [
    ("0013001", "재직자"),
    ("0013002", "자영업자"),
    ("0013003", "미취업자"),
    ("0013004", "프리랜서"),
    ("0013005", "일용근로자"),
    ("0013006", "(예비)창업자"),
    ("0013007", "단기근로자"),
    ("0013008", "영농종사자"),
    ("0013009", "기타"),
    ("0013010", "제한없음"),
]

MAJOR_CHOICES = [
    ("0011001", "인문계열"),
    ("0011002", "사회계열"),
    ("0011003", "상경계열"),
    ("0011004", "이학계열"),
    ("0011005", "공학계열"),
    ("0011006", "예체능계열"),
    ("0011007", "농산업계열"),
    ("0011008", "기타"),
    ("0011009", "제한없음"),
    ]

SBIZ_CHOICES = [
    ("0014001", "중소기업"),
    ("0014002", "여성"),
    ("0014003", "기초생활수급자"),
    ("0014004", "한부모가정"),
    ("0014005", "장애인"),
    ("0014006", "농업인"),
    ("0014007", "군인"),
    ("0014008", "지역인재"),
    ("0014009", "기타"),
    ("0014010", "제한없음"),
    ]

class Major(models.Model):
    code = models.CharField(max_length=30, choices=MAJOR_CHOICES, blank=True)

class Special(models.Model):
    code = models.CharField(max_length=30, choices=SBIZ_CHOICES, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name="profile")
    age = models.IntegerField(null=True,blank=True)
    region = models.CharField(max_length=30,null=True,blank=True)
    marry_code = models.CharField(max_length=7,choices=MARRY_CHOICES,null=True,blank=True)
    max_income = models.IntegerField(null=True,blank=True)
    min_income = models.IntegerField(null=True,blank=True)
    graduate_code = models.CharField(max_length=7,choices=GRADUATE_CHOICES,null=True,blank=True)
    employment_code = models.CharField(max_length=7,choices=EMPLOYMENT_CHOICES,null=True,blank=True)
    goal = models.TextField(blank=True, null=True)

    special_code = models.ManyToManyField(Special,null=True,blank=True,related_name='profiles')
    major_code  = models.ManyToManyField(Major,null=True,blank=True,related_name='profiles')