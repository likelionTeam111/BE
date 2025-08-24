# policy/services/recommend.py
from django.db.models import Q, IntegerField, Value, Func, F, DateField, CharField, Case, When
from django.db.models.functions import Cast, NullIf, Trim
from policy.models import Policy
from policy.langchain import vector_store
import datetime

def recommend_filter(user:object, category:str):
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
        biz_end_date=Func(NullIf(Trim(F("bizPrdEndYmd")), Value("")), Value("YYYYMMDD"), function="TO_DATE", output_field=DateField()),
        apply_end_date=Func(NullIf(Func(Func(F("aplyYmd"), Value("~"), Value(2), function="split_part", output_field=CharField()), function="btrim", output_field=CharField()), Value("")), Value("YYYYMMDD"), function="TO_DATE", output_field=DateField())
    )

    # 카테고리
    qs = qs.filter(
        Q(lclsfNm__icontains=category)
        )
    
    # 지역
    if user_profile.region:
        region = user_profile.region
        qs = qs.filter(
        Q(zipCd__icontains=region) |
        Q(zipCd="전국") |
        Q(zipCd="")
        )
    
    # 나이
    if user_profile.age:
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
    if user_profile.max_income and user_profile.min_income:
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
    if user_profile.marry_code:
        marry = user_profile.marry_code
        qs = qs.filter(
            Q(mrgSttsCd__icontains=marry) |
            Q(mrgSttsCd="0055003") |
            Q(mrgSttsCd="")
            )
    
    # 학력
    if user_profile.graduate_code:
        graduate = user_profile.graduate_code
        qs = qs.filter(
            Q(schoolCd__icontains=graduate) |
            Q(schoolCd="0049010") |
            Q(schoolCd="")
            )
    
    # 취업
    if user_profile.employment_code:
        employ = user_profile.employment_code
        qs = qs.filter(
            Q(jobCd__icontains=employ) |
            Q(jobCd="0013010") |
            Q(jobCd="")
        )

    # 전공
    if user_profile.major_code.all():
        major = [s.code for s in user_profile.major_code.all()]
        qs = qs.filter(
            Q(plcyMajorCd__icontains=major) |
            Q(plcyMajorCd="0011009") |
            Q(plcyMajorCd="")
        )  

    # 정책특화
    if user_profile.special_code.all():
        special = [s.code for s in user_profile.special_code.all()]
        qs = qs.filter(
            Q(sbizCd__icontains=special) |
            Q(sbizCd="0014010") |
            Q(sbizCd="")
        )
    
    # 날짜
    today = datetime.date.today()
    qs = qs.filter((Q(biz_end_date__isnull=True) | Q(biz_end_date__gte=today)) &
                   (Q(apply_end_date__isnull=True) | Q(apply_end_date__gte=today)))
    return qs

def recommend_by_onboarding(user : object, category : str):
    #vector store
    query = user.profile.goal
    filtered_data = recommend_filter(user, category)
    
    retrieved_docs = vector_store.similarity_search(query, k=10, filter={"id": {"$in": [p.id for p in filtered_data]}})
    recommend_list = []
    name_list = []
    for doc in retrieved_docs:
        if doc.metadata.get("정책명") in name_list:
            continue
        recommend_list.append(doc.metadata.get("id"))
        name_list.append(doc.metadata.get("정책명"))
    
    order_expr = Case(
    *[When(id=pid, then=Value(i)) for i, pid in enumerate(recommend_list)],
    default=Value(len(recommend_list)),
    output_field=IntegerField(),
    )

    qs = (
    Policy.objects
    .filter(id__in=recommend_list)
    .annotate(_ord=order_expr)
    .order_by("_ord")
    )

    return qs
