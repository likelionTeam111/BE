from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.

from .models import *
from .serializers import *
import requests
from django.http import JsonResponse

def load_policies(request):
    url = 'https://www.youthcenter.go.kr/go/ythip/getPlcy'
    headers = {'x-api-key': '6ae7fc43-0101-4352-b1c2-bcc4a0f09495'} 
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return JsonResponse({'error': 'API 요청 실패'}, status=500)
    
    policy_list = response.json().get('result', {}).get('youthPolicyList', [])

    saved = 0
    skipped = 0

    for p in policy_list:
        plcy_no = p.get('plcyNo')

        if Policy.objects.filter(plcyNo=plcy_no).exists():
            skipped += 1
            continue

        try:
            Policy.objects.create(
                plcyNo = plcy_no,
                plcyNm = p.get('plcyNm', ''),
                plcyKywdNm = p.get('plcyKywdNm', ''),
                plcySprtCn = p.get('plcySprtCn', ''),
                aplyPrdSeCd = p.get('aplyPrdSeCd', ''),
                bizPrdSeCd = p.get('bizPrdSeCd', ''),
                bizPrdBgngYmd = p.get(p.get('bizPrdBgngYmd')),
                bizPrdEndYmd = p.get(p.get('bizPrdEndYmd')),
                bizPrdEtcCn = p.get('bizPrdEtcCn', ''),
                plcyAplyMthdCn = p.get('plcyAplyMthdCn', ''),
                srngMthdCn = p.get('srngMthdCn', ''),
                aplyUrlAddr = p.get('aplyUrlAddr', ''),
                sbmsnDcmntCn = p.get('sbmsnDcmntCn', ''),
                etcMttrCn = p.get('etcMttrCn', ''),
                sprtTrgtMinAge = p.get('sprtTrgtMinAge', ''),
                sprtTrgtMaxAge = p.get('sprtTrgtMaxAge', ''),
                sprtTrgtAgeLmtYn = p.get('sprtTrgtAgeLmtYn', ''),
                mrgSttsCd = p.get('mrgSttsCd', ''),
                earnCndSeCd = p.get('earnCndSeCd', ''),
                earnMinAmt = p.get('earnMinAmt', ''),
                earnMaxAmt = p.get('earnMaxAmt', ''),
                earnEtcCn = p.get('earnEtcCn', ''),
                addAplyQlfcCndCn = p.get('addAplyQlfcCndCn', ''),
                rgtrInstCd = p.get('rgtrInstCd', ''),
                rgtrInstCdNm = p.get('rgtrInstCdNm', ''),
                zipCd = p.get('zipCd', ''),
                plcyMajorCd = p.get('plcyMajorCd', ''),
                jobCd = p.get('jobCd', ''),
                schoolCd = p.get('schoolCd', ''),
            )
            saved += 1
        except Exception as e:
            print(f"에러 발생: {e}")
            continue

    return JsonResponse({
        'result': f"{saved}개 저장 완료, {skipped}개 중복으로 건너뜀"
    })