from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from policy.models import Policy

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

class PolicyLoader(BaseLoader):
    def __init__(self, queryset):
        self.qs = queryset

    def load(self):
        docs = []
        for p in self.qs.iterator(chunk_size=500):
            docs.append(
                Document(
                    page_content=build_policy_text(p),
                    metadata={
                        "plcyNo": p.plcyNo,
                        "name": p.plcyNm,
                        "source": p.refUrlAddr1 or p.refUrlAddr2 or "",
                        "lclsfNm": p.lclsfNm, "mclsfNm": p.mclsfNm,
                    },
                )
            )
        return docs