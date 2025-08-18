from django.db import models
from pgvector.django import VectorField
from accounts.models import CustomUser

class Policy(models.Model):
    # ENUM choices
    POLICY_PROVISION_METHOD_CHOICES = [
    ("0042001", "인프라 구축"),
    ("0042002", "프로그램"),
    ("0042003", "직접대출"),
    ("0042004", "공공기관"),
    ("0042005", "계약(위탁운영)"),
    ("0042006", "보조금"),
    ("0042007", "대출보증"),
    ("0042008", "공적보험"),
    ("0042009", "조세지출"),
    ("0042010", "바우처"),
    ("0042011", "정보제공"),
    ("0042012", "경제적 규제"),
    ("0042013", "기타"),
    ]

    MARRIAGE_STATUS_CHOICES = [
        ("0055001", "기혼"),
        ("005502", "미혼"),
        ("0055003", "제한없음"),
    ]

    EARN_CONDITION_CHOICES = [
        ("0043001", "무관"),
        ("0043002", "연소득"),
        ("0043003", "기타"),
    ]

    POLICY_MAJOR_CHOICES = [
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

    JOB_CHOICES = [
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

    SCHOOL_CHOICES = [
    ("0049001", "고졸 미만"),
    ("0049002", "고교 재학"),
    ("0049003", "고졸 예정"),
    ("0049004", "고교 졸업"),
    ("0049005", "대학 재학"),
    ("0049006", "대졸 예정"),
    ("0049007", "대학 졸업"),
    ("0049008", "석·박사"),
    ("0049009", "기타"),
    ("0049010", "제한없음"),
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
    # 정책 개요
    plcyNo = models.CharField(max_length=100, null=True, blank=True)  # 정책번호
    plcyNm = models.CharField(max_length=100, null=True, blank=True)  # 정책명
    
    aiSummary  = models.TextField(null=True, blank=True)   # AI 3줄 요약
    plcyKywdNm = models.CharField(max_length=100, null=True, blank=True)  # 정책 키워드명    
    lclsfNm = models.CharField(max_length=50, null=True, blank=True)  # 정책 대분류명
    mclsfNm = models.CharField(max_length=50, null=True, blank=True)  # 정책 중분류명
    plcyPvsnMthdCd = models.CharField(max_length=50, choices=POLICY_PROVISION_METHOD_CHOICES, null=True, blank=True) # 정책제공방법코드

    # 정책 설명
    plcyExplnCn = models.TextField(null=True, blank=True)  # 정책 설명내용
    plcySprtCn = models.TextField(null=True, blank=True)  # 정책 지원내용
    etcMttrCn = models.TextField(null=True, blank=True)  # 기타사항 내용
    sprtSclCnt = models.CharField(max_length=50, null=True, blank=True)  # 지원 규모
    refUrlAddr1 = models.TextField(null=True, blank=True)  # 참고 URL 주소 1
    refUrlAddr2 = models.TextField(null=True, blank=True)  # 참고 URL 주소 2
    
    # 기간
    bizPrdBgngYmd = models.CharField(max_length=50, null=True, blank=True)  # 사업 시작일자 (YYYYMMDD)
    bizPrdEndYmd = models.CharField(max_length=50, null=True, blank=True)  # 사업 종료일자 (YYYYMMDD)
    bizPrdEtcCn = models.TextField(null=True, blank=True)  # 사업기간 기타내용

    # 신청
    plcyAplyMthdCn = models.TextField(null=True, blank=True)  # 신청방법 내용
    sbmsnDcmntCn = models.TextField(null=True, blank=True)  # 제출서류 내용
    srngMthdCn = models.TextField(null=True, blank=True)  # 심사방법 내용
    aplyYmd = models.TextField(null=True, blank=True)  # 신청 기간
    aplyUrlAddr = models.TextField(null=True, blank=True)  # 신청 URL 주소
    
    #요건
    sprtTrgtAgeLmtYn = models.CharField(max_length=50, null=True, blank=True)  # 연령 제한 여부
    sprtTrgtMinAge = models.CharField(max_length=50, null=True, blank=True)  # 지원 대상 최소 연령
    sprtTrgtMaxAge = models.CharField(max_length=50, null=True, blank=True)  # 지원 대상 최대 연령
    mrgSttsCd = models.CharField(max_length=50, choices=MARRIAGE_STATUS_CHOICES, null=True, blank=True)  # 결혼 상태 코드
    earnCndSeCd = models.CharField(max_length=50, choices=EARN_CONDITION_CHOICES, null=True, blank=True)  # 소득 조건 구분 코드
    earnMinAmt = models.CharField(max_length=50, null=True, blank=True)  # 소득 최소 금액
    earnMaxAmt = models.CharField(max_length=50, null=True, blank=True)  # 소득 최대 금액
    earnEtcCn = models.TextField(null=True, blank=True)  # 소득 기타 내용
    plcyMajorCd = models.CharField(max_length=100, choices=POLICY_MAJOR_CHOICES, null=True, blank=True)  # 정책 전공 요건 코드
    jobCd = models.CharField(max_length=100, choices=JOB_CHOICES, null=True, blank=True)  # 취업 요건 코드
    schoolCd = models.CharField(max_length=100, choices=SCHOOL_CHOICES, null=True, blank=True)  # 학력 요건 코드
    sbizCd = models.CharField(max_length=100, choices=SBIZ_CHOICES, null=True, blank=True)  # 정책 특화 요건 코드
    addAplyQlfcCndCn = models.TextField(null=True, blank=True)  # 가신청 자격조건 내용
    ptcpPrpTrgtCn = models.TextField(null=True, blank=True)  # 참여 제안 대상 내용

    # 기타 참고
    rgtrInstCdNm = models.CharField(max_length=50, null=True, blank=True)  # 등록자 기관 코드명
    rgtrHghrkInstCdNm = models.CharField(max_length=50, null=True, blank=True)  # 등록자 최상위 기관 코드명
    inqCnt = models.CharField(max_length=50, null=True, blank=True)  # 조회수
    frstRegDt = models.TextField(null=True, blank=True)  # 최초 등록일시
    lastMdfcnDt = models.TextField(null=True, blank=True)  # 최종 수정일시

    def __str__(self):
        return self.plcyNm

class Favorite_policy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite_by')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='favorite_policy')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 중복방지
        constraints = [models.UniqueConstraint(fields=['user', 'policy'], name='uniq_user_policy')]