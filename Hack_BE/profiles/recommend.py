# policy/services/recommend.py
from django.db.models import Q, IntegerField, Value
from django.db.models.functions import Cast, NullIf, Trim
from policy.models import Policy

def recommend_by_onboarding(user : object):
    try:
        user_profile = user.profile
    except user.profile.DoesNotExist:
        return Policy.objects.none()
    qs = Policy.objects.all()  

    qs = qs.annotate(
        min_age=Cast(NullIf(Trim("sprtTrgtMinAge"), Value("")), IntegerField()),
        max_age=Cast(NullIf(Trim("sprtTrgtMaxAge"), Value("")), IntegerField()),
        min_earn=Cast(NullIf(Trim("earnMinAmt"), Value("")), IntegerField()),
        max_earn=Cast(NullIf(Trim("earnMaxAmt"), Value("")), IntegerField()),
    )
    
    # 나이
    age = user_profile.age
    qs = qs.filter(
    # 1. 나이 제한 X
    Q(sprtTrgtAgeLmtYn="N") |
    # 2. 나이 범위 안
    (Q(min_age__isnull=False, max_age__isnull=False) &
     Q(min_age__lte=age, max_age__gte=age)) |
    # 3. 빈칸
    (Q(min_age__isnull=True) & Q(max_age__isnull=True)) | 
    (Q(min_age=0) & Q(max_age=0))
    )

    # 소득
    max_income = user_profile.max_income
    min_income = user_profile.min_income
    qs = qs.filter(
    # 1. 소득 무관
    Q(earnCndSeCd="0043001")|
    # 2. 나이 범위 안
    (Q(min_earn__isnull=False, max_earn__isnull=False) &
    Q(min_earn__lte=min_income, max_earn__gte=max_income)) |
    # 3. 빈칸
    (Q(min_earn__isnull=True) & Q(max_earn__isnull=True)) | 
    (Q(min_earn=0) & Q(max_earn=0))|
    # 4. 기타
    Q(earnCndSeCd="0043003")
    )

    # 결혼
    marry = user_profile.marry_code
    qs = qs.filter(
        Q(mrgSttsCd__icontains=marry) |
        Q(mrgSttsCd="0055003") |
        Q(mrgSttsCd="")
        )
    
    # 학력
    graduate = user_profile.graduate_code
    qs = qs.filter(
        Q(schoolCd__icontains=graduate) |
        Q(schoolCd="0049010") |
        Q(schoolCd="")
        )
    
    # 취업
    employ = user_profile.employment_code
    qs = qs.filter(
        Q(jobCd__icontains=employ) |
        Q(jobCd="0013010") |
        Q(jobCd="")
    )

    # 전공
    major = [s.code for s in user_profile.major_code.all()]
    qs = qs.filter(
        Q(plcyMajorCd__icontains=major) |
        Q(plcyMajorCd="0011009") |
        Q(plcyMajorCd="")
    )  

    # 정책특화
    special = [s.code for s in user_profile.special_code.all()]
    qs = qs.filter(
        Q(sbizCd__icontains=special) |
        Q(sbizCd="0014010") |
        Q(sbizCd="")
    )

    return qs