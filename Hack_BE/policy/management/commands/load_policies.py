import requests
from decouple import config
from django.core.management.base import BaseCommand
from langchain_core.documents import Document
from policy.models import Policy
from .policy_loader import build_simple_policy_text
from openai import OpenAI

class Command(BaseCommand):
    def handle(self, *args, **options):
        saved = 0
        updated = 0
        page = 1
        
        url = 'https://www.youthcenter.go.kr/go/ythip/getPlcy'
        api_key = config('youth_api_key')
        
        gpt_api_key = config("gpt_api_key")
        client = OpenAI(api_key=gpt_api_key)

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
            
            # print(policy_list)
            if not policy_list:
                break
            
            for policy_data in policy_list:
                # 중앙부처만 저장
                if policy_data.get('pvsnInstGroupCd') != '0054001':
                    continue
                
                obj, created = Policy.objects.update_or_create(
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
                        'plcyMajorCd': policy_data.get('plcyMajorCd',""),
                        'jobCd': policy_data.get('jobCd',""),
                        'schoolCd': policy_data.get('schoolCd',""),
                        'aplyYmd': policy_data.get('aplyYmd',""),
                        'frstRegDt': policy_data.get('frstRegDt',""),
                        'lastMdfcnDt': policy_data.get('lastMdfcnDt',""),
                        'sbizCd': policy_data.get('sbizCd',""),
                    }
                )

                # AI 3줄 요약 추가
                doc = Document(
                    page_content=build_simple_policy_text(obj),
                    metadata={
                        "정책명": obj.plcyNm,
                        "키워드": f"{obj.plcyKywdNm}, {obj.lclsfNm}, {obj.mclsfNm}",
                        "source": f"{obj.aplyUrlAddr} or {obj.refUrlAddr1} or {obj.refUrlAddr2}"
                    }
                )
                
    
                system = "너는 대한민국 청년정책을 간결하게 요약하는 도우미야."
                user = f"""
                        아래 정책 내용을 3줄 요약해.
                        각 줄은 '대상:', '지원 내용:', '신청방법:' 로 시작해야 해.
                        줄을 마칠 때는 단어로 끝내줘
                        불필요한 말은 금지하고, 딱 3줄만 출력해.

                        정책명 : {doc.metadata.get("정책명","")}
                        내용: {doc.page_content}
                        참고 : {doc.metadata}
                        """
                resp = client.responses.create(
                    model="gpt-4o-mini",
                    temperature=0.2,
                    input=[{"role":"system","content":system},
                        {"role":"user","content":user}],
                )
                obj.aiSummary = resp.output_text.strip()
                obj.save(update_fields=["aiSummary"])
                
                if created:
                    saved += 1
                else:
                    updated += 1
            
            self.stdout.write(self.style.SUCCESS(f"페이지 {page} 처리 완료"))
            page += 1
        self.stdout.write(self.style.SUCCESS(f"✅ 저장: {saved}개, 업데이트: {updated}개 완료되었습니다."))

