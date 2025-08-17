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
    thread_id = serializers.CharField(required=False, allow_blank=True)

class ChatResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    thread_id = serializers.CharField()

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

class BriefPolicySerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = ['plcyNm', 'aiSummary', 'is_favorited']

    def get_is_favorited(self,obj):
        user = self.context['request'].user

        if not user or not user.is_authenticated:
            return False
        
        return Favorite_policy.objects.filter(user=user, policy=obj).exists()

class DetailPolicySerializer(serializers.ModelSerializer):
    plcyPvsnMthdCd_display = serializers.SerializerMethodField()
    mrgSttsCd_display = serializers.SerializerMethodField()
    earnCndSeCd_display = serializers.SerializerMethodField()
    plcyMajorCd_display = serializers.SerializerMethodField()
    jobCd_display = serializers.SerializerMethodField()
    schoolCd_display = serializers.SerializerMethodField()
    sbizCd_display = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = [
            "plcyNm", "plcyKywdNm", "lclsfNm", "mclsfNm",
            "plcyPvsnMthdCd_display",
            "plcyExplnCn", "plcySprtCn", "etcMttrCn",
            "bizPrdBgngYmd", "bizPrdEndYmd", "bizPrdEtcCn",
            "plcyAplyMthdCn", "sbmsnDcmntCn", "srngMthdCn", "aplyYmd", 
            "aplyUrlAddr", "refUrlAddr1", "refUrlAddr2",
            "rgtrInstCdNm",
            
            "sprtTrgtAgeLmtYn", "sprtTrgtMinAge", "sprtTrgtMaxAge", 
            "mrgSttsCd_display",
            "earnCndSeCd_display", "earnMinAmt", "earnMaxAmt", "earnEtcCn",
            "plcyMajorCd_display",
            "jobCd_display", 
            "schoolCd_display",
            "sbizCd_display",
        ]

    def get_plcyPvsnMthdCd_display(self, obj): return obj.get_plcyPvsnMthdCd_display()
    def get_mrgSttsCd_display(self, obj): return obj.get_mrgSttsCd_display()
    def get_earnCndSeCd_display(self, obj): return obj.get_earnCndSeCd_display()
    def get_plcyMajorCd_display(self, obj): return obj.get_plcyMajorCd_display()
    def get_jobCd_display(self, obj): return obj.get_jobCd_display()
    def get_schoolCd_display(self, obj): return obj.get_schoolCd_display()
    def get_sbizCd_display(self, obj): return obj.get_sbizCd_display()

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite_policy
        fields = ["id", "user", "policy", "created_at"]
        read_only_fields = ["id", "user", "policy", "created_at"]

class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['plcyNo', 'plcyNm', 'plcyKywdNm', 'lclsfNm', 'mclsfNm']
