from django.core.management.base import BaseCommand
from langchain_core.documents import Document
from rag.store import vectorstore  # ← PGVector/Embeddings은 rag/store.py에서 전역 초기화
from policy.models import Policy
from tqdm import tqdm
import os

# e5 계열 쓸 때 접두어를 붙이고 싶으면 .env에 E5_PREFIX=true
USE_E5_PREFIX = os.getenv("E5_PREFIX", "false").lower() == "true"
DOC_PREFIX = "passage: " if USE_E5_PREFIX else ""

def _get_display(obj, field):
    """choices 필드면 get_FOO_display() 호출, 아니면 ''"""
    method = f"get_{field}_display"
    if hasattr(obj, method):
        try:
            return getattr(obj, method)() or ""
        except Exception:
            return ""
    return ""

def build_policy_text(p: "Policy") -> str:
    parts = [
        f"[정책명] {p.plcyNm or ''}",
        f"[정책 설명] {p.plcyExplnCn or ''}",
        f"[지원 내용] {p.plcySprtCn or ''}",
        f"[신청 방법] {p.plcyAplyMthdCn or ''}",
        f"[제출 서류] {p.sbmsnDcmntCn or ''}",
        f"[대상 연령] {getattr(p, 'sprtTrgtMinAge', '') or ''} ~ {getattr(p, 'sprtTrgtMaxAge', '') or ''}세",
        f"[신청 URL] {getattr(p, 'aplyUrlAddr', '') or ''}",
    ]

    # ENUM/choices 필드 display
    parts += [
        f"[제공 방법] {_get_display(p, 'plcyPvsnMthdCd')}",
        f"[결혼 요건] {_get_display(p, 'mrgSttsCd')}",
        f"[소득 조건] {_get_display(p, 'earnCndSeCd')}",
        f"[전공 요건] {_get_display(p, 'plcyMajorCd')}",
        f"[취업 요건] {_get_display(p, 'jobCd')}",
        f"[학력 요건] {_get_display(p, 'schoolCd')}",
        f"[특화 대상] {_get_display(p, 'sbizCd')}",
    ]

    # 기타 정보성 텍스트
    for fname in ["etcMttrCn", "addAplyQlfcCndCn", "ptcpPrpTrgtCn"]:
        v = getattr(p, fname, None)
        if v:
            parts.append(f"[{fname}] {v}")

    # 빈 문자열 제거
    parts = [s for s in parts if s and s.strip()]
    return "\n".join(parts)

class Command(BaseCommand):
    help = "Policies → LangChain PGVector에 인덱싱합니다. (문서/메타데이터 저장)"

    def add_arguments(self, parser):
        parser.add_argument("--batch", type=int, default=500, help="배치 크기 (기본 500)")
        parser.add_argument("--reindex", action="store_true",
                            help="동일 ID 문서를 먼저 삭제 후 재색인")
        parser.add_argument("--ids", type=str, default="",
                            help="쉼표로 구분된 policy id 목록만 인덱싱 (예: 12,15,99)")

    def handle(self, *args, **opts):
        batch_size = opts["batch"]
        only_ids = [int(x) for x in opts["ids"].split(",") if x.strip().isdigit()] if opts["ids"] else []
        qs = Policy.objects.filter(id__in=only_ids) if only_ids else Policy.objects.all()

        docs, ids = [], []
        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("인덱싱할 정책이 없습니다."))
            return

        pbar = tqdm(qs.iterator(chunk_size=batch_size), total=total, desc="Indexing")

        for p in pbar:
            try:
                text = build_policy_text(p)
                if not text.strip():
                    continue

                doc_id = f"policy:{p.id}"
                if opts["reindex"]:
                    # 기존 문서 삭제(있으면)
                    try:
                        vectorstore.delete(ids=[doc_id])
                    except Exception:
                        pass  # 없으면 무시

                doc = Document(
                    page_content=(DOC_PREFIX + text),
                    metadata={
                        "policy_id": p.id,
                        "plcyNo": getattr(p, "plcyNo", None),
                        "plcyNm": p.plcyNm,
                        "region": getattr(p, "regionNm", None),
                        "category": getattr(p, "majorCdNm", None),  # 일자리/주거 등
                        "ageMin": getattr(p, "sprtTrgtMinAge", None),
                        "ageMax": getattr(p, "sprtTrgtMaxAge", None),
                        "aplyUrl": getattr(p, "aplyUrlAddr", None),
                    },
                )
                docs.append(doc)
                ids.append(doc_id)

                if len(docs) >= batch_size:
                    vectorstore.add_documents(docs, ids=ids)
                    docs, ids = [], []

            except Exception as e:
                self.stderr.write(f"[SKIP] id={p.id} 에러: {e}")

        if docs:
            vectorstore.add_documents(docs, ids=ids)

        self.stdout.write(self.style.SUCCESS("✅ 인덱싱 완료"))
