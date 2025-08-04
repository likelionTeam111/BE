from django.db import models

# Create your models here.

class Policy(models.Model):
    plcyNo = models.CharField(max_length=100, unique=True)  # 정책번호
    plcyNm = models.CharField(max_length=200)  # 정책명
    plcyKywdNm = models.CharField(max_length=200, blank=True, null=True)  # 정책키워드명
    plcySprtCn = models.TextField(blank=True, null=True)  # 정책지원내용

    aplyPrdSeCd = models.CharField(max_length=50, blank=True, null=True)  # 신청기간구분코드
    bizPrdSeCd = models.CharField(max_length=50, blank=True, null=True)  # 사업기간구분코드
    bizPrdBgngYmd = models.CharField(max_length=8,blank=True, null=True)  # 사업기간시작일자
    bizPrdEndYmd = models.CharField(max_length=8,blank=True, null=True)  # 사업기간종료일자
    bizPrdEtcCn = models.TextField(blank=True, null=True)  # 사업기간기타내용

    plcyAplyMthdCn = models.TextField(blank=True, null=True)  # 정책신청방법내용
    srngMthdCn = models.TextField(blank=True, null=True)  # 심사방법내용
    aplyUrlAddr = models.URLField(max_length=500, blank=True, null=True)  # 신청URL주소
    sbmsnDcmntCn = models.TextField(blank=True, null=True)  # 제출서류내용
    etcMttrCn = models.TextField(blank=True, null=True)  # 기타사항내용

    sprtTrgtMinAge = models.IntegerField(blank=True, null=True)  # 지원대상최소연령
    sprtTrgtMaxAge = models.IntegerField(blank=True, null=True)  # 지원대상최대연령
    sprtTrgtAgeLmtYn = models.CharField(max_length=10, blank=True, null=True)  # 지원대상연령제한여부

    mrgSttsCd = models.CharField(max_length=50, blank=True, null=True)  # 결혼상태코드
    earnCndSeCd = models.CharField(max_length=50, blank=True, null=True)  # 소득조건구분코드
    earnMinAmt = models.BigIntegerField(blank=True, null=True)  # 소득최소금액
    earnMaxAmt = models.BigIntegerField(blank=True, null=True)  # 소득최대금액
    earnEtcCn = models.TextField(blank=True, null=True)  # 소득기타내용

    addAplyQlfcCndCn = models.TextField(blank=True, null=True)  # 추가신청자격조건내용
    rgtrInstCd = models.CharField(max_length=100, blank=True, null=True)  # 등록자기관코드
    rgtrInstCdNm = models.CharField(max_length=200, blank=True, null=True)  # 등록자기관코드명
    zipCd = models.TextField(blank=True, null=True)  # 정책거주지역코드

    plcyMajorCd = models.CharField(max_length=50, blank=True, null=True)  # 정책전공요건코드
    jobCd = models.CharField(max_length=50, blank=True, null=True)  # 정책취업요건코드
    schoolCd = models.CharField(max_length=50, blank=True, null=True)  # 정책학력요건코드

    def __str__(self):
        return self.plcyNm