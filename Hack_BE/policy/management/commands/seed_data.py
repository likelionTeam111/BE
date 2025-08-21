from django.core.management.base import BaseCommand
from profiles.models import Major, Special

POLICY_MAJOR_CHOICES = [
    ("0011001", "인문계열"),
    ("0011002", "사회계열"),
    ("0011003", "상경계열"),
    ("0011004", "이학계열"),
    ("0011005", "공학계열"),
    ("0011006", "예체능계열"),
    ("0011007", "농산업계열"),
    ("0011008", "기타"),
    ("0011009", "제한없음"),
]

SBIZ_CHOICES = [
    ("0014001", "중소기업"),
    ("0014002", "여성"),
    ("0014003", "기초생활수급자"),
    ("0014004", "한부모가정"),
    ("0014005", "장애인"),
    ("0014006", "농업인"),
    ("0014007", "군인"),
    ("0014008", "지역인재"),
    ("0014009", "기타"),
    ("0014010", "제한없음"),
]

class Command(BaseCommand):
    help = "Insert initial Major and Special data"

    def handle(self, *args, **kwargs):
        inserted_major = 0
        inserted_special = 0

        for code, label in POLICY_MAJOR_CHOICES:
            obj, created = Major.objects.get_or_create(
                code=code,
                #defaults={"label": label}
            )
            if created:
                inserted_major += 1

        for code, label in SBIZ_CHOICES:
            obj, created = Special.objects.get_or_create(
                code=code,
                #defaults={"label": label}
            )
            if created:
                inserted_special += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Major {inserted_major}개, Special {inserted_special}개 추가 완료!"
            )
        )