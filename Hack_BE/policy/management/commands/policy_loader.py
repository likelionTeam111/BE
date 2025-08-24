from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from policy.models import Policy

class CustomDocument(Document):
    condition: str | None = None

def _get_display(obj, field):
    fields = field.split(",")
    labels = []
    """enum 필드면 get_FOO_display() 호출, 아니면 ''"""
    for code in fields:
        method = f"get_{code}_display"
        if hasattr(obj, method):
            try:
                labels.append(getattr(obj, method)())
            except Exception:
                ""
    return ", ".join(labels)

def _add_part(parts, label, value):
    text = str(value).strip()
    if text == "" or text == "0":
        return
    if text:
        parts.append(f"[{label}] {text}")

def num_data(value):
    if value == "0":
        return ""
    else:
        return value

def build_policy_text(p: "Policy") -> str:
    parts = []

    # 기본 필드
    _add_part(parts, "정책명", p.plcyNm)
    _add_part(parts, "키워드", f"{p.plcyKywdNm}, {p.lclsfNm}, {p.mclsfNm}")
    _add_part(parts, "정책 설명", f"{p.plcyExplnCn}, {p.plcySprtCn}, {p.etcMttrCn}, {_get_display(p, 'plcyPvsnMthdCd')}")
    
    # 기타 필드
    # _add_part(parts, "사업 기간", f"{p.bizPrdBgngYmd}~{p.bizPrdEndYmd}" if p.bizPrdBgngYmd or p.bizPrdEndYmd else p.bizPrdEtcCn)
    _add_part(parts,"가신청 자격조건", p.addAplyQlfcCndCn)
    _add_part(parts,"참여 제안 대상 내용", p.ptcpPrpTrgtCn)

    return ", ".join(parts)
def build_policy_supplement(p: "Policy") -> str:
    parts = []
    _add_part(parts,"사업기간", f"{p.bizPrdBgngYmd}~{p.bizPrdEndYmd}" if p.bizPrdBgngYmd or p.bizPrdEndYmd else p.bizPrdEtcCn)
    
    # 신청 관련
    _add_part(parts, "신청 방법", p.plcyAplyMthdCn)
    _add_part(parts, "신청 서류", p.sbmsnDcmntCn)
    _add_part(parts, "심사 방법", p.srngMthdCn)
    _add_part(parts, "신청 기간", p.aplyYmd)

    # 요건 필드
    _add_part(parts, "지역", p.zipCd)
    _add_part(parts, "나이 요건", p.sprtTrgtAgeLmtYn if p.sprtTrgtAgeLmtYn == "N" else f"{num_data(p.sprtTrgtMinAge)} ~ {num_data(p.sprtTrgtMaxAge)}")
    _add_part(parts, "결혼 요건", _get_display(p, "mrgSttsCd"))
    _add_part(parts, "소득 요건", f"{_get_display(p, 'earnCndSeCd')}" if _get_display(p, 'earnCndSeCd') == "무관" else f"{num_data(p.earnMinAmt)}~{num_data(p.earnMaxAmt)} or {p.earnEtcCn}")
    _add_part(parts, "전공 요건", _get_display(p, "plcyMajorCd"))
    _add_part(parts, "취업 요건", _get_display(p, "jobCd"))
    _add_part(parts, "학력 요건", _get_display(p, "schoolCd"))
    _add_part(parts, "특화 요건", _get_display(p, "sbizCd"))

    return ", ".join(parts)

def build_simple_policy_text(p: "Policy") -> str:
    parts = []

    # 기본 필드
    _add_part(parts, "정책명", p.plcyNm)
    _add_part(parts, "키워드", f"{p.plcyKywdNm}, {p.lclsfNm}, {p.mclsfNm}")
    _add_part(parts, "제공방법", _get_display(p, "plcyPvsnMthdCd"))
    _add_part(parts, "정책 설명", f"{p.plcyExplnCn}, {p.plcySprtCn}, {p.etcMttrCn}, {_get_display(p, 'plcyPvsnMthdCd')}")
    _add_part(parts, "신청 방법", p.plcyAplyMthdCn)
    _add_part(parts, "신청 서류", p.sbmsnDcmntCn)
    _add_part(parts, "지역", p.zipCd)

    return ", ".join(parts)

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
                        "id": p.plcyNo,
                        "정책명": p.plcyNm,
                        "url": f"{p.aplyUrlAddr} or {p.refUrlAddr1} or {p.refUrlAddr2}"
                    }
                )
            )
        return docs