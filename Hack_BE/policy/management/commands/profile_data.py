from django.core.management.base import BaseCommand
from profiles.models import Major, Special

MAJOR_CHOICES = [
    "0011001",
    "0011002",
    "0011003",
    "0011004",
    "0011005",
    "0011006",
    "0011007",
    "0011008",
    "0011009",
]

SBIZ_CHOICES = [
    "0014001",
    "0014002",
    "0014003",
    "0014004",
    "0014005",
    "0014006",
    "0014007",
    "0014008",
    "0014009",
    "0014010",
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for code in MAJOR_CHOICES:
            Major.objects.update_or_create(code=code)

        for code in SBIZ_CHOICES:
            Special.objects.update_or_create(code=code)

        self.stdout.write(self.style.SUCCESS(f"Success"))