from sentence_transformers import SentenceTransformer
from policy.models import Policy
from django.db import transaction
from tqdm import tqdm
import numpy as np
from django.core.management.base import BaseCommand


# ✅ 모델 로딩

model = SentenceTransformer('jhgan/ko-sbert-sts')

# ✅ 임베딩 텍스트 생성 함수
def build_policy_embedding_text(policy: Policy) -> str:
    """하나의 정책 객체를 입력받아 임베딩용 텍스트로 변환"""
    # 1. 핵심 필드 수동 지정
    parts = [
        f"[정책명] {policy.plcyNm or ''}",
        f"[정책 설명] {policy.plcyExplnCn or ''}",
        f"[지원 내용] {policy.plcySprtCn or ''}",
        f"[신청 방법] {policy.plcyAplyMthdCn or ''}",
        f"[제출 서류] {policy.sbmsnDcmntCn or ''}",
        f"[대상 연령] {policy.sprtTrgtMinAge or ''} ~ {policy.sprtTrgtMaxAge or ''}세",
        f"[신청 URL] {policy.aplyUrlAddr or ''}"
    ]

    # 2. ENUM 타입은 display 이름으로
    if policy.get_plcyPvsnMthdCd_display():
        parts.append(f"[제공 방법] {policy.get_plcyPvsnMthdCd_display()}")

    if policy.get_mrgSttsCd_display():
        parts.append(f"[결혼 요건] {policy.get_mrgSttsCd_display()}")

    if policy.get_earnCndSeCd_display():
        parts.append(f"[소득 조건] {policy.get_earnCndSeCd_display()}")

    if policy.get_plcyMajorCd_display():
        parts.append(f"[전공 요건] {policy.get_plcyMajorCd_display()}")

    if policy.get_jobCd_display():
        parts.append(f"[취업 요건] {policy.get_jobCd_display()}")

    if policy.get_schoolCd_display():
        parts.append(f"[학력 요건] {policy.get_schoolCd_display()}")

    if policy.get_sbizCd_display():
        parts.append(f"[특화 대상] {policy.get_sbizCd_display()}")

    # 3. 기타 필드들 자동 추가 (정보성 text 위주)
    auto_fields = ['etcMttrCn', 'addAplyQlfcCndCn', 'ptcpPrpTrgtCn']
    for field_name in auto_fields:
        value = getattr(policy, field_name, "")
        if value:
            parts.append(f"[{field_name}] {value}")

    return "\n".join(parts)


class Command(BaseCommand):
    def handle(self, *args, **options):
        policies = Policy.objects.all()

        with transaction.atomic():
            for policy in tqdm(policies):
                try:
                    # 텍스트 만들기
                    text = build_policy_embedding_text(policy)

                    # 임베딩
                    embedding = model.encode(text)

                    # 저장
                    policy.embedding = embedding.tolist()
                    policy.save()

                except Exception as e:
                    print(f"에러 - {policy.id}: {e}")
        self.stdout.write(self.style.SUCCESS(f"embedding이 완료되었습니다."))