from django.db import models

class Policy(models.Model):
    # ENUM choices
    MARRIAGE_STATUS_CHOICES = [
        ("0055001", "미혼"),
        ("005502", "기혼"),
        ("0055003", "무관"),
    ]

    EARN_CONDITION_CHOICES = [
        ("0043001", "소득 무관"),
        ("0043002", "소득 하위 기준"),
        ("0043003", "일정 소득 기준"),
        ("0043004", "건강보험료 기준"),
        ("0043005", "중위소득 기준"),
    ]

    POLICY_MAJOR_CHOICES = [
        ("0011001", "일자리"),
        ("0011002", "주거"),
        ("0011003", "복지"),
        ("0011009", "기타/참여"),
    ]

    JOB_CONDITION_CHOICES = [
        ("0013001", "취업자"),
        ("0013010", "무관"),
    ]

    SCHOOL_CONDITION_CHOICES = [
        ("0049005", "대학생"),
        ("0049010", "무관"),
    ]

    # 필드 정의
    plcyNo = models.CharField(max_length=30, null=True, blank=True)  # 정책번호
    plcyNm = models.CharField(max_length=100, null=True, blank=True)  # 정책명
    plcyKywdNm = models.CharField(max_length=100, null=True, blank=True)  # 정책 키워드명
    plcyExplnCn = models.TextField(null=True, blank=True)  # 정책 설명내용
    lclsfNm = models.CharField(max_length=100, null=True, blank=True)  # 정책 대분류명
    mclsfNm = models.CharField(max_length=100, null=True, blank=True)  # 정책 중분류명
    plcySprtCn = models.TextField(null=True, blank=True)  # 정책 지원내용
    bizPrdBgngYmd = models.CharField(max_length=20, null=True, blank=True)  # 사업 시작일자 (YYYYMMDD)
    bizPrdEndYmd = models.CharField(max_length=20, null=True, blank=True)  # 사업 종료일자 (YYYYMMDD)
    bizPrdEtcCn = models.TextField(null=True, blank=True)  # 사업기간 기타내용
    plcyAplyMthdCn = models.TextField(null=True, blank=True)  # 신청방법 내용
    srngMthdCn = models.TextField(null=True, blank=True)  # 심사방법 내용
    aplyUrlAddr = models.TextField(null=True, blank=True)  # 신청 URL 주소
    sbmsnDcmntCn = models.TextField(null=True, blank=True)  # 제출서류 내용
    etcMttrCn = models.TextField(null=True, blank=True)  # 기타사항 내용
    refUrlAddr1 = models.TextField(null=True, blank=True)  # 참고 URL 주소 1
    refUrlAddr2 = models.TextField(null=True, blank=True)  # 참고 URL 주소 2
    sprtSclCnt = models.CharField(max_length=20, null=True, blank=True)  # 지원 규모
    sprtTrgtMinAge = models.CharField(max_length=10, null=True, blank=True)  # 지원 대상 최소 연령
    sprtTrgtMaxAge = models.CharField(max_length=10, null=True, blank=True)  # 지원 대상 최대 연령
    sprtTrgtAgeLmtYn = models.CharField(max_length=10, null=True, blank=True)  # 연령 제한 여부
    mrgSttsCd = models.CharField(max_length=10, choices=MARRIAGE_STATUS_CHOICES, null=True, blank=True)  # 결혼 상태 코드
    earnCndSeCd = models.CharField(max_length=10, choices=EARN_CONDITION_CHOICES, null=True, blank=True)  # 소득 조건 구분 코드
    earnMinAmt = models.CharField(max_length=20, null=True, blank=True)  # 소득 최소 금액
    earnMaxAmt = models.CharField(max_length=20, null=True, blank=True)  # 소득 최대 금액
    earnEtcCn = models.TextField(null=True, blank=True)  # 소득 기타 내용
    addAplyQlfcCndCn = models.TextField(null=True, blank=True)  # 가신청 자격조건 내용
    ptcpPrpTrgtCn = models.TextField(null=True, blank=True)  # 참여 제안 대상 내용
    nqCnt = models.CharField(max_length=20, null=True, blank=True)  # 조회수
    rgtrInstCdNm = models.CharField(max_length=30, null=True, blank=True)  # 등록자 기관 코드명
    rgtrHghrkInstCdNm = models.CharField(max_length=30, null=True, blank=True)  # 등록자 최상위 기관 코드명
    zipCd = models.TextField(null=True, blank=True)  # 거주 지역 코드
    plcyMajorCd = models.CharField(max_length=10, choices=POLICY_MAJOR_CHOICES, null=True, blank=True)  # 정책 전공 요건 코드
    jobCd = models.CharField(max_length=10, choices=JOB_CONDITION_CHOICES, null=True, blank=True)  # 취업 요건 코드
    schoolCd = models.CharField(max_length=10, choices=SCHOOL_CONDITION_CHOICES, null=True, blank=True)  # 학력 요건 코드
    aplyYmd = models.TextField(null=True, blank=True)  # 신청 기간
    frstRegDt = models.TextField(null=True, blank=True)  # 최초 등록일시
    lastMdfcnDt = models.TextField(null=True, blank=True)  # 최종 수정일시
    sBizCd = models.CharField(max_length=10, null=True, blank=True)  # 정책 특화 요건 코드

    def __str__(self):
        return self.plcyNm
