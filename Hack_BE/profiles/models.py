from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")

    #관심지역
    egion = models.CharField(max_length=50, choices=[
        ("전국", "전국"),
        ("서울특별시", "서울특별시"),
        ("부산광역시", "부산광역시"),
        ("대구광역시", "대구광역시"),
        ("인천광역시", "인천광역시"),
        ("광주광역시", "광주광역시"),
        ("대전광역시", "대전광역시"),
        ("울산광역시", "울산광역시"),
        ("세종특별자치도", "세종특별자치도"),
        ("경기도", "경기도"),
        ("충청북도", "충청북도"),
        ("충청남도", "충청남도"),
        ("전라남도", "전라남도"),
        ("경상북도", "경상북도"),
        ("경상남도", "경상남도"),
        ("강원특별자치도", "강원특별자치도"),
        ("전북특별자치도", "전북특별자치도"),
        ("제주특별자치도", "제주특별자치도"),
    ], blank=True)

    # 연령 (단순 정수로 저장, 범위검색 시 활용)
    age = models.PositiveIntegerField(null=True, blank=True)

    # 혼인여부
    marital_status = models.CharField(max_length=10, choices=[
        ("미혼", "미혼"),
        ("기혼", "기혼"),
        ("기타", "기타"),
    ], blank=True)

    # 연소득 (만원 단위 입력, min/max 조회 시 활용)
    annual_income = models.PositiveIntegerField(null=True, blank=True)

    # 학력
    education = models.CharField(max_length=20, choices=[
        ("제한없음", "제한없음"),
        ("고졸미만", "고졸미만"),
        ("고교재학", "고교재학"),
        ("고졸예정", "고졸예정"),
        ("고교졸업", "고교졸업"),
        ("대학재학", "대학재학"),
        ("대졸예정", "대졸예정"),
        ("대학졸업", "대학졸업"),
        ("석,박사", "석,박사"),
        ("기타", "기타"),
    ], blank=True)

    # 취업상태
    employment_status = models.CharField(max_length=20, choices=[
        ("제한없음", "제한없음"),
        ("재직자", "재직자"),
        ("자영업자", "자영업자"),
        ("미취업자", "미취업자"),
        ("프리랜서", "프리랜서"),
        ("일용근로자", "일용근로자"),
        ("예비창업자", "예비창업자"),
        ("단기근로자", "단기근로자"),
        ("영농종사자", "영농종사자"),
        ("기타", "기타"),
    ], blank=True)

    # 전공분야
    major_field = models.CharField(max_length=20, choices=[
        ("제한없음", "제한없음"),
        ("인문계열", "인문계열"),
        ("사회계열", "사회계열"),
        ("상경계열", "상경계열"),
        ("이학계열", "이학계열"),
        ("공학계열", "공학계열"),
        ("예체능계열", "예체능계열"),
        ("농산업계열", "농산업계열"),
        ("기타", "기타"),
    ], blank=True)

    # 특화분야
    specialty = models.CharField(max_length=20, choices=[
        ("제한없음", "제한없음"),
        ("중소기업", "중소기업"),
        ("여성", "여성"),
        ("기초생활수급자", "기초생활수급자"),
        ("한부모가정", "한부모가정"),
        ("장애인", "장애인"),
        ("농업인", "농업인"),
        ("군인", "군인"),
        ("지역인재", "지역인재"),
        ("기타", "기타"),
    ], blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"