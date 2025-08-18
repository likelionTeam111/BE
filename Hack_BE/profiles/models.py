from django.db import models
from django.conf import settings
from accounts.models import CustomUser
# Create your models here.

User = settings.AUTH_USER_MODEL


class Special(models.Model):
    code = models.CharField(max_length=30)
    label = models.CharField(max_length=100)

class Major(models.Model):
    code = models.CharField(max_length=30)
    label = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name="profile")
    special = models.ManyToManyField(Special,through="Profile_Special")
    majors = models.ManyToManyField(Major, through="Profile_Major")

    #Choice
    MARRY_CHOICES = [
        ("0055001", "기혼"),
        ("0055002", "미혼"),
        ("0055003", "제한없음"),
    ]

    GRAUDATE_CHOICES =[
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

    age = models.IntegerField(null=True,blank=True)
    region = models.CharField(max_length=30,blank=True)
    marry = models.CharField(max_length=7,choices=MARRY_CHOICES,null=True,blank=True)
    max_income = models.IntegerField(null=True,blank=True)
    max_income = models.IntegerField(null=True,blank=True)
    graduate = models.CharField(max_length=7,choices=GRAUDATE_CHOICES,null=True,blank=True)
    employment = models.CharField(max_length=7,choices=EMPLOYMENT_CHOICES,null=True,blank=True)
    goal = models.TextField(blank=True)


class Profile_Special(models.Model):
    profile_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    speical_id = models.ForeignKey(Special,on_delete=models.CASCADE)

class Profile_Major(models.Model):
    profile_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    speical_id = models.ForeignKey(Special,on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.user.username}님의 Profile"