from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.

from .models import *
from .serializers import *
import requests
from django.http import JsonResponse
from django.conf import settings

def load_policies(request):
    url = 'https://www.youthcenter.go.kr/go/ythip/getPlcy'
    youth_api_key = settings.youth_api_key  #수정 

    saved = 0
    skipped = 0
    page = 1

    while True:
        params = {
            'apiKeyNm': youth_api_key, #수정 
            'pageNum': page,
            'pageSize': 100,
            'rtnType': 'json'
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"API 요청 실패 - status: {response.status_code}")
            return JsonResponse({'error': 'API 요청 실패'}, status=500)

        try:
            data = response.json()
            policy_list = data.get('result', {}).get('youthPolicyList', [])
        except Exception as e:
            print(f"JSON 파싱 오류: {e}")
            return JsonResponse({'error': '응답 파싱 실패'}, status=500)
        
        def to_int_or_none(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        # 데이터가 없으면 종료
        if not policy_list:
            break  

        for p in policy_list:
            plcy_no = p.get('plcyNo')

            #중복방지 - DB에 이미 정책명이 존재하면 스킵 
            if Policy.objects.filter(plcyNo=plcy_no).exists():
                skipped += 1
                continue

            try:
                Policy.objects.create(
                    plcyNo=plcy_no,
                    plcyNm=p.get('plcyNm', ''),
                    plcyKywdNm=p.get('plcyKywdNm', ''),
                    plcySprtCn=p.get('plcySprtCn', ''),
                    aplyPrdSeCd=p.get('aplyPrdSeCd', ''),
                    bizPrdSeCd=p.get('bizPrdSeCd', ''),
                    bizPrdBgngYmd=p.get('bizPrdBgngYmd', ''),
                    bizPrdEndYmd=p.get('bizPrdEndYmd', ''),
                    bizPrdEtcCn=p.get('bizPrdEtcCn', ''),
                    plcyAplyMthdCn=p.get('plcyAplyMthdCn', ''),
                    srngMthdCn=p.get('srngMthdCn', ''),
                    aplyUrlAddr=p.get('aplyUrlAddr', ''),
                    sbmsnDcmntCn=p.get('sbmsnDcmntCn', ''),
                    etcMttrCn=p.get('etcMttrCn', ''),
                    sprtTrgtMinAge = to_int_or_none(p.get('sprtTrgtMinAge')),
                    sprtTrgtMaxAge = to_int_or_none(p.get('sprtTrgtMaxAge')),
                    sprtTrgtAgeLmtYn=p.get('sprtTrgtAgeLmtYn', ''),
                    mrgSttsCd=p.get('mrgSttsCd', ''),
                    earnCndSeCd=p.get('earnCndSeCd', ''),
                    earnMinAmt = to_int_or_none(p.get('earnMinAmt')),
                    earnMaxAmt = to_int_or_none(p.get('earnMaxAmt')),
                    earnEtcCn=p.get('earnEtcCn', ''),
                    addAplyQlfcCndCn=p.get('addAplyQlfcCndCn', ''),
                    rgtrInstCd=p.get('rgtrInstCd', ''),
                    rgtrInstCdNm=p.get('rgtrInstCdNm', ''),
                    zipCd=p.get('zipCd', ''),
                    plcyMajorCd=p.get('plcyMajorCd', ''),
                    jobCd=p.get('jobCd', ''),
                    schoolCd=p.get('schoolCd', ''),
                )
                saved += 1
            except Exception as e:
                print(f"에러 발생 (plcyNo={plcy_no}): {e}")
                continue

        print(f"{page}페이지 처리 완료. 저장: {saved}, 건너뜀: {skipped}")
        page += 1

    return JsonResponse({
        'result': f"{saved}개 저장 완료, {skipped}개 중복으로 건너뜀"
    })

