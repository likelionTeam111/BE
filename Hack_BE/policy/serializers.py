from rest_framework import serializers
from .models import *

def _get_display(obj, field):
    """enum 필드면 get_FOO_display() 호출, 아니면 ''"""
    method = f"get_{field}_display"
    if hasattr(obj, method):
        try:
            return getattr(obj, method)() or ""
        except Exception:
            return ""
    return ""

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False, trim_whitespace=True)
    thread_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class ChatResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    thread_id = serializers.CharField()

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'
    
class PolicyInfoSerializer(serializers.ModelSerializer):
    mrgSttsCd_display = serializers.SerializerMethodField()
    plcyMajorCd_display = serializers.SerializerMethodField()
    jobCd_display = serializers.SerializerMethodField()
    schoolCd_display = serializers.SerializerMethodField()
    sbizCd_display = serializers.SerializerMethodField()

    is_favorited = serializers.SerializerMethodField()
    addr = serializers.SerializerMethodField()
    about_benefit = serializers.SerializerMethodField()
    sprtSclCnt = serializers.SerializerMethodField()
    bizPrd = serializers.SerializerMethodField()
    ageLmt = serializers.SerializerMethodField()
    earnLmt = serializers.SerializerMethodField()
    etc = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = [
            # 개요
            'plcyNm', "plcyExplnCn",  'aiSummary', 'is_favorited', 'addr', "plcyKywdNm",
            # 사업기간
            "bizPrd", "zipCd",
            # 지원내용
            "about_benefit", 'sprtSclCnt',
            # 신청관련
            "aplyYmd", "sbmsnDcmntCn", "plcyAplyMthdCn", "srngMthdCn",  
            #요건
            "ageLmt", "earnLmt", "mrgSttsCd_display", "plcyMajorCd_display", "jobCd_display", "schoolCd_display", "sbizCd_display", 'etc',           
        ]

    def get_mrgSttsCd_display(self, obj): return obj.get_mrgSttsCd_display()
    def get_plcyMajorCd_display(self, obj): return obj.get_plcyMajorCd_display()
    def get_jobCd_display(self, obj): return obj.get_jobCd_display()
    def get_schoolCd_display(self, obj): return obj.get_schoolCd_display()
    def get_sbizCd_display(self, obj): return obj.get_sbizCd_display()

    def get_is_favorited(self,obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            return False
        
        return Favorite_policy.objects.filter(user=user, policy=obj).exists()
    
    def get_addr(self,obj):
        if obj.aplyUrlAddr:
            return obj.aplyUrlAddr
        elif obj.refUrlAddr1:
            return obj.refUrlAddr1
        return ""
    
    def get_about_benefit(self,obj):
        return f'{obj.plcySprtCn} / {obj.etcMttrCn}'
    
    def get_sprtSclCnt(self,obj):
        return obj.sprtSclCnt if obj.sprtSclCnt != "0" else ""
    
    def get_bizPrd(self, obj):
        bizprd = ""
        if obj.bizPrdBgngYmd.strip() != "" or obj.bizPrdEndYmd.strip() != "":
            bizprd += f'{obj.bizPrdBgngYmd} ~ {obj.bizPrdEndYmd}'
        if obj.bizPrdEtcCn != "":
            if bizprd:
                bizprd += " / "
            bizprd += f'{obj.bizPrdEtcCn}'
        return bizprd
    
    def get_ageLmt(self, obj):
        if obj.sprtTrgtAgeLmtYn == "Y":
            if (obj.sprtTrgtMinAge != "" or obj.sprtTrgtMaxAge != "") and obj.sprtTrgtMaxAge != "0":
                return f'{obj.sprtTrgtMinAge} ~ {obj.sprtTrgtMaxAge}'
            return "내용 참조"
        else:
            return "제한없음"
    
    def get_earnLmt(self, obj):
        earnLmt = ""
        if obj.get_earnCndSeCd_display() == "무관":
            earnLmt += obj.get_earnCndSeCd_display()
        else:
            earnLmt += obj.get_earnCndSeCd_display()
            if (obj.earnMinAmt != "0" and obj.earnMaxAmt != "0") and (obj.earnMinAmt != "" and obj.earnMaxAmt != ""):
                earnLmt += f' / {obj.earnMinAmt} ~ {obj.earnMaxAmt}'
        if obj.earnEtcCn != "":
            earnLmt += f' / {obj.earnEtcCn}'
        return earnLmt
    
    def get_etc(self, obj):
        etc = ""
        if obj.addAplyQlfcCndCn != "":
            etc += obj.addAplyQlfcCndCn
        if obj.ptcpPrpTrgtCn != "":
            if etc != "":
                etc += f'\n {obj.ptcpPrpTrgtCn}'
        return etc

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite_policy
        fields = ["id", "user", "policy", "created_at"]
        read_only_fields = ["id", "user", "policy", "created_at"]

class PolicyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'plcyNm', 'plcyKywdNm', 'lclsfNm', 'mclsfNm']