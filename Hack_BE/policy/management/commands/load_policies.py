import requests
from decouple import config
from django.core.management.base import BaseCommand
from policy.models import Policy

class Command(BaseCommand):
    def handle(self, *args, **options):
        saved = 0
        updated = 0
        page = 1
        
        url = 'https://www.youthcenter.go.kr/go/ythip/getPlcy'
        api_key = config('youth_api_key')
        
        while True:
            params = {
                    'apiKeyNm': api_key,
                    'pageNum': page,
                    'pageSize': 100,
                    'rtnType': 'json'
                }
            res = requests.get(url, params=params)
            data = res.json()
            policy_list = data.get('result', {}).get('youthPolicyList', [])
            
            if not policy_list:
                break
            
            for policy_data in policy_list:
                # 중앙부처만 저장
                if policy_data.get('pvsnInstGroupCd') != '0054001':
                    continue
                _, created = Policy.objects.update_or_create(
                    plcyNo = policy_data['plcyNo'],
                    defaults={
                        'plcyPvsnMthdCd': policy_data.get('plcyPvsnMthdCd',""),
                        'plcyNm': policy_data.get('plcyNm',""),
                        'plcyKywdNm': policy_data.get('plcyKywdNm',""),
                        'plcyExplnCn': policy_data.get('plcyExplnCn',""),
                        'lclsfNm': policy_data.get('lclsfNm',""),
                        'mclsfNm': policy_data.get('mclsfNm',""),
                        'plcySprtCn': policy_data.get('plcySprtCn',""),
                        'bizPrdBgngYmd': policy_data.get('bizPrdBgngYmd',""),
                        'bizPrdEndYmd': policy_data.get('bizPrdEndYmd',""),
                        'bizPrdEtcCn': policy_data.get('bizPrdEtcCn',""),
                        'plcyAplyMthdCn': policy_data.get('plcyAplyMthdCn',""),
                        'srngMthdCn': policy_data.get('srngMthdCn',""),
                        'aplyUrlAddr': policy_data.get('aplyUrlAddr',""),
                        'sbmsnDcmntCn': policy_data.get('sbmsnDcmntCn',""),
                        'etcMttrCn': policy_data.get('etcMttrCn',""),
                        'refUrlAddr1': policy_data.get('refUrlAddr1',""),
                        'refUrlAddr2': policy_data.get('refUrlAddr2',""),
                        'sprtSclCnt': policy_data.get('sprtSclCnt',""),
                        'sprtTrgtMinAge': policy_data.get('sprtTrgtMinAge',""),
                        'sprtTrgtMaxAge': policy_data.get('sprtTrgtMaxAge',""),
                        'sprtTrgtAgeLmtYn': policy_data.get('sprtTrgtAgeLmtYn',""),
                        'mrgSttsCd': policy_data.get('mrgSttsCd',""),
                        'earnCndSeCd': policy_data.get('earnCndSeCd',""),
                        'earnMinAmt': policy_data.get('earnMinAmt',""),
                        'earnMaxAmt': policy_data.get('earnMaxAmt',""),
                        'earnEtcCn': policy_data.get('earnEtcCn',""),
                        'addAplyQlfcCndCn': policy_data.get('addAplyQlfcCndCn',""),
                        'ptcpPrpTrgtCn': policy_data.get('ptcpPrpTrgtCn',""),
                        'inqCnt': policy_data.get('inqCnt',""),
                        'rgtrInstCdNm': policy_data.get('rgtrInstCdNm',""),
                        'rgtrHghrkInstCdNm': policy_data.get('rgtrHghrkInstCdNm',""),
                        'zipCd': policy_data.get('zipCd',""),
                        'plcyMajorCd': policy_data.get('plcyMajorCd',""),
                        'jobCd': policy_data.get('jobCd',""),
                        'schoolCd': policy_data.get('schoolCd',""),
                        'aplyYmd': policy_data.get('aplyYmd',""),
                        'frstRegDt': policy_data.get('frstRegDt',""),
                        'lastMdfcnDt': policy_data.get('lastMdfcnDt',""),
                        'sbizCd': policy_data.get('sbizCd',""),
                    }
                )
                if created:
                    saved += 1
                else:
                    updated += 1
            
            self.stdout.write(self.style.SUCCESS(f"페이지 {page} 처리 완료"))
            page += 1
        self.stdout.write(self.style.SUCCESS(f"✅ 저장: {saved}개, 업데이트: {updated}개 완료되었습니다."))

